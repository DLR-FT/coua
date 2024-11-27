from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from types import ModuleType

from coua.ontologies import Ontology


class Traces(DefinedNamespace):
    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#")

    Event: URIRef
    Location: URIRef

    file: URIRef
    line: URIRef
    requirement_id: URIRef


class TracesOntology(Ontology):
    namespace = Traces
    questions = ModuleType("questions")
    selections = ModuleType("selections")
