use std::{
    collections::{HashMap, HashSet},
    fmt::Display,
    ops::Deref,
};

use serde::Deserialize;

#[derive(Deserialize, PartialEq, Eq, Hash)]
pub struct UseCaseId(String);

impl UseCaseId {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

#[derive(Clone, Deserialize, PartialEq, Eq, Hash)]
pub struct ReqId(String);

impl ReqId {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

impl Display for ReqId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(self.0.as_str())
    }
}

#[derive(Deserialize)]
pub struct ReqDesc(String);

impl ReqDesc {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

#[derive(Deserialize)]
pub struct Stakeholder(String);

impl Stakeholder {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

#[derive(Deserialize, Hash)]
pub struct Level(String);

#[derive(Deserialize)]
#[serde(rename_all = "kebab-case")]
#[serde(deny_unknown_fields)]
pub struct Requirement {
    pub description: ReqDesc,
    pub owner: Stakeholder,
    pub level: Level,
    #[serde(default)]
    pub use_cases: HashSet<UseCaseId>,
    #[serde(default)]
    pub trace: Option<ReqId>,
}

#[derive(Deserialize)]
pub struct RequirementsData(HashMap<ReqId, Requirement>);

impl Deref for RequirementsData {
    type Target = HashMap<ReqId, Requirement>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}
