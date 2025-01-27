from pyoxigraph import Store

from coua.ontologies import Ontology
from coua.traces import trace_requirements


@trace_requirements("Req50")
class CheckResults(dict):
    pass


@trace_requirements("Req50")
def run_checks(store: Store, ontology: Ontology) -> CheckResults:
    results = CheckResults()
    for check, status in ontology.check(store):
        results[check] = status

    return results
