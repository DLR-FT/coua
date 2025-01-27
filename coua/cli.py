import logging
import sys
import os

from argparse import ArgumentParser, Namespace
from xml.etree import ElementTree as ET

from os import listdir

from coua.config import parse_config, parse_artifacts, init_config
from coua.checks import run_checks, CheckResults
from coua.ontologies import DO178C, Coua, load_ontologies
from coua.traces import get_traces, trace_requirements

logger = logging.getLogger(__name__)


@trace_requirements("Req53", "Req54", "Req55")
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
    trace.add_argument("path", nargs="?", help="path to process", default=".")
    trace.set_defaults(func=traces_cmd)

    init = subcmds.add_parser("init", help="Init project")
    init.add_argument(
        "--mode", default="do178c", help="Chooses the check mode for the project"
    )
    init.set_defaults(func=init_cmd)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


@trace_requirements("Req53", "Req57")
def check_cmd(args: Namespace):
    config = parse_config(args.config)
    artifacts = config.get("artifacts", dict())
    store = parse_artifacts(artifacts)
    load_ontologies(store)

    for triple in args.extra_triples:
        store.bulk_load(triple, "application/n-triples")

    store.flush()

    results = CheckResults()
    for check in config["checks"]:
        match check:
            case "do178c":
                check_results = run_checks(store, DO178C())
            case "coua":
                check_results = run_checks(store, Coua())
            case _:
                sys.exit(f"Unknown ontology {check}")

        for check, status in check_results.items():
            if status:
                status_out = "✓"
            else:
                status_out = "x"
            logger.info(f"{check}: {status_out}")

        results = CheckResults({**results, **check_results})

    store.dump(args.output, "application/n-triples")

    if any(not x for x in results.values()):
        sys.exit("There were failed checks")


@trace_requirements("Req54")
def traces_cmd(args: Namespace):
    traces = ET.Element("traces")
    for trace in get_traces(args.path):
        trace_el = ET.SubElement(traces, "trace", requirement_id=trace.requirement_id)
        line = str(trace.location.line)
        file = trace.location.file
        location = ET.SubElement(
            trace_el,
            "location",
            line=line,
            file=file,
        )
        location.text = f"{file}:{line}"
    tree = ET.ElementTree(traces)
    with open("traces.xml", "wb") as f:
        tree.write(f)


@trace_requirements("Req55")
def init_cmd(args: Namespace):
    if os.path.exists("coua.toml"):
        sys.exit("coua.toml already exists")
    files = listdir(".")
    with open("coua.toml", "w") as config:
        init_config(config, files, args.mode)
    if os.path.exists(".gitignore"):
        with open(".gitignore", "a") as gitignore:
            gitignore.write("\ncoua.nt\n")
