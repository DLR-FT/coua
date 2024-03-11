use crate::artifact::ArtifactLocator;

pub struct ObjectiveId(String);

pub struct ObjectiveDesc(String);

pub struct ObjectiveRef(String);

pub struct ActivityRef(String);

pub enum ApplicabilityMode {
    NotApplicable,
    WithoutIndependence,
    WithIndependence,
}

pub struct ObjectiveApplicability {
    pub dal_a: ApplicabilityMode,
    pub dal_b: ApplicabilityMode,
    pub dal_c: ApplicabilityMode,
    pub dal_d: ApplicabilityMode,
}

pub struct DataItemDescription(String);

pub struct DataItemReference(String);

pub struct DataItem {
    pub reference: DataItemReference,
    pub description: DataItemDescription,
    pub artifact: Option<ArtifactLocator>,
}

pub struct ObjectiveControlCategory {
    pub dal_a: ControlCategory,
    pub dal_b: ControlCategory,
    pub dal_c: ControlCategory,
    pub dal_d: ControlCategory,
}

pub enum ControlCategory {
    None,
    CC1,
    CC2,
}

pub struct Objective {
    /// "The activities of the software life cycle processes are defined.""
    pub description: ObjectiveDesc,
    ///  4.1.a (Explanation of the objective)
    pub reference: ObjectiveRef,
    /// [4.2.a] (Explanation of the activities)
    pub activity: Vec<ActivityRef>,
    /// An objective may apply to any DAL with or without requirement for independent review
    pub applicability: ObjectiveApplicability,
    /// Artifacts produced by the activities of this objective
    pub outputs: Vec<DataItem>,
    /// Configuration management controls placed on software life cycle data produced during the activities.
    pub control_category: ObjectiveControlCategory,
    // Objectives may be disabled in coua
    // pub active: bool,
}
