// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::{
    fs::File,
    io::{stdout, Read},
    path::Path,
};

use anyhow::Context;
use coua::{
    display_requirements, load_use_cases, parse_manifest, Artifact, CouaManifest, UseCaseData,
};

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
    let project_path = std::env::current_dir()?;
    let mut manifest_path = project_path.clone();
    manifest_path.push("coua.toml");
    let manifest = do_parse_manifest(&manifest_path)?;
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
        let _ucs: UseCaseData = load_use_cases(File::open(file).unwrap())
            .with_context(|| "Failed to read use-cases from file")
            .unwrap();
    }
    Ok(())
}
