"""
Ontology for DO-178C
"""

from importlib import resources
from typing import Iterable, Tuple

from malkoha import trace_requirements
from rdflib import URIRef, Literal, Graph
from rdflib.namespace import RDFS, DefinedNamespace, Namespace

from coua.exceptions import CouaException
from coua.ontologies import Ontology

import coua.ontologies.do178c.ask as questions
import coua.ontologies.do178c.select as selections


@trace_requirements("Req68")
class DO178C(DefinedNamespace):
    """
    RDFlib class for ontology namespace
    """

    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/do178c#")

    Requirement: URIRef
    LowLevelRequirement: URIRef
    HighLevelRequirement: URIRef
    SystemLevelRequirement: URIRef
    requires: URIRef
    TraceData: URIRef
    TestCase: URIRef
    covers: URIRef
    traces: URIRef
    requirementDescription: URIRef
    requirementRationale: URIRef


@trace_requirements("Req68")
class DO178COntology(Ontology):
    """
    RDFlib class for ontology
    """

    namespace = DO178C
    questions = questions
    selections = selections

    def check(self, graph: Graph) -> Iterable[Tuple[URIRef, Literal, bool]]:
        check_is_do178c(graph)
        qs = list(
            map(
                lambda p: (resources.files(self.questions) / p[0], Literal(p[1])),
                [
                    (
                        "obj-6.3.2.f.rq",
                        "DO-178C-6.3.2.f",
                    ),
                    (
                        "obj-6.3.4.e.rq",
                        "DO-178C-6.3.4.e",
                    ),
                    (
                        "obj-6.3.1.f.rq",
                        "DO-178C-6.3.1.f",
                    ),
                ],
            )
        )
        for question, name in qs:
            with open(str(question), "r", encoding="utf-8") as f:
                query = f.read()
            uri = URIRef(str(self.namespace) + name)

            yield uri, name, bool(graph.query(query))


@trace_requirements("Req67")
def check_is_do178c(graph: Graph):
    """
    Checks if the graph contains the DO-178C ontology.
    """

    rdfsub = RDFS.subClassOf
    do178creq = DO178COntology.namespace.Requirement
    query = f"ASK {{ ?r <{rdfsub}> <{do178creq}> }}"

    if not graph.query(query):
        raise CouaException(
            "Bindings from input data to DO-178C ontology not provided in input data."
        )
