from coua.ontologies.cobertura import CoberturaParser
from importlib import resources
from tests import res
from pyoxigraph import Store


class TestConvcobertura:
    def test_all_subjects_recognized(self, record_property):
        graph = Store()
        f = resources.files(res).joinpath("valid_cobertura.xml")
        with open(f, "r", encoding="utf-8") as xml:
            CoberturaParser.parse(graph, xml.read())
        subjects = graph.query(
            "SELECT ?line WHERE { ?line a <https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd#line> }"
        )

        assert subjects
