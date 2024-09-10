from pyoxigraph import Store

from coua.ontologies.do178c import DO178COntology as DO178C  # noqa: F401
from coua.ontologies import coua
from coua.ontologies import do178c
from importlib import resources


def load_ontologies(store: Store):

    res = [
        (resources.files(do178c).joinpath("do178c.ttl"), "text/turtle"),
        (resources.files(coua).joinpath("coua.ttl"), "text/turtle"),
    ]

    for r in res:
        store.bulk_load(r[0], r[1])
