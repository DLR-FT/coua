import json
import logging
import morph_kgc
import sys
import tomllib

from argparse import ArgumentParser, Namespace
from pyoxigraph import Store
from pathlib import Path

import coua.traces

from coua.ontologies import DO178C, load_ontologies, Ontology

logger = logging.getLogger(__name__)


def run():
    parser = ArgumentParser()
    subcmds = parser.add_subparsers(help="Subcommand help")

    check = subcmds.add_parser("check", help="Perform checks on artifact files")
    check.add_argument(
        "-e",
        "--extra-triples",
        help="Additional N-Triples files []",
        nargs="*",
        default=[],
    )
    # TODO use own config file
    check.add_argument(
        "-c",
        "--config",
        help="configuration file [coua.toml]",
        default="coua.toml",
    )
    check.add_argument(
        "-o",
        "--output",
        help="output file [coua.nt]",
        default="coua.nt",
        required=False,
    )
    check.set_defaults(func=check_cmd)

    trace = subcmds.add_parser("trace", help="Get trace info from source code")
    trace.add_argument("source_files", nargs="*", help="files to process")
    trace.set_defaults(func=get_traces)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


def check_cmd(args: Namespace):
    config = parse_config(args.config)
    mode = config["mode"]
    if mode == "do178c":
        ontology = DO178C()
    if run_checks(config["artifacts"], args.output, ontology, args.extra_triples) > 0:
        sys.exit("There were failed checks")


def run_checks(artifacts, output, ontology: Ontology, extra_triples: list[str]) -> int:
    store = parse_artifacts(artifacts, output)
    load_ontologies(store)
    for triple in extra_triples:
        store.bulk_load(triple, "application/n-triples")
    store.flush()
    fail = 0
    for check, status in ontology.check(store):
        if status:
            status_out = "✓"
        else:
            status_out = "x"
        logging.info(f"{check}: {status_out}")
        if not status:
            fail += 1

    store.dump(output, "application/n-triples")

    return fail


def get_traces(args: Namespace):
    for file in args.source_files:
        for trace in coua.traces.get_traces(Path(file)):
            print(json.dumps(trace.__dict__))


def parse_artifacts(artifacts: dict, output: str) -> Store:
    config = ""
    for name, artifact in artifacts.items():
        config += f"[{name}]\n"
        for key, value in artifact["morph"].items():
            config += f"{key}: {value}\n"
    g = morph_kgc.materialize_oxigraph(config)
    logger.info(f"Output written to {output}")

    return g


def parse_config(path: str) -> dict:
    p = Path(path)
    with open(p, "rb") as config:
        return tomllib.load(config)
