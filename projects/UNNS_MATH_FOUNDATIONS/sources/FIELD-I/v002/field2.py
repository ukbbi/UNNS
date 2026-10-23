#!/usr/bin/env python3
"""FIELD-I v002 verifier: Intrinsic Relational Selection (F6-F9).
Exact arithmetic (fractions.Fraction / integers). Status tags: PASS, FAIL, DATA, OPEN.
Rule under study (2017 fixed-nest sequence): occurrence r=(M,N), M,N>=1, d=N+1,
value v(r)=M*d^2/N, fixed-nest successor F(r)=(M+1,N).  No other rule is assumed.
"""
import os, sys, time
from fractions import Fraction as Fr
from math import gcd, isqrt, floor
from itertools import combinations, permutations
from collections import Counter, defaultdict

QUICK = os.environ.get("FIELD2_QUICK") == "1"
X0 = 800 if QUICK else 3000          # box bound for the independent construction
A0, B0 = (2500, 14) if QUICK else (8000, 30)   # corpus bounds for formula-based statistics
T0 = time.time()
NFAIL = 0
def rec(tag, status, msg):
    global NFAIL
    if status == "FAIL": NFAIL += 1
    print(f"{status} {tag}: {msg}", flush=True)

def lcm(a, b): return a // gcd(a, b) * b
def delta(d, e): return Fr(lcm(d, e) ** 2, gcd(d - 1, e - 1))      # claimed first-rendezvous increment
def latlcm(fs):                                                       # lcm of lattices fZ (reduced fractions)
    L, G = 1, 0
    for f in fs: L = lcm(L, f.numerator); G = gcd(G, f.denominator)
    return Fr(L, G)
def Dset(a, b):                                                       # T1: d>=2, d^2|a, d=1 mod b
    return [d for d in range(1 + b, isqrt(a) + 1, b) if a % (d * d) == 0]
def Dx(x): return Dset(x.numerator, x.denominator)

# ------------------------------------------------------------------ independent construction (box)
def build_box(X):
    fib = defaultdict(list)
    for N in range(1, X + 1):
        d = N + 1; step = Fr(d * d, N); M = 1
        while M * step <= X:
            fib[M * step].append((M, N)); M += 1
    return fib
BOX = build_box(X0)
BOXF = {x: sorted(v, key=lambda t: t[1]) for x, v in BOX.items() if len(v) >= 2}
rec("F0.1", "DATA", f"box X0={X0}: {len(BOX)} values, {len(BOXF)} fibres with R>=2, {sum(len(v)*(len(v)-1)//2 for v in BOXF.values())} pairs")

bad = 0
for x, occ in BOX.items():
    if sorted(n + 1 for _, n in occ) != Dx(x): bad += 1
rec("F0.2", "PASS" if bad == 0 else "FAIL", f"T1 formula == box brute force on all {len(BOX)} values <= {X0}; mismatches {bad}")
bad = 0; cnt = 0
for b in range(1, 9):
    for a in range(1, X0 * b + 1):
        if gcd(a, b) != 1: continue
        if Dset(a, b):
            cnt += 1
            if Fr(a, b) not in BOX: bad += 1
rec("F0.3", "PASS" if bad == 0 else "FAIL", f"every formula-realisable a/b (b<=8, value<={X0}) occurs in the box ({cnt} values); misses {bad}")

