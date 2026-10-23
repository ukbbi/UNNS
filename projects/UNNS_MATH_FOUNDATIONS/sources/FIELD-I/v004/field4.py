#!/usr/bin/env python3
"""FIELD-I v004 verifier: rational rigidity classification (J1), exact growth bounds (J3), growth lower bound (J2),
collective vs route-aware structure (J4). Exact arithmetic. Tags PASS/FAIL/DATA/OPEN.
Key reduction: D(a/b) = { d | s : d>=2, d = 1 (mod b) }, s = largest integer with s^2 | a  (a = s^2 t, t squarefree)."""
import os, sys, time
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter
QUICK = os.environ.get("FIELD4_QUICK") == "1"
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
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def sqrt_part(a):
    s = 1
    for p, e in factor(a).items(): s *= p ** (e // 2)
    return s
def divisors(n):
    ds = []; i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i * i != n: ds.append(n // i)
        i += 1
    return sorted(ds)
def isprime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
def wts(ds): return [Fr(gcd(d - 1, e - 1), lcm(d, e) ** 2) for d, e in combinations(ds, 2)]
def rigid(ds): return len(set(wts(ds))) == len(wts(ds))

# ---------------------------------------------------------------- J1.a  reduction theorem
A1, B1 = (1500, 12) if QUICK else (6000, 30)
bad = bad_h = n = 0
for b in range(1, B1 + 1):
    for a in range(1, A1 + 1):
        if gcd(a, b) != 1: continue
        s = sqrt_part(a); t = a // (s * s)
        ds = [d for d in divisors(s) if d >= 2 and (d - 1) % b == 0]
        if ds != Dset(a, b): bad += 1
        if len(ds) >= 2:
            n += 1; x = Fr(a, b)
            for d, e in combinations(ds, 2):
                h0 = Fr(s * s * gcd(d - 1, e - 1), b * lcm(d, e) ** 2)
                if h0.denominator != 1 or x / delta(d, e) != t * h0: bad_h += 1
rec("J1.1", "PASS" if (bad == 0 and bad_h == 0) else "FAIL",
    f"reduction: D(a/b) = {{d | s, d>=2, d=1 mod b}} for all reduced a<={A1}, b<={B1}; H(a/b) = t * H0(s,b) with H0 = s^2 g/(b L^2) integer ({n} fibres with R>=2); bad {bad}/{bad_h}")
# squarefree scaling (formal version of the review's observation)
bad = n = 0
for (a, b) in [(20736, 5), (81, 2), (2025, 2), (400, 3), (784, 3), (324, 5), (7056, 5)]:
    x = Fr(a, b); ds = Dx(x)
    for m in [q for q in range(2, 60) if isprime(q) and a * b % q != 0] + [6 * 7 * 11 * 13 if gcd(6 * 7 * 11 * 13, a * b) == 1 else 7 * 11 * 13 * 17 * 19]:
        if gcd(m, a * b) != 1: continue
        n += 1; y = Fr(m * a, b)
        if Dx(y) != ds: bad += 1
        if len(ds) >= 2 and [y / delta(d, e) for d, e in combinations(ds, 2)] != [m * x / delta(d, e) for d, e in combinations(ds, 2)]: bad += 1
rec("J1.2", "PASS" if bad == 0 else "FAIL", f"squarefree scaling: D(m a/b) = D(a/b) and every index multiplied by m, for m squarefree with gcd(m,ab)=1 (primes<60 and products); {n} cases, bad {bad}")
review = {145152: [7, 63, 112], 228096: [11, 99, 176], 269568: [13, 117, 208], 20736: [1, 9, 16]}
ok = all(sorted(int(Fr(a, 5) / delta(d, e)) for d, e in combinations(Dx(Fr(a, 5)), 2)) == v and Dx(Fr(a, 5)) == [6, 16, 36] for a, v in review.items())
rec("J1.3", "PASS" if ok else "FAIL", "table from the v003 review reproduced exactly: 20736/5, 145152/5, 228096/5, 269568/5 all have D={6,16,36} and indices (1,9,16)*m")

# ---------------------------------------------------------------- J1.b  closure lemmas
bad = 0; n = 0
for b in range(2, 25):
    for a in range(1, 4000):
        if gcd(a, b) != 1: continue
        ds = Dset(a, b); S = set(ds)
        for d in ds:
            for e in ds:
                if d < e and e % d == 0:                                  # Lemma Q: e/d in D (or 1)
                    n += 1
                    if (e // d) not in S: bad += 1
                c = gcd(d, e)
                if d < e and (c - 1) % b == 0:                             # Lemma G
                    n += 1
                    if lcm(d, e) not in S or (c != 1 and c not in S): bad += 1
rec("J1.4", "PASS" if bad == 0 else "FAIL", f"Lemma Q (d|e in D => e/d in D) and Lemma G (gcd = 1 mod b => lcm in D, gcd in D or =1); {n} checks (b=2..24), bad {bad}")

# ---------------------------------------------------------------- J1.c  classification of three-route fibres (primitive configurations)
LAM = 1200 if QUICK else 4000
prim = []
for lam in range(2, LAM + 1):
    dv = [d for d in divisors(lam) if d >= 2]; cands = set()
    for d in dv:
        for e in divisors(d - 1):
            if e >= 2: cands.add(e)
    fl = factor(lam)
    for b in cands:
        D = [d for d in dv if (d - 1) % b == 0]
        if len(D) == 3:
            L = 1
            for d in D: L = lcm(L, d)
            if L == lam and all(gcd(b, p) == 1 for p in fl): prim.append((lam, b, tuple(D)))
def classify(T, b):
    d = sorted(T); comp = [(i, j) for i, j in combinations(range(3), 2) if d[j] % d[i] == 0]
    if len(comp) == 3:
        q = d[0]; return "chain", (d == [q, q * q, q ** 3])
    if len(comp) == 2:
        if (0, 1) in comp and (0, 2) in comp: return "V", False
        return "Lambda", (d[2] == d[0] * d[1])
    if len(comp) == 1:
        i, j = comp[0]; k = 3 - i - j; q = d[i]
        return "onepair", (d[j] == q * q and d[k] % q != 0 and d[k] % (q * q) != 0 and (q * q) % d[k] != 0 and q % d[k] != 0)
    return "antichain", all((gcd(x, y) - 1) % b != 0 and gcd(x, y) >= 2 for x, y in combinations(d, 2))
cnt = Counter(); cnt_r = Counter(); shape_ok = True; exr = None; exn = None
for lam, b, T in prim:
    sh, ok = classify(T, b); cnt[sh] += 1; r = rigid(T); cnt_r[sh] += r
    if not ok: shape_ok = False
    if sh == "antichain":
        if r and exr is None: exr = (lam, b, T)
        if not r and exn is None: exn = (lam, b, T)
rec("J1.5", "PASS" if shape_ok and cnt["V"] == 0 else "FAIL", f"{len(prim)} primitive rational three-route configurations (lambda<={LAM}): shapes {dict(cnt)}; every shape obeys its structure law (chain={{q,q^2,q^3}}, Lambda={{d1,d2,d1 d2}}, one-pair={{q,q^2,e}}, antichain: pairwise gcd >=2 and != 1 mod b); V never occurs")
law = (cnt_r["chain"] == 0 and cnt_r["Lambda"] == 0 and cnt_r["onepair"] == cnt["onepair"])
rec("J1.6", "PASS" if law else "FAIL", f"rigidity by shape: chain {cnt_r['chain']}/{cnt['chain']}, Lambda {cnt_r['Lambda']}/{cnt['Lambda']}, one comparable pair {cnt_r['onepair']}/{cnt['onepair']} (all rigid), antichain {cnt_r['antichain']}/{cnt['antichain']} (both kinds occur)")
rec("J1.7", "DATA", f"antichain examples: rigid {exr}; non-rigid {exn}")
# independent route: direct enumeration over (a,b), no divisor-based primitive search
AR, BR = (20000, 20) if QUICK else (60000, 40)
cnt2 = Counter(); bad = 0; nr = 0
for b in range(2, BR + 1):
    for a in range(1, AR + 1):
        if gcd(a, b) != 1: continue
        ds = Dset(a, b)
        if len(ds) != 3: continue
        sh, ok = classify(ds, b); cnt2[(sh, rigid(ds))] += 1; nr += 1
        if not ok or sh == "V": bad += 1
        if sh in ("chain", "Lambda") and rigid(ds): bad += 1
        if sh == "onepair" and not rigid(ds): bad += 1
rec("J1.8", "PASS" if bad == 0 else "FAIL", f"independent enumeration (b<={BR}, a<={AR}): {nr} rational R=3 fibres; (shape, rigid) counts {dict(cnt2)}; violations {bad}")
# integer case consistency (T20): shapes chain/Lambda only
bad = n = 0; sh1 = Counter()
for m in range(1, 5000 if QUICK else 30000):
    ds = Dset(m, 1)
    if len(ds) == 3:
        n += 1; sh, ok = classify(ds, 1); sh1[sh] += 1
        if sh not in ("chain", "Lambda") or not ok or rigid(ds): bad += 1
rec("J1.9", "PASS" if bad == 0 else "FAIL", f"b=1 (v003 T20) is the same classification: {n} integer R=3 fibres (m<{5000 if QUICK else 30000}) have shapes {dict(sh1)} only, never one-pair/antichain, never rigid; violations {bad}")
# infinite primitive rigid family  s = 22 r, b = 3, r prime = 23 mod 63
fam = [r for r in range(23, 6000, 63) if isprime(r)]
bad = 0
for r in fam[: (6 if QUICK else 30)]:
    a = (22 * r) ** 2; x = Fr(a, 3); ds = Dset(a, 3)
    gg = sorted(gcd(u - 1, v - 1) for u, v in combinations(ds, 2))
    if ds != sorted([22, 2 * r, 11 * r]) or gg != [3, 9, 21] or not rigid(ds) or classify(ds, 3)[0] != "antichain": bad += 1
rec("J1.10", "PASS" if bad == 0 else "FAIL", f"infinite primitive family: b=3, s=22r, r prime = 23 mod 63 (r={fam[:5]}...): D={{22,2r,11r}}, gcd values {{3,9,21}}, all L=22r, rigid; checked {len(fam[:(6 if QUICK else 30)])} primes")

# ---------------------------------------------------------------- J3  exact global minimum of the growth-time bounds
def Kd(x, ds, d):
    D = Dcoll_ds(ds); v = D.denominator; gam = int(x / D); q = -(-gam // (v * d * d)); return v * d * d * q - gam
def dmin_of(ds):
    S = set(ds); d = 2
    while d in S: d += 1
    return d
def partial_bound(x, ds):
    dm = dmin_of(ds); return min(Kd(x, ds, d) for d in range(2, dm + 8) if d not in ds)
def exact_bound(x, ds):
    D = Dcoll_ds(ds); v = D.denominator; gam = int(x / D)
    dm = dmin_of(ds); k0 = Kd(x, ds, dm); dmax = isqrt((gam + k0) // v) + 1
    return min(Kd(x, ds, d) for d in range(2, max(dmax, dm) + 1) if d not in ds)
def first_growth(x, ds, cap):
    for k in range(1, cap + 2):
        x = C_ds(x, ds); nd = Dx(x)
        if len(nd) > len(ds): return k, x, nd
    return None, x, ds
seeds = [Fr(a, b) for b in range(1, 7) for a in range(1, 500) if gcd(a, b) == 1 and Dset(a, b)]
if QUICK: seeds = seeds[::5]
viol = better = ev = 0; tight = 0
for x0 in seeds:
    x = x0; ds = Dx(x)
    for _ in range(4):
        pb = partial_bound(x, ds); eb = exact_bound(x, ds)
        assert eb <= pb
        T, x, ds = first_growth(x, ds, eb)
        ev += 1
        if T is None or T > eb: viol += 1; break
        better += (eb < pb); tight += (T == eb)
rec("J3.1", "PASS" if viol == 0 else "FAIL", f"exact global minimum min_(d not in D) K_d (search d <= sqrt((gamma+k0)/v)+1): T <= exact bound on {ev} events from {len(seeds)} seeds; violations {viol}")
rec("J3.2", "DATA", f"exact minimum improves the v003 truncated minimum in {better}/{ev} events; T equals the exact bound in {tight}/{ev}")

# ---------------------------------------------------------------- J2  provable lower bound for R along orbits
bad = n = 0; rows = []
for x0 in seeds[::4]:
    x = x0; ds = Dx(x); R0 = len(ds); v0 = LG(ds)[1]; step = 0
    first_reach = {R0: 0}
    for _ in range(5):
        eb = exact_bound(x, ds)
        T, x, nd = first_growth(x, ds, eb); step += T
        for r in range(len(ds) + 1, len(nd) + 1): first_reach[r] = step
        ds = nd
        if LG(ds)[1] > v0: bad += 1                                  # G non-increasing
    for r, st in first_reach.items():
        if r == R0: continue
        n += 1
        bound_ = sum(v0 * (j + 2) ** 2 - 1 for j in range(R0, r))
        if st > bound_: bad += 1
rec("J2.1", "PASS" if bad == 0 else "FAIL", f"G(x_n)=gcd(N_i) is non-increasing along C-orbits, and the first step reaching R>=r is <= sum_(j=R0)^(r-1) (G0 (j+2)^2 - 1); {n} checks, bad {bad}")
rec("J2.2", "OPEN", "true growth rate: the proved bound gives R(x_n) >= c (n/G0)^(1/3) (cubic root); sampled orbits grow by a constant per growth event with short plateaus, suggesting near-linear growth")

# ---------------------------------------------------------------- J4  collective versus route-aware
x0 = Fr(36); Rk = [len(Dx(x0 + k * Fr(36))) for k in range(0, 8)]
rec("J4.1", "PASS" if Rk[3] == 5 and Rk[4] == 3 else "FAIL", f"route-aware orbit of the pair (2,3) at x=36 (x_k = 36(k+1)): R = {Rk}; R drops 5 -> 3 at k=4, whereas along C-orbits R never decreases (v002 G.6): monotone fibre growth is a law of the collective branch only")
drops = tot = 0
for x, in [(Fr(a, b),) for b in range(1, 5) for a in range(1, 400) if gcd(a, b) == 1]:
    ds = Dx(x)
    if len(ds) < 2: continue
    for d, e in combinations(ds, 2):
        D = delta(d, e); prev = None; tot += 1; dec = False
        for k in range(0, 10):
            r = len(Dx(x + k * D))
            if prev is not None and r < prev: dec = True
            prev = r
        drops += dec
rec("J4.2", "DATA", f"route-aware pair orbits x+k*Delta (k<=9) in which R decreases at some step: {drops}/{tot}")
rec("J4.3", "OPEN", "other structural laws distinguishing the collective branch (e.g. asymptotics of D(x_n), whether every d>=2 eventually belongs to it)")

print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL"); sys.exit(0 if NFAIL == 0 else 1)
