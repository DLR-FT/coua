// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::fs::File;
use std::io::{self, stdout};

use anyhow::Context;
use coua::{
    load_requirements, load_use_cases, Artifact, CouaManifest, RequirementsData, UseCaseData,
};

fn display_requirements<T: io::Read>(file: T) -> anyhow::Result<()> {
    let reqs: RequirementsData =
        load_requirements(file).with_context(|| "Failed to read requirements from file")?;
    let reqs = reqs
        .try_into_reqs()
        .with_context(|| "Failed to transform requirements into graph")?;
    reqs.render_to(&mut stdout())
        .with_context(|| "Failed to render requirements")
}

fn parse_manifest<T: io::Read>(mut file: T) -> anyhow::Result<CouaManifest> {
    let mut manifest = String::new();
    let _ = file
        .read_to_string(&mut manifest)
        .with_context(|| "Failed to read from manifest file")?;
    let manifest = toml::from_str(&manifest).with_context(|| "Failed to parse manifest")?;
    Ok(manifest)
}

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
        display_requirements(File::open(file)?)?;
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
