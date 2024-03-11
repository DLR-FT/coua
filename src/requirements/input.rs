use std::{cell::RefCell, collections::HashMap, io};

use super::{
    display::{Req, Reqs},
    *,
};
use anyhow::{anyhow, bail, Context, Result};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct RequirementsData(HashMap<ReqId, Requirement>);

impl RequirementsData {
    // TODO impl TryInto
    pub fn try_into_reqs<'a, 'b>(&'a self) -> Result<&'b Reqs<'a, 'b>> {
        // Lives on the heap
        let rs: Box<Reqs<'a, 'b>> = Box::new(Reqs::new(
            self.0
                .iter()
                .map(|(id, req)| {
                    (
                        id.clone(),
                        // Allows us to use dynamic lifetimes when modifying the traces between requirements
                        RefCell::new(Req {
                            id,
                            description: &req.description,
                            owner: &req.owner,
                            level: &req.level,
                            use_cases: req.use_cases.iter().collect(),
                            trace: Default::default(), // init later
                        }),
                    )
                })
                .collect(),
        ));

        // We leak this returning a reference that lives as long as the contained data.
        // This is neccessary so that the requirement values do not get moved or freed, potentially invalidating the references.
        // The memory will be freed when the process exits, which is fine in this case.
        let rs = Box::leak(rs);

        for (l_rid, rdat) in self.0.iter() {
            for r_rid in rdat.trace.iter() {
                if l_rid == r_rid {
                    bail!("Requirement is referencing itself");
                }
                // Safety: This is safe becasue the reference in trace is not used while `rs` is beeing modified
                // It is required so we can later mutably borrow `r_req` to modify its trace targets.
                let r_req = unsafe {
                    rs.get(r_rid)
                        .ok_or(anyhow!("Unknown requirement '{}'", r_rid))?
                        .try_borrow_unguarded()
                        .unwrap()
                };
                rs.get(l_rid).unwrap().borrow_mut().trace.push(r_req);
            }
        }

        Ok(rs)
    }
}

pub fn load_requirements<T: io::Read>(mut file: T) -> anyhow::Result<RequirementsData> {
    let mut requirements = String::new();
    let _ = file.read_to_string(&mut requirements);
    toml::from_str(&requirements).with_context(|| "Failed to read requirements")
}

#[cfg(test)]
mod tests {
    use std::{fs::File, io::BufReader, path::PathBuf};

    use super::load_requirements;

    #[test]
    fn process_example() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("requirements.toml");
        let file = File::open(file).expect("Failed to open requirements file");
        let file = BufReader::new(file);
        load_requirements(file).unwrap().try_into_reqs().unwrap();
    }
}
