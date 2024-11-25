import morph_kgc
import os

from pathlib import Path
from importlib import resources
from rdflib import Graph
from . import res


def load_db(graph: Graph, file: Path):
    """Loads a Mantra database into the store"""

    assert os.path.exists(file)

    ms = "mappings/mantra.ttl"
    config = (
        f"[Mantra]\nmappings: {ms}\ndb_url: sqlite:///{file}\nnumber_of_processes: 1\n"
    )
    g = morph_kgc.materialize(config)
    for triple in g:
        graph.add(triple)


class TestConvMantra:

    def test_all_subjects_recognized(self, record_property):
        db = resources.files(res).joinpath("mantra.db")
        graph = Graph()
        load_db(graph, db)
        subjects = list(graph.subjects())

        assert subjects
