#!/usr/bin/env python3
import math, argparse, json

def gcd_all(gens):
    g=0
    for x in gens:
        g=math.gcd(g,x)
    return g

def classify(gens):
    gens=sorted(set(int(x) for x in gens if int(x)>0))
    if not gens:
        raise ValueError("Need positive generators.")
    m=min(gens)
    g=gcd_all(gens)
    rci=m//g
    return {
        "generators":gens,
        "multiplicity_m":m,
        "group_step_g":g,
        "route_closure_index":rci,
        "has_global_common_refinement":m==g,
        "rank1_lattice_saturated":m==g,
        "canonical_monoid":f"{m}N0" if m==g else None,
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser(
        description="Exact rank-one common-refinement classifier for additive submonoids of N0."
    )
    ap.add_argument("generators", nargs="+", type=int)
    ns=ap.parse_args()
    print(json.dumps(classify(ns.generators), indent=2))
