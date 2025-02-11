"""
Ontology for DO-178C
"""

from typing import Iterable, Tuple

from rdflib import URIRef, Graph
from rdflib.namespace import RDFS, DefinedNamespace, Namespace

from coua.exceptions import CouaException
from coua.ontologies import Ontology
from coua.traces import trace_requirements

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


@trace_requirements("Req68")
class DO178COntology(Ontology):
    """
    RDFlib class for ontology
    """

    namespace = DO178C
    questions = questions
    selections = selections

    def check(self, graph: Graph) -> Iterable[Tuple[URIRef, bool]]:
        check_is_do178c(graph)

        return super().check(graph)


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
