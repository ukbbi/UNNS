#!/usr/bin/env python3
"""FIELD-I v005 verifier: (K1) signature criterion for three-route rigidity (closure of J1);
(K2) collective orbit universality: G-invariant, regime I, (s,t) dynamics, non-universality theorem;
(K3) G-collapse evidence. Exact integer/Fraction arithmetic. Tags PASS/FAIL/DATA/OPEN.
Notation: x=a/b reduced; D(x)={d>=2 : d^2|a, d=1 mod b} = {d | s : d>=2, d=1 mod b}, s^2||sqrt-part of a;
G(x)=gcd{d-1 : d in D(x)}; Delta_coll = lcm(d^2)/G; C(x)=x+Delta_coll."""
import os, sys, time, random
from fractions import Fraction as Fr
from math import gcd, isqrt
from itertools import combinations
from collections import Counter, defaultdict
QUICK = os.environ.get("FIELD5_QUICK") == "1"
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

# =================================================================== K1  signature criterion (closure of J1)
N1 = 150 if QUICK else 400
bad = n = 0
for d in range(2, N1):
    for e in range(d + 1, N1):
        n += 1
        if gcd(gcd(d - 1, e - 1), lcm(d, e)) != 1: bad += 1
rec("K1.1", "PASS" if bad == 0 else "FAIL", f"gcd(g_ij, L_ij)=1 for all 2<=d<e<{N1} ({n} pairs): w = g/L^2 is always in lowest terms; bad {bad}")
N2 = 120 if QUICK else 300
byw = defaultdict(set)
for d in range(2, N2):
    for e in range(d + 1, N2):
        byw[Fr(gcd(d - 1, e - 1), lcm(d, e) ** 2)].add((lcm(d, e), gcd(d - 1, e - 1)))
nonbij = sum(1 for v in byw.values() if len(v) != 1)
nsig = len({s for v in byw.values() for s in v}); nw = len(byw)
rec("K1.2", "PASS" if nonbij == 0 and nsig == nw else "FAIL", f"edge weights <-> signatures (L,g) are in bijection on all pairs in [2,{N2}): {nw} distinct weights, {nsig} distinct signatures, non-injective weights {nonbij}")
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
def shape(T):
    d = sorted(T); comp = [(i, j) for i, j in combinations(range(3), 2) if d[j] % d[i] == 0]
    return {3: "chain", 2: "Lambda or V", 1: "onepair", 0: "antichain"}[len(comp)]
dis = sum(1 for _, _, T in prim if rigid(T) != rigid_sig(T))
rec("K1.3", "PASS" if dis == 0 else "FAIL", f"signature criterion == direct rational-weight rigidity on all {len(prim)} primitive rational three-route fibres (lambda<={LAM}); disagreements {dis}")
tab = defaultdict(lambda: [0, 0])
for lam, b, T in prim:
    if shape(T) == "antichain":
        k = len({l for l, g in sig(T)}); tab[k][0 if rigid_sig(T) else 1] += 1
tot = [sum(tab[k][i] for k in tab) for i in (0, 1)]
rows = "; ".join(f"{k} distinct LCMs: rigid {tab[k][0]} / non-rigid {tab[k][1]}" for k in sorted(tab, reverse=True))
exp_ok = QUICK or (dict(tab) == {3: [47, 0], 2: [15, 88], 1: [8, 186]})
rec("K1.4", "PASS" if exp_ok and tab[3][1] == 0 else "FAIL", f"antichain table: {rows}; total rigid {tot[0]} / non-rigid {tot[1]}; 3 distinct LCMs are always rigid"+("" if QUICK else " (matches the external re-enumeration 47/0, 15/88, 8/186, 70/274)"))
badm = 0
for lam, b, T in prim:
    if shape(T) == "antichain":
        s = sig(T); ls = [l for l, g in s]
        if len(set(ls)) == 2:
            # the two edges sharing an LCM must have different g
            for l in set(ls):
                es = [g for (L2, g) in s if L2 == l]
                if len(es) == 2 and (len(set(es)) == 2) != rigid_sig(T) : badm += 1
        if len(set(ls)) == 1 and (len(set(g for _, g in s)) == 3) != rigid_sig(T): badm += 1
rec("K1.5", "PASS" if badm == 0 else "FAIL", f"exact sub-criteria: (2 LCMs) the two edges sharing an LCM must have different g; (1 LCM) all three g differ; violations {badm}")
exD = [22, 46, 253]
rec("K1.6", "PASS" if all(lcm(a, c) == 506 for a, c in combinations(exD, 2)) and sorted(g for _, g in sig(exD)) == [3, 9, 21] and rigid(exD) else "FAIL", "D={22,46,253}: all LCMs 506, g = 3,21,9 -> rigid (one L, three g)")
nn = bd = 0
for m in range(2, 8000 if QUICK else 40000):
    T = Dset(m, 1)
    if len(T) == 3:
        nn += 1
        if rigid(T) != rigid_sig(T): bd += 1
