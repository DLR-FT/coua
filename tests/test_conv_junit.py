from coua.input import load_junit_xml
from importlib import resources
from rdflib import Graph, URIRef, Literal
from . import res


class TestConvJunit:
    def test_all_subjects_recognized(self, record_property):
        record_property("requirement", "Req21")

        xml = resources.files(res).joinpath("valid_junit.xml")
        graph = Graph()
        load_junit_xml(graph, xml)

        subjects = list(graph.subjects())
        for i in range(1, 10):
            assert URIRef(f"https://llg.cubic.org/docs/junit#testCase{i}") in subjects

    def test_requirements_property_is_parsed(self, record_property):
        record_property("requirement", "Req21")

        xml = resources.files(res).joinpath("valid_junit_with_requirements.xml")
        graph = Graph()
        load_junit_xml(graph, xml)

        objects = list(graph.objects())

        assert Literal("Req21") in objects
