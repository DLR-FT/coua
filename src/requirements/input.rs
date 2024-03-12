use anyhow::Context;

use crate::RequirementsData;

pub fn parse_requirements(requirements: &str) -> anyhow::Result<RequirementsData> {
    toml::from_str(requirements).with_context(|| "Failed to read requirements")
}

#[cfg(test)]
mod tests {
    use std::{fs::read_to_string, path::PathBuf};

    use super::parse_requirements;

    #[test]
    fn process_example() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("requirements.toml");
        let requirements = read_to_string(file).expect("Failed to open requirements file");
        parse_requirements(&requirements).unwrap();
    }

    #[test]
    fn unknown_key() {
        let requirements = r#"
          [Req01]
description = "The certification framework shall provide a library of functions for ingesting artifacts produced by COTS tools."
owner = "DLR"
level = "functional"
use-cases = [ "UC04" ]
unknown = "key"
        "#;
        assert!(parse_requirements(requirements).is_err());
    }
}
