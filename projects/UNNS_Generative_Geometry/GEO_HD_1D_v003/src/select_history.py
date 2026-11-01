"""HD-1D v001 builder layer: SELECT-II transitions, valuations, occurrence fibres, histories.  Exact integer arithmetic only.

T_N(m) = m (N+1)^2 / N  for N | m, N >= 1.   Predecessors of t: d >= 2, d^2 | t, m = t (d-1) / d^2 (label N = d-1).
"""
from functools import lru_cache
from itertools import product


@lru_cache(maxsize=None)
def factor(n):
    """prime factorisation as a tuple of (p, e) sorted; trial division (n up to ~1e13 is fine)."""
    assert n >= 1
    out = []; p = 2
    while p * p <= n:
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p; e += 1
            out.append((p, e))
        p += 1 if p == 2 else 2
    if n > 1:
        out.append((n, 1))
    return tuple(out)


def val(n):
    """valuation vector as dict {p: v_p(n)} (only positive entries)"""
    return dict(factor(n))


def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p; e += 1
    return e


def is_squarefree(n):
    return all(e == 1 for _, e in factor(n))


def T(N, m):
    """the transition m -> m (N+1)^2 / N; raises ValueError when N does not divide m"""
    if N < 1 or m % N:
        raise ValueError("label %d not admissible at state %d" % (N, m))
    return m // N * (N + 1) ** 2


def divisors(n):
    ds = [1]
    for p, e in factor(n):
        ds = [d * p ** k for d in ds for k in range(e + 1)]
    return sorted(ds)


def admissible_labels(m):
    """all labels N >= 1 with N | m"""
    return divisors(m)


def successors(m):
    return [(N, T(N, m)) for N in admissible_labels(m)]


def delta(N):
    """valuation displacement of label N as a dict {p: 2 v_p(N+1) - v_p(N)} (zero entries dropped)"""
    d = {}
    for p, e in factor(N):
        d[p] = d.get(p, 0) - e
    for p, e in factor(N + 1):
        d[p] = d.get(p, 0) + 2 * e
    return {p: x for p, x in d.items() if x}


def square_divisors_d(t):
    """all d >= 2 with d^2 | t, increasing"""
    f = factor(t)
    ranges = [range(0, e // 2 + 1) for _, e in f]
    ds = []
    for exps in product(*ranges):
        d = 1
        for (p, _), b in zip(f, exps):
            d *= p ** b
        if d >= 2:
            ds.append(d)
    return sorted(ds)


def predecessors(t):
    """[(label N, predecessor state m)] for all edges m --N--> t"""
    return [(d - 1, t // (d * d) * (d - 1)) for d in square_divisors_d(t)]


def run(m0, labels):
    """states m_0..m_l of the history (m0; labels); ValueError if some label is inadmissible"""
    st = [m0]
    for N in labels:
        st.append(T(N, st[-1]))
    return st


def is_admissible(m0, labels):
    m = m0
    for N in labels:
        if m % N:
            return False
        m = m // N * (N + 1) ** 2
    return True


def endpoint(m0, labels):
    return run(m0, labels)[-1]


def half_valuation(m):
    """e(m) = (floor(v_p(m)/2))_p as a sorted tuple of (p, e) with e > 0.  Determines the occurrence fibre D(m) and conversely."""
    return tuple((p, e // 2) for p, e in factor(m) if e // 2)


def s_of(m):
    s = 1
    for p, e in factor(m):
        s *= p ** (e // 2)
    return s


def fibre(m):
    """D(m) = {d >= 2 : d | s(m)} as a sorted tuple"""
    return tuple(d for d in divisors(s_of(m)) if d >= 2)


def complete_histories(t):
    """all complete histories (squarefree source, labels) ending at t, built backwards from the predecessor characterisation"""
    if is_squarefree(t):
        yield (t, ())
        return
    for N, m in predecessors(t):
        for (m0, labs) in complete_histories(m):
            yield (m0, labs + (N,))
