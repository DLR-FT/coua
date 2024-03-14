#![feature(register_tool)] // For marking tests that cover requirements in the AST
#![register_tool(coua)]
#![allow(dead_code)]

mod artifact;
mod check;
mod data;
mod do178c;
mod manifest;
mod ontology;
mod requirements;
mod use_cases;

pub use check::check;
pub use manifest::get_manifest;
