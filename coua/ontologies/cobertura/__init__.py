"""
Ontology for Cobertura coverage format  
"""

from types import ModuleType

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from coua.ontologies import Ontology
from coua.traces import trace_requirements


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


@trace_requirements("Req67")
class CoberturaOntology(Ontology):
    """
    RDFlib class for Cobertura ontology
    """

    namespace = Cobertura
    questions = ModuleType("questions")
    selections = ModuleType("selections")
