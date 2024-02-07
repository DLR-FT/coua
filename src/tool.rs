use std::process::Command;
use url::Url;

pub struct CouaURI {
    uri: Url,
}

impl std::str::FromStr for CouaURI {
    type Err = anyhow::Error;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(Self {
            uri: Url::parse(s)?,
        })
    }
}

impl CouaURI {
    pub fn execute_command(&mut self) -> anyhow::Result<std::process::Output> {
        let command_str = self
            .uri
            .host_str()
            .and_then(|s| s.split_once("-"))
            .ok_or_else(|| anyhow::anyhow!("Failed to convert URI to command"))?;

        let mut command = Command::new(command_str.0);
        let command = command.arg(command_str.1);
        println!("running {:?}", command);

        command.output().map_err(Into::into)
    }
}
