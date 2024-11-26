from itertools import count
from typing import Iterable
from pathlib import Path


class Trace:
    file: str
    line: int
    requirement_id: str

    def __init__(self, file, line, requirement_id):
        self.file = file
        self.line = line
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
