from coua.config import parse_malkoha_output
from importlib import resources
from pyoxigraph import Store

from tests import res


def test_load_traces_json():
    """Loads a traces JSON"""

    graph = Store()
    parse_malkoha_output(
        graph, resources.files(res).joinpath("test_source_traces.json")
    )
    assert bool(
        graph.query(
            """
PREFIX traces: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces#>
ASK {
    ?location a traces:Location .
    ?trace a traces:Event ;
        traces:location ?location .
}"""
        )
    )
