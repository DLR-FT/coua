from pyoxigraph import Store

from .ontologies import Ontology


class CheckResults(dict):
    pass


def run_checks(store: Store, ontology: Ontology) -> CheckResults:
    results = CheckResults()
    for check, status in ontology.check(store):
        results[check] = status

    return results
