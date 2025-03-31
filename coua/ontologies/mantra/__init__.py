"""
Ontology for requirements from Mantra DB
"""

from malkoha import trace_requirements
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from types import ModuleType

from coua.ontologies import Ontology


@trace_requirements("Req70")
class Mantra(DefinedNamespace):
    """
    RDFLib ontology namespace
    """

    _NS = Namespace("https://github.com/mhatzl/mantra/0.2.14#")

    Location: URIRef
    Requirement: URIRef
    Trace: URIRef

    id: URIRef
    title: URIRef
    filepath: URIRef
    line: URIRef
    requirement: URIRef


@trace_requirements("Req70")
class MantraOntology(Ontology):
    """
    RDFLib ontology
    """

    namespace = Mantra
    questions = ModuleType("questions")
    selections = ModuleType("selections")
