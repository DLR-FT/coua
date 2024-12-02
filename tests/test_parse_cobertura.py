import morph_kgc

from coua import mappings
from pathlib import Path
from importlib import resources
from rdflib import Graph, URIRef
from . import res


def load_cobertura_xml(graph: Graph, file: Path):
    """Loads a cobertura XML into the store"""

    ms = resources.files(mappings).joinpath("cobertura.ttl")
    config = f"[cobertura]\nmappings: {ms}\nfile_path: {file}\nnumber_of_processes: 1\n"
    g = morph_kgc.materialize(config)
    for triple in g:
        graph.add(triple)


class TestConvcobertura:
    def test_all_subjects_recognized(self, record_property):
        graph = Graph()
        json = resources.files(res).joinpath("valid_cobertura.xml")
        load_cobertura_xml(graph, json)
        subjects = list(graph.subjects())

        assert (
            URIRef(
                "https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd#package/ontologies.needy"
            )
            in subjects
        )
