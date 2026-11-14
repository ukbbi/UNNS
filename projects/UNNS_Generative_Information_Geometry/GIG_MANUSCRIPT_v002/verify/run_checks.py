#!/usr/bin/env python3
"""Independent re-derivations for the GIG Comprehensive Manuscript v001.
Exact integer / Fraction / GF(2) arithmetic only; no frozen GIG package is imported.
Writes results.json next to this file.  Run:  python3 run_checks.py [--quick]"""
import json, sys, os, random, time, math
from fractions import Fraction
from itertools import permutations, combinations
from math import comb, log2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gigmini import *

def factorint(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def divisors(n):
    ds = [1]
    for p, e in factorint(n).items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
    return sorted(ds)

OUT = {}
def rec(name, **kw): OUT[name] = kw; print(name, json.dumps(kw)[:300])

# ---------------- Ch.3: the histories of 72, and growth of 72^r ----------------
def reverse_edges(t):
    f = factorint(t); s = 1
    for p, e in f.items(): s *= p ** (e // 2)
    return [(d - 1, t // (d * d) * (d - 1)) for d in divisors(s) if d >= 2]   # (label N, predecessor m)

def complete_histories(t, memo={}):
    if t in memo: return memo[t]
    rev = reverse_edges(t)
    if not rev: res = [(t, ())]
    else:
        res = []
        for N, m in rev:
            for src, w in complete_histories(m): res.append((src, w + (N,)))
    memo[t] = res; return res

h72 = complete_histories(72)
rec("ch3_histories_of_72", histories=sorted(h72), n=len(h72))
def swap_classes(hs):
    hs = list(hs); idx = {h: i for i, h in enumerate(hs)}; par = list(range(len(hs)))
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    def adm(src, w):
        x = src
        for N in w:
            if x % N: return False
            x = x // N * (N + 1) ** 2
        return True
    for h in hs:
        s, w = h
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]:
                w2 = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                if (s, w2) in idx: par[find(idx[h])] = find(idx[(s, w2)])
    comps = {}
    for i in range(len(hs)): comps.setdefault(find(i), []).append(i)
    return list(comps.values())
cl = swap_classes(h72); sizes = sorted(len(c) for c in cl)
N = len(h72)
HCT = -sum(s / N * log2(s / N) for s in sizes)
HWC = sum(s / N * log2(s) for s in sizes)
srcs = {}
for s, w in h72: srcs[s] = srcs.get(s, 0) + 1
HM = -sum(c / N * log2(c / N) for c in srcs.values())
rec("ch3_decomposition_72", class_sizes=sizes, A=log2(N), H_C_given_T=HCT, H_W_given_C_T=HWC, H_M_given_T=HM,
    chain_rule_ok=abs(log2(N) - (HCT + HWC)) < 1e-12)

counts = {}
def cnt(t, memo={}):
    if t in memo: return memo[t]
    rev = reverse_edges(t)
    memo[t] = 1 if not rev else sum(cnt(m) for _, m in rev); return memo[t]
exp = [4, 100, 3601, 194864, 14177856, 1258011667]
got = [cnt(72 ** r) for r in range(1, 7)]
rec("ch3_72r_counts", computed=got, registered=exp, match=got == exp,
    lower_bound_ok=all(g >= comb(2 * r, r) for r, g in zip(range(1, 7), got)))

# ---------------- Ch.4: Lemma F against simulation; anchors; source filtration ----------------
def lemmaF_check(lab, ms):
    for m in ms:
        A = admissible_perms(lab, m)
        for p in permutations(range(len(lab))):
            if admissible_by_simulation(lab, m, p) != (p in A): return False
    return True
rec("ch4_lemmaF", ok=lemmaF_check((2, 3, 4, 5, 8, 9), [288, 576, 864, 1440, 2016]) and lemmaF_check((2, 3, 6, 7), range(1, 200)))

anchors = {"A": ((2, 3, 4, 5, 8, 9), 288), "B": ((2, 3, 6, 7, 8, 9), 432)}
surv = {}
quick = "--quick" in sys.argv
for nm, (lab, m0) in anchors.items():
    row = {}; cache = {}
    for t in range(1, 61):
        m = m0 * t
        A = frozenset(admissible_perms(lab, m))
        if A not in cache:
            f, b = betti_arith(lab, m); cache[A] = (len(A), b[2] if len(b) > 2 else 0, b)
        row[t] = cache[A]
    surv[nm] = row
    ts = [t for t in row if row[t][1] > 0]
    pred = [t for t in range(1, 61) if math.gcd(t, 30 if nm == "A" else 42) == 1]
    rec("ch6_anchor_" + nm, source=m0, survivors_t=ts, predicted_gcd_law=pred, law_matches=ts == pred,
        n_survive=len(ts), N_by_t={t: row[t][0] for t in (1, 2, 3, 5, 7, 6, 10, 14, 15)})
    # H(Y) over t=1..60 uniform
    p = len(ts) / 60; HY = -p * log2(p) - (1 - p) * log2(1 - p)
    OUT["ch6_anchor_" + nm]["H_Y_bits"] = HY
    OUT["ch6_anchor_" + nm]["beta_vectors"] = {t: row[t][2] for t in (1, 2, 3, 5)}
    # history counts: injectivity on the comparable window (sources m0*t with A(m) containing A(m0))
    A0 = frozenset(admissible_perms(lab, m0))
    win = {}
    for t in range(1, 61):
        A = frozenset(admissible_perms(lab, m0 * t))
        if A0 <= A: win[A] = (len(A), row[t][1])
    OUT["ch10_anchor_" + nm + "_window"] = {"classes": len(win), "history_counts": sorted(v[0] for v in win.values()),
                                           "N_injective": len({v[0] for v in win.values()}) == len(win)}
    print(nm, OUT["ch10_anchor_" + nm + "_window"])

# ---------------- Ch.5/10: witnesses W1-W6 (N, E, f, beta) ----------------
def piece(lab, m):
    A = admissible_perms(lab, m); k = len(lab)
    faces = complex_from_vertex_set(k, A)
    f, b = betti(k, faces)
    E = f[1] if len(f) > 1 else 0
    return {"N": len(A), "f": f, "beta": b}
W = {"W1a": ((2, 3, 14, 15), 210), "W1b": ((1, 2, 3, 4), 6), "W2a": ((2, 3, 8, 9), 72), "W2b": ((2, 3, 5, 6), 30),
     "W5a": ((2, 3, 9, 15, 21), 189), "W5b": ((1, 2, 12, 13, 26), 52), "W6a": ((2, 3, 8, 21, 26), 273), "W6b": ((6, 8, 9, 14, 15), 168)}
wres = {k: piece(*v) for k, v in W.items()}
rec("ch10_witnesses", pieces=wres)

# ---------------- Ch.9: radius-2 identity on random induced subgraphs of the permutohedron ----------------
def swap_graph(k, A):
    A = set(A); adj = {p: [] for p in A}
    for p in A:
        for i in range(k - 1):
            q = p[:i] + (p[i + 1], p[i]) + p[i + 2:]
            if q in A: adj[p].append(q)
    return adj
def check_radius2(k, A):
    adj = swap_graph(k, A)
    for w in adj:
        d = len(adj[w]); s = sum(len(adj[u]) - 1 for u in adj[w])
        # q(w): number of 4-cycles through w
        q = 0
        nb = adj[w]
        for a, b in combinations(nb, 2):
            common = (set(adj[a]) & set(adj[b])) - {w}
            q += len(common)
        B2 = {w} | set(nb) | {x for u in nb for x in adj[u]}
        if len(B2) != 1 + d + s - q: return False
    return True
rnd = random.Random(20261106); ok = True
for trial in range(300):
    k = rnd.choice([4, 5, 6]); allp = list(permutations(range(k)))
    A = rnd.sample(allp, rnd.randint(len(allp) // 4, 3 * len(allp) // 4))
    ok &= check_radius2(k, A)
rec("ch9_radius2_identity", trials=300, all_ok=ok)

# ---------------- Ch.12: Alexander duality + dead-set nerve on named systems ----------------
def flags_of(k):
    return list(permutations(range(k)))
def Y_complex_faces(k, A):
    """Simplices of Y_A (subsets of proper subsets forming chains) as frozensets of masks: generated by prefix chains of non-admissible perms."""
    simp = set()
    for p in permutations(range(k)):
        if p in A: continue
        ch = prefix_sets(p)
        for r in range(1, len(ch) + 1):
            for sub in combinations(ch, r): simp.add(sub)
    return simp
def homology_of_simplices(simps, maxdim=4):
    by = {}
    for s in simps: by.setdefault(len(s) - 1, []).append(s)
    idx = {d: {s: i for i, s in enumerate(sorted(L))} for d, L in by.items()}
    rho = {}
    for d in sorted(by):
        if d == 0: rho[0] = 0; continue
        rows = []
        for s in by[d]:
            v = 0
            for i in range(len(s)):
                f = s[:i] + s[i + 1:]
                v ^= 1 << idx[d - 1][f]
            rows.append(v)
        rho[d] = rank_gf2(rows)
    top = max(by)
    f = [len(by.get(d, [])) for d in range(top + 1)]
    b = [f[d] - rho.get(d, 0) - rho.get(d + 1, 0) for d in range(top + 1)]
    return f, b
def dead_sets(k, A):
    full = (1 << k) - 1; D = []
    byI = {}
    for p in permutations(range(k)):
        for I in prefix_sets(p): byI.setdefault(I, []).append(p)
    for I, L in byI.items():
        if all(p not in A for p in L): D.append(I)
    return sorted(D)
def comparable(a, b): return (a & b) == a or (a & b) == b
def nerve_betti(k, D):
    full = (1 << k) - 1
    P = range(1, full)
    facets = set()
    for z in P:
        C = tuple(sorted(d for d in D if comparable(d, z)))
        if C: facets.add(C)
    simp = set()
    for C in facets:
        for r in range(1, min(len(C), 3) + 1):   # up to triangles (dim 2): enough for H0,H1
            for sub in combinations(C, r): simp.add(sub)
    f, b = homology_of_simplices(simp)
    # b[1] computed with 2-skeleton is exact for H1
    return len(D), f, b
def dual_check(lab, m):
    k = len(lab)
    A = admissible_perms(lab, m)
    f, b = betti(k, complex_from_vertex_set(k, A))
    D = dead_sets(k, A)
    nD, nf, nb = nerve_betti(k, D)
    # reduced b0 of N[D]: components-1
    return {"N": len(A), "beta_K": b, "dead_sets": len(D), "H1_nerve": nb[1] if len(nb) > 1 else 0,
            "H0_nerve": nb[0], "beta2_equals_H1_nerve": (b[2] if len(b) > 2 else 0) == (nb[1] if len(nb) > 1 else 0)}
NER = {}
for name, (lab, m) in {"pos_2520": ((2, 4, 5, 9, 14, 15), 2520), "neg_3780": ((2, 4, 5, 9, 14, 15), 3780),
                       "pos_480": ((2, 3, 4, 5, 8, 15), 480), "neg_800": ((2, 3, 4, 5, 8, 15), 800),
                       "anchorA_288": ((2, 3, 4, 5, 8, 9), 288), "anchorA_576": ((2, 3, 4, 5, 8, 9), 576)}.items():
    NER[name] = dual_check(lab, m)
rec("ch12_nerve_theorem_instances", systems=NER, all_ok=all(v["beta2_equals_H1_nerve"] for v in NER.values()))

# full Alexander duality check on 40 random vertex sets in S_6 (reduced b_j(K) = reduced b_{3-j}(Y))
if not quick:
    rnd = random.Random(7); good = 0; tried = 0
    allp = list(permutations(range(6)))
    for _ in range(12):
        A = set(rnd.sample(allp, rnd.randint(60, 660)))
        k = 6
        f, b = betti(k, complex_from_vertex_set(k, A))
        b = list(b) + [0] * (6 - len(b))
        simp = Y_complex_faces(k, A)
        fy, by = homology_of_simplices(simp)
        by = list(by) + [0] * (6 - len(by))
        rb = lambda L, j: L[j] - (1 if j == 0 else 0)
        ok = all(rb(b, j) == rb(by, 3 - j) for j in range(0, 4)) if True else False
        # note: reduced b_j(K) vs reduced b_{3-j}(Y): j=0..3 (Y has dimension<=4)
        tried += 1; good += ok
    rec("ch12_alexander_duality_random", tried=tried, ok=good)

# ---------------- Ch.14: pairwise adjacency lemmas (30 / 435 / 4060) and the triple counterexample ----------------
k = 6
ops = [p for p in ordered_partitions(k) if len(p) >= 2]
def blockidx(F):
    b = {}
    for i, B in enumerate(F):
        for e in range(k):
            if B >> e & 1: b[e] = i
    return b
pairs = [(x, y) for x in range(k) for y in range(k) if x != y]
pmask = {}
for F in ops:
    b = blockidx(F); mk = 0
    for j, (x, y) in enumerate(pairs):
        if b[y] - b[x] in (0, 1): mk |= 1 << j
    pmask[F] = mk
def Z(S):
    need = 0
    for p in S: need |= 1 << pairs.index(p)
    return [F for F in ops if pmask[F] & need == need]
def merge_boundary(F):
    out = []
    for i in range(len(F) - 1):
        G = F[:i] + (F[i] | F[i + 1],) + F[i + 2:]
        if len(G) >= 2: out.append(G)
    return out
def reduced_betti_Z(simps):
    if not simps: return None
    by = {}
    for F in simps: by.setdefault(len(F) - 2, []).append(F)
    idx = {d: {F: i for i, F in enumerate(L)} for d, L in by.items()}
    rho = {0: 0}
    for d in by:
        if d == 0: continue
        rows = []
        for F in by[d]:
            v = 0
            for G in merge_boundary(F): v ^= 1 << idx[d - 1][G]
            rows.append(v)
        rho[d] = rank_gf2(rows)
    top = max(by); f = [len(by.get(d, [])) for d in range(top + 1)]
    b = [f[d] - rho.get(d, 0) - rho.get(d + 1, 0) for d in range(top + 1)]
    b[0] -= 1
    return b
def ncomp(simps):
    V = [F for F in simps if len(F) == 2]; E = [F for F in simps if len(F) == 3]
    par = {F: F for F in V}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for F in E:
        v1 = (F[0],) + (F[1] | F[2],); v2 = (F[0] | F[1], F[2])
        par[find(v1)] = find(v2)
    return len({find(v) for v in V})
F1 = all(max(reduced_betti_Z(Z([p]))[:3]) == 0 for p in pairs)
rec("ch14_F1_singles_acyclic_deg012", count=len(pairs), ok=F1)
F2 = True; nPair = 0
for p, q in combinations(pairs, 2):
    z = Z([p, q]); nPair += 1
    if not z or ncomp(z) != 1: F2 = False
rec("ch14_F2_pairs_nonempty_connected", count=nPair, ok=F2)
masks_set = set(pmask.values())
F3 = True; nTrip = 0; disc = 0
for S in combinations(range(len(pairs)), 3):
    need = sum(1 << j for j in S); nTrip += 1
    if not any(mk & need == need for mk in masks_set): F3 = False
rec("ch14_F3_triples_nonempty", count=nTrip, ok=F3)
# disconnected triples (informational, source says 120)
disc = 0
for S in combinations(range(len(pairs)), 3):
    z = Z([pairs[j] for j in S])
    if z and ncomp(z) > 1: disc += 1
rec("ch14_triples_disconnected", count=disc)

def has_consecutive(p, trip):
    return any(p[i:i + 3] == trip for i in range(len(p) - 2))
A3 = {p for p in permutations(range(6)) if not has_consecutive(p, (1, 2, 0)) and not has_consecutive(p, (5, 4, 3))}
f3, b3 = betti(6, complex_from_vertex_set(6, A3))
rec("ch14_triple_counterexample", N=len(A3), f=f3, beta=b3, ok=(len(A3) == 674 and b3[:3] == [1, 2, 5]))
# pairwise sample: random digraphs
rnd = random.Random(99); mx = 0; cntpos = 0; tried = 0
for _ in range(80):
    pr = rnd.choice([0.45, 0.6, 0.75, 0.85])
    arcs = {(x, y) for x in range(6) for y in range(6) if x != y and rnd.random() < pr}
    A = {p for p in permutations(range(6)) if all((p[i], p[i + 1]) in arcs for i in range(5))}
    if not A or len(A) == 720: continue
    f, b = betti(6, complex_from_vertex_set(6, A)); tried += 1
    mx = max(mx, b[2] if len(b) > 2 else 0)
rec("ch14_pairwise_random_sample", tried=tried, max_beta2=mx)

# ---------------- Ch.8: lift identities (chain-level) ----------------
def bd(F): return face_boundary(F)
def addset(S, F):
    if F in S: S.remove(F)
    else: S.add(F)
def Ins(F, i): return F[:i] + (F[i] | (1 << 6),) + F[i + 1:]
def Lam(F): return {Ins(F, i) for i in range(len(F))}
def Lam_chain(c):
    S = set()
    for F in c:
        for G in Lam(F): addset(S, G)
    return S
def bd_chain(c):
    S = set()
    for F in c:
        for G in bd(F): addset(S, G)
    return S
first = lambda F: ((1 << 6),) + F
last = lambda F: F + ((1 << 6),)
ok = True; nfaces = 0
for F in ordered_partitions(6):
    nfaces += 1
    lhs = bd_chain(Lam(F))
    rhs = Lam_chain(bd(F))
    addset(rhs, first(F)); addset(rhs, last(F))
    if lhs != rhs: ok = False
rec("ch8_LT0_boundary_lemma", faces_checked=nfaces, ok=ok)
# retraction chain map on P_6 with r=5
def rho_face(G, r=5):
    for i, B in enumerate(G):
        if B == 1 << r: return G[:i] + G[i + 1:]
    return None
ok2 = True
for G in ordered_partitions(6):
    lhs = set()
    g = rho_face(G)
    if g is not None: lhs = set(bd(g)) if g else set()
    rhs = set()
    for H in bd(G):
        h = rho_face(H)
        if h is not None: addset(rhs, h)
    # rho(dG) should equal d rho(G); the singleton {r} cannot be split so the identity is exact
    if lhs != rhs and not (g is None and not rhs): ok2 = False
rec("ch8_J2_retraction_chain_map", ok=ok2)
json.dump(OUT, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w"), indent=1, default=str)
print("DONE")
