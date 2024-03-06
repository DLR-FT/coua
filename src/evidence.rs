use std::path::Path;

pub struct EvidenceMeta {
    pub objective: crate::objective::ObjectiveId,
    pub uri: crate::tool::CouaURI,
    pub kind: EvidenceKind,
}

// determine how the associated evidence is interpreted
// should follow from the uri
pub enum EvidenceKind {
    Justification,
    CoverageReport,
    TestReport,
    StaticAnalysisReport,
    FileJustExists,
}

impl EvidenceMeta {
    pub fn get_evidence<P: AsRef<Path>>(mut self, project_path: &P) -> anyhow::Result<()> {
        std::env::set_current_dir(project_path)?;
        let output = self.uri.execute_command()?;

        let status = output.status;
        println!("status {status}");
        let report = std::str::from_utf8(&output.stdout)?;
        println!("report\n{report}");
        let errors = std::str::from_utf8(&output.stderr)?;
        println!("errors\n{errors}");
        Ok(())
    }
}
