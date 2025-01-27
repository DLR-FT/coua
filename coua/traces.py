import inspect
import pkgutil
import os

from typing import cast
from importlib.abc import PathEntryFinder, Loader
from  typing import Iterable
from pathlib import Path
from dataclasses import dataclass


# @trace_requirements("Req54")
def trace_requirements(*traced_requirements):
    """Traces an object to a list of requirements"""

    def fun(obj):
        setattr(obj, "__traced_requirements__", list(traced_requirements))

        return obj

    return fun


@trace_requirements("Req10")
@dataclass
class Location:
    name: str
    file: str | None
    line: int | None


@trace_requirements("Req10")
@dataclass
class Trace:
    location: Location
    requirement_id: str | None

    def __init__(self, name, file, line, requirement_id):
        self.location = Location(name, file, line)
        self.requirement_id = requirement_id


@trace_requirements("Req10")
def get_traces(path: Path) -> Iterable[Trace]:
    """Get requirement traces from python code"""

    search_path: str = os.path.abspath(path)
    for info in pkgutil.walk_packages(path=[search_path]):
        finder = cast(PathEntryFinder, info.module_finder)
        loader = cast(Loader, finder.find_loader(info.name)[0])
        mod = loader.load_module(info.name)

        for name, value in inspect.getmembers(
            mod,
            lambda x: (not inspect.isbuiltin(x))
            and inspect.getmodule(x) == mod
            and x != trace_requirements
            and (inspect.isclass(x) or inspect.ismodule(x) or inspect.isfunction(x)),
        ):
            try:
                file = inspect.getsourcefile(mod)
                line = inspect.getsourcelines(value)[1]
            except (OSError, TypeError):
                file = None
                line = None
            if hasattr(value, "__traced_requirements__"):
                requirements = value.__traced_requirements__
                for requirement_id in requirements:
                    yield Trace(
                        name=name,
                        file=file,
                        line=line,
                        requirement_id=requirement_id,
                    )
            else:
                # This means that the object is missing requirements tracing
                yield Trace(
                    name=name,
                    file=file,
                    line=line,
                    requirement_id=None,
                )
