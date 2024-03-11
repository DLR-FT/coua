use serde::Deserialize;

use crate::requirements::{Level, Stakeholder};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
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

#[derive(Deserialize)]
pub struct Actor(String);

#[derive(Deserialize)]
pub struct Extension(String);

#[derive(Deserialize)]
pub struct Flow(String);

#[derive(Deserialize)]
pub struct Goal(String);

#[derive(Deserialize)]
pub struct PostCond(String);

#[derive(Deserialize)]
pub struct PreCond(String);

#[derive(Deserialize)]
pub struct Scope(String);

#[derive(Deserialize)]
pub struct Story(String);

#[derive(Deserialize)]
pub struct Title(String);

#[derive(Deserialize)]
pub struct Trigger(String);

#[derive(Deserialize)]
pub struct WorkPackage(f32);
