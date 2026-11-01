"""HD-1D v002 builder: admissibility thresholds K(w), threshold graphs, lcm-closure classification of swap classes.

Theorem D-T7:  an ordering w = (N_1..N_l) is admissible from m  <=>  K(w) | m,  K(w) = prod_p p^{b_p},
               b_p = max(0, max_j -sum_{i<=j} Delta_p(N_i)),  Delta_p(N) = 2 v_p(N+1) - v_p(N).
"""
from math import lcm
from itertools import permutations
from select_history import factor


def _delta_table(labels):
    tab = {}
    for N in set(labels):
        d = {}
        for p, e in factor(N): d[p] = d.get(p, 0) - e
        for p, e in factor(N + 1): d[p] = d.get(p, 0) + 2 * e
        tab[N] = d
    return tab


def K(w, tab=None):
    tab = tab or _delta_table(w)
    primes = set()
    for N in w: primes |= set(tab[N])
    k = 1
    for p in primes:
        s = b = 0
        for N in w:
            s += tab[N].get(p, 0)
            if -s > b: b = -s
        k *= p ** b
    return k


def arrangements(content):
    return sorted(set(permutations(sorted(content))))


def threshold_table(content):
    arr = arrangements(content); tab = _delta_table(content)
    return {w: K(w, tab) for w in arr}


def neighbours(w):
    for i in range(len(w) - 1):
        if w[i] != w[i + 1]:
            yield w[:i] + (w[i + 1], w[i]) + w[i + 2:]


def components(vertices):
    vs = set(vertices); seen = set(); comps = []
    for v in sorted(vs):
        if v in seen: continue
        stack = [v]; seen.add(v); c = [v]
        while stack:
            x = stack.pop()
            for y in neighbours(x):
                if y in vs and y not in seen: seen.add(y); stack.append(y); c.append(y)
        comps.append(sorted(c))
    return comps


def classes_at(thr, m):
    """swap classes (components) of the admissible arrangements of the content at source m; thr = threshold_table"""
    return components([w for w, k in thr.items() if m % k == 0])


def lcm_closure(values, cap=200000):
    """all lcms of non-empty subsets of the given numbers (the only sources at which the threshold graph can change)"""
    S = set(values); frontier = set(values)
    while frontier:
        new = set()
        for a in frontier:
            for b in list(S):
                c = lcm(a, b)
                if c not in S: new.add(c)
        S |= new; frontier = new
        if len(S) > cap: raise OverflowError("closure too large")
    return sorted(S)


def split_sources(content):
    """minimal (w.r.t. divisibility) closure sources m at which the content has >= 2 swap classes; plus the closure size"""
    thr = threshold_table(content)
    cl = lcm_closure(set(thr.values()))
    split = [m for m in cl if len(classes_at(thr, m)) >= 2]
    mins = [m for m in split if not any(n != m and m % n == 0 for n in split)]
    return thr, cl, split, mins


def connect_thresholds(thr, w1, w2):
    """minimal divisibility thresholds M with w1,w2 swap-connected at every source divisible by M (antichain), via label-correcting search over the permutation graph"""
    best = {w1: {thr[w1]}}
    work = [w1]
    def minimal(S):
        return {a for a in S if not any(b != a and a % b == 0 for b in S)}
    while work:
        x = work.pop()
        for y in neighbours(x):
            if y not in thr: continue
            cand = {lcm(a, thr[y]) for a in best[x]}
            cur = best.get(y, set())
            new = minimal(cur | cand)
            if new != cur:
                best[y] = new; work.append(y)
    return sorted(best.get(w2, set()))
