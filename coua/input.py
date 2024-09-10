from typing import TextIO, TYPE_CHECKING

import json

from rdflib import Graph, URIRef, Literal

if TYPE_CHECKING:
    from rdflib.graph import Graph


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
