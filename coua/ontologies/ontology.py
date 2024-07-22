from rdflib.namespace import DefinedNamespace
from rdflib import Graph
from pyoxigraph import QuerySolutions, Store


class Ontology:
    namespace: DefinedNamespace

    def apply(graph: Graph, **kwargs):
        pass

    def check(graph: Graph) -> iter(str, bool):
        return []

    def select(store: Store, query_path_segment: str) -> QuerySolutions:
        return QuerySolutions()
