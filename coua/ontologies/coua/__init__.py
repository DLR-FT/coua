"""
Ontology for Coua requirement and use-case formats
"""

from importlib import resources
from typing import Iterable, Tuple, Set

from malkoha import trace_requirements
from rdflib import URIRef, Graph, Literal
from rdflib.namespace import DefinedNamespace, Namespace

from coua.ontologies import Ontology
from coua.ontologies.ontology import CheckResult
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
    checkDisabled: URIRef


@trace_requirements("Req26")
class CouaOntology(Ontology):
    """
    RDFLib ontology
    """

    namespace = COUA
    questions = questions
    selections = selections

    def check(
        self, graph: Graph, disabled_checks: Set[URIRef], **kwargs
    ) -> Iterable[Tuple[URIRef, Literal, CheckResult]]:
        qs = list(
            map(
                lambda p: (
                    resources.files(self.questions) / p[0],
                    Literal(p[1]),
                ),
                [
                    ("ask_ucs_covered.rq", "CheckAskUcsCovered"),
                ],
            )
        )
        for question, name in qs:
            uri = URIRef(str(self.namespace) + name)

            if str(uri) in disabled_checks:
                continue

            with open(str(question), "r", encoding="utf-8") as f:
                query = f.read()

            yield uri, name, CheckResult(bool(graph.query(query)))
