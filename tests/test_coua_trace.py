from coua.traces import get_traces
from importlib import resources

from . import res


def test_read_traces():
    file = resources.files(res).joinpath("tracable_python_file.py")
    traces = [r.requirement_id for r in get_traces(file)]
    assert traces == ["Req123", "Re234", "Re234", "R5"]
