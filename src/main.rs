// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use clap::Parser;
use coua::do_run;

mod cli;

fn main() -> anyhow::Result<()> {
    let cli = cli::Cli::parse();
    let (out_dir, manifest_path) = cli::process_args(cli)?;

    do_run(manifest_path, out_dir)
}
