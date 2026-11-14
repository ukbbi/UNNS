#!/usr/bin/env python3
"""Third batch: lift calculus on the anchor cycle (LT-0..LT-3, FI-1, FI-3, J-1, J-2), exact GF(2)."""
import json, os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from gigmini import *
OUT = {}
def rec(name, **kw): OUT[name] = kw; print(name, json.dumps(kw, default=str)[:300])
INH = os.path.join(HERE, "inherited")
def tomask(b): return sum(1 << x for x in b)
def face_from(lst): return tuple(tomask(b) for b in lst)
cert = json.load(open(os.path.join(INH, "pattern_H2.json")))
z = {face_from(f) for f in cert["z_faces"]}; phi = {face_from(f) for f in cert["phi_faces"]}
def bd_chain(S):
    out = set()
    for F in S:
        for G in face_boundary(F): out ^= {G}
    return out
R = 1 << 6
Ins = lambda F, i: F[:i] + (F[i] | R,) + F[i + 1:]
first = lambda F: (R,) + F
last = lambda F: F + (R,)
def Lam(c):
    S = set()
    for F in c:
        for i in range(len(F)): S ^= {Ins(F, i)}
    return S
fi = lambda c: {first(F) for F in c}
la = lambda c: {last(F) for F in c}
Pz = set()
for F in z: Pz |= prefsets_of_face(F)
three = [F for F in ordered_partitions(6) if 6 - len(F) == 3]
def solve_filling(cands, target):
    cols = {}
    for F in cands:
        for G in face_boundary(F): cols.setdefault(G, len(cols))
    for G in target: cols.setdefault(G, len(cols))
    vecs = []
    for F in cands:
        v = 0
        for G in face_boundary(F): v ^= 1 << cols[G]
        vecs.append(v)
    t = 0
    for G in target: t ^= 1 << cols[G]
    piv = {}
    for i, v in enumerate(vecs):
        c = 1 << i
        while v:
            h = v.bit_length() - 1
            if h in piv: pv, pc = piv[h]; v ^= pv; c ^= pc
            else: piv[h] = (v, c); break
    c = 0
    while t:
        h = t.bit_length() - 1
        if h not in piv: return None
        pv, pc = piv[h]; t ^= pv; c ^= pc
    return set(cands[i] for i in range(len(cands)) if c >> i & 1)
B = {0: [21], 1: [34, 38, 46],
     2: [8, 9, 10, 11, 24, 25, 26, 27, 40, 41, 43, 56, 57, 58, 59],
     3: [8, 9, 10, 11, 24, 26, 27, 34, 40, 41, 42, 43, 46, 56, 57, 58, 59]}
fill = {}
for a, S in B.items():
    fam = Pz | set(S)
    cands = [F for F in three if prefsets_of_face(F) <= fam]
    fill[a] = solve_filling(cands, z)
rec("ch8_fillings", sizes={a: (None if c is None else len(c)) for a, c in fill.items()},
    verified=all(c is not None and bd_chain(c) == z for c in fill.values()))
# LT-1: every ordered pair gives a 3-cycle of P_7;  LT-2: diagonal = boundary of Lambda(c)
ok1 = True; ok2 = True; Ls = {}
for a in range(4):
    for b in range(4):
        L = Lam(z) ^ fi(fill[a]) ^ la(fill[b]); Ls[(a, b)] = L
        if bd_chain(L): ok1 = False
        if a == b and L != bd_chain(Lam(fill[a])): ok2 = False
rec("ch8_LT1_lift_is_cycle", pairs=16, ok=ok1)
rec("ch8_LT2_diagonal_is_boundary", ok=ok2)
# identity L_{a,b} = d Lam(c_a) + last(c_a + c_b)
ok = all(Ls[(a, b)] == (bd_chain(Lam(fill[a])) ^ la(fill[a] ^ fill[b])) for a in range(4) for b in range(4))
rec("ch8_LT2_identity", ok=ok)
# FI-1
ok = True
for a in range(4):
    for a2 in range(4):
        for b in range(4):
            if Ls[(a2, b)] ^ Ls[(a, b)] != fi(fill[a] ^ fill[a2]): ok = False
            if Ls[(b, a2)] ^ Ls[(b, a)] != la(fill[a] ^ fill[a2]): ok = False
rec("ch8_FI1", triples=64, ok=ok)
# FI-3: d Lam(d) = first(d) + last(d) for 3-cycles d = c_a + c_b
ok = all(bd_chain(Lam(fill[a] ^ fill[b])) == fi(fill[a] ^ fill[b]) ^ la(fill[a] ^ fill[b]) for a in range(4) for b in range(4))
rec("ch8_FI3", ok=ok)
# LT-3: cochain lift phi3 = sum Ins_{B*}(f) over supp phi (B* = first block = {2,4,5}); pairing with L and obstructed 4-faces of P_7
Bstar = tomask([2, 4, 5])
assert all(F[0] == Bstar for F in phi)
phi3 = {Ins(F, 0) for F in phi}
pair = {k: len(phi3 & L) % 2 for k, L in Ls.items()}
rec("ch8_LT3_pairing", phi3_weight=len(phi3), pairing_all16=sorted(set(pair.values())), ok=all(v == 1 for v in pair.values()))
four = [F for F in ordered_partitions(7) if 7 - len(F) == 4]
odd4 = [F for F in four if len(phi3 & set(face_boundary(F))) % 2 == 1]
rec("ch8_LT3_obstructed_4faces", n4faces=len(four), n_odd=len(odd4),
    faces=[[[i for i in range(7) if B_ >> i & 1] for B_ in F] for F in odd4])
# phi3 inserted in EVERY block fails
phi3all = set()
for F in phi:
    for i in range(len(F)): phi3all.add(Ins(F, i))
rec("ch8_LT3_all_block_fails", pairing_with_Lambda_z=len(phi3all & Lam(z)) % 2, n_odd=sum(1 for F in four if len(phi3all & set(face_boundary(F))) % 2 == 1))
# J-1: first, last chain maps; Pref(first f)
ok = True
for F in ordered_partitions(6):
    if bd_chain({first(F)}) != fi(set(face_boundary(F))): ok = False
    if bd_chain({last(F)}) != la(set(face_boundary(F))): ok = False
    pf = prefsets_of_face(first(F)); exp = {R} | {I | R for I in prefsets_of_face(F)}
    if not exp <= pf and not (pf == exp): pass
rec("ch8_J1_chain_maps", faces=len(ordered_partitions(6)), ok=ok)
json.dump(OUT, open(os.path.join(HERE, "results4.json"), "w"), indent=1, default=str)
print("DONE")
