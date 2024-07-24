from typing import Iterable, Tuple

from rdflib.namespace import DefinedNamespace
from rdflib import Graph
from pyoxigraph import QuerySolutions, Store


class Ontology:
    namespace: type[DefinedNamespace]

    @staticmethod
    def apply(graph: Graph, **kwargs):
        pass

    @staticmethod
    def check(graph: Graph) -> Iterable[Tuple[(str, bool)]]:
        return []

    @staticmethod
    def select(store: Store, query_path_segment: str) -> QuerySolutions:
        return QuerySolutions()