# ------------------------------------------------------------------ brute-force rendezvous (integer sets)
def brute_first_common(x, routes, limit_mult=2):
    LN = 1
    for _, N in routes: LN = lcm(LN, N)
    cap = (limit_mult * x.numerator * LN) // x.denominator       # floor(limit*x*LN)
    sets = []
    for (M, N) in routes:
        unit = (N + 1) ** 2 * (LN // N)
        sets.append({m * unit for m in range(M + 1, cap // unit + 1)})
    com = set.intersection(*sets)
    return Fr(min(com), LN) if com else None

# ---------------------------------------------------------------- F6: rendezvous spectrum
bad = 0; npair = 0; nonint = 0
for x, occ in BOXF.items():
    for r, s in combinations(occ, 2):
        npair += 1
        y = brute_first_common(x, [r, s], 2)
        d, e = r[1] + 1, s[1] + 1
        if y is None or y - x != delta(d, e): bad += 1; continue
        h = x / (y - x)
        if h.denominator != 1 or h < 1: bad += 1
rec("F6.1", "PASS" if bad == 0 else "FAIL", f"pairwise first rendezvous: brute-force search (window <=2x) == L^2/g, and x/Delta is an integer >=1; {npair} pairs, bad {bad}")

bad = 0; ncol = 0
for x, occ in BOXF.items():
    ds = [n + 1 for _, n in occ]
    D_coll = Fr(1); L = 1; G = 0
    for d in ds: L = lcm(L, d * d); G = gcd(G, d - 1)
    D_coll = Fr(L, G)
    y = brute_first_common(x, occ, 2)
    pw = latlcm([delta(d, e) for d, e in combinations(ds, 2)])
    ncol += 1
    if y is None or y - x != D_coll or pw != D_coll or (x / D_coll).denominator != 1: bad += 1
rec("F6.2", "PASS" if bad == 0 else "FAIL", f"collective first rendezvous: brute force == lcm(d_i^2)/gcd(N_i) == lattice-lcm of the pairwise Deltas (coherence); x/Delta_coll integer; {ncol} fibres, bad {bad}")

# corpus (formula based; validated against box by F0.2)
CORP = {}
for b in range(1, B0 + 1):
    for a in range(1, A0 + 1):
        if gcd(a, b) != 1: continue
        ds = Dset(a, b)
        if len(ds) >= 2: CORP[Fr(a, b)] = ds
rec("F0.4", "DATA", f"corpus a<={A0}, b<={B0}: {len(CORP)} fibres with R>=2; max R = {max(len(v) for v in CORP.values())}")

def hmat(x, ds):
    R = len(ds); W = [[0] * R for _ in range(R)]
    for i, j in combinations(range(R), 2):
        h = x / delta(ds[i], ds[j]); assert h.denominator == 1
        W[i][j] = W[j][i] = int(h)
    return W
def gcd_all(v):
    g = 0
    for t in v: g = gcd(g, t)
    return g
bad = 0; GAM = {}; SPEC = {}; W_ = {}
for x, ds in CORP.items():
    W = hmat(x, ds); W_[x] = W
    H = tuple(sorted(W[i][j] for i, j in combinations(range(len(ds)), 2)))
    SPEC[x] = H; GAM[x] = gcd_all(H)
    L = 1; G = 0
    for d in ds: L = lcm(L, d * d); G = gcd(G, d - 1)
    if x / Fr(L, G) != GAM[x]: bad += 1
rec("F6.3", "PASS" if bad == 0 else "FAIL", f"h_coll(x) = x/Delta_coll = gcd of the pairwise indices, i.e. gcd H(x); {len(CORP)} fibres, bad {bad}")

ex = Fr(2025, 2)
rec("F6.4", "PASS" if SPEC[ex] == (1, 1, 1, 2, 2, 2, 9, 9, 9, 25) and GAM[ex] == 1 else "FAIL",
    f"x=2025/2, D={CORP[ex]}: H={SPEC[ex]}, gcd H = {GAM[ex]}")

# every positive integer is a pair index (anchor construction m=36h, d=2,3)
okh = all(Fr(36 * h, 1) / delta(2, 3) == h and 36 * h % 4 == 0 and 36 * h % 9 == 0 for h in range(1, 3000))
rec("F6.5", "PASS" if okh else "FAIL", "every h in 1..2999 occurs as a pair index: x=36h, pair (d,d')=(2,3), Delta=36 (hence all positive integers)")
gs = sorted(set(GAM.values()))
miss = [g for g in range(1, 41) if g not in gs]
rec("F6.6", "DATA", f"collective indices gcd H observed in corpus (<=40): {[g for g in range(1,41) if g in gs]}; not observed: {miss}")
rec("F6.6b", "OPEN", "characterise exactly which integers gamma = gcd H(x) occur (pair indices are all of Z>0; collective ones are not obviously)")

# information ladder: classes in the corpus
cl_R = len({len(CORP[x]) for x in CORP})
cl_RG = len({(len(CORP[x]), GAM[x]) for x in CORP})
cl_H = len(set(SPEC.values()))
rec("F6.7", "DATA", f"classification ladder over {len(CORP)} fibres: #R-classes={cl_R}, #(R,gamma)-classes={cl_RG}, #H-classes={cl_H}, #distinct x={len(CORP)}")
byH = defaultdict(list)
for x, H in SPEC.items(): byH[H].append(x)
rec("F6.8", "DATA", f"H(x) is coarse: {sum(1 for v in byH.values() if len(v)>1)} spectra are shared by >=2 distinct values x; largest sharing class {max(len(v) for v in byH.values())}")

# gcd correction of T4 (v001) : g in D <=> g>=2 and g = 1 (mod b)
bad = 0; n = 0
for x, ds in CORP.items():
    a, b = x.numerator, x.denominator; S = set(ds)
    for d, e in combinations(ds, 2):
        g = gcd(d, e); n += 1
        if (g in S) != (g >= 2 and (g - 1) % b == 0): bad += 1
        L = lcm(d, e)
        if (L in S) != ((g - 1) % b == 0): bad += 1
rec("F6.9", "PASS" if bad == 0 else "FAIL", f"T4 corrected: gcd(d,d') in D <=> gcd>=2 and gcd=1 mod b ; lcm in D <=> gcd = 1 mod b ; {n} pairs, bad {bad}")
D784 = Dset(784, 3)
rec("F6.9b", "PASS" if (4 in D784 and 7 in D784 and gcd(4, 7) == 1 and 1 not in D784 and 28 in D784) else "FAIL",
    f"adversarial: x=784/3, D={D784}: 4,7 in D, gcd(4,7)=1 is excluded although 1=1 mod 3, lcm 28 in D")

# ---------------------------------------------------------------- F7: observability regimes
# Regime A: value only. Pi = prod_x Sym(F(x)) is the automorphism group of (Occ, v).
okA = True
for x, occ in BOXF.items():
    R = len(occ); par = {p: p for p in combinations(range(R), 2)}
    def find(p):
        while par[p] != p: par[p] = par[par[p]]; p = par[p]
        return p
    for k in range(R - 1):
        for (i, j) in list(par):
            sw = lambda t: k + 1 if t == k else (k if t == k + 1 else t)
            q = tuple(sorted((sw(i), sw(j))))
            par[find((i, j))] = find(q)
    if len({find(p) for p in par}) != 1: okA = False
rec("F7.1", "PASS" if okA else "FAIL", "Regime A: route permutations act transitively on unordered pairs of every fibre (one orbit), so any Pi-invariant pair function is constant on a fibre")

# Regime B: (x, successor) recovers (M,N);  rigidity of (Occ,v,F)
seen = {}; bad = 0
for N in range(1, 1500):
    d = N + 1; st = Fr(d * d, N)
    if st.numerator != d * d or st.denominator != N: bad += 1
    if st in seen: bad += 1
    seen[st] = N
rec("F7.2", "PASS" if bad == 0 else "FAIL", f"step d^2/N is already reduced and injective in N (N<1500): numerator d^2, denominator N; bad {bad}")
bad = 0
for x, occ in BOX.items():
    for (M, N) in occ:
        st = Fr((N + 1) ** 2, N); x2 = x + st                      # observed (x, F(r))
        N2 = (x2 - x).denominator; M2 = x / (x2 - x)
        if (M2, N2) != (M, N): bad += 1
rec("F7.3", "PASS" if bad == 0 else "FAIL", f"Regime B: (v(r), v(F r)) recovers (M,N) exactly on all {sum(len(v) for v in BOX.values())} box occurrences; bad {bad}")
vs = {}
bad = 0
for N in range(1, 400):
    key = tuple(Fr(M * (N + 1) ** 2, N) for M in range(1, 41))
    if key in vs: bad += 1
    vs[key] = N
rec("F7.4", "PASS" if bad == 0 else "FAIL", "route value-sequences are pairwise distinct (N<400, 40 terms): (Occ, v, route-membership) is rigid; route labels are recoverable")

# Regime D: unlabelled future intersection of a pair: does (x, Delta) identify the pair?
uniq = tot = 0
for x, ds in CORP.items():
    c = Counter(delta(d, e) for d, e in combinations(ds, 2))
    for d, e in combinations(ds, 2):
        tot += 1; uniq += (c[delta(d, e)] == 1)
rec("F7.5", "DATA", f"Regime D: pair identified inside its fibre by (x,Delta): {uniq}/{tot} = {uniq/tot:.4f}")

# Regime C refined: automorphisms of the weighted rendezvous graph G(x)
def aut_count(W, cap=5000):
    R = len(W); perm = [-1] * R; used = [False] * R; cnt = 0
    def rec_(i):
        nonlocal cnt
        if cnt >= cap: return
        if i == R: cnt += 1; return
        for c in range(R):
            if used[c]: continue
            if all(W[i][j] == W[c][perm[j]] for j in range(i)):
                used[c] = True; perm[i] = c; rec_(i + 1); used[c] = False
    rec_(0); return cnt
AUT = {}
for x, W in W_.items(): AUT[x] = aut_count(W)
byR = defaultdict(lambda: [0, 0])
for x, ds in CORP.items():
    byR[len(ds)][0] += 1; byR[len(ds)][1] += (AUT[x] == 1)
rec("F7.6", "DATA", "rigid fibres (Aut of weighted rendezvous graph trivial) by R: " +
    "; ".join(f"R={R}: {v[1]}/{v[0]}" for R, v in sorted(byR.items())))
r2 = all(AUT[x] == 2 for x in CORP if len(CORP[x]) == 2)
rec("F7.7", "PASS" if r2 else "FAIL", "R=2: Aut(G)=Z2 always, so no label-blind structure can distinguish the two routes of a two-route fibre")
tot = sum(v[0] for v in byR.values()); rig = sum(v[1] for v in byR.values())
rec("F7.8", "DATA", f"overall rigid fraction {rig}/{tot} = {rig/tot:.4f} ; in rigid fibres label-blind structure individuates every route (equivalent to knowing N up to the unique structural isomorphism)")

# canonical forms: does H lose graph information?
def canon(W):
    R = len(W); best = None
    for p in permutations(range(R)):
        t = tuple(W[p[i]][p[j]] for i in range(R) for j in range(i + 1, R))
        if best is None or t < best: best = t
    return best
coll = 0; examples = []
for H, xs in byH.items():
    xs6 = [x for x in xs if len(CORP[x]) <= 6]
    if len(xs6) > 1:
        cs = {canon(W_[x]) for x in xs6}
        if len(cs) > 1:
            coll += 1
            if len(examples) < 2: examples.append((str(xs6[0]), str(xs6[1])))
rec("F7.9", "DATA", f"spectra H shared by fibres whose rendezvous graphs are NOT isomorphic (R<=6): {coll}; examples {examples}")

# ---------------------------------------------------------------- F8: operations
def fibre_N(x): return [d - 1 for d in Dx(x)]
def step(N): return Fr((N + 1) ** 2, N)
def shifted(r, s, x, i):
    d, e = r[1] + 1, s[1] + 1; D = delta(d, e)
    tr = D / step(r[1]); ts = D / step(s[1]); assert tr.denominator == 1 and ts.denominator == 1
    return (r[0] + i * int(tr), r[1]), (s[0] + i * int(ts), s[1]), x + i * D
def Dcoll(x):
    ds = Dx(x); L = 1; G = 0
    for d in ds: L = lcm(L, d * d); G = gcd(G, d - 1)
    return Fr(L, G)
OPS = {
 "star_1  (x+D)":              lambda x, r, s: x + delta(r[1] + 1, s[1] + 1),
 "star_2  (x+2D)":             lambda x, r, s: x + 2 * delta(r[1] + 1, s[1] + 1),
 "star_3  (x+3D)":             lambda x, r, s: x + 3 * delta(r[1] + 1, s[1] + 1),
 "star_L2 (x+L^2)":            lambda x, r, s: x + lcm(r[1] + 1, s[1] + 1) ** 2,
 "star_alt(j=1+minN mod 2)":   lambda x, r, s: x + (1 + min(r[1], s[1]) % 2) * delta(r[1] + 1, s[1] + 1),
 "star_pos(j=1+(M+M') mod 2)": lambda x, r, s: x + (1 + (r[0] + s[0]) % 2) * delta(r[1] + 1, s[1] + 1),
 "Y_1     (x+Dcoll)":          lambda x, r, s: x + Dcoll(x),
 "Y_2     (x+2Dcoll)":         lambda x, r, s: x + 2 * Dcoll(x),
}
EXPECT = {  # A2 symmetric, A3 common-future, A4 stationarity, A6 label-blind, A7 minimal
 "star_1  (x+D)": "PPPFP", "star_2  (x+2D)": "PPPFF", "star_3  (x+3D)": "PPPFF", "star_L2 (x+L^2)": "PPPFF",
 "star_alt(j=1+minN mod 2)": "PPPFF", "star_pos(j=1+(M+M') mod 2)": "PPFFF",
 "Y_1     (x+Dcoll)": "PPFPF", "Y_2     (x+2Dcoll)": "PPFPF"}
def in_route(y, r):  # y is a value of route r strictly after x?
    M2 = y * r[1] / (r[1] + 1) ** 2
    return M2.denominator == 1 and M2 > r[0]
# sample for speed
items = [(x, occ) for x, occ in BOXF.items()]
def evaluate(name, op):
    A2 = A3 = A4 = A7 = True; A6 = True
    for x, occ in items:
        outs = set()
        for r, s in combinations(occ, 2):
            o = op(x, r, s); outs.add(o)
            if o != op(x, s, r): A2 = False
            if not (o > x and in_route(o, r) and in_route(o, s)): A3 = False
            if o != x + delta(r[1] + 1, s[1] + 1): A7 = False
            for i in (1, 2, 3):
                r_i, s_i, y = shifted(r, s, x, i)
                if op(y, r_i, s_i) != o + (y - x): A4 = False
        if len(outs) > 1: A6 = False
    return "".join("P" if v else "F" for v in (A2, A3, A4, A6, A7))
for name, op in OPS.items():
    got = evaluate(name, op)
    rec("F8.1", "PASS" if got == EXPECT[name] else "FAIL", f"{name:30s} A2/A3/A4/A6/A7 = {got} (expected {EXPECT[name]})")
rec("F8.1n", "DATA", "axioms: A2 symmetric; A3 output is a strictly later common value of both routes; A4 stationarity (op(shifted pair) = op + shift along the pair's own rendezvous period); A6 label-blind (Pi-equivariant => depends on the fibre only); A7 minimality (first common future)")

# common-future set is exactly x + jD
bad = 0; n = 0
for x, occ in list(BOXF.items())[:400]:
    for r, s in list(combinations(occ, 2))[:3]:
        D = delta(r[1] + 1, s[1] + 1); lim = x + 6 * D
        LN = lcm(r[1], s[1]); cap = floor(lim * LN)
        sets = []
        for (M, N) in (r, s):
            unit = (N + 1) ** 2 * (LN // N); sets.append({m * unit for m in range(M, cap // unit + 1)})
        com = sorted(Fr(v, LN) for v in set.intersection(*sets))
        n += 1
        if com != [x + j * D for j in range(0, 7) if x + j * D <= lim]: bad += 1
rec("F8.2", "PASS" if bad == 0 else "FAIL", f"common future of a pair = {{x + jD : j>=0}} exactly (brute-force intersection in window x+6D); {n} pairs, bad {bad}")

# no equivariant occurrence-valued operation: output fibre has >=2 members
bad = 0; n = 0; minR = 99
for x, occ in BOXF.items():
    for r, s in combinations(occ, 2):
        D = delta(r[1] + 1, s[1] + 1)
        for j in (1, 2, 3):
            y = x + j * D; n += 1
            Ry = len(Dx(y)); minR = min(minR, Ry)
            if Ry < 2 or not (in_route(y, r) and in_route(y, s)): bad += 1
rec("F8.3", "PASS" if bad == 0 else "FAIL", f"output value y=x+jD (j=1,2,3) always carries both continuations r_y != s_y, so R(y)>=2 (min R(y)={minR}); {n} cases, bad {bad}  => no Pi-equivariant occurrence-valued operation")

# join and totalisation on rational fibres
none_ = uniq_ = multi_ = 0; ex_none = ex_multi = None; tot = 0
for x, ds in CORP.items():
    b = x.denominator
    if b == 1: continue
    S = set(ds)
    for d, e in combinations(ds, 2):
        L = lcm(d, e); ub = [u for u in ds if u % L == 0]
        mins = [u for u in ub if not any(w != u and u % w == 0 for w in ub)]
        tot += 1
        if not ub: none_ += 1; ex_none = ex_none or (str(x), d, e)
        elif len(mins) == 1: uniq_ += 1
        else: multi_ += 1; ex_multi = ex_multi or (str(x), d, e, mins)
rec("F8.4", "DATA", f"rational fibres (b>1), pairs {tot}: join exists in D: {uniq_}; no upper bound in D: {none_} (first {ex_none}); several incomparable minimal upper bounds: {multi_} (first {ex_multi})")
bad = 0
for x, ds in CORP.items():
    if x.denominator == 1:
        S = set(ds)
        for d, e in combinations(ds, 2):
            if lcm(d, e) not in S: bad += 1
rec("F8.5", "PASS" if bad == 0 else "FAIL", f"integer fibres: D(m) is closed under lcm (join-semilattice) ; violations {bad}")

# ---- incompatibility of A4 and A6: constructive instances
def is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True
def instance(a, b, d, e, nprimes):
    x = Fr(a, b); N, Np = d - 1, e - 1; g = gcd(N, Np); L = lcm(d, e); D = delta(d, e)
    assert b % 1 == 0 and g % b == 0
    out = []; p = max(g, L) + 1; ok = True
    while len(out) < nprimes:
        p += 1
        if not is_prime(p) or (p - 1) % g != 0: continue
        c0 = (a * g // b) % (p * p)
        i = (-c0 * pow(L * L, -1, p * p)) % (p * p)           # a g/b + i L^2 = 0 mod p^2
        y = x + i * D
        Mpp = y * (p - 1) / (p * p)                             # route d''=p present at y?
        pres = Mpp.denominator == 1 and Mpp >= 1
        Dy = Dx(y)
        pair_ok = d in Dy and e in Dy and p in Dy
        Dpp = delta(d, p)
        num_ok = Dpp.numerator % (p * p) == 0 and Dpp.denominator % p != 0
        ok = ok and pres and pair_ok and num_ok
        out.append((p, i, str(y)[:24], pres, pair_ok, num_ok))
    return ok, out
for (a, b, d, e) in [(81, 1, 3, 9), (81, 2, 3, 9), (36, 1, 2, 3), (2025, 2, 3, 5)]:
    ok, out = instance(a, b, d, e, 5)
    rec("F8.6", "PASS" if ok else "FAIL", f"A4+A6 obstruction instance x={a}/{b}, pair d=({d},{e}): " +
        "; ".join(f"p={p}: i={i}" for p, i, _, _, _, _ in out) + " -> new route d''=p present at x+iD, Delta(r_i,p) has p^2 in its numerator")
# the same A4 failure for Y_1 seen concretely
x = Fr(36); r = (9, 1)  # d=2 : M*4/1 = 36 -> M=9
s = (4, 2)               # d=3 : 4*9/2 = 18 ? -> check below
occ36 = sorted(BOX[Fr(36)], key=lambda t: t[1]); r2 = [t for t in occ36 if t[1] == 1][0]; s3 = [t for t in occ36 if t[1] == 2][0]
r_i, s_i, y = shifted(r2, s3, Fr(36), 3)
rec("F8.7", "PASS" if (y == 144 and Dcoll(Fr(36)) == 36 and Dcoll(y) == 144) else "FAIL",
    f"concrete stationarity failure of the collective operator: x=36 pair (2,3) shifted by 3D reaches y={y}; Dcoll(36)={Dcoll(Fr(36))}, Dcoll({y})={Dcoll(y)}, so Y_1(y)-y changes")

# collective operator facts
bad = 0
for x, ds in CORP.items():
    nxt = x * (1 + Fr(1, GAM[x]))
    if nxt != x + Dcoll(x) or not (x < nxt <= 2 * x): bad += 1
rec("F8.8", "PASS" if bad == 0 else "FAIL", f"label-blind minimal operator Y_1(x) = x(1+1/gcd H(x)), x < Y_1(x) <= 2x ; {len(CORP)} fibres, bad {bad}")
fixed2x = sum(1 for x in CORP if GAM[x] == 1)
rec("F8.9", "DATA", f"fibres whose first collective meeting is exactly 2x (gcd H = 1): {fixed2x}/{len(CORP)}")

# ---------------------------------------------------------------- F9 status lines
rec("F9.1", "OPEN", "which additional grammar (selection of j; choice between stationary-route-aware and label-blind-collective interaction; closure/output-occurrence rule) is to be adopted is a modelling decision, not a consequence of the fixed-nest rule")
rec("F9.2", "OPEN", "whether a weaker stationarity (A4 only along the fibre-refinement order) is compatible with A6")
rec("F9.3", "OPEN", "density of rigid fibres as the bound grows (F7.6 is finite data)")
print(f"\nelapsed {time.time()-T0:.1f}s  failures {NFAIL}")
print("ALL PASS" if NFAIL == 0 else "SOME FAIL")
sys.exit(0 if NFAIL == 0 else 1)
