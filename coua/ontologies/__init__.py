from importlib import resources
from pyoxigraph import Store

__all__ = ["Ontology"]

from .ontology import Ontology
from . import coua, do178c, junit, mantra, needy, traces
from .coua import CouaOntology as Coua  # noqa: F401
from .do178c import DO178COntology as DO178C  # noqa: F401


def load_ontologies(store: Store):
    res = [
        (resources.files(do178c).joinpath("do178c.ttl"), "text/turtle"),
        (resources.files(coua).joinpath("coua.ttl"), "text/turtle"),
        (resources.files(junit).joinpath("junit.ttl"), "text/turtle"),
        (resources.files(mantra).joinpath("mantra.ttl"), "text/turtle"),
        (resources.files(needy).joinpath("needy.ttl"), "text/turtle"),
        (resources.files(traces).joinpath("traces.ttl"), "text/turtle"),
    ]

    for r in res:
        store.bulk_load(r[0], r[1])
