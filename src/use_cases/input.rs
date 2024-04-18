use std::collections::HashMap;

use anyhow::Context;
use serde::Deserialize;

use crate::{UseCase, UseCaseId};

pub fn parse_use_cases(ucs: &str) -> Result<UseCaseData, anyhow::Error> {
    toml::from_str(ucs).with_context(|| "Failed to read use-cases")
}

// Not used right now, only parsed
#[allow(dead_code)]
#[derive(Deserialize)]
pub struct UseCaseData(HashMap<UseCaseId, UseCase>);

#[cfg(test)]
mod tests {
    use std::{fs::read_to_string, path::PathBuf};

    use crate::parse_use_cases;

    #[test]
    fn test_load_use_cases() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("use-cases.toml");
        let use_cases = read_to_string(file).unwrap();
        parse_use_cases(&use_cases).unwrap();
    }

    #[test]
    fn test_load_unknown_field() {
        let ucs = r#"
[UC05]
unknown = "field"
title = "Shared Reality"
actor = "Developer"
goal = "DLR-SMART3"
scope = "ADF"
affects = [2.2, 2.3, 4.1]
level = "System"
story = "As a developer I want the certification framework to produce the same results every time I give it the same inputs as someone else so that everyone has a shared reality of the current certification status of the project."
stakeholders = ["Developer", "Reviewer", "Certification Authority"]
pre = ["The project's artifacts are reproducible in a way that they do not change if they are created twice from the same data."]
trigger = "The certification status is queried by a stakeholder."
flow = ["The artifacts are reproducibly retrieved or created.", "All stakeholders run the certification framework using the same version of the artifacts."]
post = ["All stakeholders get the same certification results."]
extensions = ["As the certification authority I want to inspect the identical report as the developer so that I am sure to certify the right revision of the product."]        "#;
        assert!(parse_use_cases(ucs).is_err());
    }
}
