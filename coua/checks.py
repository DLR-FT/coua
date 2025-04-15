from malkoha import trace_requirements
from pyoxigraph import Store, Quad, NamedNode, Literal
from rdflib import URIRef
from typing import Set

from coua.ontologies import Ontology, Coua


@trace_requirements("Req50")
class CheckResults(dict):
    pass


@trace_requirements("Req50", "Req41")
def run_checks(
    store: Store, ontology: Ontology, disabled_checks: Set[URIRef], **kwargs
) -> CheckResults:
    results = CheckResults()
    for check, name, status in ontology.check(store, disabled_checks, **kwargs):
        results[check] = status

        # All checks are subclasses of coua:Check
        subject = NamedNode(str(check))
        store.add(
            Quad(
                subject=subject,
                predicate=NamedNode(str(Coua.namespace.status)),
                object=Literal(bool(status)),
            )
        )
    # Mark disabled checks as disabled
    for disabled in disabled_checks:
        subject = NamedNode(str(disabled))
        store.add(
            Quad(
                subject=NamedNode(disabled),
                predicate=NamedNode(str(Coua.namespace.checkDisabled)),
                object=Literal(True),
            )
        )

    return results
