#!/usr/bin/env python3
"""Numerical checks quoted in FIELD1_GRAMMAR_G1-G3_v001.md (exact arithmetic). Tags PASS/FAIL/DATA."""
import sys
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
NF = 0
def rec(t, s, m):
    global NF
    if s == "FAIL": NF += 1
    print(f"{s} {t}: {m}")
def lcm(a, b): return a // gcd(a, b) * b
def Dset(a, b): return [d for d in range(1 + b, isqrt(a) + 1, b) if a % (d * d) == 0]
def Dx(x): return Dset(x.numerator, x.denominator)
def delta(d, e): return Fr(lcm(d, e) ** 2, gcd(d - 1, e - 1))
def Dcoll(x):
    L, G = 1, 0
    for d in Dx(x): L = lcm(L, d * d); G = gcd(G, d - 1)
    return Fr(L, G)
def gamma(x): return int(x / Dcoll(x))
def C(x): return x + Dcoll(x)

# 1. concrete incompatibility instances (a g / b + i L^2 = 0 mod p^2)
def inst(a, b, d, e, p):
    x = Fr(a, b); N, Np = d - 1, e - 1; g = gcd(N, Np); L = lcm(d, e); D = delta(d, e)
    i = (-(a * g // b) * pow(L * L, -1, p * p)) % (p * p); y = x + i * D
    Mq = y * (p - 1) / (p * p)
    ok = Mq.denominator == 1 and Mq >= 1 and p in Dx(y) and d in Dx(y) and e in Dx(y)
    dl = delta(d, p)
    return ok and dl.numerator % (p * p) == 0, i, y, Mq, dl
for (a, b, d, e, p) in [(36, 1, 2, 3, 7), (36, 1, 2, 3, 11), (81, 1, 3, 9, 11), (81, 2, 3, 9, 11)]:
    ok, i, y, Mq, dl = inst(a, b, d, e, p)
    rec("G.1", "PASS" if ok else "FAIL", f"x={a}/{b} pair d=({d},{e}) p={p}: i={i}, y={y}, new route (M'',N'')=({Mq},{p-1}), Delta(d,p)={dl}")
# P0 for x=36, pair (2,3) must be a multiple of Delta(2,p)=4p^2 for every such p
rec("G.2", "PASS" if all(delta(2, p) == 4 * p * p for p in (7, 11, 13, 17, 19, 23)) else "FAIL", "x=36: Delta(2,p) = 4p^2 for p=7,11,13,17,19,23 (so the fixed gap P0 would be divisible by 4p^2 for all these p)")
x = Fr(36); y = x + 3 * delta(2, 3)
rec("G.3", "PASS" if (y == 144 and Dcoll(x) == 36 and Dcoll(y) == 144 and C(y) - y == 144 and C(x) - x == 36) else "FAIL", f"x=36, pair (2,3), shift 3 periods: y={y}; C(x)-x=36, C(y)-y=144 (stationarity would need 36)")

# 2. corpus
CORP = {}
for b in range(1, 31):
    for a in range(1, 8001):
        if gcd(a, b) == 1:
            ds = Dset(a, b)
            if len(ds) >= 2: CORP[Fr(a, b)] = ds
# 2a. star_1 and C coincide on every two-route fibre
bad = sum(1 for x, ds in CORP.items() if len(ds) == 2 and x + delta(ds[0], ds[1]) != C(x))
n2 = sum(1 for ds in CORP.values() if len(ds) == 2)
rec("G.4", "PASS" if bad == 0 else "FAIL", f"R=2 fibres: first pair rendezvous == C(x) in all {n2} cases")
diff = sum(1 for x, ds in CORP.items() if len(ds) >= 3 for d, e in combinations(ds, 2) if x + delta(d, e) != C(x))
tot = sum(1 for x, ds in CORP.items() if len(ds) >= 3 for _ in combinations(ds, 2))
rec("G.5", "DATA", f"R>=3 fibres: pairs whose first rendezvous differs from C(x): {diff}/{tot}")
# 2b. C is monotone in the fibre: D(x) subset D(C(x)), R(Cx)>=R(x)
bad = sum(1 for x, ds in CORP.items() if not set(ds) <= set(Dx(C(x))))
rec("G.6", "PASS" if bad == 0 else "FAIL", f"D(x) is contained in D(C(x)) (hence R(C(x)) >= R(x)) for all {len(CORP)} corpus fibres; violations {bad}")
# 2c. doubling is the collective choice j = gamma
bad = sum(1 for x in CORP if x + gamma(x) * Dcoll(x) != 2 * x)
rec("G.7", "PASS" if bad == 0 else "FAIL", f"j(x)=gamma(x) gives x + gamma*Delta_coll = 2x in every fibre; violations {bad}")
# 2d. orbits of C
for seed in (Fr(36), Fr(81), Fr(2025, 2), Fr(400, 3), Fr(144)):
    x = seed; row = []
    for k in range(10):
        row.append((str(x) if x.denominator > 1 else str(x.numerator), len(Dx(x)), gamma(x) if len(Dx(x)) >= 1 else None)); x = C(x) if Dx(x) else x
    rec("G.8", "DATA", f"C-orbit of {seed} (value,R,gamma) first 10: " + "; ".join(f"{v}|R{r}|g{g}" for v, r, g in row))
# 2e. join (lcm) at the output value y = x + Delta_rs
yes = {"b=1": [0, 0], "b>1": [0, 0]}
for x, ds in CORP.items():
    key = "b=1" if x.denominator == 1 else "b>1"
    for d, e in combinations(ds, 2):
        y = x + delta(d, e); yes[key][1] += 1; yes[key][0] += (lcm(d, e) in Dx(y))
rec("G.9", "DATA", "occurrence 'join' lcm(d,d') present in F(y) at y = x+Delta: " + "; ".join(f"{k}: {v[0]}/{v[1]}" for k, v in yes.items()))
# 2f. plateau structure and gamma-reset along C-orbits
nb = nreset = nplateau = 0; seeds = list(CORP)[::29][:30]; maxsteps = 20; fails = []
for x0 in seeds:
    x = x0
    for k in range(maxsteps):
        D0 = Dx(x); nx = C(x); D1 = Dx(nx)
        if D1 == D0:
            nplateau += 1
            if nx - x != Dcoll(x0) and k == 0: pass
        else:
            nb += 1
            if gamma(nx) == 1: nreset += 1
            else: fails.append((str(x0), str(nx), gamma(nx)))
        x = nx
rec("G.10", "DATA", f"C-orbits from {len(seeds)} seeds, {maxsteps} steps: {nb} fibre-growth events, gamma = 1 right after growth in {nreset}/{nb}; exceptions (first 3): {fails[:3]}")
bad = 0
for x0 in seeds:
    x = x0
    for k in range(maxsteps):
        nx = C(x)
        if Dx(nx) == Dx(x) and nx - x != Dcoll(x): bad += 1
        x = nx
rec("G.11", "PASS" if bad == 0 else "FAIL", f"while D(x) is unchanged the C-step is the constant Delta_coll (arithmetic progression); violations {bad}")
print("ALL PASS" if NF == 0 else "SOME FAIL"); sys.exit(0 if NF == 0 else 1)
