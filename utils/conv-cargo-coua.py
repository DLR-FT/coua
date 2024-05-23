#!/usr/bin/env python3


import json
import sys

print("""
@prefix coua: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/schema#> .
@prefix req: <https://gitlab.dlr.de/ft-ssy-avs/ap/coua/resources/requirements#> .
""")

data = json.load(sys.stdin)

for k, v in data.items():
    for test in v:
        print("req:{k} coua:coveredBy {test} .".format(k=k,test=test))
