use std::{fmt::Display, fs::File, ops::Deref, str::FromStr};

use anyhow::{bail, Context, Result};
use url::Url;

#[derive(Debug, Clone)]
pub struct ArtifactLocator(Url);

impl Deref for ArtifactLocator {
    type Target = Url;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug, Clone)]
pub struct ArtifactLocatorParseError(url::ParseError);

impl Deref for ArtifactLocatorParseError {
    type Target = url::ParseError;
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl FromStr for ArtifactLocator {
    type Err = ArtifactLocatorParseError;

    fn from_str(s: &str) -> std::result::Result<Self, Self::Err> {
        Ok(Self(s.parse().map_err(ArtifactLocatorParseError)?))
    }
}

impl Display for ArtifactLocator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.0.fmt(f)
    }
}

impl ArtifactLocator {
    pub fn fetch_content(&self) -> Result<File> {
        let scheme = self.0.scheme();
        match scheme {
            "file" => File::open(self.0.path())
                .with_context(|| format!("Failed to open artifact file {self}")),
            _ => bail!(format!("Unsupported URL scheme: {scheme}")),
        }
    }
}
