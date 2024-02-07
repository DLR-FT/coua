#![allow(dead_code)]

// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use coua::evidence::{EvidenceKind, EvidenceMeta};
use coua::objective::{Objective, Reference};

static PROJECT_PATH: &str = "/home/brei_no/Projects/a653rs-linux";

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
        e.get_evidence(PROJECT_PATH)?
    }
    Ok(())
}
