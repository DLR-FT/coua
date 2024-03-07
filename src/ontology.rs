use std::{
    ops::Deref,
    path::{Path, PathBuf},
};

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
pub struct OntologyLocator(PathBuf);

impl AsRef<Path> for OntologyLocator {
    fn as_ref(&self) -> &Path {
        &self.0
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OntologyName(String);

impl Deref for OntologyName {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OntologyReference(String);

impl Deref for OntologyReference {
    type Target = str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Ontology {
    pub name: OntologyName,
    pub source: OntologyLocator,
    pub reference: OntologyReference,
}
