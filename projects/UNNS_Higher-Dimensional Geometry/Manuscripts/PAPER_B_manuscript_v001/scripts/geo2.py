#!/usr/bin/env python3
"""geo2.py -- independent exact engine for Paper B (binary 0/1 Graver-cell model).

Written for Paper B; it does NOT import any GEO-I release code.  Pure standard library.
Conventions
  * a code C <= F_2^n is a set of n-bit integers (bit i = coordinate i);
  * a *point set* X = [x_0,...,x_{n-1}] of k-bit integers spans F_2^k; the code is
    C(X) = { w_f : f in F_2^k },  w_f = sum_i parity(f & x_i) << i      (dim C = k when X spans);
  * AG(k-1,2) = { x in F_2^k : top bit (1<<(k-1)) set }.
"""
from itertools import combinations
from collections import defaultdict


def par(x):
    return bin(x).count("1") & 1


def rank_bits(vs):
    b = []
    for v in vs:
        for c in b:
            v = min(v, v ^ c)
        if v:
            b.append(v)
    return len(b)


def weight(w):
    return bin(w).count("1")


# ----------------------------------------------------------------------------- codes
def code_from_points(X):
    k = max(x.bit_length() for x in X)
    words = {}
    for f in range(1 << k):
        w = 0
        for i, x in enumerate(X):
            if par(f & x):
                w |= 1 << i
        words[f] = w
    return words, k


def span_words(gens):
    S = {0}
    for g in gens:
        S |= {s ^ g for s in S}
    return S


def nonzero_words(C):
    return sorted(w for w in C if w)


def circuits_of(C):
    """minimal supports of nonzero words (brute force from the definition)"""
    nz = nonzero_words(C)
    return [w for w in nz if not any(v != w and (v & w) == v for v in nz)]


def circuits_by_rank(X, k):
    """circuit test used for cross-checking: w_f is a circuit iff rank(X cap f-perp)=k-1"""
    out = []
    for f in range(1, 1 << k):
        zero = [x for x in X if not par(f & x)]
        supp = [x for x in X if par(f & x)]
        if supp and rank_bits(zero) == k - 1:
            out.append(sum(par(f & x) << i for i, x in enumerate(X)))
    return sorted(set(out))


# ----------------------------------------------------------------------------- partitions / E1
def disjoint_families(circs):
    """all non-empty sets of pairwise disjoint circuits, as (union, tuple(sorted circuits))"""
    circs = sorted(circs)
    res = []

    def rec(start, used, chosen):
        for j in range(start, len(circs)):
            c = circs[j]
            if c & used == 0:
                ch = chosen + [c]
                res.append((used | c, tuple(ch)))
                rec(j + 1, used | c, ch)

    rec(0, 0, [])
    return res


def partitions_by_union(circs):
    d = defaultdict(list)
    for U, fam in disjoint_families(circs):
        d[U].append(fam)
    return d


def is_nonembedded_E1(circs):
    """Theorem E1: non-embedded iff some set U has two distinct partitions into circuits"""
    return any(len(v) >= 2 for v in partitions_by_union(circs).values())


def partitions_of(circs, target):
    """all partitions of the word `target` into pairwise disjoint circuits"""
    circs = sorted(c for c in circs if c & ~target == 0)
    out = []

    def rec(rem, chosen):
        if rem == 0:
            out.append(tuple(sorted(chosen)))
            return
        low = rem & -rem
        for c in circs:
            if c & low and c & ~rem == 0:
                rec(rem & ~c, chosen + [c])

    rec(target, [])
    return out


def shorten_circuits(circs, i):
    """circuits of the shortened code (words vanishing at coordinate i) = circuits avoiding i"""
    return [c for c in circs if not (c >> i) & 1]


def is_minimal_nonembedded(circs, n):
    if not is_nonembedded_E1(circs):
        return False
    return all(not is_nonembedded_E1(shorten_circuits(circs, i)) for i in range(n))


# ----------------------------------------------------------------------------- cells / collisions (definition level)
def cells(C, n):
    """all Graver cells (S,x): S non-empty set of pairwise disjoint circuits, x in C \\ span S modulo span S.
    returns dict key=(S, canonical x) -> (U, offU_pattern)"""
    circs = circuits_of(C)
    out = {}
    for U, fam in disjoint_families(circs):
        sp = span_words(fam)
        seen = set()
        for x in C:
            if x in sp:
                continue
            rep = min(x ^ s for s in sp)
            if rep in seen:
                continue
            seen.add(rep)
            out[(fam, rep)] = (U, x & ~U)
    return out


def generators(fam, x, n):
    """rows of the generator matrix: g_j = (1-2x_i) on S_j, 0 elsewhere (integer vectors)"""
    G = []
    for c in fam:
        G.append([(1 - 2 * ((x >> i) & 1)) if (c >> i) & 1 else 0 for i in range(n)])
    return G


def rank_int(rows):
    from fractions import Fraction
    M = [[Fraction(v) for v in r] for r in rows]
    r = 0
    ncol = len(M[0]) if M else 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def collisions(C, n):
    """all unordered pairs of distinct cells with the same union and the same pattern off the union"""
    cl = cells(C, n)
    groups = defaultdict(list)
    for key, (U, off) in cl.items():
        groups[(U, off)].append(key)
    res = []
    for g in groups.values():
        for a, b in combinations(g, 2):
            res.append((a, b))
    return res


def collision_rank(a, b, n):
    (S, x), (T, y) = a, b
    return rank_int(generators(S, x, n) + generators(T, y, n))


# ----------------------------------------------------------------------------- vector-space partition data
def one_partitions(circs, n):
    full = (1 << n) - 1
    return partitions_of(circs, full)


def block_span(P):
    return span_words(list(P))


def n2_count(parts):
    return sum(1 for P in parts if len(P) == 2)


def check_identities(X, k):
    """returns dict with p, k, number of partitions, counting identity, Parseval identity, n2"""
    n = len(X)
    C, _ = code_from_points(X)
    Cw = set(C.values())
    circs = circuits_of(Cw)
    full = (1 << n) - 1
    assert full in Cw
    parts = one_partitions(circs, n)
    cnt = sum((1 << len(P)) - 2 for P in parts)
    # Parseval: sum_P (2^{m_P} S_P - 2 p^2) = p (2^k - 2p)
    pars = 0
    for P in parts:
        S_P = sum(weight(c) ** 2 for c in P)
        pars += (1 << len(P)) * S_P - 2 * n * n
    # vector space partition of C/<1>: every w not in {0,1} lies in exactly one V_P
    owner = defaultdict(int)
    spans = [block_span(P) for P in parts]
    for sp in spans:
        for w in sp:
            if w not in (0, full):
                owner[w] += 1
    vsp = all(owner.get(w, 0) == 1 for w in Cw if w not in (0, full))
    # pairwise intersections of V_P are {0,1}
    pair_ok = all(spans[i] & spans[j] == {0, full} for i in range(len(spans)) for j in range(i + 1, len(spans)))
    return dict(p=n, k=k, parts=len(parts), m=sorted(len(P) for P in parts), counting=(cnt == (1 << k) - 2),
                parseval=(pars == n * ((1 << k) - 2 * n)), vsp=vsp, pair_ok=pair_ok, n2=n2_count(parts))


def affine_points(m):
    return [x for x in range(1 << (m + 1)) if x >> m & 1]
