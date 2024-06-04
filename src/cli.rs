use std::{
    env::{current_dir, set_current_dir},
    path::PathBuf,
};

use anyhow::bail;
use clap::Parser;

/// Coua certification utility
#[derive(Parser)]
#[command(version, about, long_about = None)]
pub struct Cli {
    /// Change the directory before doing anything
    #[arg(short = 'D', long, value_name = "DIRECTORY")]
    pub(crate) directory: Option<PathBuf>,

    /// Resources in Turtle notation to reason about
    pub(crate) inputs: Vec<PathBuf>,

    /// Standard to use for arguing
    #[arg(short, long, value_name = "DIRECTORY")]
    pub(crate) standard: PathBuf,

    /// Output directory
    #[arg(short, long, value_name = "DIRECTORY")]
    pub(crate) out: Option<PathBuf>,
}

pub fn process_args(cli: Cli) -> anyhow::Result<(Vec<PathBuf>, Vec<PathBuf>, PathBuf)> {
    if let Some(dir) = cli.directory {
        set_current_dir(dir)?;
    }
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

    let mut inputs = cli.inputs.clone();
    let mut queries = vec![];
    for entry in cli.standard.read_dir()? {
        let Ok(entry) = entry else { continue };
        let path = entry.path();
        let Some(ext) = path.extension() else {
            continue;
        };
        match ext.to_str() {
            Some("ttl") => inputs.push(path),
            Some("rq") => queries.push(path),
            _ => (),
        }
    }

    Ok((inputs, queries, out_dir))
}

#[cfg(test)]
mod tests {
    use std::{env::current_dir, path::PathBuf};

    use super::{process_args, Cli};

    #[test]
    fn with_current_dir() {
        let cli = Cli {
            directory: None,
            out: None,
            inputs: vec![],
            standard: current_dir().unwrap(),
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_current_dir_and_output_rel() {
        let cli = Cli {
            directory: None,
            out: Some(PathBuf::from("./.")),
            inputs: vec![],
            standard: current_dir().unwrap(),
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_current_dir_and_output_abs() {
        let cli = Cli {
            directory: None,
            out: Some(PathBuf::from("./.").canonicalize().unwrap()),
            inputs: vec![],
            standard: current_dir().unwrap(),
        };
        process_args(cli).unwrap();
    }

    #[test]
    fn with_other_dir() {
        let cli = Cli {
            directory: Some(PathBuf::from("./.").canonicalize().unwrap()),
            out: None,
            inputs: vec![],
            standard: current_dir().unwrap(),
        };
        process_args(cli).unwrap();
    }
}
