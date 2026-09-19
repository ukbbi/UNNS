#!/usr/bin/env python3
from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve()
scan=HERE.parents[2]/"02_NONREF"/"scripts"/"NONREF_SCAN.py"
spec=importlib.util.spec_from_file_location("nr",scan)
nr=importlib.util.module_from_spec(spec); spec.loader.exec_module(nr)

tests=[
    ([2,3],2,4,3,3,1),
    ([1],2,4,3,3,0),
    ([2,4,6],4,8,6,6,0),
]
for gens,a,b,c,d,expect in tests:
    got=nr.exact_verdict(gens,a,b,c,d)["D_R"]
    assert got==expect,(gens,a,b,c,d,expect,got)
print("PASS",len(tests),"exact non-refinement controls")
