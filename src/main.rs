use std::{
    fs::{self, read_to_string, File},
    io::BufReader,
};

use clap::Parser;
use oxigraph::{
    io::GraphFormat::Turtle, model::GraphNameRef, sparql::QueryResultsFormat, store::Store,
};
use sparesults::{QueryResultsParser, QueryResultsReader};

mod cli;

fn main() -> anyhow::Result<()> {
    let cli = cli::Cli::parse();
    let (inputs, queries, out_dir) = cli::process_args(cli)?;
    if !out_dir.exists() {
        fs::create_dir(&out_dir)?;
    }

    let store = Store::new()?;
    let loader = store.bulk_loader();
    for input in inputs.into_iter() {
        loader.load_graph(
            BufReader::new(File::open(input)?),
            Turtle,
            GraphNameRef::DefaultGraph,
            None,
        )?;
    }

    let mut out_files = vec![];
    // TODO run in parallel
    for query in queries.iter() {
        let result = store.query(&read_to_string(query)?)?;
        let out_file = {
            let mut file = query
                .as_path()
                .file_stem()
                .unwrap()
                .to_str()
                .unwrap()
                .to_owned();
            file.push_str(".json");
            let mut dir = out_dir.clone();
            dir.push(file);
            dir
        };
        result.write(File::create(out_file.clone())?, QueryResultsFormat::Json)?;
        out_files.push(out_file);
    }

    let mut exit = 0i32;
    // TODO run in parallel
    for out_file in out_files.iter() {
        let json_parser = QueryResultsParser::from_format(QueryResultsFormat::Json);
        let results = json_parser.read_results(BufReader::new(File::open(out_file)?))?;
        // Result of an ASK query, certifying something about the input using the standard, true means there exists a defect
        if let QueryResultsReader::Boolean(true) = results {
            exit += 1
        }
    }

    std::process::exit(exit);
}
