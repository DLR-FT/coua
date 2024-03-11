// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::{fs::File, io::stdout};

use anyhow::Context;
use coua::{display_requirements, load_use_cases, parse_manifest, Artifact, UseCaseData};

fn main() -> anyhow::Result<()> {
    let project_path = std::env::current_dir()?;
    let mut manifest_path = project_path.clone();
    manifest_path.push("coua.toml");
    let manifest = parse_manifest(File::open(manifest_path)?)?;
    let requirements: Vec<&Artifact> = manifest
        .artifacts
        .iter()
        .filter(|r| matches!(r, Artifact::Requirements(_)))
        .collect();
    for file in requirements.into_iter() {
        display_requirements(File::open(file)?, stdout())?;
    }
    let use_cases: Vec<&Artifact> = manifest
        .artifacts
        .iter()
        .filter(|uc| matches!(uc, Artifact::UseCases(_)))
        .collect();
    for file in use_cases.into_iter() {
        let ucs: UseCaseData = load_use_cases(File::open(file).unwrap())
            .with_context(|| "Failed to read use-cases from file")
            .unwrap();
        dbg!(ucs);
    }
    Ok(())
}
