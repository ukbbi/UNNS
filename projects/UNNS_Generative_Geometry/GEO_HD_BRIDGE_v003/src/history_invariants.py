"""R3-C/D: swap components of fixed-source fixed-content history complexes and the pair-order invariant.
Admissible word: every label N divides the current state; edge m -> m(N+1)^2/N.  Swap = adjacent transposition keeping admissibility."""
import _paths
from itertools import combinations
from collections import Counter

def words(m, content):
    """all admissible orderings of the multiset `content` (DFS, exact)."""
    cnt = Counter(content); out = []
    def rec(s, pref):
        if not any(cnt.values()): out.append(tuple(pref)); return
        for N in sorted(k for k, v in cnt.items() if v):
            if s % N: continue
            cnt[N] -= 1; pref.append(N)
            rec(s * (N + 1) ** 2 // N, pref)
            pref.pop(); cnt[N] += 1
    rec(m, [])
    return out

def swap_components(ws):
    S = set(ws); par = {w: w for w in ws}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for w in ws:
        for i in range(len(w) - 1):
            if w[i] == w[i + 1]: continue
            v = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
            if v in S: par[find(w)] = find(v)
    cl = {}
    for w in ws: cl.setdefault(find(w), []).append(w)
    return sorted(cl.values(), key=lambda c: (len(c), c))

def order_bit(w, a=2, b=4): return w.index(a) < w.index(b)

def junction_both_orders(s, N, M):
    """both N,M and M,N admissible from s (then they commute, same endpoint)."""
    def ok(a, b):
        if s % a: return False
        s1 = s * (a + 1) ** 2 // a
        return s1 % b == 0
    return ok(N, M) and ok(M, N)

def extension_chain(base=(5, 9), steps=5):
    """grow the content by appending a fresh label dividing the common endpoint (labels never in {1,2,4})"""
    A = list(base); m = 4
    for _ in range(steps):
        ws = words(m, tuple(sorted((2, 4) + tuple(A))))
        from fractions import Fraction as Fr
        E = Fr(4)
        for N in (2, 4) + tuple(A): E = E * Fr((N + 1) ** 2, N)
        assert E.denominator == 1; E = int(E)
        yield tuple(A), E
        used = set(A) | {1, 2, 4}
        L = next(d for d in range(3, E + 1) if E % d == 0 and d not in used)
        A.append(L)
    yield tuple(A), None

def analyse_content(A, m=4):
    content = tuple(sorted((2, 4) + tuple(A)))
    ws = words(m, content); cl = swap_components(ws)
    bits = [{order_bit(w) for w in c} for c in cl]
    return {'A': list(A), 'n_words': len(ws), 'components': len(cl), 'sizes': [len(c) for c in cl],
            'bit_constant_on_components': all(len(b) == 1 for b in bits),
            'both_orders_present': len({x for b in bits for x in b}) == 2,
            'first_labels': sorted({w[0] for w in ws}),
            'adjacent_2_4_in_some_word': any(abs(w.index(2) - w.index(4)) == 1 for w in ws)}
