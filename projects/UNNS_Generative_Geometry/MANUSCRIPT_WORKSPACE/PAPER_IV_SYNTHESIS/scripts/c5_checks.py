"""Stdlib verification of three lemmas used in Paper IV: L-comp, L-edge, nu({2,3,14}); writes results/c5_checks.json"""
import random, json, itertools
from math import gcd
from fractions import Fraction as Fr
import eng3, hist
random.seed(20261103)
out = {}
# L-comp
bad = 0; n = 0
for _ in range(3000):
    D = sorted(random.sample(range(2, 400), random.randint(2, 9)))
    E = eng3.edges(D)
    par = {d: d for d in D}
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for u, v in E: par[f(u)] = f(v)
    c1 = {}
    for d in D: c1.setdefault(f(d), set()).add(d)
    par2 = {d: d for d in D}
    def g_(a):
        while par2[a] != a: par2[a] = par2[par2[a]]; a = par2[a]
        return a
    for u, v in itertools.combinations(D, 2):
        if gcd(u, v) > 1: par2[g_(u)] = g_(v)
    c2 = {}
    for d in D: c2.setdefault(g_(d), set()).add(d)
    n += 1
    if sorted(map(sorted, c1.values())) != sorted(map(sorted, c2.values())): bad += 1
out['Lcomp'] = {'trials': n, 'violations': bad}
# L-edge: edge of K(D') between u,v in D iff edge in K(D) and no new element in [u,v]
bad = 0; n = 0
for _ in range(3000):
    D = sorted(random.sample(range(2, 300), random.randint(2, 7)))
    N = sorted(set(random.sample(range(2, 300), random.randint(1, 4))) - set(D))
    D2 = sorted(D + N); E = eng3.edges(D); E2 = eng3.edges(D2)
    for u, v in itertools.combinations(D, 2):
        g = gcd(u, v); l = u // g * v
        newin = any(w % g == 0 and l % w == 0 and w not in (u, v) for w in N)
        pred = ((u, v) in E) and not newin
        n += 1
        if pred != ((u, v) in E2): bad += 1
out['Ledge'] = {'pairs': n, 'violations': bad}
# nu({2,3,14})
def nu(m):
    best = None; res = {}
    for perm in itertools.permutations((2, 3, 14)):
        w = perm
        if hist.admissible(m, w):
            t = m
            for N in w: t = t * (N + 1) ** 2 // N
            res.setdefault(t, set()).add(w)
    if not res: return 0
    t = next(iter(res))
    H = [w for w in hist.histories(m, t) if sorted(w) == [2, 3, 14]]
    H, cl = hist.classes(m, t) if False else (H, None)
    idx = {w: i for i, w in enumerate(H)}; par = list(range(len(H)))
    def f(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for w in H:
        for i in range(2):
            w2 = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
            if w2 in idx: par[f(idx[w])] = f(idx[w2])
    return len({f(i) for i in range(len(H))})
bad = 0; vals = {}
for m in range(1, 1500):
    v = nu(m); 
    if m % 14 == 0 and gcd(m // 14, 6) == 1: pred = 2
    elif m % 14 == 0 or m % 21 == 0: pred = 1
    else: pred = 0
    vals[pred] = vals.get(pred, 0) + 1
    if v != pred: bad += 1
out['nu2314'] = {'sources_tested': 1499, 'violations': bad, 'counts': vals}
# 72 from source 1
H = hist.histories(1, 72)
out['h72'] = [list(h) for h in H]
json.dump(out, open('../results/c5_checks.json', 'w'), indent=1)
print(out['Lcomp'], out['Ledge'], out['nu2314'], out['h72'])
