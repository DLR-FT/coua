use crate::{artifact::ArtifactLocator, objective::ObjectiveId};

#[derive(Debug, Clone)]
pub struct EvidenceMetaData {
    pub objective: ObjectiveId,
    pub location: ArtifactLocator,
    pub kind: EvidenceKind,
}

#[derive(Debug, Clone)]
pub enum EvidenceKind {
    Justification,
    CoverageReport,
    TestReport,
    StaticAnalysisReport,
    FileJustExists,
}
