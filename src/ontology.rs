#![allow(dead_code)]

use std::path::PathBuf;

use serde::Deserialize;

#[derive(Deserialize)]
pub struct OntologyLocator(PathBuf);

#[derive(Deserialize)]
pub struct OntologyName(String);

#[derive(Deserialize)]
pub struct OntologyReference(String);

#[derive(Deserialize)]
pub struct Ontology {
    pub name: OntologyName,
    pub source: OntologyLocator,
    pub reference: OntologyReference,
}
