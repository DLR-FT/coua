from importlib import resources
from malkoha import trace_requirements
from pyoxigraph import Store

__all__ = ["Ontology"]

from coua.ontologies.ontology import Ontology
from coua.ontologies import cobertura, coua, do178c, junit, mantra, needy, traces
from coua.ontologies.coua import CouaOntology as Coua  # noqa: F401
from coua.ontologies.do178c import DO178COntology as DO178C  # noqa: F401
from coua.ontologies.cobertura import CoberturaOntology as Cobertura  # noqa: F401


@trace_requirements(
    "Req33", "Req26", "Req68", "Req69", "Req70", "Req71", "Req72", "Req73"
)
def load_ontologies(store: Store):
    res = [
        (resources.files(do178c).joinpath("do178c.ttl"), "text/turtle"),
        (resources.files(cobertura).joinpath("cobertura.ttl"), "text/turtle"),
        (resources.files(coua).joinpath("coua.ttl"), "text/turtle"),
        (resources.files(junit).joinpath("junit.ttl"), "text/turtle"),
        (resources.files(mantra).joinpath("mantra.ttl"), "text/turtle"),
        (resources.files(needy).joinpath("needy.ttl"), "text/turtle"),
        (resources.files(traces).joinpath("traces.ttl"), "text/turtle"),
    ]

    for r in res:
        with open(str(r[0]), "rb") as f:
            store.bulk_load(f, r[1])
