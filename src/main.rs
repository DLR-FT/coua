#![allow(dead_code)]

// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::process::Command;
use url::Url;

static PROJECT_PATH: &str = "/home/brei_no/Projects/a653rs-linux";

type ObjectiveId = String;

struct CouaURI {
    uri: Url,
}

impl std::str::FromStr for CouaURI {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            uri: Url::parse(s)?,
        })
    }
}

impl CouaURI {
    fn execute_command(&mut self) -> anyhow::Result<std::process::Output> {
        let command_str = self
            .uri
            .host_str()
            .and_then(|s| s.split_once("-"))
            .ok_or_else(|| anyhow::anyhow!("Failed to convert URI to command"))?;

        let mut command = Command::new(command_str.0);
        let command = command.arg(command_str.1);
        println!("running {:?}", command);

        command.output().map_err(Into::into)
    }
}

struct Objective {
    id: ObjectiveId,
    name: String,         // 1.1 (name is not quite right)
    description: String,  // "The activities of the software life cycle processes are defined.""
    reference: Reference, //  4.1.a (Chapter in the Standard)
    //applicability: Applicability, // not here, we already know which DAL level we need
    satisfied: Option<ObjectiveState>,
}

#[derive(Clone)]
struct Reference {
    document: String,
    isbn: Option<()>,
    reference: String, // chapter in standard
}

enum ObjectiveState {
    Failed,
    Satisfied,
    // We want to be stateless, thus an objective is always either failed or satisfied.
    // Pending
}

struct EvidenceMeta {
    objective: ObjectiveId,
    uri: CouaURI,
    kind: EvidenceKind,
}

// determine how the associated evidence is interpreted
// should follow from the uri
enum EvidenceKind {
    Justification,
    CoverageReport,
    TestReport,
    StaticAnalysisReport,
    FileJustExists,
}

// Should come from the manifest
// mock associated manifests
fn associated_evidences(objective: &Objective) -> Vec<EvidenceMeta> {
    let ev = match objective.id.as_str() {
        "O1" => EvidenceMeta {
            objective: "O1".to_owned(),
            uri: "coua://cargo-test/".parse().unwrap(),
            kind: EvidenceKind::TestReport,
        },
        "O2" => EvidenceMeta {
            objective: "O2".to_owned(),
            uri: "coua://cargo-clippy/".parse().unwrap(),
            kind: EvidenceKind::TestReport,
        },
        _ => todo!(),
    };
    vec![ev]
}

impl EvidenceMeta {
    fn get_evidence(mut self) -> anyhow::Result<()> {
        println!("{:?}", std::env::current_dir()?);
        std::env::set_current_dir(PROJECT_PATH)?;
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

// mock objectives
fn create_objectives() -> Vec<Objective> {
    let reference = Reference {
        document: "My first standard".to_owned(),
        isbn: None,
        reference: "Chapter 1".to_owned(),
    };
    let objective1 = Objective {
        id: "O1".to_owned(),
        name: "Test success".to_owned(),
        description: "All tests are successful".to_owned(),
        reference: reference.clone(),
        satisfied: None,
    };
    let objective2 = Objective {
        id: "O2".to_owned(),
        name: "Clippy clean".to_owned(),
        description: "clean clippy report".to_owned(),
        reference,
        satisfied: None,
    };
    vec![objective1, objective2]
}

fn main() -> anyhow::Result<()> {
    let objectives = create_objectives();
    let evidences = objectives
        .iter()
        .map(|o| associated_evidences(o))
        .flatten()
        .collect::<Vec<_>>();
    for e in evidences {
        e.get_evidence()?
    }
    Ok(())
}
