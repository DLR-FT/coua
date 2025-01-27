"""
Ontology for Coua traces.xml
"""

from types import ModuleType

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from coua.ontologies import Ontology
from coua.traces import trace_requirements


@trace_requirements("Req72")
class Traces(DefinedNamespace):
    """
    RDFlib class for ontology namespace
    """

    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#")

    Event: URIRef
    Location: URIRef

    file: URIRef
    line: URIRef
    requirement_id: URIRef


@trace_requirements("Req72")
class TracesOntology(Ontology):
    """
    RDFlib class for ontology
    """

    namespace = Traces
    questions = ModuleType("questions")
    selections = ModuleType("selections")
