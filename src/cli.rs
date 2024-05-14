use std::{
    env::{current_dir, set_current_dir},
    path::PathBuf,
};

use anyhow::bail;
use clap::Parser;

/// Coua certification utility
#[derive(Parser)]
#[command(version, about, long_about = None)]
pub(crate) struct Cli {
    /// Change the directory before doing anything
    #[arg(short, long, value_name = "DIRECTORY")]
    pub(crate) directory: Option<PathBuf>,

    /// Output directory
    #[arg(short, long, value_name = "DIRECTORY")]
    pub(crate) out: Option<PathBuf>,
}

pub(crate) fn process_args(cli: Cli) -> Result<(PathBuf, PathBuf), anyhow::Error> {
    let out_dir: PathBuf = {
        let path = if let Some(out) = cli.out {
            if out.is_absolute() {
                out
            } else {
                let mut path = current_dir()?;
                path.push(out);
                path
            }
        } else {
            current_dir()?
        };
        if path.exists() && !path.is_dir() {
            bail!("{path:?} is not a directory");
        }
        path
    };
    if let Some(dir) = cli.directory {
        set_current_dir(dir)?;
    }
    let manifest_path = {
        let mut path = current_dir()?;
        path.push("coua.toml");
        path.canonicalize()
    }?;

    Ok((out_dir, manifest_path))
}

#[cfg(test)]
mod tests {
    use std::path::PathBuf;

    use super::{process_args, Cli};

    #[test]
    fn with_current_dir() {
        let cli = Cli {
            directory: None,
            out: None,
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_current_dir_and_output_rel() {
        let cli = Cli {
            directory: None,
            out: Some(PathBuf::from("./.")),
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_current_dir_and_output_abs() {
        let cli = Cli {
            directory: None,
            out: Some(PathBuf::from("./.").canonicalize().unwrap()),
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_other_dir() {
        let cli = Cli {
            directory: Some(PathBuf::from("./.").canonicalize().unwrap()),
            out: None,
        };
        process_args(cli).unwrap();
    }
}
