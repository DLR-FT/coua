use std::path::PathBuf;

use anyhow::Context;
use serde::Deserialize;

use crate::{artifact::Artifact, ontology::Ontology};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CouaManifest {
    #[serde(rename = "model")]
    pub models: Vec<Ontology>,
    #[serde(rename = "artifact")]
    pub artifacts: Vec<Artifact>,
}

pub fn parse_manifest(manifest: &str) -> Result<CouaManifest, anyhow::Error> {
    toml::from_str(manifest).with_context(|| "Failed to parse manifest")
}

#[cfg(test)]
mod tests {
    use std::{fs::read_to_string, path::PathBuf};

    use crate::parse_manifest;

    #[coua::requirement = "Req01"]
    #[test]
    fn parse_example() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("coua.toml");
        let manifest = read_to_string(file).unwrap();
        parse_manifest(&manifest).unwrap();
    }

    #[test]
    fn parse_invalid() {
        assert!(parse_manifest(
            r#"
[[unknown]]
name = "ED-12C"
source = "file:models/do178c.owl"
# Source document for text references to point to
reference = "https://eshop.eurocae.net/eurocae-documents-and-reports/ed-12c-with-corrigendum-1"
            "#,
        )
        .is_err());
    }
}
