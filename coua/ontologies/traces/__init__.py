from rdflib import URIRef
from rdflib.namespace import DefinedNamespace, Namespace


class Traces(DefinedNamespace):
    _NS = Namespace("https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#")

    Event: URIRef
    Location: URIRef

    file: URIRef
    line: URIRef
    requirement_id: URIRef
