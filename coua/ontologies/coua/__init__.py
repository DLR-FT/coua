from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace

from coua.ontologies import Ontology

from . import ask as questions


class COUA(DefinedNamespace):
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


class CouaOntology(Ontology):
    namespace = COUA
    questions = questions
