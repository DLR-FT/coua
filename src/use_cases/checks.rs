use std::fs::read_to_string;

use anyhow::Context;

use crate::{artifact::Artifact, manifest::CouaManifest};

use super::input::{parse_use_cases, UseCaseData};

pub fn check_use_cases(manifest: &CouaManifest) -> Result<(), anyhow::Error> {
    let use_cases: Vec<&Artifact> = manifest
        .artifacts
        .iter()
        .filter(|uc| matches!(uc, Artifact::UseCases(_)))
        .collect();
    for file in use_cases.into_iter() {
        let _ucs: UseCaseData = parse_use_cases(&read_to_string(file)?)
            .with_context(|| "Failed to read use-cases from file")?;
    }
    Ok(())
}
