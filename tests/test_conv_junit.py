import io  # noqa: F401

from coua.input import load_junit_xml
from importlib import resources
from rdflib import Graph, URIRef
from . import res


class TestConvJunit:
    def test_all_subjects_recognized(self):
        xml = resources.files(res).joinpath("valid_junit.xml")
        graph = Graph()
        load_junit_xml(graph, xml)

        subjects = list(graph.subjects())
        for i in range(1, 10):
            assert URIRef(f"https://llg.cubic.org/docs/junit#testCase{i}") in subjects
