use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct ArtifactLocator(PathBuf);

impl AsRef<Path> for ArtifactLocator {
    fn as_ref(&self) -> &Path {
        &self.0
    }
}

impl From<String> for ArtifactLocator {
    fn from(value: String) -> Self {
        Self(value.into())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
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
