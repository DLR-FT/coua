import json
import logging
import sys

from argparse import ArgumentParser, Namespace
from pyoxigraph import Store
from rdflib.namespace import RDFS
from pathlib import Path

import coua.traces

from coua.ontologies import DO178C, load_ontologies
from coua.exceptions import CouaException

logger = logging.getLogger(__name__)


def run():
    parser = ArgumentParser()
    subcmds = parser.add_subparsers(help="subcommand help")

    check = subcmds.add_parser("check", help="perform checks")
    check.add_argument("--mode", choices=["do178c"], default="do178c")
    check.add_argument("triples", help="N-Triples file")
    check.set_defaults(func=check_cmd)

    trace = subcmds.add_parser("trace", help="Get trace info")
    trace.add_argument("file", nargs="*", help="files to process")
    trace.set_defaults(func=get_traces)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_help()
        sys.exit(1)


def check_cmd(args: Namespace):
    mode = args.mode
    triples = args.triples
    if mode == "do178c":
        res = run_check_do178c(triples)
        if res > 0:
            sys.exit("There were failed checks")


def run_check_do178c(triples: str) -> int:
    store = Store()
    load_ontologies(store)
    store.bulk_load(triples, "application/n-triples")
    store.flush()
    check_is_do178c(store)
    fail = 0
    for check, status in DO178C.check(store):
        if status:
            status_out = "✓"
        else:
            status_out = "x"
        print(f"{check}: {status_out}")
        if not status:
            fail += 1

    return fail


def check_is_do178c(store):
    rdfsub = RDFS.subClassOf
    do178creq = DO178C.namespace.Requirement
    query = f"ASK {{ ?r <{rdfsub}> <{do178creq}> }}"

    if not store.query(query):
        raise CouaException(
            "Bindings from input data to DO-178C ontology not provided in input data. May need to generate bindings using coua-gen-do178c."
        )


def get_traces(args: Namespace):
    for file in args.file:
        for trace in coua.traces.get_traces(Path(file)):
            print(json.dumps(trace.__dict__))
