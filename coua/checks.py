from pyoxigraph import Store, Quad, NamedNode, Literal
from rdflib.namespace import RDF

from coua.ontologies import Ontology, Coua
from coua.traces import trace_requirements


@trace_requirements("Req50")
class CheckResults(dict):
    pass


@trace_requirements("Req50")
def run_checks(store: Store, ontology: Ontology) -> CheckResults:
    results = CheckResults()
    for check, name, status in ontology.check(store):
        results[check] = status

        subject = NamedNode(str(check))
        store.add(
            Quad(
                subject=subject,
                predicate=NamedNode(str(Coua.namespace.status)),
                object=Literal(str(status).lower()),
            )
        )
        store.add(
            Quad(
                subject=subject,
                predicate=NamedNode(str(Coua.namespace.checkName)),
                object=Literal(str(name)),
            )
        )
        store.add(
            Quad(
                subject=NamedNode(str(check)),
                predicate=NamedNode(RDF.type),
                object=NamedNode(str(Coua.namespace.Check)),
            )
        )

    return results
