"""
Ontology for Coua requirement and use-case formats
"""

from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from coua.ontologies import Ontology
from coua.traces import trace_requirements

from coua.ontologies.coua import ask as questions, select as selections


@trace_requirements("Req26")
class COUA(DefinedNamespace):
    """
    RDFLib ontology namespace
    """

    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/schema#")

    Product: URIRef
    TestCase: URIRef
    covers: URIRef
    name: URIRef
    requires: URIRef
    traces: URIRef
    useCases: URIRef
    Requirement: URIRef
    LowLevelRequirement: URIRef
    HighLevelRequirement: URIRef
    SystemLevelRequirement: URIRef
    UseCase: URIRef
    # TODO add to ontology file
    Check: URIRef
    checkName: URIRef
    status: URIRef
    description: URIRef
    owner: URIRef
    useCase: URIRef
    title: URIRef
    actor: URIRef
    goal: URIRef
    scope: URIRef
    story: URIRef
    stakeholder: URIRef
    precondition: URIRef
    postcondition: URIRef
    trigger: URIRef
    flow: URIRef
    extension: URIRef
    project: URIRef
    timestamp: URIRef
    time: URIRef
    failureType: URIRef
    failure: URIRef


@trace_requirements("Req26")
class CouaOntology(Ontology):
    """
    RDFLib ontology
    """

    namespace = COUA
    questions = questions
    selections = selections
