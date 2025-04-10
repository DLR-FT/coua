import morph_kgc
import tomllib
import importlib
import json
import urllib

from malkoha import trace_requirements
from malkoha.data import Trace
from pyoxigraph import Store, NamedNode, Quad, Literal
from pathlib import Path

from coua import mappings
from io import IOBase
from typing import List, Dict, Any


@trace_requirements("Req58", "Req21", "Req25", "Req06")
def parse_artifacts(artifacts: Dict[str, Any]) -> Store:
    morph_config = ""
    for section, artifact in artifacts.items():
        if "morph" in artifact:
            morph_config += parse_morph_config(section, artifact)
    # morph_kgc will produce an error if the config is empty
    if morph_config != "":
        g = morph_kgc.materialize_oxigraph(morph_config)
    else:
        g = Store()

    for section, artifact in artifacts.items():
        if "type" in artifact:
            match artifact["type"]:
                case "malkoha":
                    parse_malkoha_output(g, section)

    return g


@trace_requirements("Req58")
def parse_malkoha_output(g: Store, path: str):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            trace = Trace(
                d["location"]["name"],
                d["location"]["file"],
                d["location"]["line"],
                d["requirements"],
            )
            t = "https://gitlab.dlr.de/ft-ssy-avs/ap/coua/ontologies/traces"
            file = urllib.parse.quote(trace.location.file, safe="")
            line = trace.location.line
            g.extend(
                (
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#file"),
                        Literal(trace.location.file),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
                        NamedNode(f"{t}#Location"),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#line"),
                        Literal(trace.location.line),
                    ),
                    Quad(
                        NamedNode(f"{t}#location/{file}/{line}"),
                        NamedNode(f"{t}#displayName"),
                        Literal(trace.location.name),
                    ),
                    Quad(
                        NamedNode(f"{t}#event/{file}/{line}"),
                        NamedNode(f"{t}#location"),
                        NamedNode(f"{t}#location/{file}/{line}"),
                    ),
                )
            )
            if trace.requirements:
                for requirement in trace.requirements:
                    g.extend(
                        (
                            Quad(
                                NamedNode(f"{t}#event/{file}/{line}"),
                                NamedNode(f"{t}#requirement_id"),
                                Literal(requirement),
                            ),
                            Quad(
                                NamedNode(f"{t}#event/{file}/{line}"),
                                NamedNode(
                                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
                                ),
                                NamedNode(f"{t}#Event"),
                            ),
                        )
                    )


@trace_requirements("Req58")
def parse_morph_config(section: str, artifact: dict) -> str:
    morph_config = ""
    settings = artifact["morph"]
    if "mappings" not in settings:
        inferred = infer_mappings(section)
        if inferred:
            artifact["morph"]["mappings"] = inferred
    morph_config += f"\n[{section}]\n"
    for key, value in artifact["morph"].items():
        morph_config += f"{key}: {value}\n"

    return morph_config


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
