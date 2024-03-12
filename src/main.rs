// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::{
    fs::File,
    io::Read,
    path::{Path},
};

use anyhow::{Context};
use clap::Parser;
use coua::{
    display_requirements, load_use_cases, parse_manifest, Artifact, CouaManifest, UseCaseData,
};

mod cli;

pub fn do_parse_manifest<T: AsRef<Path>>(file: T) -> anyhow::Result<CouaManifest> {
    let mut manifest = String::new();
    let mut file = File::open(file)?;
    let _ = file
        .read_to_string(&mut manifest)
        .with_context(|| "Failed to read from manifest file")?;
    let manifest = parse_manifest(&manifest)?;
    Ok(manifest)
}

fn main() -> anyhow::Result<()> {
    let cli = cli::Cli::parse();

    let (out_dir, manifest_path) = cli::process_args(cli)?;

    let manifest = do_parse_manifest(manifest_path)?;

    let requirements: Vec<&Artifact> = manifest
        .artifacts
        .iter()
        .filter(|r| matches!(r, Artifact::Requirements(_)))
        .collect();
    for file in requirements.into_iter() {
        let requirements_out = {
            let mut p = out_dir.clone();
            p.push("requirements.dot");
            p
        };
        let input = File::open(file)?;
        let output = File::create(requirements_out)?;
        display_requirements(input, output)?;
    }
    let use_cases: Vec<&Artifact> = manifest
        .artifacts
        .iter()
        .filter(|uc| matches!(uc, Artifact::UseCases(_)))
        .collect();
    for file in use_cases.into_iter() {
        let _ucs: UseCaseData = load_use_cases(File::open(file).unwrap())
            .with_context(|| "Failed to read use-cases from file")
            .unwrap();
    }
    Ok(())
}
