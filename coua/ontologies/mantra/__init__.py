from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class Mantra(DefinedNamespace):
    """
    Requirements: Req51, ReqXX
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
