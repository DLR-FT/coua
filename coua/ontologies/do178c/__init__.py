from importlib import resources

from typing import Iterable, Tuple

from pyoxigraph import QuerySolutions, Store
from rdflib import URIRef, Graph
from rdflib.namespace import RDFS, DefinedNamespace, Namespace

from coua.ontologies.ontology import Ontology

import coua.ontologies.do178c.ask as questions
import coua.ontologies.do178c.select as selections


class DO178C(DefinedNamespace):
    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/do178c#")

    Requirement: URIRef
    requires: URIRef
    TraceData: URIRef
    TestCase: URIRef
    covers: URIRef


class DO178COntology(Ontology):
    namespace = DO178C

    @staticmethod
    def apply(graph: Graph, **kwargs):
        """Relates the contents of the graph to DO178C.

        This is a helper function that facilitates assignment of subproperty and
        subclass relationships from a user-defined ontology to the DO-178C ontology.
        This is the same as declaring these relationships in a manifest file.
        """

        requirement_class = kwargs["requirement_class"]
        trace_class = kwargs["trace_args"]
        covers_property = kwargs["covers_property"]
        requires_property = kwargs["requires_property"]

        graph.bind("do178c", DO178C)
        graph.add((requirement_class, RDFS.subClassOf, DO178C.Requirement))
        graph.add((requires_property, RDFS.subPropertyOf, DO178C.requires))
        graph.add((trace_class, RDFS.subClassOf, DO178C.TraceData))
        graph.add((covers_property, RDFS.subPropertyOf, DO178C.covers))

    @staticmethod
    def check(graph: Graph) -> Iterable[Tuple[str, bool]]:
        qs = resources.files(questions)
        for question in qs.iterdir():
            query = question.read_text()
            yield question.name, bool(graph.query(query))

    @staticmethod
    def select(store: Store, query_path_segment: str) -> QuerySolutions:
        query: str = (
            resources.files(selections).joinpath(query_path_segment).read_text()
        )
        solutions: QuerySolutions = store.query(query)

        return solutions
