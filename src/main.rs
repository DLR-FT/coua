// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::fs;

use clap::Parser;
use coua::{check, get_manifest};

mod cli;

fn main() -> anyhow::Result<()> {
    let cli = cli::Cli::parse();
    let (out_dir, manifest_path) = cli::process_args(cli)?;
    if !out_dir.exists() {
        fs::create_dir(&out_dir)?;
    }

    let manifest = get_manifest(manifest_path)?;
    check(&manifest, out_dir)
}
