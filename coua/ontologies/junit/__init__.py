"""
Junit ontology
"""

from malkoha import trace_requirements
from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace
from types import ModuleType

from coua.ontologies import Ontology


@trace_requirements("Req69")
class JUnit(DefinedNamespace):
    """
    RDFLib JUnit ontology namespace
    """

    _NS = Namespace("https://llg.cubic.org/docs/junit#")

    classname: URIRef
    disabled: URIRef
    errors: URIRef
    failure: URIRef
    failures: URIRef
    file: URIRef
    flakyError: URIRef
    flakyFailure: URIRef
    group: URIRef
    hasFailure: URIRef
    hasProperty: URIRef
    hasTestCase: URIRef
    hostname: URIRef
    log: URIRef
    message: URIRef
    name: URIRef
    package: URIRef
    property: URIRef
    requirement: URIRef
    rerunError: URIRef
    rerunFailure: URIRef
    skipped: URIRef
    status: URIRef
    testcase: URIRef
    tests: URIRef
    testsuite: URIRef
    testsuites: URIRef
    time: URIRef
    timestamp: URIRef
    type: URIRef
    url: URIRef
    value: URIRef
    version: URIRef


@trace_requirements("Req69")
class JunitOntology(Ontology):
    """
    RDFLib JUnit ontology
    """

    namespace = JUnit
    questions = ModuleType("questions")
    selections = ModuleType("selections")
