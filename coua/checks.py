from malkoha import trace_requirements
from pyoxigraph import Store, Quad, NamedNode, Literal

from coua.ontologies import Ontology, Coua


@trace_requirements("Req50")
class CheckResults(dict):
    pass


@trace_requirements("Req50")
def run_checks(store: Store, ontology: Ontology, **kwargs) -> CheckResults:
    results = CheckResults()
    for check, name, status in ontology.check(store, **kwargs):
        results[check] = status

        # All checks are subclasses of coua:Check
        subject = NamedNode(str(check))
        store.add(
            Quad(
                subject=subject,
                predicate=NamedNode(str(Coua.namespace.status)),
                object=Literal(str(status).lower()),
            )
        )

    return results
