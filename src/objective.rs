pub type ObjectiveId = String;

pub struct Objective {
    pub id: ObjectiveId,
    pub name: String,         // 1.1 (name is not quite right)
    pub description: String,  // "The activities of the software life cycle processes are defined.""
    pub reference: Reference, //  4.1.a (Chapter in the Standard)
    //applicability: Applicability, // not here, we already know which DAL level we need
    pub satisfied: Option<ObjectiveState>,
}

#[derive(Clone)]
pub struct Reference {
    pub document: String,
    pub isbn: Option<()>,
    pub reference: String, // chapter in standard
}

pub enum ObjectiveState {
    Failed,
    Satisfied,
    // We want to be stateless, thus an objective is always either failed or satisfied.
    // Pending
}
