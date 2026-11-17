"""Exact density accounting of proved route-length-<=K classes: union of v003 covers, Theorem-G classes and v004 identities."""
import json, sys, glob, os
import numpy as np
from math import gcd
from functools import reduce
V003 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "UNNS-SCALE-I_v003", "results")  # read-only sibling release
def lcm(a, b): return a * b // gcd(a, b)
def union_open(classes):
    L = reduce(lcm, [M for M, r in classes], 1)
    cov = np.zeros(L, bool); idx = np.arange(L)
    for M, r in classes: cov |= (idx % M == r % M)
    return L, cov
def summarize(classes):
    L, cov = union_open(classes)
    opn = np.nonzero(~cov)[0]
    g = 0
    for n in opn: g = gcd(g, int(n + 1))
    return {"period": L, "open_density": f"{len(opn)}/{L}", "open_density_float": len(opn) / L, "covered_density_float": 1 - len(opn) / L,
            "gcd_of_n_plus_1_over_open_set": g, "open_residues_count": int(len(opn))}
G = [(4, 1), (16, 7)]    # Theorem G classes (n>=5 / n>=7 ; small members checked exactly elsewhere)
def v003(B, K):
    r = json.load(open(os.path.join(V003, f"D2_B{B}_K{K}.json")))
    return [(c["M"], c["r"]) for c in r["identities"]]
if __name__ == "__main__":
    for B, K in [(2, 5), (4, 5), (5, 5), (6, 5), (10, 5), (3, 5), (12, 4)]:
        base = v003(B, K)
        a = summarize(base); b = summarize(base + G)
        print(B, K, "v003 open", a["open_density"], f"{a['open_density_float']:.6f}", "| +G open", b["open_density"], f"{b['open_density_float']:.6f}", "gcd(n+1) on open set:", b["gcd_of_n_plus_1_over_open_set"])
