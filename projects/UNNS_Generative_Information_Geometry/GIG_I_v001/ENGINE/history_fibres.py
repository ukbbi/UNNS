"""GIG-I v001 -- history fibres of the SELECT-II operator.

Self-contained (standard library only); exact integer arithmetic throughout.

Frozen definitions reused (SELECT-II / GEO-HD-1D):
  T_N(m) = m (N+1)^2 / N  for a label N >= 1 with N | m.
  A history is a pair (m0, labels): a source m0 and an ordered label word admissible from m0.
  A history is COMPLETE when its source m0 is squarefree (the source then has no predecessor).
Source conventions (every function states which one it uses):
  complete-history fibre  F_t       : all complete histories ending at t         (sources vary)
  fixed-source fibre      F_t(m0)   : all histories from the given m0 ending at t (m0 need not be squarefree)
"""
from functools import lru_cache
from fractions import Fraction
from itertools import product
from math import lcm


# ----------------------------------------------------------------- arithmetic
@lru_cache(maxsize=None)
def factor(n):
    """prime factorisation of n >= 1 as a sorted tuple of (p, e); trial division."""
    assert n >= 1
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return tuple(out)


def is_squarefree(n):
    return all(e == 1 for _, e in factor(n))


def R(N):
    """multiplier R(N) = (N+1)^2 / N as an exact Fraction."""
    return Fraction((N + 1) ** 2, N)


def T(N, m):
    """forward SELECT-II step; ValueError if the label is not admissible at m."""
    if N < 1 or m % N:
        raise ValueError("label %d not admissible at state %d" % (N, m))
    return m // N * (N + 1) ** 2


def square_divisor_d(t):
    """all d >= 2 with d^2 | t, increasing."""
    f = factor(t)
    ds = []
    for exps in product(*[range(e // 2 + 1) for _, e in f]):
        d = 1
        for (p, _), b in zip(f, exps):
            d *= p ** b
        if d >= 2:
            ds.append(d)
    return sorted(ds)


def reverse_edges(t):
    """GIG-T1 lemma: all edges m --N--> t as pairs (N, m).
    An edge with label N exists  iff  (N+1)^2 | t,  and then  m = N t / (N+1)^2."""
    return [(d - 1, (d - 1) * (t // (d * d))) for d in square_divisor_d(t)]


# ------------------------------------------------------------------ histories
def is_admissible(m0, labels):
    """step-by-step simulation (does NOT use the threshold formula)."""
    m = m0
    for N in labels:
        if m % N:
            return False
        m = m // N * (N + 1) ** 2
    return True


def states(m0, labels):
    st = [m0]
    for N in labels:
        st.append(T(N, st[-1]))
    return st


def endpoint(m0, labels):
    return states(m0, labels)[-1]


def content(labels):
    """generating content: the sorted multiset of labels."""
    return tuple(sorted(labels))


def threshold(labels):
    """K(w) = prod_p p^{max(0, max_j -sum_{i<=j} Delta_p(N_i))}, Delta_p(N) = 2 v_p(N+1) - v_p(N).
    An ordered word w is admissible from m  iff  K(w) | m  (frozen GEO-HD-1D law D-T7); used here
    only for the independent cross-check of the simulation-based admissibility."""
    primes = set()
    for N in set(labels):
        primes |= {p for p, _ in factor(N)} | {p for p, _ in factor(N + 1)}
    k = 1
    for p in primes:
        s = best = 0
        for N in labels:
            d = 2 * _vp(N + 1, p) - _vp(N, p)
            s += d
            if -s > best:
                best = -s
        k *= p ** best
    return k


def _vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


# ---------------------------------------------------- complete-history fibres
def complete_histories(t):
    """generator of all complete histories (m0, labels) ending at t (complete-history fibre F_t)."""
    if is_squarefree(t):
        yield (t, ())
        return
    for N, m in reverse_edges(t):
        for m0, labs in complete_histories(m):
            yield (m0, labs + (N,))


@lru_cache(maxsize=None)
def count_complete(t):
    """|F_t| by memoised dynamic programming (no history is materialised)."""
    if is_squarefree(t):
        return 1
    return sum(count_complete(m) for _, m in reverse_edges(t))


@lru_cache(maxsize=None)
def count_complete_by_source(t):
    """dict {source m0: number of complete histories from m0 to t} (a refinement of count_complete)."""
    if is_squarefree(t):
        return {t: 1}
    out = {}
    for _, m in reverse_edges(t):
        for s, c in count_complete_by_source(m).items():
            out[s] = out.get(s, 0) + c
    return out


# ------------------------------------------------------- fixed-source fibres
def fixed_source_histories(m0, t):
    """generator of all histories from m0 to t (fixed-source fibre F_t(m0)); backward search, pruned by
    the exact bound t/m >= 4 per step (GIG-T1)."""
    def rec(s, labs):
        if s == m0:
            yield (m0, labs)
            return
        if s < 4 * m0:
            return
        for N, m in reverse_edges(s):
            if m >= m0:
                yield from rec(m, (N,) + labs)
    yield from rec(t, ())


@lru_cache(maxsize=None)
def count_fixed_source(m0, t):
    if t == m0:
        return 1
    if t < 4 * m0:
        return 0
    return sum(count_fixed_source(m0, m) for _, m in reverse_edges(t) if m >= m0)


# --------------------------------------------------------------- classification
def classify(histories):
    """group histories by (source, content): the 'pieces' of a fibre. Returns dict (m0, content)->list."""
    out = {}
    for h in histories:
        out.setdefault((h[0], content(h[1])), []).append(h)
    return out
