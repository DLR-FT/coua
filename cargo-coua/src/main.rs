#![feature(rustc_private)]
#![feature(lazy_cell)]
#![feature(iter_intersperse)]

#[allow(unused_extern_crates)]
extern crate rustc_driver;

extern crate rustc_ast;
extern crate rustc_hir;
extern crate rustc_interface;
extern crate rustc_middle;
extern crate rustc_span;

use anyhow::{anyhow, Context};
use cargo::{
    core::{
        compiler::{Compilation, CompileMode, Executor, Unit},
        Package, PackageId, Shell, Verbosity, Workspace,
    },
    ops::{compile_with_exec, CompileOptions},
    util::{homedir, important_paths},
    CargoResult,
};
use clap::{arg, Parser};
use rustc_ast::{AttrArgs, AttrArgsEq, AttrKind};
use rustc_driver::RunCompiler;
use rustc_hir::Item;
use rustc_middle::ty::TyCtxt;
use rustc_span::Symbol;
use serde::Serialize;
use std::collections::{BTreeMap, HashSet};
use std::fs::File;
use std::io::BufWriter;
use std::path::PathBuf;
use std::sync::{Arc, Mutex};
use std::{env, process, str};

#[derive(Debug, Default, Serialize)]
struct Output(BTreeMap<String, Vec<String>>);

#[derive(Debug)]
struct RequirementTrace {
    req: Symbol,
    test: String,
}

/// Coua certification utility
#[derive(Parser)]
#[command(version, about, long_about = None)]
pub(crate) struct Cli {
    /// Output file
    #[arg(long, value_name = "FILE")]
    output: Option<PathBuf>,
}

fn main() {
    let args = Cli::parse();
    let mut shell = Shell::new();
    shell.set_verbosity(Verbosity::Quiet);
    let cwd = env::current_dir()
        .with_context(|| "couldn't get the current directory of the process")
        .unwrap();
    let homedir = homedir(&cwd)
        .ok_or_else(|| {
            anyhow!(
                "Cargo couldn't find your home directory. \
                 This probably means that $HOME was not set."
            )
        })
        .unwrap();
    let config = cargo::Config::new(shell, cwd, homedir);
    let ws = workspace(&config).unwrap();
    let compile_options = compile_options(&config).unwrap();

    let out = Arc::new(Mutex::new(Output::default()));
    compile(&ws, &compile_options, out.clone()).unwrap();

    let out_file = args.output.unwrap_or_else(|| {
        let mut target = ws.target_dir();
        target.push("coua_trace.json");
        target.into_path_unlocked()
    });

    let out = out.lock().unwrap();
    serde_json::to_writer(BufWriter::new(File::create(out_file).unwrap()), &*out).unwrap();
}

fn sysroot() -> String {
    let out = process::Command::new("rustc")
        .arg("--print=sysroot")
        .current_dir(".")
        .output()
        .unwrap();
    str::from_utf8(&out.stdout).unwrap().trim().to_owned()
}

fn compile_options(config: &cargo::Config) -> CargoResult<CompileOptions> {
    CompileOptions::new(config, CompileMode::Check { test: true })
}

pub fn workspace(config: &cargo::Config) -> CargoResult<Workspace> {
    let root = important_paths::find_root_manifest_for_wd(config.cwd())?;
    Workspace::new(&root, config)
}

fn compile<'a>(
    ws: &Workspace<'a>,
    options: &CompileOptions,
    out: Arc<Mutex<Output>>,
) -> CargoResult<Compilation<'a>> {
    let member_packages: HashSet<_> = ws.members().map(Package::package_id).collect();
    let executor = CustomExecutor {
        member_packages: Mutex::new(member_packages),
        out,
    };
    let executor: Arc<dyn Executor> = Arc::new(executor);
    compile_with_exec(ws, options, &executor)
}

// TODO cached state for compilation of multiple files
struct CustomExecutor {
    member_packages: Mutex<HashSet<PackageId>>,
    out: Arc<Mutex<Output>>,
}

impl CustomExecutor {
    fn primary_package(&self, id: &cargo::core::PackageId) -> bool {
        id.source_id().is_path() || self.member_packages.lock().unwrap().contains(id)
    }
}

