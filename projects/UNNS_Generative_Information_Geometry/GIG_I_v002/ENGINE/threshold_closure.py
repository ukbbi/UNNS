"""GIG-I v002 -- arithmetic closure of admissible arrangement sets (theorem GIG-T12).

For a content C of k distinct labels (sorted) and a permutation p (arrangement), the threshold law D-T7 gives
    K(w) | m   <=>   w admissible from source m,           K(w) = prod_q q^{e_q(w)}.
Hence A_C(m) = { w : e_q(w) <= v_q(m) for every prime q } = INTERSECTION over primes q of the level sets
    M_{q,e} = { w : e_q(w) <= e }  at e = v_q(m).
Everything below is exact integer / bitmask arithmetic (bit i <-> i-th permutation of history_complex.perms(k)).
"""
import _v1path  # noqa: F401
from math import lcm
import history_complex as hc
from history_fibres import factor


def _vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def word(labels, p):
    return tuple(labels[i] for i in p)


def exponent_table(labels):
    """{prime q: [e_q(w) for w in perms(k)]} for the arrangement words of the sorted content `labels`.
    e_q(w) = max(0, max_j -sum_{i<=j} Delta_q(N_i)),  Delta_q(N) = 2 v_q(N+1) - v_q(N).  Only primes with some e_q > 0 are kept."""
    labs = sorted(labels)
    k = len(labs)
    primes = set()
    for N in labs:
        primes |= {q for q, _ in factor(N)} | {q for q, _ in factor(N + 1)}
    delta = {q: [2 * _vp(N + 1, q) - _vp(N, q) for N in labs] for q in primes}
    P = hc.perms(k)
    tab = {}
    for q in sorted(primes):
        d = delta[q]
        col = []
        for p in P:
            s = best = 0
            for i in p:
                s += d[i]
                if -s > best:
                    best = -s
            col.append(best)
        if any(col):
            tab[q] = col
    return tab


def level_masks(labels):
    """{q: [(e, M_{q,e}) ...]} for the distinct values e of e_q (increasing); the last mask is full."""
    tab = exponent_table(labels)
    out = {}
    for q, col in tab.items():
        lv = []
        for e in sorted(set(col)):
            m = 0
            for i, x in enumerate(col):
                if x <= e:
                    m |= 1 << i
            lv.append((e, m))
        out[q] = lv
    return out


def threshold_values(labels):
    """K(w) for every arrangement (list aligned with perms(k)), as integers."""
    tab = exponent_table(labels)
    n = len(hc.perms(len(labels)))
    K = [1] * n
    for q, col in tab.items():
        for i, e in enumerate(col):
            if e:
                K[i] *= q ** e
    return K


def realizable_masks_of_content(labels):
    """ALL nonempty sets A_C(m), m = 1,2,3,... , as a set of bitmasks (exhaustive: m only matters through v_q(m) for
    the finitely many primes q with e_q != 0, and only up to the largest value of e_q)."""
    k = len(labels)
    cur = {(1 << len(hc.perms(k))) - 1}
    for q, lv in level_masks(labels).items():
        cur = {m & M for m in cur for _, M in lv}
    cur.discard(0)
    return cur


def minimal_source_exponents(labels, mask):
    """{q: v_q(L(S))} for S = mask: the least e with S subset of M_{q,e}  (L(S) = lcm of K(w), w in S)."""
    out = {}
    for q, lv in level_masks(labels).items():
        for e, M in lv:
            if mask & ~M == 0:
                if e:
                    out[q] = e
                break
    return out


def minimal_source(labels, mask):
    """L(S) = lcm{K(w) : w in S}  (computed from level masks; equals the lcm of the thresholds, see tests)."""
    L = 1
    for q, e in minimal_source_exponents(labels, mask).items():
        L *= q ** e
    return L


def closure(labels, mask):
    """cl_K(S) = { v : K(v) | L(S) }  -- the smallest realizable set containing S (GIG-T12)."""
    ex = minimal_source_exponents(labels, mask)
    full = (1 << len(hc.perms(len(labels)))) - 1
    r = full
    for q, lv in level_masks(labels).items():
        e = ex.get(q, 0)
        for ee, M in lv:
            if ee >= e:
                r &= M
                break
    return r


def is_closed(labels, mask):
    return mask != 0 and closure(labels, mask) == mask


def squarefree_realizable(labels, mask):
    """GIG-T12(iii): a closed S is realizable by a squarefree source iff L(S) is squarefree."""
    return is_closed(labels, mask) and all(e <= 1 for e in minimal_source_exponents(labels, mask).values())


def lcm_of_thresholds(labels, mask):
    """direct definition L(S) = lcm of K(w) over w in S (independent of the level-mask shortcut)."""
    K = threshold_values(labels)
    L = 1
    i = 0
    while mask >> i:
        if mask >> i & 1:
            L = lcm(L, K[i])
        i += 1
    return L


def source_mask(labels, m):
    """A_C(m) from the threshold law (no simulation)."""
    K = threshold_values(labels)
    mask = 0
    for i, x in enumerate(K):
        if m % x == 0:
            mask |= 1 << i
    return mask


class ContentClosure:
    """cached closure machinery for one content (avoids recomputing level masks)."""

    def __init__(self, labels):
        self.labels = tuple(sorted(labels))
        self.k = len(self.labels)
        self.levels = level_masks(self.labels)
        self.full = (1 << len(hc.perms(self.k))) - 1

    def exponents(self, mask):
        out = {}
        for q, lv in self.levels.items():
            for e, M in lv:
                if mask & ~M == 0:
                    out[q] = e
                    break
        return out

    def closure(self, mask):
        r = self.full
        for q, lv in self.levels.items():
            for e, M in lv:
                if mask & ~M == 0:
                    r &= M
                    break
        return r

    def is_closed(self, mask):
        return mask != 0 and self.closure(mask) == mask

    def minimal_source(self, mask):
        L = 1
        for q, e in self.exponents(mask).items():
            if e:
                L *= q ** e
        return L
