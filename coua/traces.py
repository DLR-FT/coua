from itertools import count
from typing import Iterable
from pathlib import Path


class Location:
    file: str
    line: int

    def __init__(self, file, line):
        self.file = file
        self.line = line


class Trace:
    location: Location
    requirement_id: str

    def __init__(self, file, line, requirement_id):
        self.location = Location(file, line)
        self.requirement_id = requirement_id


def get_traces(file: Path) -> Iterable[Trace]:
    for line, i in zip(open(file, "r"), count(1)):
        if "Requirements" ": " not in line:
            continue
        reqs = line.split(":")
        if len(reqs) > 1:
            for req in reqs[1].split(","):
                req = req.strip()
                if req == "":
                    continue
                yield Trace(file=file.absolute().as_posix(), line=i, requirement_id=req)


def get_locations(file: Path) -> Iterable[Location]:
    for line, i in zip(open(file, "r"), count(1)):
        yield Location(file=file.absolute().as_posix(), line=i)
