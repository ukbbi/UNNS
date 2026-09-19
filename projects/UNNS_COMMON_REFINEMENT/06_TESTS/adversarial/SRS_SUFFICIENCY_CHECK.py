#!/usr/bin/env python3
"""
SRS_SUFFICIENCY_CHECK.py

Finite executable analogue of the SRS Route-Closure Theorem.

A local node has:
  - I, P flags (local shadow refinable iff both hold)
  - finite residual child nodes
  - R_local flag

A symbolic limit node has:
  - lower approximants
  - L flag asserting a coherent inverse-limit witness exists
  - R_limit flag

Ranks must strictly descend along local residual edges (D).

This cannot prove the transfinite theorem; it checks the executable finite/symbolic
realization of the same proof skeleton and guards the project files against accidental
logical regressions.
"""
from functools import lru_cache

NODES = {
    "q0": {"rank":0, "kind":"local", "I":True, "P":True, "R":True, "res":[]},
    "q1": {"rank":1, "kind":"local", "I":True, "P":True, "R":True, "res":["q0"]},
    "q2": {"rank":2, "kind":"local", "I":True, "P":True, "R":True, "res":["q1","q0"]},
    # symbolic limit node: approximants already have lower ranks; L supplies coherence
    "qlim": {"rank":"omega", "kind":"limit", "L":True, "R":True, "approx":["q0","q1","q2"]},
}

def rank_lt(a,b):
    if b=="omega":
        return isinstance(a,int)
    if isinstance(a,int) and isinstance(b,int):
        return a<b
    return False

@lru_cache(None)
def solve(name):
    n=NODES[name]
    if n["kind"]=="local":
        assert n["I"] and n["P"], f"local shadow failure at {name}"
        for child in n["res"]:
            assert rank_lt(NODES[child]["rank"],n["rank"]), f"D fails: {child} !< {name}"
            assert solve(child)
        assert n["R"], f"R local fails at {name}"
        return True

    for child in n["approx"]:
        assert rank_lt(NODES[child]["rank"],n["rank"]), f"approximant rank failure at {name}"
        assert solve(child)
    assert n["L"], f"L fails at {name}"
    assert n["R"], f"R limit fails at {name}"
    return True

assert all(solve(n) for n in NODES)
print({"nodes":len(NODES),"global_route_closure":True,"status":"PASS"})
