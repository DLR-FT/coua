from typing import TextIO, TYPE_CHECKING

import morph_kgc
import json

from importlib import resources
from rdflib import Graph, URIRef, Literal
from pathlib import Path

if TYPE_CHECKING:
    from rdflib.graph import Graph

from . import mappings


def load_junit_xml(graph: Graph, file: Path):
    """Loads a JUnit XML file into the store"""

    ms = resources.files(mappings).joinpath("junit.ttl")
    config = f"[Junit]\nmappings: {ms}\nfile_path: {file}\n"
    g = morph_kgc.materialize(config)
    for triple in g:
        graph.add(triple)


def load_test_trace(graph: Graph, file: TextIO):
    """Imports JSON-encoded requirements trace data

    {"Req_001": { "test_it_works": "main.py:10" }}
    """

    data = json.load(file)

    for k, v in data.items():
        for test in v:
            req = URIRef(
                f"https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/requirements#{k}"
            )
            pred = URIRef("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/schema#coveredBy")
            test = Literal(test)
            graph.add((req, pred, test))
