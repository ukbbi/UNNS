#!/usr/bin/env python3
"""SELECT-II v002: exact reachability, complete histories, and history-sensitive relational tests on the nest-iteration graph.
Graph: vertices positive integers; edges m -> m(N+1)^2/N, N | m.  P(t)={t(d-1)/d^2 : d>=2, d^2 | t} (immediate predecessors).
select2.py (v001) is not modified or imported.  Deterministic, exact integer arithmetic, standard library only.
PASS/FAIL = asserted check; DATA = reported count, not asserted."""
import json, sys, itertools, random
from math import gcd, log
from functools import lru_cache
sys.setrecursionlimit(100000)

out, ok_all = {}, True
def check(name, cond, detail=""):
    global ok_all
    ok_all &= bool(cond); out[name] = {"pass": bool(cond), "detail": detail}
    print(("PASS " if cond else "FAIL ") + name + (f" [{detail}]" if detail else ""))
def info(name, detail):
    out[name] = {"data": detail}; print("DATA " + name + f" [{detail}]")

def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def Rmult(t):
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
@lru_cache(None)
def P(t): return tuple(sorted({(t // (d * d)) * (d - 1) for d in range(2, int(t ** 0.5) + 1) if t % (d * d) == 0}))
@lru_cache(None)
def S(m): return tuple(sorted((m // N) * (N + 1) ** 2 for N in divisors(m)))
def fibre(t): return [(t // (d * d), d) for d in range(2, int(t ** 0.5) + 1) if t % (d * d) == 0]

# ===================== Track A: exact reachability =====================
# A1 backward recurrence  m ~> t  iff  m=t or exists p in P(t): m ~> p   (terminates: p <= t/4)
@lru_cache(None)
def reaches(m, t):
    if m == t: return True
    if 4 * m > t: return False                 # every non-trivial path multiplies by >= 4
    return any(reaches(m, p) for p in P(t))
T = 1500
fw = {}
for m in range(1, T + 1):
    seen, st = {m}, [m]
    while st:
        x = st.pop()
        for y in S(x):
            if y <= T and y not in seen: seen.add(y); st.append(y)
    fw[m] = seen
okA = all(reaches(m, t) == (t in fw[m]) for m in range(1, T + 1) for t in range(m, T + 1))
check("A1.backward recurrence = forward reachability for ALL pairs 1<=m<=t<=1500", okA, f"{T*(T+1)//2} pairs")
check("A2.termination: p<=t/4 for every p in P(t) (t<=20000); hence recursion depth <= floor(log_4(t/m))",
      all(4 * p <= t for t in range(1, 20001) for p in P(t)))
@lru_cache(None)
def longest(m, t):                              # longest path length m ~> t, -1 if unreachable
    if m == t: return 0
    if 4 * m > t: return -1
    best = -1
    for p in P(t):
        l = longest(m, p)
        if l >= 0: best = max(best, l + 1)
    return best
okL = all(longest(m, t) <= int(log(t / m, 4) + 1e-9) for m in range(1, 400) for t in range(m, 2500) if longest(m, t) >= 0)
check("A3.every path m~>t has at most floor(log_4(t/m)) edges (m<400, t<2500)", okL)
random.seed(20261021); okR = True; nr = 0
for _ in range(60):                             # adversarial: larger t, forward search from m bounded by t
    m = random.randint(1, 300); t = random.choice([x for x in range(m, 10 ** 5) if len(P(x)) >= 1 and x > 50][:1] or [m])
    t = random.randint(1000, 10 ** 5); seen, st = {m}, [m]
    while st:
        x = st.pop()
        for y in S(x):
            if y <= t and y not in seen: seen.add(y); st.append(y)
    okR &= reaches(m, t) == (t in seen); nr += 1
check("A4.random adversarial pairs, t up to 10^5: backward = forward", okR, f"{nr} pairs")

# A5 NO SHORTCUTS: if p -> t is an edge, t is not reachable from p by any path of >=2 edges.
# proof: phi(d)=d^2/(d-1) in lowest terms; phi(d)=prod phi(d_i), j>=2 forces prod d_i = d a, prod(d_i-1)=(d-1)a^2, then a=1 and d1+..>=3 contradiction.
okS = True
for p in range(1, 3001):
    one = set(y for y in S(p) if y <= 10 ** 6); seen = set(); st = list(one)
    while st:
        x = st.pop()
        for y in S(x):
            if y <= 10 ** 6 and y not in seen: seen.add(y); st.append(y)
    okS &= not (one & seen)
check("A5.no shortcuts: no t is both a 1-step and a >=2-step successor of the same p (p<3000, t<=10^6)", okS)
from fractions import Fraction
phi = lambda d: Fraction(d * d, d - 1)
def is_phi(x):                                  # is the Fraction x equal to phi(d)=d^2/(d-1) for some integer d>=2 ?
    f = x.numerator // x.denominator
    return any(d >= 2 and phi(d) == x for d in (f - 2, f - 1, f))
okP = all(not is_phi(phi(a) * phi(b)) for a in range(2, 400) for b in range(a, 400))
okP &= all(not is_phi(phi(a) * phi(b) * phi(c)) for a in range(2, 60) for b in range(a, 60) for c in range(b, 60))
check("A6.Diophantine core of A5: phi(d1)phi(d2)=phi(d) and phi(d1)phi(d2)phi(d3)=phi(d) have no solutions (d_i<400 for two factors, d_i<60 for three; any d)", okP)
exs = [(m, t, sorted({l for l in range(0, 9) if False}))]  if False else None
def pathlens(m, t):
    @lru_cache(None)
    def f(x):
        if x == m: return frozenset({0})
        if 4 * m > x: return frozenset()
        s = set()
        for p in P(x):
            for l in f(p): s.add(l + 1)
        return frozenset(s)
    return f(t)
check("A7.reachability is NOT graded: 6 ~> 784 has paths of length 2 and 3", pathlens(6, 784) == frozenset({2, 3}), str(sorted(pathlens(6, 784))))
nong = sum(1 for t in range(2, 4000) for m in range(1, t // 4 + 1) if reaches(m, t) and len(pathlens(m, t)) > 1) if False else None

# ===================== Track B: complete histories =====================
@lru_cache(None)
def H(t):
    p = P(t)
    return 1 if not p else sum(H(q) for q in p)
def histories(t):                               # explicit labelled paths source -> ... -> t
    p = P(t)
    if not p: return [(t,)]
    return [h + (t,) for q in p for h in histories(q)]
check("B1.H(t) recurrence = explicit enumeration of source-to-t paths, t<=3000", all(H(t) == len(histories(t)) for t in range(1, 3001)))
check("B2.H(72)=4 with histories 1-4-18-72, 1-4-16-72, 3-16-72, 10-72 (R(72)=3)",
      sorted(histories(72)) == sorted([(1, 4, 18, 72), (1, 4, 16, 72), (3, 16, 72), (10, 72)]) and H(72) == 4 and Rmult(72) == 3)
check("B3.H(t)>=max(1,R(t)); H(t)=R(t) for non-sources iff every predecessor has exactly one history (t<=20000)",
      all(H(t) >= max(1, Rmult(t)) and (H(t) == Rmult(t)) == (Rmult(t) > 0 and all(H(q) == 1 for q in P(t))) for t in range(1, 20001) if Rmult(t) > 0 or H(t) == 1))
nonsrc = [t for t in range(1, 20001) if Rmult(t) > 0]
gt = [t for t in nonsrc if H(t) > Rmult(t)]
mx = max(range(1, 20001), key=H)
info("B4.R versus H, t<=20000", f"non-sources {len(nonsrc)}; H>R for {len(gt)}; smallest t with H>R: {gt[0]}; max H = {H(mx)} at t={mx}")
@lru_cache(None)
def srclens(t):
    p = P(t)
    return frozenset({0}) if not p else frozenset(l + 1 for q in p for l in srclens(q))
mixed = [t for t in range(1, 20001) if len(srclens(t)) > 1]
check("B5.history length is not determined by the endpoint: t=16 has histories 3-16 and 1-4-16 (lengths 1,2)", srclens(16) == frozenset({1, 2}))
info("B6.endpoints with histories of different lengths, t<=20000", f"{len(mixed)} of 20000; first {mixed[:6]}")

# ===================== Track C: history-sensitive relational tests =====================
# C1 Markov no-go: the set of continuations of a history depends only on its endpoint.
def futures(h, depth):                           # set of (extension, ) as paths of length <=depth added to history h
    res, frontier = {h}, [h]
    for _ in range(depth):
        nxt = []
        for x in frontier:
            for y in S(x[-1]): nxt.append(x + (y,))
        res |= set(nxt); frontier = nxt
    return res
okM = True; nM = 0
for t in range(1, 400):
    hs = histories(t)
    if len(hs) < 2: continue
    sig = [frozenset(x[len(h):] for x in futures(h, 3)) for h in hs]
    okM &= all(s == sig[0] for s in sig); nM += 1
check("C1.Markov no-go: for every endpoint t<400 with >=2 histories, all histories have identical continuation sets (depth 3)", okM, f"{nM} endpoints")
info("C2.consequence of C1 (argument, not a numerical row)", "every continuation-defined joint operation with observation = merge endpoints depends on endpoints only; Theorem 11.9 criterion holds trivially, set deficit 0")
# C3 tower value -> route -> history
Tm = 5000
nV = Tm; nE = sum(Rmult(t) for t in range(1, Tm + 1)); nH = sum(H(t) for t in range(1, Tm + 1))
info("C3.state-space tower up to 5000", f"values {nV}; routes (incoming edges) {nE}; complete histories {nH}")
routes_multi = [(t, k, d) for t in range(1, 3001) for (k, d) in fibre(t) if H(k * (d - 1)) >= 2]
check("C4.route does not determine history: t=72, route (8,3) (predecessor 16) has two histories", (72, 8, 3) in routes_multi)
info("C5.routes whose predecessor has >=2 histories, t<=3000", f"{len(routes_multi)} routes; first {routes_multi[:4]}")
# C6 confluence test: merge of two routes of one fibre at t
def minimal_common_successors(a, b, B):
    def R(x):
        seen, st = {x}, [x]
        while st:
            y = st.pop()
            for z in S(y):
                if z <= B and z not in seen: seen.add(z); st.append(z)
        return seen
    C = R(a) & R(b)
    return sorted(c for c in C if not any(c2 != c and c in R(c2) for c2 in C))
tot = minimal_t = double = 0; dbl_ex = []
for t in range(4, 3001):
    F = fibre(t)
    for r, s in itertools.combinations(F, 2):
        p, q = r[0] * (r[1] - 1), s[0] * (s[1] - 1)
        mc = minimal_common_successors(p, q, t)
        tot += 1; minimal_t += (t in mc)
        if len(mc) > 1: double += 1; dbl_ex.append((t, r, s, mc))
check("C6.every confluence is minimal: t is a minimal common successor of the two predecessors of any fibre pair (t<=3000)", minimal_t == tot, f"{tot} pairs")
info("C7.second incomparable merge below t ('double confluence')", f"{double}/{tot} pairs; examples {[(e[0], e[1], e[2], e[3]) for e in dbl_ex[:3]]}")
# C8 leakage-controlled comparison for J_pred(r,s)=Min(Desc(p(r)) ∩ Desc(p(s))) (reflexive Desc)
sep_one = sep_both = tot2 = 0
for t in range(4, 3001):
    for r, s in itertools.combinations(fibre(t), 2):
        p, q = r[0] * (r[1] - 1), s[0] * (s[1] - 1)
        a = not reaches(q, p)         # probe r separates r from s  iff  NOT(q ~> p)
        b = not reaches(p, q)         # probe s separates s from r  iff  NOT(p ~> q)
        tot2 += 1; sep_one += (a or b); sep_both += (a and b)
info("C9.J_pred separation of fibre pairs, t<=3000", f"{tot2} pairs; separated by at least one probe {sep_one}; by both probes {sep_both}")
check("C10.predecessors of one value form an antichain (corollary of A5: p~>q plus edges p->t, q->t would be a shortcut): 0 comparable pairs", tot2 - sep_both == 0, f"{tot2} pairs")
info("C8.J_pred with probe r", "J_pred(r,r)={p} equals J_pred(s,r)=Min C(q,p) iff q ~> p; by C10 never, so J_pred separates every fibre pair automatically (leakage, not continuation information)")

json.dump(out, open("select2b_report.json", "w"), indent=1, default=str)
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)
