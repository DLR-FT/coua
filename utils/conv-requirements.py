#!/usr/bin/env python3

import tomllib


with open("requirements.toml", "rb") as f:
    data = tomllib.load(f)
    print("""
@prefix coua: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/schema#> .
@prefix req: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/requirements#> .
@prefix uc: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/use-cases#> .""")
    for k, r in data.items():
        if "use-cases" in r:
            ucs = ",".join(["cert:{}".format(uc) for uc in r["use-cases"]])
        else:
            ucs = ""
        print("""
req:{k} a coua:Requirement ;
    coua:description "{desc}"@en ;
    coua:owner "{owner}" ;
    coua:level "{level}" ;
    coua:useCases {ucs} .
""".format(k=k, desc=r["description"], owner=r["owner"], level=r["level"], ucs=ucs))