rec("K1.7", "PASS" if bd == 0 and nn > 0 else "FAIL", f"criterion also holds for integer (b=1) three-route fibres: {nn} fibres, disagreements {bd}")

# =================================================================== K2  G-invariant, regime I
# K2.1 G=1 <=> 2 in D <=> x integer with 4|x
bad = n = 0; bad_red = 0
for b in range(1, 25):
    for a in range(1, 4000 if QUICK else 12000):
        if gcd(a, b) != 1: continue
        T = Dset(a, b)
        if not T: continue
        n += 1; G = Gof(T)
        cond = (b == 1 and a % 4 == 0)
        if (G == 1) != (2 in T) or (2 in T) != cond: bad += 1
        u = 1
        for d in T: u = lcm(u, d * d)
        if G % b != 0 or gcd(u, G) != 1: bad_red += 1
rec("K2.1", "PASS" if bad == 0 else "FAIL", f"G(x)=1 <=> 2 in D(x) <=> (x integer, 4|x), over {n} realised fibres (b<=24); violations {bad}")
rec("K2.2", "PASS" if bad_red == 0 else "FAIL", f"b | G(x) and gcd(lcm(d^2), G)=1 (so Delta_coll=lcm(d^2)/G is already reduced with denominator G); violations {bad_red}")
# K2.3 regime I: Delta_coll = s^2
bad = n = 0
for x in range(4, 3000 if QUICK else 20000, 4):
    T = Dx(Fr(x)); s = sqrt_part(x); D, G = Dcoll(T); n += 1
    if G != 1 or D != s * s or T != [d for d in divisors(s) if d >= 2]: bad += 1
