"""Exact SELECT-II history engine (stdlib): histories from a source to an endpoint, swap classes."""
import sys, itertools
from math import gcd
from fractions import Fraction as Fr
def sqdivs(t):
    d = 2; out = []
    while d * d <= t:
        if t % (d * d) == 0: out.append(d)
        d += 1
    return out
_cache = {}
def histories(m0, t):
    """all histories (m0; w) ending at t as tuples of labels"""
    key = (m0, t)
    if key in _cache: return _cache[key]
    res = []
    if t == m0: res.append(())
    for d in sqdivs(t):
        N = d - 1; m = t * (d - 1) // (d * d)
        if m < m0: continue
        for w in histories(m0, m): res.append(w + (N,))
    _cache[key] = res
    return res
def admissible(m0, w):
    x = Fr(m0)
    for N in w:
        if x.denominator != 1 or x.numerator % N: return False
        x = x * Fr((N + 1) ** 2, N)
    return True
def classes(m0, t):
    H = histories(m0, t); idx = {w: i for i, w in enumerate(H)}; par = list(range(len(H)))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for w in H:
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]:
                v = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                if v in idx: par[f(idx[w])] = f(idx[v])
    comp = {}
    for i, w in enumerate(H): comp.setdefault(f(i), []).append(w)
    return H, list(comp.values())
if __name__ == '__main__':
    for t in (72,):
        for m0 in (1, 3, 10):
            H, C = classes(m0, t); print(t, m0, len(H), len(C), H)
    H, C = classes(4, 9000); print(9000, len(H), len(C))

def content(w):
    from collections import Counter
    return tuple(sorted(Counter(w).items()))
def rewrite_classes(m0, t, moves, restrict=None):
    """components of histories (m0 -> t) under swaps and block rewrites; moves = list of (plus_multiset, minus_multiset)"""
    H = histories(m0, t)
    if restrict: H = [w for w in H if restrict(w)]
    idx = {w: i for i, w in enumerate(H)}; par = list(range(len(H)))
    def f(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    def uni(a, b):
        if b in idx: par[f(idx[a])] = f(idx[b])
    for w in H:
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]: uni(w, w[:i] + (w[i + 1], w[i]) + w[i + 2:])
        for (u, v) in moves:
            for (a, b) in ((u, v), (v, u)):
                la = sum(a.values())
                for i in range(len(w) - la + 1):
                    from collections import Counter
                    if Counter(w[i:i + la]) == Counter(a):
                        for arr in set(itertools.permutations(sorted(b.elements()))):
                            uni(w, w[:i] + tuple(arr) + w[i + la:])
    comp = {}
    for i, w in enumerate(H): comp.setdefault(f(i), []).append(w)
    return H, list(comp.values())
