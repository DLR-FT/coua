#![allow(dead_code)]

// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::fs::File;
use std::io::{self, stdout};

use anyhow::Context;
use coua::evidence::{EvidenceKind, EvidenceMeta};
use coua::objective::{Objective, Reference};
use coua::requirements::{load_file, RequirementsData};

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

pub fn display_requirements<T: io::Read>(file: T) -> anyhow::Result<()> {
    let reqs: RequirementsData =
        load_file(file).with_context(|| "Failed to read requirements from standard input")?;
    let reqs = reqs
        .try_into_reqs()
        .with_context(|| "Failed to transform requirements into graph")?;
    reqs.render_to(&mut stdout())
        .with_context(|| "Failed to render requirements")
}

fn main() -> anyhow::Result<()> {
    let project_path = std::env::current_dir()?;
    let objectives = create_objectives();
    let evidences = objectives
        .iter()
        .flat_map(associated_evidences)
        .collect::<Vec<_>>();
    for e in evidences {
        e.get_evidence(&project_path)?
    }
    let mut requirements = project_path.clone();
    requirements.push("requirements.yml");
    let requirements = File::open(requirements)?;
    display_requirements(requirements)?;
    Ok(())
}
