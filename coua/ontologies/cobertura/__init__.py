"""
Ontology for Cobertura coverage format
"""

import xml.etree.ElementTree as ET

from importlib import resources
from malkoha import trace_requirements
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from types import ModuleType
from typing import Set, Iterable, Tuple
from coua.ontologies.ontology import CheckResult
from pyoxigraph import Store, Quad, NamedNode, Literal
from rdflib import Graph

from coua.ontologies import Ontology
from coua.ontologies.cobertura import ask as questions


@trace_requirements("Req73")
class Cobertura(DefinedNamespace):
    """
    RDFlib class for Cobertura ontology namespace
    """

    _NS = Namespace(
        "https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd#"
    )

    condition: URIRef
    coverage: URIRef
    line: URIRef
    method: URIRef
    package: URIRef
    source: URIRef
    branch: URIRef
    branches_covered: URIRef
    branches_valid: URIRef
    branch_rate: URIRef
    complexity: URIRef
    condition_coverage: URIRef
    filename: URIRef
    hasClass: URIRef
    hasCondition: URIRef
    hasLine: URIRef
    hasMethod: URIRef
    hasSource: URIRef
    hits: URIRef
    line_rate: URIRef
    lines_covered: URIRef
    lines_valid: URIRef
    name: URIRef
    number: URIRef
    path: URIRef
    signature: URIRef
    timestamp: URIRef

    # Checks
    check_all_lines_covered: URIRef


@trace_requirements("Req67")
class CoberturaOntology(Ontology):
    """
    RDFlib class for Cobertura ontology
    """

    namespace = Cobertura
    questions = questions
    selections = ModuleType("selections")

    def check(
        self, graph: Graph, disabled_checks: Set[URIRef], **kwargs
    ) -> Iterable[Tuple[URIRef, Literal, CheckResult]]:
        questions = [
            # FIXME: should be made generic via DO-178C ontology
            ("check_all_lines_covered", "All lines covered", "all_lines_covered.rq")
        ]
        for slug, name, question in questions:
            uri = URIRef(self.namespace + slug)
            if uri in disabled_checks:
                continue
            with open(
                str(resources.files(self.questions) / question), "r", encoding="utf-8"
            ) as f:
                query = f.read()

            yield uri, Literal(name), CheckResult(bool(graph.query(query)))


@trace_requirements("Req81")
class CoberturaParser:
    def parse(store: Store, document: str):
        xml = ET.fromstring(document)

        def get_class_elements():
            for el in xml.findall("./packages//class"):
                yield el

        t = "https://raw.githubusercontent.com/cobertura/web/master/htdocs/xml/coverage-04.dtd"
        cls = get_class_elements()
        for cl in cls:
            filename = cl.attrib["filename"]
            for li in cl.findall("./lines/line"):
                item = {}
                item["filename"] = filename
                ln = li.attrib["number"]
                item["number"] = ln
                item["hits"] = li.attrib["hits"]
                if "branch" in li.attrib:
                    item["branch"] = li.attrib["branch"] == "true"
                if "condition-coverage" in li.attrib:
                    item["condition-coverage"] = li.attrib["condition-coverage"]
                if "missing-branches" in li.attrib:
                    item["missing-branches"] = li.attrib["missing-branches"]
                store.extend(
                    (
                        Quad(
                            NamedNode(f"{t}#line/{filename}/{ln}"),
                            NamedNode(
                                "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
                            ),
                            NamedNode(str(Cobertura.line)),
                        ),
                    )
                )
                store.extend(
                    tuple(
                        [
                            Quad(
                                NamedNode(f"{t}#line/{filename}/{ln}"),
                                NamedNode(f"{t}#{key}"),
                                Literal(value),
                            )
                            for key, value in item.items()
                        ]
                    )
                )
