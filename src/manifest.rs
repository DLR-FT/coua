use std::io;

use anyhow::Context;
use serde::{Deserialize, Serialize};

use crate::{artifact::Artifact, ontology::Ontology};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouaManifest {
    #[serde(rename = "model")]
    pub models: Vec<Ontology>,
    #[serde(rename = "artifact")]
    pub artifacts: Vec<Artifact>,
}

pub fn parse_manifest<T: io::Read>(mut file: T) -> anyhow::Result<CouaManifest> {
    let mut manifest = String::new();
    let _ = file
        .read_to_string(&mut manifest)
        .with_context(|| "Failed to read from manifest file")?;
    let manifest = toml::from_str(&manifest).with_context(|| "Failed to parse manifest")?;
    Ok(manifest)
}

#[cfg(test)]
mod tests {
    use std::{fs::File, path::PathBuf};

    use crate::parse_manifest;

    #[test]
    fn parse() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("coua.toml");
        parse_manifest(File::open(file).unwrap()).unwrap();
    }
}
