#!/usr/bin/env python3
"""FIELD-I v003 verifier: collective growth and R=3 rendezvous graphs. Exact arithmetic. Tags PASS/FAIL/DATA/OPEN.
Collective map C(x) = x + Delta_coll(x),  Delta_coll = lcm(d_i^2)/gcd(N_i) over D(x) (v002 T8)."""
import os, sys, time
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter
QUICK = os.environ.get("FIELD3_QUICK") == "1"
NFAIL = 0; T0 = time.time()
def rec(tag, status, msg):
    global NFAIL
    if status == "FAIL": NFAIL += 1
    print(f"{status} {tag}: {msg}", flush=True)
def lcm(a, b): return a // gcd(a, b) * b
def Dset(a, b): return [d for d in range(1 + b, isqrt(a) + 1, b) if a % (d * d) == 0]
def Dx(x): return Dset(x.numerator, x.denominator)
def delta(d, e): return Fr(lcm(d, e) ** 2, gcd(d - 1, e - 1))
def LG(ds):
    L, G = 1, 0
    for d in ds: L = lcm(L, d * d); G = gcd(G, d - 1)
    return L, G
def Dcoll_ds(ds): L, G = LG(ds); return Fr(L, G)
def C_ds(x, ds): return x + Dcoll_ds(ds)

