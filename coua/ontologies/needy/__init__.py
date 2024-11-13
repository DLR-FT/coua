from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


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
