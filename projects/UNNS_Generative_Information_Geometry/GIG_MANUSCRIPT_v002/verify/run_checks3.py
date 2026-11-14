#!/usr/bin/env python3
"""Third batch: refutation of gate necessity (explicit CRT counterexamples), re-derived from the definition."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gigmini import *
INH = os.path.join(HERE, "inherited")
OUT = {}
def tomask(b): return sum(1 << x for x in b)
cert = json.load(open(os.path.join(INH, "pattern_H2.json")))
z = {tuple(tomask(b) for b in f) for f in cert["z_faces"]}
Pz = set()
for F in z: Pz |= prefsets_of_face(F)
P6 = ordered_partitions(6)
three = [F for F in P6 if 6 - len(F) == 3]
def bd_chain(S):
    out = set()
    for F in S:
        for G in face_boundary(F): out ^= {G}
    return out
def in_span(cands, target):
    cols = {}
    for F in cands:
        for G in face_boundary(F): cols.setdefault(G, len(cols))
    for G in target: cols.setdefault(G, len(cols))
    piv = {}
    for F in cands:
        v = 0
        for G in face_boundary(F): v ^= 1 << cols[G]
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; break
    t = 0
    for G in target: t ^= 1 << cols[G]
    while t:
        h = t.bit_length() - 1
        if h not in piv: return False
        t ^= piv[h]
    return True
gates = {0: [0b010101], 1: [0b100010, 0b100110], 3: [8, 24, 40, 56]}
for g in (1, 3):
    c = json.load(open(os.path.join(INH, f"gate{g}_counterexample.json")))
    lab, m = tuple(c["labels"]), c["m"]
    fam = {I for I in range(1, 64) if m % Dmask(lab, I) == 0}
    zin = Pz <= fam
    gate_open = all(I in fam for I in gates[g])
    present3 = [F for F in three if prefsets_of_face(F) <= fam]
    bounds = in_span(present3, z)
    # which of the six obstructed octahedra are present
    OUT[f"gate{g}"] = {"labels": lab, "z_present": zin, "gate_open": gate_open, "n_present_3faces": len(present3), "z_bounds": bounds,
                       "hole_survives": zin and not bounds, "d_values_gate": {bin(I): (Dmask(lab, I)) for I in gates[g]}}
    print(g, OUT[f"gate{g}"]["z_present"], gate_open, bounds, OUT[f"gate{g}"]["hole_survives"])
json.dump(OUT, open(os.path.join(HERE, "results3.json"), "w"), indent=1, default=str)