# ---------------------------------------------------------------- independent C (brute force) on a small box
def brute_first_common(x, routes, mult=2):
    LN = 1
    for _, N in routes: LN = lcm(LN, N)
    cap = (mult * x.numerator * LN) // x.denominator; sets = []
    for (M, N) in routes:
        unit = (N + 1) ** 2 * (LN // N); sets.append({m * unit for m in range(M + 1, cap // unit + 1)})
    com = set.intersection(*sets); return Fr(min(com), LN) if com else None
X0 = 600 if QUICK else 2000
box = {}
for N in range(1, X0 + 1):
    st = Fr((N + 1) ** 2, N); M = 1
    while M * st <= X0: box.setdefault(M * st, []).append((M, N)); M += 1
bad = 0
for x, occ in box.items():
    y = brute_first_common(x, occ, 2)
    if y is None or y != C_ds(x, [n + 1 for _, n in occ]): bad += 1
rec("H0.1", "PASS" if bad == 0 else "FAIL", f"formula C(x) == brute-force first common future of the whole fibre, all {len(box)} box values (R>=1) <= {X0}; mismatches {bad}")

# ---------------------------------------------------------------- H1  plateau structure, growth bound
def Kd(x, ds, d):
    D = Dcoll_ds(ds); u, v = D.numerator, D.denominator; gam = x / D; assert gam.denominator == 1
    gam = int(gam); q = -(-gam // (v * d * d)); return v * d * d * q - gam, v, gam
def bound(x, ds):
    S = set(ds); best = None; v = None; dmin = None
    d = 2
    while dmin is None:
        if d not in S: dmin = d
        d += 1
    for d in range(2, dmin + 8):
        if d in S: continue
        k, v, gam = Kd(x, ds, d)
        best = k if best is None or k < best else best
    return best, dmin, v
def first_growth(x, ds, cap):
    n = len(ds)
    for k in range(1, cap + 2):
        x = C_ds(x, ds); nd = Dx(x)
        assert set(ds) <= set(nd)
        if len(nd) > n: return k, x, nd
        ds = nd
    return None, x, ds
seeds = [Fr(a, b) for b in range(1, 9) for a in range(1, 700) if gcd(a, b) == 1 and len(Dset(a, b)) >= 1]
if QUICK: seeds = seeds[::5]
nev = 0; viol = 0; ratios = []; kmin_viol = 0; kd_range_viol = 0; nodrop = 0; maxT = 0
EV = 4
for x0 in seeds:
    x = x0; ds = Dx(x)
    for ev in range(EV):
        bd, dmin, v = bound(x, ds)
        if not (1 <= bd <= v * dmin * dmin - 1): kd_range_viol += 1
        for d in range(2, dmin + 8):
            if d not in ds:
                k, v_, gam = Kd(x, ds, d)
                if not (1 <= k <= v_ * d * d - 1): kd_range_viol += 1
        T, x, ds = first_growth(x, ds, bd)
        nev += 1
        if T is None or T > bd: viol += 1; break
        ratios.append(T / bd); maxT = max(maxT, T)
rec("H1.1", "PASS" if viol == 0 else "FAIL", f"growth-time bound T(x) <= min_(d>=2, d not in D(x)) K_d verified for {nev} consecutive growth events from {len(seeds)} seeds (4 events each); violations {viol}")
rec("H1.2", "PASS" if kd_range_viol == 0 else "FAIL", f"1 <= K_d <= v d^2 - 1 for every tested d not in D(x) (v = gcd(N_i) = denominator of Delta_coll); violations {kd_range_viol}")
ratios.sort()
rec("H1.3", "DATA", f"tightness T/bound over {len(ratios)} events: median {ratios[len(ratios)//2]:.3f}, 90th pct {ratios[int(.9*len(ratios))]:.3f}, share with T = bound {sum(1 for r in ratios if r==1)/len(ratios):.3f}; largest observed T = {maxT}")

# plateau law and the proof's construction, checked directly
bad = 0; n = 0
for x0 in seeds[::3]:
    ds = Dx(x0); D = Dcoll_ds(ds); u, v = D.numerator, D.denominator
    if gcd(u, v) != 1: bad += 1
    x = x0
    for k in range(1, 25):
        x = C_ds(x, ds); nd = Dx(x)
        if len(nd) > len(ds): break
        n += 1
        if x != (x0 / D + k) * D: bad += 1
rec("H1.4", "PASS" if bad == 0 else "FAIL", f"Delta_coll = lcm(d_i^2)/gcd(N_i) is already reduced (u,v) and a plateau is the progression x_k = (gamma_0 + k) Delta; {n} plateau steps, bad {bad}")
bad = 0; n = 0
for x0 in seeds[::3]:
    ds = Dx(x0); D = Dcoll_ds(ds); u, v = D.numerator, D.denominator; g0 = int(x0 / D)
    for d in range(2, 9):
        if d in ds: continue
        for q in (1, 2, 5):
            k = v * d * d * q - g0
            if k < 0: continue
            xk = (g0 + k) * D; n += 1
            if not (xk.denominator == 1 and xk == u * d * d * q and d in Dx(xk)): bad += 1
rec("H1.5", "PASS" if bad == 0 else "FAIL", f"construction of the growth proof: gamma_0+k = v d^2 q gives x_k = u d^2 q, an integer divisible by d^2, so d in D(x_k); {n} constructions, bad {bad}")

# long-run illustration (not the proof): R along C-orbits
rows = []
for x0 in (Fr(36), Fr(81), Fr(2025, 2), Fr(400, 3), Fr(8), Fr(64)):
    x = x0; ds = Dx(x); Rs = [len(ds)]; ev = 0
    while ev < 6:
        bd, _, _ = bound(x, ds)
        T, x, ds = first_growth(x, ds, bd); ev += 1; Rs.append(len(ds))
    rows.append((str(x0), Rs))
rec("H1.6", "DATA", "R after each successive growth event: " + "; ".join(f"{s}: {Rs}" for s, Rs in rows))
rec("H1.7", "OPEN", "growth RATE along orbits (R(x_n) vs n); whether every integer d>=2 eventually lies in D(x_n); characterisation of the first growth value")

# ---------------------------------------------------------------- H2  R = 3 rendezvous graph
A_ANC = 20000 if QUICK else 200000
def weights(ds):  # (g, L^2) pairs: Delta = L^2/g , h = x g / L^2
    return [(gcd(d - 1, e - 1), lcm(d, e) ** 2) for d, e in combinations(ds, 2)]
cl_bad = 0; n3 = 0; shapes = Counter(); eq_bad = 0
def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
for m in range(1, A_ANC + 1):
    ds = Dset(m, 1); S = set(ds)
    for d in ds:                       # downward closure
        for e in range(2, d):
            if d % e == 0 and e not in S: cl_bad += 1
    for d, e in combinations(ds, 2):   # lcm closure
        if lcm(d, e) not in S: cl_bad += 1
    if len(ds) == 3:
        n3 += 1; s = sorted(ds)
        pq = len([t for t in s if isprime(t)]) == 2 and s[2] == s[0] * s[1]
        pp = isprime(s[0]) and s[1] == s[0] ** 2 and s[2] == s[0] ** 3
        shapes["{p,q,pq}" if pq else "{p,p^2,p^3}" if pp else "OTHER"] += 1
        w = weights(ds); ratios_ = [Fr(g, L2) for g, L2 in w]
        if pq and len(set(ratios_)) != 1: eq_bad += 1
        if pp and len(set(ratios_)) != 2: eq_bad += 1
rec("H2.1", "PASS" if cl_bad == 0 else "FAIL", f"integer fibres m<={A_ANC}: D(m) is closed downward (e|d, e>=2) and under lcm; violations {cl_bad}")
rec("H2.2", "PASS" if (shapes["OTHER"] == 0 and eq_bad == 0) else "FAIL",
    f"integer fibres with R=3 ({n3}): shapes {dict(shapes)}; weights all equal for {{p,q,pq}}, exactly two equal for {{p,p^2,p^3}}; violations {eq_bad}; unexpected shapes {shapes['OTHER']}")
# algebraic identities used in the proof
bad = 0
for p in range(2, 60):
    if not isprime(p): continue
    for q in range(2, 60):
        if not isprime(q) or q == p: continue
        if gcd(p - 1, p * q - 1) != gcd(p - 1, q - 1) or gcd(q - 1, p * q - 1) != gcd(p - 1, q - 1): bad += 1
    for a_, b_ in ((1, 2), (1, 3), (2, 3)):
        if gcd(p ** a_ - 1, p ** b_ - 1) != p ** gcd(a_, b_) - 1: bad += 1
rec("H2.3", "PASS" if bad == 0 else "FAIL", f"identities gcd(p-1,pq-1)=gcd(q-1,pq-1)=gcd(p-1,q-1) and gcd(p^a-1,p^b-1)=p^gcd(a,b)-1 for all primes p,q<60; bad {bad}")
# rational fibres: rigid triangles
AR, BR = (8000, 14) if QUICK else (40000, 40)
rigid = []; n3r = 0
for b in range(2, BR + 1):
    for a in range(1, AR + 1):
        if gcd(a, b) != 1: continue
        ds = Dset(a, b)
        if len(ds) != 3: continue
        n3r += 1
        r_ = [Fr(g, L2) for g, L2 in weights(ds)]
        if len(set(r_)) == 3: rigid.append((a, b, ds))
rec("H2.4", "DATA", f"rational fibres (b>=2, a<={AR}, b<={BR}) with R=3: {n3r}; with three distinct pair indices (rigid triangle): {len(rigid)} -> {rigid[:5]}")
if not QUICK:
    ok = rigid == [(20736, 5, [6, 16, 36])]
    x = Fr(20736, 5); ds = [6, 16, 36]
    hs = sorted(int(x / delta(d, e)) for d, e in combinations(ds, 2))
    occ = [(int(x * (d - 1) / (d * d)), d - 1) for d in ds]
    okocc = all(Fr(M * (N + 1) ** 2, N) == x for M, N in occ)
    y = brute_first_common(x, occ, 2)
    rec("H2.5", "PASS" if (ok and hs == [1, 9, 16] and okocc and y == C_ds(x, ds) and Dx(x) == ds) else "FAIL",
        f"x=20736/5: D={Dx(x)}, occurrences {occ}, pair indices H={hs} (rigid), unique in the search range; brute-force collective rendezvous matches ({y})")
else:
    rec("H2.5", "DATA", "skipped in QUICK mode")
rec("H2.6", "OPEN", "complete classification of R=3 rational fibres; rigidity of fibres with R>=4 (data: 61% rigid in v002)")

print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL"); sys.exit(0 if NFAIL == 0 else 1)
