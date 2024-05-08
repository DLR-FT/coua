use serde::Deserialize;

#[derive(Deserialize)]
pub struct Stakeholder(String);

impl Stakeholder {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

#[derive(Deserialize, Hash)]
pub struct Level(String);
