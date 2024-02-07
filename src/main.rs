#![allow(dead_code)]

type Id = String;

struct Objective {
    id: Id,
    name: String,         // 1.1 (name is not quite right)
    description: String,  // "The activities of the software life cycle processes are defined.""
    reference: Reference, //  4.1.a (Chapter in the Standard)
    //applicability: Applicability, // not here, we already know which DAL level we need
    satisfied: ObjectiveState,
}

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

struct Evidence {
    objective: Id,
    uri: url::Url,
    kind: EvidenceKind,
}

// determine how the associated evidence is interpreted
enum EvidenceKind {
    Justification,
    CoverageReport,
    FileJustExists,
}

// struct Applicability {
//     dal_a: ApplicabilityType,
//     dal_b: ApplicabilityType,
//     dal_c: ApplicabilityType,
//     dal_d: ApplicabilityType,
// }

// enum ApplicabilityType {
//     NotApplicable,
//     Applicable,
//     ApplicableWithIndependence,
// }

fn main() {
    println!("Hello, world!");
}
