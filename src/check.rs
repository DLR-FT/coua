use crate::{
    parse_manifest, parse_requirements, parse_use_cases, Artifact, CouaManifest, Reqs,
    RequirementsData, UseCaseData,
};

use std::fs::{read_to_string, File};

use anyhow::Context;

pub fn do_run(
    manifest_path: std::path::PathBuf,
    out_dir: std::path::PathBuf,
) -> Result<(), anyhow::Error> {
    let manifest = get_manifest(manifest_path)?;
    check_requirements(&manifest, out_dir)?;
    check_use_cases(&manifest)?;
    Ok(())
}

fn get_manifest(manifest_path: std::path::PathBuf) -> Result<CouaManifest, anyhow::Error> {
    let manifest: CouaManifest = {
        let manifest =
            read_to_string(manifest_path).with_context(|| "Failed to read from manifest file")?;
        parse_manifest(&manifest)?
    };
    Ok(manifest)
}

fn check_use_cases(manifest: &CouaManifest) -> Result<(), anyhow::Error> {
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

fn check_requirements(
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
        let reqs: &Reqs<'_, '_> = (&requirements).try_into()?;
        dot::render(reqs, &mut output)?;
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use tempfile::TempDir;

    use super::do_run;

    #[test]
    fn test_run() -> anyhow::Result<()> {
        let mut in_ = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        in_.push("coua.toml");
        let out = TempDir::new().unwrap();
        do_run(in_, out.into_path())
    }

    #[test]
    fn get_manifest_fail() {
        let mut in_ = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        in_.push("couaaaaa.toml");
        let out = TempDir::new().unwrap();
        assert!(do_run(in_, out.into_path()).is_err())
    }
}
