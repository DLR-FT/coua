use std::ops::Deref;

use crate::artifact::ArtifactLocator;

#[derive(Debug, Clone)]
pub struct ObjectiveId(String);

impl Deref for ObjectiveId {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone)]
pub struct ObjectiveDesc(String);

impl Deref for ObjectiveDesc {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone)]
pub struct ObjectiveRef(String);

impl Deref for ObjectiveRef {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        self.0.as_str()
    }
}

#[derive(Debug, Clone)]
pub struct ActivityRef(String);

impl Deref for ActivityRef {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ApplicabilityMode {
    NotApplicable,
    WithoutIndependence,
    WithIndependence,
}

#[derive(Debug, Clone)]
pub struct ObjectiveApplicability {
    pub dal_a: ApplicabilityMode,
    pub dal_b: ApplicabilityMode,
    pub dal_c: ApplicabilityMode,
    pub dal_d: ApplicabilityMode,
}

#[derive(Debug, Clone)]
pub struct DataItemDescription(String);

impl Deref for DataItemDescription {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone)]
pub struct DataItemReference(String);

impl Deref for DataItemReference {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone)]
pub struct DataItem {
    pub reference: DataItemReference,
    pub description: DataItemDescription,
    pub artifact: Option<ArtifactLocator>,
}

#[derive(Debug, Clone)]
pub struct ObjectiveControlCategory {
    pub dal_a: ControlCategory,
    pub dal_b: ControlCategory,
    pub dal_c: ControlCategory,
    pub dal_d: ControlCategory,
}

#[derive(Debug, Clone)]
pub enum ControlCategory {
    None,
    CC1,
    CC2,
}

#[derive(Debug, Clone)]
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
