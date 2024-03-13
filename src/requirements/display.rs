use std::{
    borrow::Cow,
    cell::RefCell,
    collections::hash_map::DefaultHasher,
    collections::HashMap,
    hash::{Hash, Hasher},
    ops::Deref,
};

use anyhow::{anyhow, bail};

use super::*;

pub struct Req<'a, 'b>
where
    'b: 'a,
{
    pub id: &'a ReqId,
    pub description: &'a ReqDesc,
    pub owner: &'a Stakeholder,
    pub level: &'a Level,
    // TODO use reference to actual use-case
    pub use_cases: Vec<&'a UseCaseId>,
    pub trace: Vec<&'b Req<'a, 'b>>,
}

pub struct Reqs<'a, 'b>(HashMap<ReqId, RefCell<Req<'a, 'b>>>);

impl<'a, 'b> Deref for Reqs<'a, 'b> {
    type Target = HashMap<ReqId, RefCell<Req<'a, 'b>>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<'a, 'b> Reqs<'a, 'b> {
    pub fn new(value: HashMap<ReqId, RefCell<Req<'a, 'b>>>) -> Self {
        Self(value)
    }
}

impl<'a> dot::Labeller<'a, &'a Req<'a, 'a>, (&'a Req<'a, 'a>, &'a Req<'a, 'a>)> for Reqs<'a, 'a> {
    fn graph_id(&'a self) -> dot::Id<'a> {
        dot::Id::new("G").unwrap()
    }

    fn node_id(&'a self, n: &&'a Req<'a, 'a>) -> dot::Id<'a> {
        dot::Id::new(format!("{}", n.id)).unwrap()
    }

    fn node_label(&'a self, n: &&'a Req<'a, 'a>) -> dot::LabelText<'a> {
        let use_cases: String = itertools::join(n.use_cases.iter().map(|v| v.as_str()), ",");
        dot::LabelText::LabelStr(Cow::Owned(format!(
            "{} ({}@{})\n{}",
            n.id.as_str(),
            use_cases,
            n.owner.as_str(),
            n.description.as_str(),
        )))
    }

    fn node_color(&'a self, node: &&'a Req<'a, 'a>) -> Option<dot::LabelText<'a>> {
        let mut hasher = DefaultHasher::default();
        node.level.hash(&mut hasher);
        let color = match hasher.finish() % 6 {
            0..=1 => "red",
            2..=3 => "green",
            4..=5 => "blue",
            _ => "magenta",
        };
        Some(dot::LabelText::LabelStr(Cow::Borrowed(color)))
    }
}

impl<'a> dot::GraphWalk<'a, &Req<'a, 'a>, (&'a Req<'a, 'a>, &'a Req<'a, 'a>)> for Reqs<'a, 'a> {
    fn nodes(&'a self) -> dot::Nodes<'a, &'a Req<'a, 'a>> {
        Cow::Owned(
            self.values()
                .map(|v| unsafe { v.try_borrow_unguarded().unwrap() })
                .collect(),
        )
    }

    fn edges(&'a self) -> dot::Edges<'a, (&'a Req<'a, 'a>, &'a Req<'a, 'a>)> {
        let mut edges = vec![];
        for node in self.values() {
            let mut es = vec![];
            let node = unsafe { node.try_borrow_unguarded() }.unwrap();
            for t in node.trace.iter() {
                es.push((node, *t));
            }
            edges.append(&mut es)
        }

        Cow::Owned(edges)
    }

    fn source(&'a self, edge: &(&'a Req<'a, 'a>, &'a Req<'a, 'a>)) -> &Req<'a, 'a> {
        edge.0
    }

    fn target(&'a self, edge: &(&'a Req<'a, 'a>, &'a Req<'a, 'a>)) -> &Req<'a, 'a> {
        edge.1
    }
}

impl<'a, 'b> TryFrom<&'a RequirementsData> for &'b Reqs<'a, 'b> {
    type Error = anyhow::Error;

    fn try_from(value: &'a RequirementsData) -> Result<&'b Reqs<'a, 'b>, Self::Error> {
        // Lives on the heap
        let rs: Box<Reqs<'a, 'b>> = Box::new(Reqs::new(
            value
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

        for (l_rid, rdat) in value.iter() {
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

#[cfg(test)]
mod test {
    use std::{fs::read_to_string, io::sink, path::PathBuf};

    use anyhow::Result;

    use crate::parse_requirements;

    use super::Reqs;

    #[test]
    fn display_example() {
        let mut file = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
        file.push("requirements.toml");
        let binding = parse_requirements(&read_to_string(file).unwrap()).unwrap();
        let reqs: &Reqs<'_, '_> = (&binding).try_into().unwrap();
        dot::render(reqs, &mut sink()).unwrap()
    }

    #[test]
    fn reference_cycle() {
        let rs = parse_requirements(
            r#"
[Req01]
description = "The certification framework shall provide a library of functions for ingesting artifacts produced by COTS tools."
owner = "DLR"
level = "system"
use-cases = [ "UC04" ]
trace = "Req01"
            "#,
        ).unwrap();
        let reqs: Result<&Reqs<'_, '_>> = (&rs).try_into();
        assert!(reqs.is_err());
    }
}
