import morph_kgc

from pathlib import Path
from importlib import resources
from rdflib import Graph, URIRef
from . import res


def load_needy_json(graph: Graph, file: Path):
    """Loads a needy JSON stream into the store"""

    ms = "mappings/needy.ttl"
    config = f"[Needy]\nmappings: {ms}\nfile_path: {file}\nnumber_of_processes: 1\n"
    g = morph_kgc.materialize(config)
    for triple in g:
        graph.add(triple)


class TestConvNeedy:
    def test_all_subjects_recognized(self, record_property):
        # TODO add requirement for ingesting needy

        # This file is the output of
        # `cargo needy cargo-needy/tests/test-crate | jq -s '.'`
        # which converts the stream of events into one JSON document containing
        # a single array of all the events.
        json = resources.files(res).joinpath("needy_lsif_list.json")
        graph = Graph()
        load_needy_json(graph, json)
        subjects = list(graph.subjects())

        assert (
            URIRef("https://github.com/ferrocene/needy#it_works::it_works/REQ_002")
            in subjects
        )
