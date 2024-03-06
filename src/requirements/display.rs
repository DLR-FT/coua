use std::{
    borrow::Cow,
    collections::hash_map::DefaultHasher,
    hash::{Hash, Hasher},
};

use super::*;

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
