use std::{
    borrow::Cow,
    cell::RefCell,
    collections::hash_map::DefaultHasher,
    collections::HashMap,
    hash::{Hash, Hasher},
    io::{self, Write},
    ops::Deref,
};

use anyhow::Context;

use super::*;

#[derive(Debug, Clone)]
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

    pub fn render_to<W: Write>(&'a self, output: &mut W) -> io::Result<()> {
        dot::render(self, output)
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

pub fn display_requirements<T: io::Read, O: io::Write>(file: T, mut out: O) -> anyhow::Result<()> {
    let reqs: RequirementsData =
        load_requirements(file).with_context(|| "Failed to read requirements from file")?;
    let reqs = reqs
        .try_into_reqs()
        .with_context(|| "Failed to transform requirements into graph")?;
    reqs.render_to(&mut out)
        .with_context(|| "Failed to render requirements")
}
