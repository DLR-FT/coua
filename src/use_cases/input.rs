use std::{collections::HashMap, io};

use anyhow::Context;
use serde::{Deserialize, Serialize};

use crate::{UseCase, UseCaseId};

pub fn load_use_cases<T: io::Read>(mut file: T) -> anyhow::Result<UseCaseData> {
    let mut ucs = String::new();
    let _ = file.read_to_string(&mut ucs);
    toml::from_str(&ucs).with_context(|| "Failed to read use-cases")
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UseCaseData(HashMap<UseCaseId, UseCase>);
