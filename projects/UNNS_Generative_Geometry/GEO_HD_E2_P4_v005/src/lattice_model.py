"""Pure-lattice models for E2-P4 v002 (P4-E3 planar, P4-E4 spatial).  A lattice-only candidate is NEVER a FIELD-I result (spec 7.4).
Lattices of Z^k are given by Hermite normal form; membership by back-substitution.  Cells/unions use the pinned engine."""
from itertools import product
from math import gcd

import _boot  # noqa: F401
import coverage_gap as cg
import exact_containment as ec


def hnf2(n):
    """All sublattices of Z^2 of index n: basis ((a,x),(0,b)), a*b=n, 0<=x<b... rows (a,x),(0,b)."""
    out = []
    for a in range(1, n + 1):
        if n % a == 0:
            b = n // a
            for x in range(b):
                out.append(((a, x), (0, b)))
    return out


def hnf3(n):
    out = []
    for a in range(1, n + 1):
        if n % a:
            continue
        for b in range(1, n // a + 1):
            if (n // a) % b:
                continue
            c = n // (a * b)
            for x in range(b):
                for y in range(c):
                    for z in range(c):
                        out.append(((a, x, y), (0, b, z), (0, 0, c)))
    return out


def member2(B):
    (a, x), (_, b) = B

    def f(v):
        i, r = divmod(v[0], a)
        return r == 0 and (v[1] - i * x) % b == 0
    return f


def member3(B):
    (a, x, y), (_, b, z), (_, _, c) = B

    def f(v):
        i, r = divmod(v[0], a)
        if r:
            return False
        v1, v2 = v[1] - i * x, v[2] - i * y
        j, r = divmod(v1, b)
        if r:
            return False
        return (v2 - j * z) % c == 0
    return f


def index_of(B):
    p = 1
    for i, row in enumerate(B):
        p *= row[i]
    return p


def reduce_basis(B):
    """Canonical HNF key is the basis itself (hnf enumerations are canonical)."""
    return tuple(tuple(r) for r in B)


def subset_lattice(inner, outer, k, bound):
    """inner subset outer?  Test on inner's HNF basis rows."""
    return all(outer(tuple(r)) for r in inner_rows(inner))


def inner_rows(B):
    return B


def cells_of_member(inL, q):
    k = len(q)
    F = tuple(sorted(v for v in product(*[range(m + 1) for m in q]) if any(v) and inL(v)))
    L = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and inL(v)]
    G = [v for v in L if not any(w != v and all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(w, v)) for w in L)]
    cx = cg.ct0.build_complex(F, cg.ft.oriented(G), k)
    return F, [(tuple(c.base), tuple(tuple(g) for g in c.gens)) for j in cx for c in cx[j].values()]


def compare_lattices(inL, outL, q, node_limit=100000):
    """Exact U(inner) <= U(outer) with certificate; inner must be a sublattice of outer."""
    k = len(q)
    F, cs = cells_of_member(inL, q)
    F2, ct = cells_of_member(outL, q)
    if not F:
        return {"verdict": "EMPTY_SOURCE", "n_F": 0, "n_F2": len(F2)}
    r = ec.decide_union(cs, ct, k, node_limit)
    r["n_F"], r["n_F2"] = len(F), len(F2)
    return r


# ----------------------------------------------------------------------------------------------- decomposability (v002)
def _reduce3(v, B):
    (a, x, y), (_, b, z), (_, _, c) = B
    v = list(v)
    i = v[0] // a
    v = [v[0] - i * a, v[1] - i * x, v[2] - i * y]
    j = v[1] // b
    v = [v[0], v[1] - j * b, v[2] - j * z]
    k = v[2] // c
    return (v[0], v[1], v[2] - k * c)


def _sub_index3(B, S):
    """|image of Z^S in Z^3/L| = [Z^S : L cap Z^S]."""
    zero = (0, 0, 0)
    seen = {zero}
    fr = [zero]
    while fr:
        h = fr.pop()
        for i in S:
            e = [0, 0, 0]
            e[i] = 1
            n = _reduce3(tuple(a + b for a, b in zip(h, e)), B)
            if n not in seen:
                seen.add(n)
                fr.append(n)
    return len(seen)


def decomposable3(B):
    """L = (L cap Z^S) (+) (L cap Z^T) for some partition S|T of the three coordinates (then L is a product lattice)."""
    n = index_of(B)
    for S in ((0,), (1,), (2,)):
        T = tuple(i for i in range(3) if i not in S)
        if _sub_index3(B, S) * _sub_index3(B, T) == n:
            return True
    return False


def free_coordinates3(inL):
    out = []
    for i in range(3):
        e = [0, 0, 0]
        e[i] = 1
        if inL(tuple(e)):
            out.append(i)
    return out
