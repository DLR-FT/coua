use serde::Deserialize;
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
pub struct ArtifactLocator(PathBuf);

impl AsRef<Path> for ArtifactLocator {
    fn as_ref(&self) -> &Path {
        &self.0
    }
}

impl From<&str> for ArtifactLocator {
    fn from(value: &str) -> Self {
        Self(value.into())
    }
}

#[derive(Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum Artifact {
    Justification(ArtifactLocator),
    CoverageReport(ArtifactLocator),
    TestReport(ArtifactLocator),
    StaticAnalysisReport(ArtifactLocator),
    FileJustExists(ArtifactLocator),
    Requirements(ArtifactLocator),
    UseCases(ArtifactLocator),
}

impl AsRef<Path> for Artifact {
    fn as_ref(&self) -> &Path {
        match &self {
            Artifact::Justification(l)
            | Artifact::CoverageReport(l)
            | Artifact::TestReport(l)
            | Artifact::StaticAnalysisReport(l)
            | Artifact::FileJustExists(l)
            | Artifact::Requirements(l)
            | Artifact::UseCases(l) => l.as_ref(),
        }
    }
}

#[cfg(test)]
mod test {
    use crate::artifact::{Artifact, ArtifactLocator};

    #[test]
    fn as_path() {
        const PATH: &str = "/nix/store/2298shs98hs98sh-test";
        let rs = vec![
            Artifact::Justification(PATH.into()),
            Artifact::CoverageReport(PATH.into()),
            Artifact::TestReport(PATH.into()),
            Artifact::StaticAnalysisReport(PATH.into()),
            Artifact::FileJustExists(PATH.into()),
            Artifact::Requirements(PATH.into()),
            Artifact::UseCases(PATH.into()),
        ];
        for r in rs.into_iter() {
            let ref_r = r.as_ref();
            assert!(ref_r == ArtifactLocator::from(PATH).as_ref())
        }
    }
}
