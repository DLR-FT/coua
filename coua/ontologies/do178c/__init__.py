"""
Ontology for DO-178C
"""

from enum import Enum
from importlib import resources
from typing import Set, Tuple, Iterable, List, cast

from malkoha import trace_requirements
from rdflib import URIRef, Literal, Graph
from rdflib.namespace import RDFS, DefinedNamespace, Namespace, RDF
from pyoxigraph import Quad, NamedNode, Variable, QuerySolution

from coua.exceptions import CouaException
from coua.ontologies import Ontology

from coua.ontologies.ontology import CheckResult
import coua.ontologies.do178c.ask as questions
import coua.ontologies.do178c.select as selections


@trace_requirements("Req80")
class DO178C(DefinedNamespace):
    """
    RDFlib class for ontology namespace
    """

    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/do178c#")

    Requirement: URIRef
    LowLevelRequirement: URIRef
    HighLevelRequirement: URIRef
    Software: URIRef
    SoftwareLevel: URIRef
    SoftwareLevelA: URIRef
    SoftwareLevelB: URIRef
    SoftwareLevelC: URIRef
    hasSoftwareLevel: URIRef
    SystemLevelRequirement: URIRef
    requires: URIRef
    TraceData: URIRef
    TestCase: URIRef
    covers: URIRef
    traces: URIRef
    requirementDescription: URIRef
    requirementRationale: URIRef


@trace_requirements("Req75")
class SoftwareLevel(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    def do178c(self):
        match self:
            case SoftwareLevel.A:
                level = DO178C.SoftwareLevelA
            case SoftwareLevel.B:
                level = DO178C.SoftwareLevelB
            case SoftwareLevel.C:
                level = DO178C.SoftwareLevelC
            case SoftwareLevel.D:
                level = DO178C.SoftwareLevelD
            case l:
                # Should never occur
                raise ValueError(f"Unrecognized software level {l}")
        return level


@trace_requirements("Req68", "Req76", "Req74")
class DO178COntology(Ontology):
    """
    RDFlib class for ontology
    """

    namespace = DO178C
    questions = questions
    selections = selections

    def check(
        self, graph: Graph, disabled_checks: Set[URIRef], **kwargs
    ) -> Iterable[Tuple[URIRef, Literal, CheckResult]]:
        software: str = kwargs["software"]
        software_level: str = kwargs["software_level"]
        sw = URIRef(software)
        swl = SoftwareLevel[software_level]
        activate_software_level(graph, sw, swl)
        check_is_do178c(graph)
        qs = list(
            map(
                lambda p: (
                    resources.files(self.questions) / p[0],
                    Literal(p[1]),
                ),
                [
                    ("obj-A-2-1.rq", "Obj_A_2_1"),
                    ("obj-A-2-4.rq", "Obj_A_2_4"),
                    ("obj-A-3-6.rq", "Obj_A_3_6"),
                    ("obj-A-4-6.rq", "Obj_A_4_6"),
                    ("obj-A-5-1.rq", "Obj_A_5_1"),
                    ("obj-A-5-5.rq", "Obj_A_5_5"),
                ],
            ),
        )
        applicable = self.applicable_objectives(graph, swl)
        for question, name in qs:
            uri = URIRef(str(self.namespace) + name)
            if str(uri) in disabled_checks or str(uri) not in applicable:
                continue

            with open(str(question), "r", encoding="utf-8") as f:
                query = f.read()

            yield uri, name, CheckResult(bool(graph.query(query)))

    # TODO add requirement for checking only applicable objectives
    def applicable_objectives(
        self, graph: Graph, software_level: SoftwareLevel
    ) -> List[URIRef]:
        query = resources.files(self.selections) / "applicable_objectives.rq"
        with open(str(query), "r", encoding="utf-8") as f:
            objs = graph.query(
                f.read(),
                substitutions={Variable("swl"): NamedNode(software_level.do178c())},
            )
        # Query solutions are slightly incompatible with rdflib graph
        obs = [cast(QuerySolution, obj)["Objective"].value for obj in objs]

        return obs


@trace_requirements("Req76")
def activate_software_level(
    graph: Graph, software: URIRef, software_level: SoftwareLevel
):
    """
    Activate a SWL
    """
    graph.add(
        Quad(
            subject=NamedNode(software),
            predicate=NamedNode(RDF.type),
            object=NamedNode(DO178C.Software),
        )
    )
    level = software_level.do178c()
    graph.add(
        Quad(
            subject=NamedNode(software),
            predicate=NamedNode(DO178C.hasSoftwareLevel),
            object=NamedNode(level),
        )
    )


@trace_requirements("Req67")
def check_is_do178c(graph: Graph):
    """
    Checks if the graph contains the DO-178C ontology.
    """

    rdfsub = RDFS.subClassOf
    do178creq = DO178COntology.namespace.Requirement
    query = f"ASK {{ ?r <{rdfsub}> <{do178creq}> }}"

    if not graph.query(query):
        raise CouaException(
            "Bindings from input data to DO-178C ontology not provided in input data."
        )
