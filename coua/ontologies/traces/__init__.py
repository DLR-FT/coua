"""
Ontology for Coua traces.xml
"""

import urllib
import json

from malkoha import trace_requirements
from malkoha.data import Trace
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from types import ModuleType
from pyoxigraph import NamedNode, Quad, Literal, Store

from coua.ontologies import Ontology


@trace_requirements("Req72")
class Traces(DefinedNamespace):
    """
    RDFlib class for ontology namespace
    """

    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#")

    Event: URIRef
    Location: URIRef

    file: URIRef
    line: URIRef
    requirement_id: URIRef


@trace_requirements("Req72")
class TracesOntology(Ontology):
    """
    RDFlib class for ontology
    """

    namespace = Traces
    questions = ModuleType("questions")
    selections = ModuleType("selections")


@trace_requirements("Req58")
def parse_malkoha_output(g: Store, path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            trace = Trace(
                d["location"]["name"],
                d["location"]["file"],
                d["location"]["line"],
                d["requirements"],
            )
            t = "https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces"
            file = urllib.parse.quote(trace.location.file, safe="")
            line = trace.location.line
            g.extend(
                (
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#file"),
                        Literal(trace.location.file),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                        NamedNode(f"{t}#Location"),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#line"),
                        Literal(trace.location.line),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#displayName"),
                        Literal(trace.location.name),
                    ),
                    Quad(
                        NamedNode(f"{t}#event/{file}/{line}"),
                        NamedNode(f"{t}#location"),
                        NamedNode(f"{t}#location/{file}/{line}"),
                    ),
                )
            )
            if trace.requirements:
                for requirement in trace.requirements:
                    g.extend(
                        (
                            Quad(
                                NamedNode(f"{t}#event/{file}/{line}"),
                                NamedNode(f"{t}#requirement_id"),
                                Literal(requirement),
                            ),
                            Quad(
                                NamedNode(f"{t}#event/{file}/{line}"),
                                NamedNode(
                                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
                                ),
                                NamedNode(f"{t}#Event"),
                            ),
                        )
                    )
