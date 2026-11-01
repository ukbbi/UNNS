"""HD-1D v004 builder: the swap / rewrite graph of the histories of a content fibre from a fixed source, with exact component counts and
the quotient graph (nodes = swap classes, edges = exposable blocks)."""
from collections import defaultdict
from valuation_matrix import product_P
from block_rewrites import word_arrangements, move_blocks, admissible, rewrite_neighbours, state_after


def words_of(m, labels, content):
    out = []
    def rec(m, cnt, acc):
        if not any(cnt): out.append(tuple(acc)); return
        for i, N in enumerate(labels):
            if cnt[i] and m % N == 0:
                cnt[i] -= 1; acc.append(N); rec(m // N * (N + 1) ** 2, cnt, acc); acc.pop(); cnt[i] += 1
    rec(m, list(content), []); return out


def fibre_contents(base, z, L):
    return [tuple(b + k * c for b, c in zip(base, z)) for k in range(L)]


class UF:
    def __init__(self, n): self.p = list(range(n))
    def f(self, x):
        while self.p[x] != x: self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def u(self, a, b): self.p[self.f(a)] = self.f(b)


def analyse(m, labels, moves, contents):
    """returns dict: n (words), swap (list of classes as lists of word indices), rewrite (classes), words, content_of"""
    W = []; cof = []
    for c in contents:
        ws = words_of(m, labels, c); W += ws; cof += [c] * len(ws)
    idx = {w: i for i, w in enumerate(W)}
    sw = UF(len(W))
    for w in W:
        for i in range(len(w) - 1):
            if w[i] != w[i + 1]:
                w2 = w[:i] + (w[i + 1], w[i]) + w[i + 2:]
                j = idx.get(w2)
                if j is not None: sw.u(idx[w], j)
    blocks = []
    for z in moves:
        mi, pl = move_blocks(labels, z); blocks.append((word_arrangements(mi), word_arrangements(pl)))
    rw = UF(len(W))
    for i in range(len(W)): rw.u(i, sw.f(i))
    for w in W:
        for w2 in rewrite_neighbours(w, m, blocks):
            j = idx.get(w2)
            if j is not None: rw.u(idx[w], j)
    def classes(uf):
        d = defaultdict(list)
        for i in range(len(W)): d[uf.f(i)].append(i)
        return list(d.values())
    return {"words": W, "content_of": cof, "swap": classes(sw), "rewrite": classes(rw), "n": len(W)}


def divisors_of_P(labels, contents):
    """all divisors d of P* = lcm_c P(c) (the only sources that matter, by the gcd reduction)"""
    from math import lcm
    P = 1
    for c in contents: P = lcm(P, product_P(labels, c))
    ds = [d for d in range(1, P + 1) if P % d == 0] if P < 10 ** 6 else None
    return P, ds
