#!/usr/bin/env python3
"""SELECT-II: intrinsic generative reachability. Vertices: positive integers m. Edges: m -> m(N+1)^2/N for N | m
(direct self-iteration of the nest rule, integer successors only). No joint operation is assumed.
Deterministic, exact integer arithmetic, standard library only. Independent of rgg*.py and select1.py.
PASS/FAIL = asserted check; DATA = reported count, not asserted."""
import json, sys, itertools
from math import gcd
from functools import lru_cache

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))
def info(name, detail):
    out[name] = {"data": detail}; print("DATA " + name + f" [{detail}]")

lcm = lambda a, b: a * b // gcd(a, b)
def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def Rmult(t):                                   # nest-fibre multiplicity R(t)=prod(floor(e/2)+1)-1 (manuscript Cor. 10.2)
    r = 1
    for e in factor(t).values(): r *= e // 2 + 1
    return r - 1
def divisors(m):
    r, i = [], 1
    while i * i <= m:
        if m % i == 0:
            r.append(i)
            if i * i != m: r.append(m // i)
        i += 1
    return sorted(r)
def fibre(t): return [(t // (d * d), d) for d in range(2, int(t ** 0.5) + 1) if t % (d * d) == 0]
def succ_all(m): return [(N, (m // N) * (N + 1) ** 2) for N in divisors(m)]
def preds(t): return sorted({(t // (d * d)) * (d - 1) for d in range(2, int(t ** 0.5) + 1) if t % (d * d) == 0})

# ============ A. basic structure of the nest-iteration graph ============
LIM = 20000
okA1 = okA2 = okA3 = okA4 = okA5 = True
for m in range(1, 3001):
    sc = succ_all(m)
    vals = [t for _, t in sc]
    okA1 &= len(set(vals)) == len(vals)                                      # distinct N give distinct successors
    okA1 &= all((t == 4 * m) == (N == 1) and t >= 4 * m for N, t in sc)      # step factor >=4, equality iff N=1
    okA4 &= len(sc) == len(divisors(m))
check("A1.successors: one per divisor N|m, all distinct, t>=4m with equality iff N=1 (hence acyclic, no sinks)", okA1 and okA4, "m<=3000")
for t in range(1, LIM + 1):
    P = preds(t); F = fibre(t)
    okA2 &= len(P) == len(set(P)) == len(F) == Rmult(t)                      # in-degree = R(t)
    # edge <-> route bijection: pred m of t with parameter N: route (m/N, N+1) in F(t); (M,N)=(m,N) is the occurrence
    for (k, d) in F:
        m, N = k * (d - 1), d - 1
        okA3 &= m % N == 0 and (m // N) * (N + 1) ** 2 == t and (m // N, N + 1) == (k, d)
    okA5 &= all(4 * p <= t for p in P)
check("A2.in-degree of t = |F(t)| = R(t) distinct predecessors (t<=20000)", okA2)
check("A3.each incoming edge m->t is exactly one anchor route (k,d) in F(t) with m=k(d-1), N=d-1; generated occurrence (M,N) = edge M->M(+)N", okA3)
check("A4.predecessors satisfy 4p<=t, so every ancestor chain has length <= log_4 t", okA5)
src = [t for t in range(1, LIM + 1) if not preds(t)]
sqfree = lambda n: all(e == 1 for e in factor(n).values())
check("A5.sources (no incoming edge) are exactly the squarefree integers (t<=20000)", src == [t for t in range(1, LIM + 1) if sqfree(t)], f"{len(src)} sources")

# ============ B. the join fails: the SELECT-II finding ============
def is_edge(a, b): return any(t == b for _, t in succ_all(a))
paths = {81: [[1, 4, 18, 81], [2, 8, 81]], 100: [[1, 4, 16, 100], [2, 9, 100]]}
check("B1.the four listed paths 1->4->18->81, 2->8->81, 1->4->16->100, 2->9->100 consist of valid nest steps",
      all(is_edge(p[i], p[i + 1]) for ps in paths.values() for p in ps for i in range(len(p) - 1)))
B = 20000
_succ = {}
def S(m):
    if m not in _succ: _succ[m] = [t for _, t in succ_all(m) if t <= B]
    return _succ[m]
_reach = {}
def Rch(m):
    if m in _reach: return _reach[m]
    seen, st = {m}, [m]
    while st:
        x = st.pop()
        for y in S(x):
            if y not in seen: seen.add(y); st.append(y)
    _reach[m] = seen; return seen
C12 = sorted(Rch(1) & Rch(2))
check("B2.common successors of 1 and 2 up to 100 are exactly {81,100}; neither reaches the other (steps are >=x4, 4*81>100)",
      [c for c in C12 if c <= 100] == [81, 100] and 100 not in Rch(81) and 81 not in Rch(100))
def minimal_common(a, b):
    C = Rch(a) & Rch(b)
    return sorted(c for c in C if not any(c2 != c and c in Rch(c2) for c2 in C))
M12 = minimal_common(1, 2)
check("B3.minimal common successors of 1 and 2 (all <=20000, hence globally minimal): >=2, so no least common successor exists", len(M12) >= 2 and 81 in M12 and 100 in M12, f"{len(M12)} minimal: {M12[:6]}...")
A = 40; st = {"comparable": 0, "no common successor <=20000": 0, "exactly one minimal found": 0, ">=2 minimal (certified no join)": 0}
for a in range(1, A + 1):
    for b in range(a + 1, A + 1):
        if b in Rch(a) or a in Rch(b): st["comparable"] += 1; continue
        mc = minimal_common(a, b)
        if not mc: st["no common successor <=20000"] += 1
        elif len(mc) == 1: st["exactly one minimal found"] += 1
        else: st[">=2 minimal (certified no join)"] += 1
info("B4.pairs a<b<=40 under the successor order (B=20000)", st)
check("B5.the nest-iteration order is not a join-semilattice: certified for a majority of tested pairs", st[">=2 minimal (certified no join)"] > sum(st.values()) // 2)

# ============ C. the dual question is exact: common ancestors ============
@lru_cache(None)
def anc(t):
    s = set()
    for p in preds(t): s.add(p); s |= anc(p)
    return frozenset(s)
NC = 400; stc = {"comparable": 0, "no common ancestor": 0, "unique maximal": 0, ">=2 maximal (no meet)": 0}; ex = None
for a in range(2, NC):
    for b in range(a + 1, NC):
        if a in anc(b) or b in anc(a): stc["comparable"] += 1; continue
        Cn = anc(a) & anc(b)
        if not Cn: stc["no common ancestor"] += 1; continue
        mx = [c for c in Cn if not any(c != d and c in anc(d) for d in Cn)]
        if len(mx) == 1: stc["unique maximal"] += 1
        else:
            stc[">=2 maximal (no meet)"] += 1
            if ex is None: ex = (a, b, sorted(mx))
info("C1.pairs 2<=a<b<400, common ancestors (exact, no truncation)", {**stc, "first no-meet example": ex})
Cn32 = anc(32) & anc(300)
mx32 = sorted(c for c in Cn32 if not any(c != d and c in anc(d) for d in Cn32))
check("C2.no meet in general either: (32,300) has maximal common ancestors exactly {2,6}", mx32 == [2, 6], str(mx32))

# ============ D. relation to the SELECT-I / manuscript structures ============
# D1: a fibre route r=(k,d) in F(t) is the incoming edge from p(r)=k(d-1); fibre separation = difference of predecessors.
okD1 = all(len({k * (d - 1) for k, d in fibre(t)}) == len(fibre(t)) for t in range(1, 5001))
check("D1.distinct routes of one value fibre have distinct predecessors (route = incoming edge), t<=5000", okD1)
# D2: is the manuscript's join value v(r v r') a successor-order object of the two predecessors?
B2 = 300000; _s2 = {}; _r2 = {}
def S2(m):
    if m not in _s2: _s2[m] = [t for _, t in succ_all(m) if t <= B2]
    return _s2[m]
def Rc2(m):
    if m in _r2: return _r2[m]
    seen, st = {m}, [m]
    while st:
        x = st.pop()
        for y in S2(x):
            if y not in seen: seen.add(y); st.append(y)
    _r2[m] = seen; return seen
tot = fromt = fromboth = 0
for t in range(4, 400):
    for r, s in itertools.combinations(fibre(t), 2):
        p, q = r[0] * (r[1] - 1), s[0] * (s[1] - 1)
        g, L = gcd(r[1], s[1]), lcm(r[1], s[1]); u = t * (L // g) ** 2
        if u > B2: continue
        tot += 1; fromt += u in Rc2(t); fromboth += (u in Rc2(p) and u in Rc2(q))
info("D2.value of r v r' (manuscript join) versus the successor order, fibre pairs t<400", f"{tot} pairs; reachable from t: {fromt}; common successor of both predecessors: {fromboth}")
check("D3.the manuscript join value is not generally a successor-order object: some fibre pair's join value is not reachable from t", fromt < tot)

json.dump(out, open("select2_report.json", "w"), indent=1, default=str)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)