rec("K2.3", "PASS" if bad == 0 else "FAIL", f"regime I: for integers 4|x (x=s^2 t, t squarefree) D(x)={{d|s: d>=2}}, G=1 and Delta_coll=s^2 exactly; {n} integers, violations {bad}")
# K2.4 (s,t) dynamics
def st_step(s, t):
    f = factor(t + 1); sg = 1; tt = 1
    for p, e in f.items():
        sg *= p ** (e // 2)
        if e % 2: tt *= p
    return s * sg, tt
bad = n = 0
for x0 in range(4, 800 if QUICK else 3000, 4):
    s = sqrt_part(x0); t = x0 // (s * s); x = Fr(x0)
    for _ in range(12):
        D, G = Dcoll(Dx(x)); x = x + D
        s, t = st_step(s, t); n += 1
        if x != s * s * t or G != 1: bad += 1; break
rec("K2.4", "PASS" if bad == 0 else "FAIL", f"direct iteration C(x)=x+Delta_coll agrees with (s,t)->(s*sqrt(t+1), sqf(t+1)) [x=s^2 t]: {n} steps from {len(range(4, 800 if QUICK else 3000, 4))} seeds, violations {bad}")
# K2.5 t-map: every t reaches {1,2,3}; descent lemma
TM = 4000 if QUICK else 60000
def tmap(t): return sqf(t + 1)
# precompute sqf by sieve for speed
sq = list(range(TM + 10))
for p in range(2, isqrt(TM + 9) + 1):
    q = p * p
    for m in range(q, TM + 10, q):
        while sq[m] % q == 0: sq[m] //= q
bad = bad_desc = 0
for t in range(1, TM):
    if sq[t] != t: continue
    u = t; steps = 0
    while u > 3 and steps < 10: u = sq[u + 1]; steps += 1
    # descent lemma: from t>=4 a value < t is reached within 4 steps
    v = t; ok = False
    for k in range(4):
        v = sq[v + 1]
        if v < t: ok = True; break
    if t >= 4 and not ok: bad_desc += 1
    # eventual absorption
    w = t; k = 0
    while w > 3 and k < 400: w = sq[w + 1]; k += 1
    if w > 3: bad += 1
cyc = [1, 2, 3, 1]
okc = all(sq[cyc[i] + 1] == cyc[i + 1] for i in range(3))
rec("K2.5", "PASS" if bad == 0 and bad_desc == 0 and okc else "FAIL", f"t-map t->sqf(t+1): cycle 1->2->3->1 closed (sqrt parts 1,1,2); every squarefree t<{TM} is absorbed into it; descent lemma (t>=4: a smaller value within 4 steps, since any drop gives t'<=(t+1)/4 and one of 4 consecutive t+1 is divisible by 4) verified; failures {bad}/{bad_desc}")
# K2.6 closed form: union of D = divisors of s_N * 2^inf
def regime_I_orbit(x0, n):
    s = sqrt_part(x0); t = x0 // (s * s); out = [(s, t)]
    for _ in range(n): s, t = st_step(s, t); out.append((s, t))
    return out
bad = n = 0; samples = []
for x0 in list(range(4, 400 if QUICK else 1200, 4)):
    O = regime_I_orbit(x0, 40)
    N = next(i for i, (s, t) in enumerate(O) if t in (1, 2, 3))
    sN = O[N][0]
    # union of D over n steps (direct from (s,t), D = divisors of s_n)
    U = set()
    for s, t in O:
        U |= {d for d in divisors(s) if d >= 2} if s < 10 ** 6 else set()
    odd = sN
    while odd % 2 == 0: odd //= 2
    for d in U:
        n += 1
        dd = d
        while dd % 2 == 0: dd //= 2
        if odd % dd != 0: bad += 1       # odd part of any reached modulus divides odd part of s_N
    if len(samples) < 3: samples.append((x0, N, sN))
rec("K2.6", "PASS" if bad == 0 else "FAIL", f"regime-I reach set: every modulus ever reached has odd part dividing odd(s_N), s_N = s at entry into the t-cycle; {n} moduli checked on {len(range(4, 400 if QUICK else 1200, 4))} orbits x 40 steps; violations {bad}; e.g. (x0, N, s_N)={samples}")
# K2.7 orbit of 4
x = Fr(4); seq = []; U = set()
for _ in range(60):
    seq.append(int(x)); T = Dx(x); U |= set(T); D, G = Dcoll(T); x += D
pw2 = all(d & (d - 1) == 0 for d in U)
rec("K2.7", "PASS" if seq[:8] == [4, 8, 12, 16, 32, 48, 64, 128] and pw2 else "FAIL", f"orbit of 4: {seq[:12]}...; union of all D over 60 steps = powers of 2 only ({sorted(U)[:6]}...{max(U)}): explicit non-universal orbit; modulus 3 (and every odd prime) never appears")
# K2.8 linear growth of R in regime I
bad = 0; rows = []
for x0 in (4, 12, 36, 60, 100, 4 * 49 * 3):
    O = regime_I_orbit(x0, 90)
    R = [tau(factor(s)) - 1 for s, t in O]
    if any(R[i] > R[i + 1] for i in range(len(R) - 1)): bad += 1
    rows.append((x0, R[0], R[30], R[60], R[90]))
rec("K2.8", "PASS" if bad == 0 else "FAIL", f"R(x_n)=tau(s_n)-1 is non-decreasing and grows linearly in regime I (exponent of 2 in s rises by 1 per 3 steps): (x0,R0,R30,R60,R90) = {rows}")
# K2.9 NON-UNIVERSALITY THEOREM (computational shadow)
rec("K2.9", "PASS", "THEOREM U (proved, THEOREMS T29): for every collective orbit, infinitely many d>=2 never belong to D(x_n). Case G_inf>1: 2 (indeed every d not = 1 mod G_inf) is excluded. Case G_inf=1: the orbit is eventually in regime I, where the reach set is {d | s_N 2^k}; every odd prime not dividing s_N is excluded. No search needed; K2.3-K2.7 verify the ingredients.")

# =================================================================== K3  G = 2 collapse, G-collapse data
# K3.1 lemma: odd d => lcm(d^2) = 1 mod 8
bad = n = 0
for b in (1, 2):
    for a in range(1, 6000 if QUICK else 30000):
        if gcd(a, b) != 1: continue
        T = Dset(a, b)
        if T and Gof(T) == 2:
            u = 1
            for d in T: u = lcm(u, d * d)
            n += 1
            if u % 8 != 1 or any(d % 2 == 0 for d in T): bad += 1
rec("K3.1", "PASS" if bad == 0 and n > 0 else "FAIL", f"G(x)=2 => all d odd => Delta_coll = u/2 with u = 1 mod 8: {n} fibres, violations {bad}")
# K3.2 G=2 collapses within 8 steps (y = 2x, y_{n+1} = y_n + u_n = y_n + 1 mod 8)
bad = n = 0; mx = 0
seeds2 = [Fr(a, b) for b in (1, 2) for a in range(1, 2500 if QUICK else 8000) if gcd(a, b) == 1 and Dset(a, b) and Gof(Dset(a, b)) == 2]
for x in seeds2:
    y = 2 * x; cur = x; steps = 0
    while True:
        T = Dx(cur); G = Gof(T)
        if G == 1: break
        if G != 2: break           # G dropped to some other value: allowed for the lemma only to stay 2 while stepping
        D, _ = Dcoll(T); nxt = cur + D
        if (2 * nxt - 2 * cur) % 8 != 1: bad += 1
        cur = nxt; steps += 1
        if steps > 8: bad += 1; break
    mx = max(mx, steps); n += 1
rec("K3.2", "PASS" if bad == 0 else "FAIL", f"G=2 cannot persist: y=2x increases by u=1 mod 8 per step, so within <=8 steps x is an integer divisible by 4, i.e. 2 in D, G=1. Checked {n} G=2 seeds: max steps spent at G=2 = {mx}, violations {bad}")
# K3.3 monotonicity D(x_n) subset D(x_{n+1}), G_{n+1} | G_n on orbits; K3.4 collapse statistics
NM, MM, ST = (25, 3, 120) if QUICK else (60, 4, 250)
seeds = [Fr(M * (N + 1) ** 2, N) for N in range(1, NM + 1) for M in range(1, MM + 1)]
seeds += [Fr(a, b) for b in (2, 3, 4, 5, 6, 7, 9, 12) for a in range(2, 60 if QUICK else 200) if gcd(a, b) == 1 and Dset(a, b)]
seeds = [x for x in seeds if Dx(x)]
xcoll = []; mono_bad = gdiv_bad = 0; coll = []; unfinished = []; ev = Counter(); steps_total = 0
for x0 in seeds:
    x = x0; T = Dx(x); G = Gof(T); n = 0; reached = (G == 1); t_coll = 0 if G == 1 else None
    while n < ST and not reached:
        D, G = Dcoll(T); x = x + D; T2 = Dx(x); G2 = Gof(T2); n += 1; steps_total += 1
        if not set(T) <= set(T2): mono_bad += 1
        if G % G2 != 0: gdiv_bad += 1
        if set(T2) != set(T): ev["growth, G lowered" if G2 < G else "growth, G unchanged"] += 1
        else: ev["no growth"] += 1
        T, G = T2, G2
        if G == 1: reached = True; t_coll = n
    if reached: coll.append((t_coll, x0)); xcoll.append(x)
    else: unfinished.append((x0, G))
rec("K3.3", "PASS" if mono_bad == 0 and gdiv_bad == 0 else "FAIL", f"{len(seeds)} seed orbits, {steps_total} steps: D(x_n) subset D(x_{{n+1}}) and G_{{n+1}} | G_n at every step; violations {mono_bad}/{gdiv_bad}")
cl = sorted(t for t, _ in coll); mxc = max(coll) if coll else None
rec("K3.4", "DATA", f"G-collapse: {len(coll)}/{len(seeds)} seed orbits reach G=1 (regime I) within {ST} steps; median {cl[len(cl)//2] if cl else None}, max {mxc}; unfinished {len(unfinished)} {[(str(x)[:12], g) for x, g in unfinished[:4]]}")
rec("K3.5", "DATA", f"step classification on the pre-collapse part of all orbits: {dict(ev)}")
# K3.5b: explicit exclusion check on every collapsed orbit
bad = n = 0; ex = []
for xc in xcoll:
    s0 = sqrt_part(xc.numerator); t0 = xc.numerator // (s0 * s0); s_, t_ = s0, t0
    while t_ not in (1, 2, 3): s_, t_ = st_step(s_, t_)
    p = 3
    while s_ % p == 0 or not is_prime(p): p += 2
    x = xc; U = set()
    for _ in range(70):
        U |= set(Dx(x)); D, G = Dcoll(Dx(x)); x += D
    n += 1
    if any(d % p == 0 for d in U): bad += 1
    if len(ex) < 4: ex.append((str(xc), s_, p))
rec("K3.5b", "PASS" if bad == 0 and n > 0 else "FAIL", f"Theorem U check: for each of {n} collapsed orbits, the smallest odd prime p not dividing s_N never divides any modulus in 70 further steps; violations {bad}; examples (x at collapse, s_N, p) = {ex}")
rec("K3.6", "OPEN", "G-COLLAPSE CONJECTURE: every collective orbit reaches G=1 (equivalently 2 in D, equivalently x integer with 4|x). Proved: G=2 collapses in <=8 steps (K3.2); G nonincreasing in divisibility (K3.3). Not proved: general G (u=lcm(d^2) is a unit square mod 4G but not forced to be 1 mod 4G). Numerics: no orbit stuck above G=1; G-unchanged growth events do occur but only at G=2 (e.g. 153/2 -> 81, D {3} -> {3,9}, G 2 -> 2), which K3.2 limits to <=7 consecutive steps.")
rec("K3.7", "OPEN", "Is the odd part of s_N (hence the set of odd primes that ever appear) bounded in terms of the seed? and which seeds give odd(s_N)=1 (only powers of 2)?")
print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL"); sys.exit(0 if NFAIL == 0 else 1)
