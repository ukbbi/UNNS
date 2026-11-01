"""HD-1D v004 builder: elementary block replacements u <-> v with R(u) = R(v), executed inside longer histories.

A block replacement at position i of an admissible history h = p.u.s from source m is legal iff p.v.s is admissible from m.
Because R(u) = R(v) the two histories have the same endpoint and the same state after the block, so the condition is exactly
'v is admissible from the state x_p reached after the prefix p'  (Theorem D4-T3, source-relative form); i.e. K(v) | x_p."""
from itertools import permutations
from math import lcm
from thresholds import K


def word_arrangements(parts):
    """all distinct arrangements of the multiset given as [(label, count)]"""
    base = []
    for N, c in parts: base += [N] * c
    return sorted(set(permutations(base)))


def state_after(m, w):
    for N in w:
        if m % N: return None
        m = m // N * (N + 1) ** 2
    return m


def admissible(m, w): return state_after(m, w) is not None


def move_blocks(labels, z):
    """(minus_parts, plus_parts): contents z^- and z^+ of a kernel vector z"""
    return [(N, -c) for N, c in zip(labels, z) if c < 0], [(N, c) for N, c in zip(labels, z) if c > 0]


def rewrite_neighbours(w, m, blocks):
    """all histories reachable from the admissible word w by ONE legal block replacement along any of the given moves
    blocks = list of (left_words, right_words): the replacement  u <-> v  for u in left_words, v in right_words (both directions)"""
    out = set()
    for L, Rw in blocks:
        for A, B in ((L, Rw), (Rw, L)):
            Aset = set(A); la = len(A[0])
            for i in range(len(w) - la + 1):
                if w[i:i + la] in Aset:
                    for v in B:
                        w2 = w[:i] + v + w[i + la:]
                        if w2 != w and admissible(m, w2): out.add(w2)
    return out


def rewrite_threshold(u, v):
    """lcm(K(u), K(v)): the executability threshold of u <-> v at the BEGINNING of a history (D4-T3)"""
    return lcm(K(u), K(v))
