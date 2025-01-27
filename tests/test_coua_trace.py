import morph_kgc

from coua import mappings
from coua.traces import get_traces
from importlib import resources
from rdflib import Graph

from tests import res


def test_read_traces():
    project = resources.files(res).joinpath("test_package")
    traces = [r.requirement_id for r in get_traces(project)]
    assert traces.sort() == ["Req123", "Re234", "Re234", "R5"].sort()


def test_load_traces_json():
    """Loads a traces JSON"""

    file = resources.files(res).joinpath("test_source_traces.xml")
    graph = Graph()
    ms = resources.files(mappings).joinpath("traces.ttl")
    config = f"[Traces]\nmappings: {ms}\nfile_path: {file}\nnumber_of_processes: 1\n"
    g = morph_kgc.materialize(config)
    for triple in g:
        graph.add(triple)
    assert bool(
        graph.query(
            """
PREFIX traces: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
ASK {
    ?location a traces:Location .
    ?trace a traces:Event ;
        traces:location ?location .
}"""
        )
    )
