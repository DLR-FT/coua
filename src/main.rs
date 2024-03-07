// ontology => contains objective
// manifest maps objective to evidences
// manifest maps evidences to tool/invocation
// tool outputs report
// coua collects reports

use std::fs::File;
use std::io::{self, stdout};

use anyhow::Context;
use coua::requirements::{load_file, RequirementsData};

pub fn display_requirements<T: io::Read>(file: T) -> anyhow::Result<()> {
    let reqs: RequirementsData =
        load_file(file).with_context(|| "Failed to read requirements from standard input")?;
    let reqs = reqs
        .try_into_reqs()
        .with_context(|| "Failed to transform requirements into graph")?;
    reqs.render_to(&mut stdout())
        .with_context(|| "Failed to render requirements")
}

fn main() -> anyhow::Result<()> {
    let project_path = std::env::current_dir()?;
    let mut requirements = project_path.clone();
    requirements.push("requirements.yml");
    let requirements = File::open(requirements)?;
    display_requirements(requirements)?;
    Ok(())
}
