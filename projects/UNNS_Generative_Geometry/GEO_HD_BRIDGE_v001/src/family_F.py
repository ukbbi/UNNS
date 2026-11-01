"""Addendum to D4-T7 (all-j): the family F_j :  U_j = {2^4, 3^j}  <->  V_j = {1, 8, 8, 3^j}   (move z=(1,-4,0,2) on {1,2,3,8}).
Fresh implementation (no import of the v004 verifier).  R(2)^4 = R(1) R(8)^2 = 3^8/2^4."""
from math import comb


def admissible_words(m, content):
    """all admissible orderings of the multiset `content` (dict label->count) from source m"""
    labs = sorted(content); out = []
    def rec(m, cnt, acc):
        if not any(cnt.values()): out.append(tuple(acc)); return
        for N in labs:
            if cnt[N] and m % N == 0:
                cnt[N] -= 1; acc.append(N); rec(m // N * (N + 1) ** 2, cnt, acc); acc.pop(); cnt[N] += 1
    rec(m, dict(content), []); return out


def contents(j): return {"U": {2: 4, 3: j}, "V": {1: 1, 8: 2, 3: j}}


def uf_classes(words, edges):
    idx = {w: i for i, w in enumerate(words)}; par = list(range(len(words)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for w, w2 in edges:
        if w2 in idx: par[f(idx[w])] = f(idx[w2])
    return len({f(i) for i in range(len(words))}), f, idx


def swap_edges(words):
    for w in words:
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]: yield w, w[:i] + (w[i + 1], w[i]) + w[i + 2:]


def rewrite_edges(words):
    """block replacement 2222 <-> any arrangement of {1,8,8}"""
    arrV = [(1, 8, 8), (8, 1, 8), (8, 8, 1)]
    for w in words:
        for i in range(len(w) - 3):
            if w[i:i + 4] == (2, 2, 2, 2):
                for v in arrV: yield w, w[:i] + v + w[i + 4:]
        for i in range(len(w) - 2):
            if w[i:i + 3] in arrV: yield w, w[:i] + (2, 2, 2, 2) + w[i + 3:]


def analyse(a, b, j):
    m = 2 ** a * 3 ** b; c = contents(j)
    WU = admissible_words(m, c["U"]); WV = admissible_words(m, c["V"]); W = WU + WV
    n_sw, f, idx = uf_classes(W, swap_edges(W))
    swU = len({f(idx[w]) for w in WU}); swV = len({f(idx[w]) for w in WV})
    n_rw, _, _ = uf_classes(W, list(swap_edges(W)) + list(rewrite_edges(W)))
    return {"realU": bool(WU), "realV": bool(WV), "swapU": swU, "swapV": swV, "rewrite_classes": n_rw, "nU": len(WU), "nV": len(WV)}


def predicted(a, b, j):
    real = (b + 8 >= j) and not (a == 0 and b == 0)
    return {"realizable": real, "connected": (b >= 1 or a >= 4)}


def witnesses(a, b, j):
    """explicit words used in the proof"""
    if b >= 1: return {"U": (3,) + (2,) * 4 + (3,) * (j - 1), "V": (3, 1, 8, 8) + (3,) * (j - 1)}
    return {"U": (2, 3, 2, 2, 2) + (3,) * (j - 1), "V": (1, 8, 3, 8) + (3,) * (j - 1)}
