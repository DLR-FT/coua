from .config import parse_artifacts
from .ontologies import load_ontologies, Ontology


class CheckResults(dict):
    pass


def run_checks(
    artifacts: dict, output: str, ontology: Ontology, extra_triples: list[str]
) -> CheckResults:
    store = parse_artifacts(artifacts, output)
    load_ontologies(store)
    for triple in extra_triples:
        store.bulk_load(triple, "application/n-triples")
    store.flush()
    results = CheckResults()
    for check, status in ontology.check(store):
        results[check] = status

    store.dump(output, "application/n-triples")

    return results
