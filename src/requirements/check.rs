use std::fs::read_to_string;
use std::fs::File;

use anyhow::Context;

use crate::artifact::Artifact;
use crate::manifest::CouaManifest;

use super::display::Reqs;
use super::input::data::RequirementsData;
use super::input::parse_requirements;

pub fn check_requirements(
    manifest: &CouaManifest,
    out_dir: std::path::PathBuf,
) -> Result<(), anyhow::Error> {
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
        let requirements: RequirementsData = parse_requirements(&read_to_string(file)?)
            .with_context(|| "Failed to read requirements from file")?;
        let mut output = File::create(requirements_out)?;
        // TODO Do not use Reqs
        let reqs: &Reqs<'_, '_> = (&requirements).try_into()?;
        dot::render(reqs, &mut output)?;
    }
    Ok(())
}
