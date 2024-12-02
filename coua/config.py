import morph_kgc
import tomllib
import importlib

from pyoxigraph import Store
from pathlib import Path

from coua import mappings


def parse_artifacts(artifacts: dict, output: str) -> Store:
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

    g = morph_kgc.materialize_oxigraph(config)

    return g


def infer_mappings(section: str) -> importlib.resources.abc.Traversable | None:
    if section.lower() == "junit":
        return importlib.resources.files(mappings).joinpath("junit.ttl")
    else:
        return None


def parse_config(path: str) -> dict:
    p = Path(path)
    with open(p, "rb") as config:
        return tomllib.load(config)
