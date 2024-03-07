use serde::{Deserialize, Serialize};

use crate::{artifact::Artifact, ontology::Ontology};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CouaManifest {
    #[serde(rename = "model")]
    pub models: Vec<Ontology>,
    #[serde(rename = "artifact")]
    pub artifacts: Vec<Artifact>,
}
