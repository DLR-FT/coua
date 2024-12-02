import json
import logging
import sys

from argparse import ArgumentParser, Namespace
from pathlib import Path

from .traces import get_traces
from .config import parse_config
from .checks import run_checks

from coua.ontologies import DO178C

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
    trace.set_defaults(func=traces_cmd)

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
    results = run_checks(config["artifacts"], args.output, ontology, args.extra_triples)
    for check, status in results.items():
        if status:
            status_out = "✓"
        else:
            status_out = "x"
        logger.info(f"{check}: {status_out}")
    if any(not x for x in results.values()):
        sys.exit("There were failed checks")


def traces_cmd(args: Namespace):
    for file in args.source_files:
        for trace in get_traces(Path(file)):
            print(json.dumps(trace.__dict__))
