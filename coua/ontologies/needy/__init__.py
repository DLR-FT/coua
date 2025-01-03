from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from types import ModuleType

from coua.ontologies import Ontology
from coua.traces import trace_requirements


@trace_requirements("Req71")
class Needy(DefinedNamespace):
    _NS = Namespace("https://github.com/ferrocene/needy#")

    Span: URIRef
    Event: URIRef
    Location: URIRef

    file: URIRef
    function_name: URIRef
    module: URIRef
    requirement_id: URIRef
    span: URIRef
    start: URIRef
    end: URIRef
    line: URIRef
    character: URIRef
    version: URIRef


@trace_requirements("Req71")
class NeedyOntology(Ontology):
    namespace = Needy
    questions = ModuleType("questions")
    selections = ModuleType("selections")
