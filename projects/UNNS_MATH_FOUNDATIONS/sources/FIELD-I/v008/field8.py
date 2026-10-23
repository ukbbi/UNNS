#!/usr/bin/env python3
"""FIELD-I v008 verifier (helpers copied from v005 for standalone use): (K1) signature criterion for three-route rigidity (closure of J1);
(K2) collective orbit universality: G-invariant, regime I, (s,t) dynamics, non-universality theorem;
(K3) G-collapse evidence. Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b} = {d | s : d>=2, d=1 mod b}, s^2||sqrt-part of a;
G(x)=gcd{d-1 : d in D(x)}; Delta_coll = lcm(d^2)/G; C(x)=x+Delta_coll."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD8_QUICK") == "1"
NFAIL = 0; T0 = time.time(); random.seed(5)
def rec(tag, status, msg):
    global NFAIL
    if status == "FAIL": NFAIL += 1
    print(f"{status} {tag}: {msg}", flush=True)
def lcm(a, b): return a // gcd(a, b) * b
# ---- exact factoring (Miller-Rabin + Pollard rho), no external packages
SP = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)
def is_prime(n):
    if n < 2: return False
    for p in SP[:12]:
        if n % p == 0: return n == p
    d = n - 1; r = 0
    while d % 2 == 0: d //= 2; r += 1
    for a in SP[:12]:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def rho(n):
    if n % 2 == 0: return 2
    while True:
        c = random.randrange(1, n); f = lambda x: (x * x + c) % n
        x = y = random.randrange(0, n); d = 1
        while d == 1:
            x = f(x); y = f(f(y)); d = gcd(abs(x - y), n)
        if d != n: return d
def factor(n, res=None):
    if res is None: res = {}
    if n == 1: return res
    for p in SP:
        while n % p == 0: res[p] = res.get(p, 0) + 1; n //= p
    if n == 1: return res
    if is_prime(n): res[n] = res.get(n, 0) + 1; return res
    d = rho(n); factor(d, res); factor(n // d, res); return res
def divisors_from(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
    return ds
def sqrt_part_f(f): return {p: e // 2 for p, e in f.items() if e // 2 > 0}
def sqrt_part(n):
    s = 1
    for p, e in factor(n).items(): s *= p ** (e // 2)
    return s
def sqf(n):
    t = 1
    for p, e in factor(n).items():
        if e % 2: t *= p
    return t
def Dset(a, b): return [d for d in range(1 + b, isqrt(a) + 1, b) if a % (d * d) == 0]   # brute reference
def Dx(x):                                                                                 # fast, via factorisation
    a, b = x.numerator, x.denominator
    s = sqrt_part_f(factor(a))
    return sorted(d for d in divisors_from(s) if d >= 2 and (d - 1) % b == 0)
def Gof(ds):
    g = 0
    for d in ds: g = gcd(g, d - 1)
    return g
def Dcoll(ds):
    L = 1
    for d in ds: L = lcm(L, d * d)
    G = Gof(ds); return Fr(L, G), G
def tau(f):
    t = 1
    for e in f.values(): t *= e + 1
    return t
def divisors(n):
    ds = []; i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i * i != n: ds.append(n // i)
        i += 1
    return sorted(ds)
def wts(ds): return [Fr(gcd(d - 1, e - 1), lcm(d, e) ** 2) for d, e in combinations(ds, 2)]
def rigid(ds): return len(set(wts(ds))) == len(wts(ds))
def sig(ds): return [(lcm(d, e), gcd(d - 1, e - 1)) for d, e in combinations(ds, 2)]
def rigid_sig(ds): s = sig(ds); return len(set(s)) == len(s)

assert Dx(Fr(784, 3)) == Dset(784, 3) == [4, 7, 28]
def Lof(ds):
    L = 1
    for d in ds: L = lcm(L, d)
    return L
def ordmod(a, g):
    k, v = 1, a % g
    while v != 1: v = v * a % g; k += 1
    return k
def divs_of(n): return sorted(divisors_from(factor(n)))
def st_step(s, t):
    f = factor(t + 1); sg = 1; tt = 1
    for p, e in f.items():
        sg *= p ** (e // 2)
        if e % 2: tt *= p
    return s * sg, tt
def v2(n):
    k = 0
    while n % 2 == 0: n //= 2; k += 1
    return k
def odd_part(n):
    while n % 2 == 0: n //= 2
    return n
def hyp_P(g, k, m, star=False):
    """Finite hypotheses of Theorem P (star=False: gcd(g,6)=1) or Theorem P* (star=True: g odd, 3 | g allowed).
    s = 2^k m.  H1 residues of divisors of m contain <2>; H2 saturation of every prime power of m and of 2^(k'), k' in [k,k+o);
    H3 (g+1) | s and G(s^2/g) = g; H4 (relaxed denominators): for t in {1,2,3}, b_t = g/gcd(g,t): every divisor d=2^j a (a | m, 0<=j<o) with d = 1 mod b_t has d = 1 mod g."""
    if g < 5 or g % 2 == 0: return False, "need g>=5 odd"
    if not star and gcd(g, 6) != 1: return False, "need gcd(g,6)=1"
    if k < 1 or m % 2 == 0 or gcd(m, g) != 1: return False, "k>=1, m odd, gcd(m,g)=1"
    o = ordmod(2, g); H = {pow(2, i, g) for i in range(o)}; dm = divs_of(m)
    if not H <= {d % g for d in dm}: return False, "H1 fails"
    for q, e in factor(m).items():
        rest = m // q ** e; dr = divs_of(rest)
        if not any((q ** e * 2 ** c * u) % g == 1 for c in range(k + 1) for u in dr): return False, f"H2 fails at {q}^{e}"
    for kk in range(k, k + o):
        if not any((2 ** kk * u) % g == 1 for u in dm): return False, "H2 fails at power of 2"
    s = 2 ** k * m
    if s % (g + 1): return False, "H3: g+1 does not divide s"
    D = [d for d in divs_of(s) if d >= 2 and d % g == 1]
    if Lof(D) != s or Gof(D) != g: return False, "H3: lcm D != s or G != g"
    for t in (1, 2, 3):
        b = g // gcd(g, t)
        for a in dm:
            for j in range(o):
                d = 2 ** j * a
                if d >= 2 and d % b == 1 and d % g != 1: return False, f"H4 fails: t={t} d={d}"
    return True, "ok"
def P_orbit(g, k, m, N, check=True):
    """direct forward iteration of the collective map from x0=s^2/g; returns (bad, Rs, ks, gammas)"""
    s = 2 ** k * m; t = 1; x = Fr(s * s, g); bad = 0; Rs = []; ks = []; gam = []
    for n in range(N):
        T = Dx(x)
        if check:
            b = g // gcd(g, t); D = [d for d in divs_of(s) if d >= 2 and d % b == 1]
            if x != Fr(s * s * t, g) or T != D or Lof(T) != s or Gof(T) != g: bad += 1
        Rs.append(len(T)); ks.append(v2(s)); L = Lof(T); gam.append(int(g * x) // (L * L))
        Dl, G = Dcoll(T); x = x + Dl; s, t = st_step(s, t)
    return bad, Rs, ks, gam

# =================================================================== M1  elementary construction
def elem_s(g):
    o = ordmod(2, g); return o, (g + 1) * (g + 2) ** o
lemma_bad = 0; rows = []
GMAX = 60 if QUICK else 150
gl = [g for g in range(5, GMAX) if gcd(g, 6) == 1]
for g in gl:
    o, s = elem_s(g)
    if gcd(g + 1, g) != 1 or gcd(g + 2, g) != 1 or (g + 2) % g != 2 or pow(g + 2, o, g) != 1 or s % g != 1: lemma_bad += 1
rec("M1.1", "PASS" if lemma_bad == 0 else "FAIL", f"elementary lemma for all {len(gl)} g in [5,{GMAX}) with gcd(g,6)=1: gcd(g+1,g)=gcd(g+2,g)=1 (g odd, 3 not dividing g), g+2 = 2 (mod g), (g+2)^o = 1 (mod g), hence s = (g+1)(g+2)^o = 1 (mod g); violations {lemma_bad}")
hyp_bad = []; nh = 0
for g in gl:
    o, s = elem_s(g); k = v2(s); m = s >> k
    if g > (80 if QUICK else 130): continue
    ok, why = hyp_P(g, k, m); nh += 1
    if not ok: hyp_bad.append((g, why))
rec("M1.2", "PASS" if not hyp_bad else "FAIL", f"T38 hypotheses H1 (residues cover <2>), H2 (saturation), H3 (g+1 | s, G=g, lcm D = s) verified separately for the elementary seed s=(g+1)(g+2)^o, k=v2(g+1), m=odd part, for {nh} values of g; failures {hyp_bad}")
bad_all = []; steps = 18 if QUICK else 30
for g in [g for g in gl if g <= (40 if QUICK else 77)]:
    o, s = elem_s(g); k = v2(s); m = s >> k
    bad, Rs, ks, gam = P_orbit(g, k, m, steps)
    x = Fr(s * s, g); xs = []
    for n in range(steps):
        xs.append(x); Dl, _ = Dcoll(Dx(x)); x = x + Dl
    if bad or any(xs[i + 3] != 4 * xs[i] for i in range(steps - 3)): bad_all.append(g)
rec("M1.3", "PASS" if not bad_all else "FAIL", f"direct orbits x0 = s^2/g (elementary s) for g<= {40 if QUICK else 77}: G(x_n)=g, x_n = s_n^2 t_n/g, D = divisors of s_n congruent 1 mod g, lcm D = s_n, and x_(n+3) = 4 x_n at every one of {steps} steps; failures {bad_all}")

# =================================================================== M2  periodic increment law
# R(x_n) = #{(a,j): a | m, 0<=j<=k_n, 2^j a = 1 mod g} - [d=1 excluded];  R(x_{n+3o}) - R(x_n) = A_g(m)
rowsM2 = []; failM2 = []
for g, mode in [(5, 0), (7, 0), (11, 0), (13, 0), (15, 1), (17, 0), (19, 0), (23, 0), (25, 0)] + ([] if QUICK else [(29, 0), (35, 0), (55, 0)]):
    o = ordmod(2, g)
    if mode == 0: _, s = elem_s(g)
    else: s = (g + 1) * (g + 2) ** o
    k = v2(s); m = s >> k
    ok, why = hyp_P(g, k, m, star=(mode == 1))
    N = 9 * o + 3; bad, Rs, ks, gam = P_orbit(g, k, m, N)
    H = {pow(2, i, g) for i in range(o)}; A = sum(1 for a in divs_of(m) if a % g in H)
    comps = N - 3 * o; viol = sum(1 for n in range(comps) if Rs[n + 3 * o] - Rs[n] != A)
    kviol = sum(1 for n in range(comps) if ks[n + 3 * o] - ks[n] != o)
    periods = comps // (3 * o)
    row = (g, o, A, comps, periods, viol, kviol, bad)
    rowsM2.append(row)
    if not ok or comps < 6 * o or viol or kviol or bad: failM2.append(row)
rec("M2.1", "PASS" if not failM2 else "FAIL", "periodic-increment law R(x_(n+3o)) - R(x_n) = A_g(m), k_(n+3o) = k_n + o, over direct orbits; rows (g, o, A_g, comparisons made, full 3o-periods compared, violations, k-violations, invariant violations): " + str(rowsM2) + ("" if not failM2 else f"  FAILED: {failM2}"))
rec("M2.2", "PASS" if all(r[3] >= 6 * r[1] for r in rowsM2) and len(rowsM2) >= 9 else "FAIL", f"nonvacuity: every tested g made >= 2 complete 3o-periods of comparisons (min comparisons / 3o = {min(r[3] / (3 * r[1]) for r in rowsM2):.1f}); g = 13, 19, 25 {'and 55 ' if not QUICK else ''}included; the test is built to FAIL when fewer than 6o comparisons are available")
# counting identity R = #{(a,j)} - 1 for an independent construction (no orbit)
bad = 0
for g in (5, 7, 11, 13, 19, 25):
    o, s = elem_s(g); k = v2(s); m = s >> k; dm = divs_of(m)
    for kk in range(k, k + 2 * o + 1):
        R1 = sum(1 for a in dm for j in range(kk + 1) if (2 ** j * a) % g == 1) - 1
        R2 = len([d for d in divs_of(2 ** kk * m) if d >= 2 and d % g == 1])
        if R1 != R2: bad += 1
rec("M2.3", "PASS" if bad == 0 else "FAIL", f"counting identity R = #{{(a,j): a | m, 0<=j<=k, 2^j a = 1 (mod g)}} - 1 (the proof of the law) checked against brute-force divisor enumeration for 6 values of g and 2o+1 values of k each; violations {bad}")

# =================================================================== M3  gamma-framework and persistent-G classification
POOL = []
def pool_states():
    if POOL: return POOL
    for gg in (2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24):
        for b in [b for b in range(1, gg + 1) if gg % b == 0]:
            for a in range(1, 700 if QUICK else 2500):
                if gcd(a, b) != 1: continue
                T = Dset(a, b)
                if T and Gof(T) == gg: POOL.append(Fr(a, b))
    random.shuffle(POOL); del POOL[(300 if QUICK else 1200):]
    return POOL
nstep = nprs = bad_int = bad_rec = bad_adv = bad_col = 0
for x0 in pool_states():
    x = x0
    for _ in range(5):
        T = Dx(x); g = Gof(T)
        if g == 1: break
        L = Lof(T); y = int(g * x)
        if y % (L * L): bad_int += 1; break
        gam = y // (L * L)
        # collapse criterion: x integer divisible by 4  <=>  4g | gamma L^2
        coll = (x.denominator == 1 and x.numerator % 4 == 0)
        if coll != (y % (4 * g) == 0): bad_col += 1
        D, _ = Dcoll(T); x2 = x + D; T2 = Dx(x2); g2 = Gof(T2); nstep += 1
        if g2 == g:
            L2 = Lof(T2); r, rem = divmod(L2, L)
            y2 = int(g * x2)
            if rem or y2 % (L2 * L2): bad_rec += 1; break
            gam2 = y2 // (L2 * L2); nprs += 1
            if (gam + 1) != gam2 * r * r: bad_rec += 1
            if g % 2 == 0 and r % 2 == 1 and (gam2 - gam - 1) % 8: bad_adv += 1
            if g % 3 == 0 and r % 3 != 0 and (gam2 - gam - 1) % 3: bad_adv += 1
            if g % 6 == 0 and gcd(r, 6) == 1 and (gam2 - gam - 1) % 24: bad_adv += 1
        x = x2
rec("M3.1", "PASS" if bad_int == 0 and bad_col == 0 else "FAIL", f"gamma = y/L^2 (y = g x) is an integer, and 'x integer divisible by 4' <=> 4g | gamma L^2, on {nstep} steps from the pool (G>1 states); violations {bad_int}/{bad_col}")
rec("M3.2", "PASS" if bad_rec == 0 and nprs > 0 else "FAIL", f"gamma recurrence gamma' = (gamma+1)/r^2, r = L'/L integer, at every G-preserving step (plateau r=1 included): {nprs} steps; violations {bad_rec}")
rec("M3.3", "PASS" if bad_adv == 0 else "FAIL", f"congruence advance: g even => gamma' = gamma+1 (mod 8); 3 | g and 3 not| r => gamma' = gamma+1 (mod 3); 6 | g and gcd(r,6)=1 => gamma' = gamma+1 (mod 24); violations {bad_adv} on the same preserving steps")
# adversarial: if g | gamma (x integer), every prime q | L has q^2 | numerator, q in D(x), so G | q-1
bad = n = 0
for g in (2, 4, 6, 8, 12, 24):
    for _ in range(300 if QUICK else 1500):
        w = random.choice([1, 1, 2, 3, 5, 7, 9]); L = 1
        for q in random.sample([3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 61, 73, 97, 241], random.randint(1, 3)): L *= q ** random.randint(1, 2)
        if gcd(L, 2 * g) != 1: continue
        x = Fr(g * w * L * L, g)                     # gamma = g w, x = w L^2 integer
        if x % 4 == 0: continue
        T = Dx(x)
        if not T: continue
        G = Gof(T); n += 1
        for q in factor(L):
            if (q - 1) % G: bad += 1
rec("M3.4", "PASS" if bad == 0 and n > 0 else "FAIL", f"adversarial lemma: if g | gamma (so x is an integer) every prime q of L lies in D(x), hence G(x) | q-1; {n} random integer states, violations {bad}")
# descent inequality of Theorem E
bad = 0
for g in (2, 4, 6, 8, 12, 24):
    M = 4 * g
    for a in range(1, 3000):
        if not ((a + M - 1) < (g + 1) ** 2 * a): bad += 1
rec("M3.5", "PASS" if bad == 0 else "FAIL", f"descent inequality of Theorem E: a' <= (a+M-1)/(g+1)^2 < a for all a>=1, M=4g, g in {{2,4,6,8,12,24}} (equivalent to (g-1)^2 > 0); violations {bad}")
# empirical collapse for g | 24
cap = 150 if QUICK else 300; mx = {}
for gg in (4, 8, 12, 24):
    best = 0; tot = 0
    for b in [b for b in range(1, gg + 1) if gg % b == 0]:
        for a in range(1, 4000 if QUICK else 12000):
            if gcd(a, b) != 1: continue
            T = Dset(a, b)
            if not T or Gof(T) != gg: continue
            tot += 1; x = Fr(a, b); T = Dx(x); n = 0
            while n < cap:
                Dl, _ = Dcoll(T); x += Dl; T = Dx(x); n += 1
                if Gof(T) != gg: break
            best = max(best, n)
    mx[gg] = (tot, best)
rec("M3.6", "DATA", f"natural seeds with G in {{4,8,12,24}}: (count, longest stay at that G within {cap} steps) = {mx}; every one eventually left G (consistent with Theorem E, which proves it)")
# P* instances: odd g with 3 | g
def find_Pstar(g):
    o = ordmod(2, g); s = (g + 1) * (g + 2) ** o; k = v2(s); m = s >> k
    if hyp_P(g, k, m, star=True)[0]: return ("elementary", k, m)
    H = {pow(2, i, g) for i in range(o)}
    pr = [p for p in range(3, 400) if is_prime(p) and gcd(p, g) == 1 and p % g in H]
    for kk in (2, 3, 4, 5):
        for i, p in enumerate(pr[:30]):
            for q in [1] + pr[i:i + 25]:
                if hyp_P(g, kk, p * q, star=True)[0]: return ("search", kk, p * q)
    return None
inst = {}; none = []
for g in ([15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 75, 87, 93, 99] if not QUICK else [15, 21, 33]):
    r = find_Pstar(g)
    if r: inst[g] = r
    else: none.append(g)
okP = True; sumP = {}
for g, (how, k, m) in inst.items():
    N = 60 if QUICK else 120
    bad, Rs, ks, gam = P_orbit(g, k, m, N)
    ex = Fr(2 ** (2 * k) * m * m, g); x = ex; xs = []
    for n in range(24):
        xs.append(x); Dl, _ = Dcoll(Dx(x)); x = x + Dl
    form = all(xs[i + 3] == 4 * xs[i] for i in range(21))
    sumP[g] = (how, k, m if m < 10 ** 9 else "big", bad, form, max(gam))
    if bad or not form: okP = False
rec("M3.7", "PASS" if okP and 15 in inst else "FAIL", f"THEOREM P* instances with 3 | g (gcd(g,6)>1): (how, k, m, violations, x_(n+3)=4x_n, max gamma) = {sumP}; G(x_n) = g > 1 for every n, though gcd(g,6) = 3")
rec("M3.8", "DATA", f"odd g with 3 | g for which no P* instance was found in the bounded search (this is NOT a non-existence result): {none}")
seed15 = Fr(4 * 323) ** 2 / 15
x = seed15; G15 = set()
for n in range(200):
    T = Dx(x); G15.add(Gof(T)); Dl, _ = Dcoll(T); x += Dl
rec("M3.9", "PASS" if G15 == {15} else "FAIL", f"g=15 seed s = 4*17*19 = 1292, x0 = s^2/15: G = {sorted(G15)} for 200 consecutive steps (found by a plain search, before the elementary form was known)")
rec("M3.10", "OPEN", "Even g > 24 (g = 10, 16, 20, 28, ...), and odd g with 3 | g not covered by P* (9, 21, 27, ...): neither a persistent orbit nor a proof of collapse. Theorem E proves collapse only for g | 24; natural seeds with g = 20, 45 survived 64 and 44 steps and then collapsed (DATA).")

# =================================================================== M4  asymptotic classification
# bounded-gamma lemma on persistent orbits
mxg = {}
for g, mode in [(5, 0), (7, 0), (11, 0), (15, 1), (13, 0)]:
    o = ordmod(2, g); s = (g + 1) * (g + 2) ** o; k = v2(s); m = s >> k
    bad, Rs, ks, gam = P_orbit(g, k, m, 40, check=False); mxg[g] = max(gam)
rec("M4.1", "PASS" if all(v <= 3 for v in mxg.values()) else "FAIL", f"bounded-gamma lemma (T47: along a persistent orbit gamma_n <= 2M eventually, M = collapse modulus) and the exact value gamma_n in {{1,2,3}} on the P_g / P*_g orbits: max gamma = {mxg}")
NC = 150 if QUICK else 400; Nst = 120 if QUICK else 300
seeds = [Fr(a, b) for b in (1, 2, 3, 4, 5, 6, 7, 9) for a in range(2, 500 if QUICK else 1500) if gcd(a, b) == 1 and Dset(a, b)]
random.shuffle(seeds); seeds = seeds[:NC]; entry = []; notyet = []; persist = 0
for x0 in seeds:
    x = x0; xs = []; Gs = []
    for _ in range(Nst):
        T = Dx(x); xs.append(x); Gs.append(Gof(T)); Dl, _ = Dcoll(T); x = x + Dl
    n0 = None
    for n in range(Nst - 4, -1, -1):
        if xs[n + 3] == 4 * xs[n]: n0 = n
        else: break
    if n0 is None: notyet.append(str(x0))
    else: entry.append(n0)
    if Gs[-1] > 1: persist += 1
entry.sort()
rec("M4.2", "DATA", f"x_(n+3)=4x_n eventually? {len(seeds)} natural seeds (b in 1..9), {Nst} steps: {len(entry)} already in scaling form at the end (entry step: median {entry[len(entry)//2]}, max {entry[-1]}), not yet: {len(notyet)} {notyet[:4]}; orbits ending with G>1: {persist}")
dsg = {}
for g, (how, k, m) in list(inst.items())[:3]:
    bad, Rs, ks, gam = P_orbit(g, k, m, 30, check=False); dsg[g] = sorted(set(gam))
rec("M4.3", "DATA", f"gamma-value sets in P*_g orbits: {dsg} (cycle 1,2,3 forced because t -> squarefree(t+1) is absorbed whenever the square is a divisor congruent 1 mod g)")
rec("M4.4", "OPEN", "M4a. For every realised x0 there is n0 with x_(n+3) = 4 x_n for n >= n0. PROVED when G_inf = 1 (v005 T32) and inside P_g, P*_g; OPEN in general. A counterexample would be a persistent orbit in which some prime square dividing gamma+1 is NOT absorbed (not congruent 1 modulo g), so the gamma-cycle differs from 1,2,3.")
rec("M4.5", "OPEN", "M4b (stronger). Every orbit is eventually of the form x = s^2 t/g, t in {1,2,3}. Not implied by M4a: a different persistent regime could also have a three-step 4-fold scaling.")
print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL"); sys.exit(0 if NFAIL == 0 else 1)
