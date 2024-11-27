from importlib.resources import files, Package
from pyoxigraph import QuerySolutions, Store
from rdflib import Graph
from rdflib.namespace import DefinedNamespace
from typing import Iterable, Tuple


class Ontology:
    namespace: type[DefinedNamespace]
    questions: Package
    selections: Package

    def check(self, graph: Graph) -> Iterable[Tuple[str, bool]]:
        qs = files(self.questions)
        for question in qs.iterdir():
            query = question.read_text()
            yield question.name, bool(graph.query(query))

    def select(self, store: Store, query_path_segment: str) -> QuerySolutions:
        query: str = files(self.selections).joinpath(query_path_segment).read_text()
        solutions: QuerySolutions = store.query(query)

        return solutions
