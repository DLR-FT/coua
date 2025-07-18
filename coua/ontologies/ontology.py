"""
Abstract ontology definitions
"""

from abc import abstractmethod
from enum import Enum
from importlib.resources import files, Package
from malkoha import trace_requirements
from typing import Iterable, Tuple, Set

from pyoxigraph import QuerySolutions, Store
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DefinedNamespace


@trace_requirements("Req28")
class CheckResult(Enum):
    Passed = True
    Failed = False

    def __str__(self):
        if self == CheckResult.Failed:
            return "false^^<http://www.w3.org/2001/XMLSchema#boolean>"
        else:
            return "true^^<http://www.w3.org/2001/XMLSchema#boolean>"

    def __bool__(self):
        return self.value


@trace_requirements("Req28")
class Ontology:
    """
    An abstract ontology
    """

    namespace: type[DefinedNamespace]
    questions: Package
    selections: Package

    @abstractmethod
    def check(
        self, graph: Graph, disabled_checks: Set[URIRef], **kwargs
    ) -> Iterable[Tuple[URIRef, Literal, CheckResult]]:
        """
        Performs checks defined by the ontology implementation.

        By default will call all ASK questions defined in the ontology module.
        By default the file name will be used as the display name.
        Specific classes may override this e.g. with the objective name.
        """
        while False:
            yield None

    def select(self, store: Store, query_path_segment: str) -> QuerySolutions:
        """
        Runs a query from the ontology module using its file name.

        Ontologies may override this to modify or filter solutions.
        """

        query: str = files(self.selections).joinpath(query_path_segment).read_text()
        solutions: QuerySolutions = store.query(query)

        return solutions
