// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use clap::Parser;
use coua::{check, get_manifest};

mod cli;

fn main() -> anyhow::Result<()> {
    let cli = cli::Cli::parse();
    let (out_dir, manifest_path) = cli::process_args(cli)?;

    let manifest = get_manifest(manifest_path)?;
    check(&manifest, out_dir)
}
