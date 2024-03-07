use crate::artifact::ArtifactLocator;

#[derive(Debug, Clone)]
pub enum Evidence {
    Justification(ArtifactLocator),
    CoverageReport(ArtifactLocator),
    TestReport(ArtifactLocator),
    StaticAnalysisReport(ArtifactLocator),
    FileJustExists(ArtifactLocator),
}
