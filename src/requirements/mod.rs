mod data;
mod display;
mod input;

pub use data::*;
pub use input::load_file;
pub use input::RequirementsData;

use anyhow::{anyhow, Result};

use std::{
    cell::RefCell,
    collections::HashMap,
    io::{self, Write},
    ops::Deref,
};

#[derive(Debug, Clone)]
pub struct Req<'a, 'b>
where
    'b: 'a,
{
    pub id: &'a ReqId,
    pub description: &'a ReqDesc,
    pub owner: &'a ReqOwner,
    pub level: &'a ReqLevel,
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
    pub fn render_to<W: Write>(&'a self, output: &mut W) -> io::Result<()> {
        dot::render(self, output)
    }
}
