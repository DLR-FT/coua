#![feature(rustc_private)]
#![feature(lazy_cell)]
#![feature(iter_intersperse)]

#[allow(unused_extern_crates)]
extern crate rustc_driver;

extern crate rustc_ast;
extern crate rustc_data_structures;
extern crate rustc_error_codes;
extern crate rustc_errors;
extern crate rustc_hash;
extern crate rustc_hir;
extern crate rustc_interface;
extern crate rustc_lint;
extern crate rustc_middle;
extern crate rustc_session;
extern crate rustc_span;

use std::path::PathBuf;
use std::{path, process, str};

use rustc_ast::AttrKind;
use rustc_hash::FxHashMap;
use rustc_session::config;

use clap::Parser;

/// Coua certification utility
#[derive(Parser)]
#[command(version, about, long_about = None)]
pub(crate) struct Cli {
    /// Output file
    #[arg(
        long,
        value_name = "FILE",
        default_value = "coua_requirements_trace.json"
    )]
    pub(crate) out: Option<PathBuf>,

    /// Change the directory before doing anything
    pub(crate) files: Vec<PathBuf>,
}

fn main() {
    let args = Cli::parse();
    let mut input_files = args.files;
    // TODO do for all input files
    let input = input_files.pop().unwrap();
    let out = process::Command::new("rustc")
        .arg("--print=sysroot")
        .current_dir(".")
        .output()
        .unwrap();
    let sysroot = str::from_utf8(&out.stdout).unwrap().trim();
    let config = rustc_interface::Config {
        hash_untracked_state: Default::default(),
        psess_created: Default::default(),
        using_internal_features: Default::default(),
        opts: config::Options {
            unstable_opts: config::UnstableOptions {
                crate_attr: vec![
                    String::from("feature(register_tool)"),
                    String::from("register_tool(coua)"),
                ],
                ..config::UnstableOptions::default()
            },
            maybe_sysroot: Some(path::PathBuf::from(sysroot)),
            test: true,
            ..config::Options::default()
        },
        crate_cfg: Default::default(),
        crate_check_cfg: Default::default(),
        input: config::Input::File(input),
        output_dir: None,
        output_file: None,
        file_loader: None,
        locale_resources: rustc_driver::DEFAULT_LOCALE_RESOURCES,
        lint_caps: FxHashMap::default(),
        register_lints: None,
        registry: rustc_driver::diagnostics_registry(),
        make_codegen_backend: None,
        expanded_args: Vec::new(),
        ice_file: None,
        override_queries: Default::default(),
    };
    rustc_interface::run_compiler(config, |compiler| {
        compiler.enter(|queries| {
            // Parse the program and print the syntax tree.
            //let parse = queries.parse().unwrap().get_mut().clone();
            queries.global_ctxt().unwrap().enter(|tcx| {
                for id in tcx.hir().items() {
                    let hir = tcx.hir();
                    let item = hir.item(id);
                    // TODO Check if item has test attribute
                    // TODO Try to get coua::requirement attribute
                    // TODO Warn if there is no coua::requirement
                    // TODO Log discovered requirement
                    // TODO Write discovered requirement to output file
                    if let rustc_hir::ItemKind::Fn(_, _, _) = item.kind {
                        let name = item.ident;
                        let attrs = tcx.hir().attrs(item.hir_id());
                        let _ty = tcx.type_of(item.hir_id().owner.def_id);
                        for attr in attrs.iter() {
                            if let AttrKind::Normal(attr) = attr.kind.clone() {
                                let item = attr.item.clone();
                                let path = item.path.clone();

                                let mut segments = path.segments.iter();
                                let mut span = None;
                                if let Some(seg) = segments.next() {
                                    if seg.ident.name.as_str() == "coua" {
                                        if let Some(seg) = segments.next() {
                                            if seg.ident.name.as_str() == "trace" {
                                                span = Some(path.span)
                                            }
                                        }
                                    }
                                }
                                if let Some(span) = span {
                                    let args = item.args;
                                    let requirements = args.inner_tokens();
                                    println!("{name:?} {span:?} {requirements:?}");
                                }
                            }
                        }
                    }
                }
            })
        });
    });
}
