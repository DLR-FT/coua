use crate::{manifest::CouaManifest, requirements::check_requirements, use_cases::check_use_cases};

pub fn check(manifest: &CouaManifest, out_dir: std::path::PathBuf) -> Result<(), anyhow::Error> {
    check_requirements(manifest, out_dir)?;
    check_use_cases(manifest)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use tempfile::TempDir;

    use crate::manifest::get_manifest;

    use super::check;

    #[test]
    fn test_run() -> anyhow::Result<()> {
        let mut in_ = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        in_.push("coua.toml");
        let in_ = get_manifest(in_).unwrap();
        let out = TempDir::new().unwrap();
        check(&in_, out.into_path())
    }

    #[test]
    fn get_manifest_fail() {
        let mut in_ = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        in_.push("couaaaaa.toml");
        let in_ = get_manifest(in_);
        assert!(in_.is_err())
    }
}
