import morph_kgc
import tomllib
import importlib

from pyoxigraph import Store
from pathlib import Path

from coua.traces import trace_requirements
from coua import mappings
from io import IOBase
from typing import List, Dict, Any


@trace_requirements("Req58")
def parse_artifacts(artifacts: Dict[str, Any]) -> Store:
    config = ""
    for section, artifact in artifacts.items():
        settings = artifact["morph"]
        if "mappings" not in settings:
            inferred = infer_mappings(section)
            if inferred:
                artifact["morph"]["mappings"] = inferred
        config += f"\n[{section}]\n"
        for key, value in artifact["morph"].items():
            config += f"{key}: {value}\n"

    # morph_kgc will produce an error if the config is empty
    if config != "":
        g = morph_kgc.materialize_oxigraph(config)
    else:
        g = Store()

    return g


@trace_requirements("Req58")
def infer_mappings(section: str) -> importlib.resources.abc.Traversable | None:
    mapping = section.lower()
    if mapping in ["junit", "traces", "needy", "mantra", "cobertura"]:
        return importlib.resources.files(mappings).joinpath(f"{mapping}.ttl")
    else:
        return None


@trace_requirements("Req58", "Req57")
def parse_config(path: str) -> dict:
    p = Path(path)
    with open(p, "rb") as config:
        return tomllib.load(config)


@trace_requirements("Req58", "Req57", "Req55")
def init_config(config: IOBase, files: List[str], checks: List[str]):
    config.write("checks = [")
    for check in checks:
        config.write(f'"{check}", ')
    config.write("]\n")
    inferred = [("JUnit", "junit.xml")]
    for section, file in inferred:
        if file in files:
            config.write(f'[artifacts.{section}]\nfile_path = "{file}"')
