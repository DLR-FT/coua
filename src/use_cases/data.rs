use serde::{Deserialize, Serialize};

use crate::requirements::{Level, Stakeholder};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UseCase {
    pub actor: Actor,
    #[serde(default)]
    pub affects: Vec<WorkPackage>,
    #[serde(default)]
    pub extensions: Vec<Extension>,
    pub flow: Vec<Flow>,
    pub goal: Goal,
    pub level: Level,
    #[serde(default)]
    pub post: Vec<PostCond>,
    #[serde(default)]
    pub pre: Vec<PreCond>,
    pub scope: Scope,
    #[serde(default)]
    pub stakeholders: Vec<Stakeholder>,
    pub story: Story,
    pub title: Title,
    pub trigger: Trigger,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Actor(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Description(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Extension(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Flow(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Goal(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PostCond(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PreCond(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Scope(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Story(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Title(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Trigger(String);

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WorkPackage(f32);
