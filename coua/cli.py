import sys

from pyoxigraph import Store
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS

from coua.input import load_junit_xml, load_test_trace
from coua.ontologies import DO178C
from coua.exceptions import CouaException

import logging

logger = logging.getLogger(__name__)


def convert_junit():
    junit = sys.argv[1:-1]
    out = sys.argv[-1]

    graph = Graph()
    for f in junit:
        load_junit_xml(graph, junit)

    with open(out, "w") as out:
        graph.print(format="turtle", out=out)


def convert_cargo_requirements():
    traces = sys.argv[1:-1]
    out = sys.argv[-1]

    graph = Graph()
    for trace in traces:
        with open(trace, "r") as f:
            load_test_trace(graph, f)

    with open(out, "w") as out:
        graph.print(format="turtle", out=out)


def run_check_do178c():
    resources = sys.argv[1:]
    store = Store()

    for f in resources:
        store.bulk_load(f, "text/turtle")

    store.flush()

    try:
        check_is_do178c(store)
    except CouaException as e:
        logger.error(e)
        sys.exit(1)

    fail = None
    for check, status in DO178C.check(store):
        print(f"{check}: {status}")
        if not status:
            fail = status

    sys.exit(fail)


def check_is_do178c(store):
    rdfsub = RDFS.subClassOf
    do178creq = DO178C.namespace.Requirement
    query = f"ASK {{ ?r <{rdfsub}> <{do178creq}> }}"

    if not store.query(query):
        raise CouaException(
            "Bindings from input data to DO-178C ontology not provided in input data. May need to generate bindings using coua-gen-do178c."
        )


def gen_do178c_bindings():
    """Run this once to create or update the bindings from your ontology to DO-178C."""

    graph = Graph()

    DO178C.apply(
        graph,
        requirement_class=URIRef(sys.argv[1]),
        trace_class=URIRef(sys.argv[2]),
        covers_property=URIRef(sys.argv[3]),
        requires_property=URIRef(sys.argv[4]),
    )

    with open(sys.argv[5], "w") as out:
        graph.print(format="turtle", out=out)
