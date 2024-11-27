from typing import Iterable, Tuple

from rdflib import URIRef, Graph
from rdflib.namespace import RDFS, DefinedNamespace, Namespace

from coua.exceptions import CouaException

import coua.ontologies.do178c.ask as questions
import coua.ontologies.do178c.select as selections

from coua.ontologies import Ontology


class DO178C(DefinedNamespace):
    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/do178c#")

    Requirement: URIRef
    requires: URIRef
    TraceData: URIRef
    TestCase: URIRef
    covers: URIRef


class DO178COntology(Ontology):
    namespace = DO178C
    questions = questions
    selections = selections

    def check(self, graph: Graph) -> Iterable[Tuple[str, bool]]:
        check_is_do178c(graph)

        return super().check(graph)


def check_is_do178c(graph: Graph):
    rdfsub = RDFS.subClassOf
    do178creq = DO178COntology.namespace.Requirement
    query = f"ASK {{ ?r <{rdfsub}> <{do178creq}> }}"

    if not graph.query(query):
        raise CouaException(
            "Bindings from input data to DO-178C ontology not provided in input data. May need to generate bindings using coua-gen-do178c."
        )