impl Executor for CustomExecutor {
    fn force_rebuild(&self, unit: &Unit) -> bool {
        // Always force rebuild the primary crate
        let id = unit.pkg.package_id();
        self.primary_package(&id)
    }

    fn exec(
        &self,
        cmd: &cargo_util::ProcessBuilder,
        id: cargo::core::PackageId,
        // TODO maybe one output file per target
        _target: &cargo::core::Target,
        _mode: cargo::core::compiler::CompileMode,
        on_stdout_line: &mut dyn FnMut(&str) -> CargoResult<()>,
        on_stderr_line: &mut dyn FnMut(&str) -> CargoResult<()>,
    ) -> CargoResult<()> {
        let mut args: Vec<_> = cmd
            .get_args()
            .map(|a| {
                (*a).to_owned()
                    .into_string()
                    .expect("cannot stringify command arg")
            })
            .collect();
        let program = cmd
            .get_program()
            .clone()
            .into_string()
            .expect("cannot stringify command program");

        if !args.iter().any(|x| x.as_str() == "--sysroot") {
            args.push("--sysroot".to_owned());
            args.push(sysroot());
        }

        args.insert(0, program.clone());
        if self.primary_package(&id) {
            run_compiler(&args, self.out.clone())
                .map(|_| ())
                .map_err(|_| anyhow::format_err!("Build error"))
        } else {
            cmd.exec_with_streaming(on_stdout_line, on_stderr_line, false)
                .map(drop)
        }
    }
}

struct CouaCallbacks {
    out: Arc<Mutex<Output>>,
}

impl rustc_driver::Callbacks for CouaCallbacks {
    fn after_expansion<'tcx>(
        &mut self,
        _compiler: &rustc_interface::interface::Compiler,
        queries: &'tcx rustc_interface::Queries<'tcx>,
    ) -> rustc_driver::Compilation {
        queries
            .global_ctxt()
            .expect("Failed to aquire global context")
            .enter(|tcx| {
                tcx.hir()
                    .items()
                    .flat_map(|id| {
                        let hir = tcx.hir();
                        let item = hir.item(id);
                        if let rustc_hir::ItemKind::Fn(_, _, _) = item.kind {
                            filter_requirements(item, &tcx)
                        } else {
                            vec![]
                        }
                    })
                    .for_each(|req| {
                        let mut out = self.out.lock().unwrap();
                        let key = req.req.as_str().to_owned();
                        out.0.entry(key).or_default().push(req.test)
                    })
            });

        rustc_driver::Compilation::Continue
    }
}

fn run_compiler(args: &[String], out: Arc<Mutex<Output>>) -> Result<(), ()> {
    let mut callbacks = CouaCallbacks { out };
    rustc_driver::install_ice_hook("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/issues", |_| {});
    rustc_driver::catch_fatal_errors(move || {
        // TODO: Runs the compiler in-process, should run as subprocess and hide stderr json messages (the diagnostic stuff with `$message_type`)
        let run_compiler = RunCompiler::new(args, &mut callbacks);
        run_compiler.run()
    })
    .map(|_| ())
    .map_err(|_| ())
}

fn filter_requirements(item: &Item, tcx: &TyCtxt) -> Vec<RequirementTrace> {
    let hir = item.hir_id();
    let attrs = tcx.hir().attrs(hir);
    let mut reqs = Vec::default();
    for attr in attrs.iter() {
        if let AttrKind::Normal(attr) = attr.kind.clone() {
            let attr_item = attr.item.clone();
            let path = attr_item.path.clone();
            let mut segments = path.segments.iter();
            if let (Some(coua), Some(trace)) = (segments.next(), segments.next()) {
                if coua.ident.name.as_str() == "coua" && trace.ident.name.as_str() == "trace" {
                    if let AttrArgs::Eq(_, AttrArgsEq::Hir(lit)) = attr_item.args {
                        // TODO nope this is just the identifier path, not the full path inside the crate
                        let ident = tcx.def_path_str(hir.owner);
                        reqs.push(RequirementTrace {
                            req: lit.symbol,
                            test: ident,
                        })
                    }
                }
            }
        }
    }

    reqs
}
