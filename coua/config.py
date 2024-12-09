import morph_kgc
import tomllib
import importlib

from pyoxigraph import Store
from pathlib import Path

from coua import mappings
from io import IOBase
from typing import List, Dict, Any


def parse_artifacts(artifacts: Dict[str, Any], output: str) -> Store:
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


def infer_mappings(section: str) -> importlib.resources.abc.Traversable | None:
    if section.lower() == "junit":
        return importlib.resources.files(mappings).joinpath("junit.ttl")
    else:
        return None


def parse_config(path: str) -> dict:
    p = Path(path)
    with open(p, "rb") as config:
        return tomllib.load(config)


def init_config(config: IOBase, files: List[str], mode: str):
    config.write(f'mode = "{mode}"\n')
    inferred = [("JUnit", "junit.xml")]
    for section, file in inferred:
        if file in files:
            config.write(f'[artifacts.{section}]\nfile_path = "{file}"')
