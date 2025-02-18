"""
Abstract ontology definitions
"""

from importlib.resources import files, Package
from typing import Iterable, Tuple

from pyoxigraph import QuerySolutions, Store
from rdflib import Graph, URIRef
from rdflib.namespace import DefinedNamespace

from coua.traces import trace_requirements


@trace_requirements("Req28")
class Ontology:
    """
    An abstract ontology
    """

    namespace: type[DefinedNamespace]
    questions: Package
    selections: Package

    def check(self, graph: Graph) -> Iterable[Tuple[URIRef, bool]]:
        """
        Performs checks defined by the ontology implementation.

        By default will call all ASK questions defined in the ontology module.
        """

        qs = files(self.questions)
        for question in qs.iterdir():
            query = question.read_text()
            name = URIRef(str(self.namespace) + question.name)

            yield name, bool(graph.query(query))

    def select(self, store: Store, query_path_segment: str) -> QuerySolutions:
        """
        Runs a query from the ontology module using its file name.

        Ontologies may override this to modify or filter solutions.
        """

        query: str = files(self.selections).joinpath(query_path_segment).read_text()
        solutions: QuerySolutions = store.query(query)

        return solutions
