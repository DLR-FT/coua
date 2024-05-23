#!/usr/bin/env python3

import tomllib


with open("use-cases.toml", "rb") as f:
    data = tomllib.load(f)
    print("""
@prefix coua: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/schema#> .
@prefix req: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/requirements#> .
@prefix uc: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/use-cases#> .
""")
    for k, r in data.items():
        stakeholder = ",".join(["\"{}\"@en".format(uc) for uc in r["stakeholders"]])
        precondition = ",".join(["\"{}\"@en".format(uc) for uc in r["pre"]])
        postcondition = ",".join(["\"{}\"@en".format(uc) for uc in r["post"]])
        flow = " ".join(["\"{}\"@en".format(uc) for uc in r["flow"]])
        extension = ",".join(["\"{}\"@en".format(uc) for uc in r["extensions"]])
        print("""
uc:{k} a coua:UseCase ;
    coua:title "{title}"@en ;
    coua:actor "{actor}" ;
    coua:goal "{goal}" ;
    coua:scope "{scope}"@en ;
    coua:level "{level}"@en ;
    coua:story "{story}"@en ;
    coua:stakeholder {stakeholder} ;
    coua:precondition {precondition} ;
    coua:postcondition {postcondition} ;
    coua:trigger "{trigger}"@en ;
    coua:flow ( {flow} ) ;
    coua:extension {extension} .""".format(
        k=k,
        title=r["title"],
        actor=r["actor"],
        goal=r["goal"],
        scope=r["scope"],
        level=r["level"],
        story=r["story"],
        stakeholder=stakeholder,
        precondition=precondition,
        postcondition=postcondition,
        trigger=r["trigger"],
        flow=flow,
        extension=extension))
