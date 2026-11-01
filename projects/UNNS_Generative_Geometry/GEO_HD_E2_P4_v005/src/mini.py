"""v005 THIRD implementation (pure standard library, exact integers/Fractions, brute force from the DEFINITIONS only).
No numpy, no pinned engine, no shared code with geo3.py.  Intended for small boxes (<= ~(6,6,6)).
Definitions (E2-P4 DEFINITIONS.md): F(M) = (M cap [0,Q]) minus {0};  Graver set = conformally minimal nonzero vectors of M inside [-Q,Q];
a j-cell P(u;g_1..g_j) has linearly independent Graver generators and all 2^j corners in F;  U(M,Q) = union of the closed cells.
`allow_origin=True` gives the origin-allowed union U^0 (corners may be 0)."""
from fractions import Fraction as Fr
from itertools import product, combinations


def conf_le(w, v):
    return all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(w, v))


def lexpos(v):
    for x in v:
        if x:
            return x > 0
    return False


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def rank(vs):
    rows = [[Fr(x) for x in v] for v in vs]
    r = 0
    for c in range(len(rows[0]) if rows else 0):
        p = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r


def graver_region(member, Q):
    pts = [v for v in product(*[range(-q, q + 1) for q in Q]) if any(v) and member(v)]
    return [v for v in pts if not any(w != v and conf_le(w, v) for w in pts)]


def corners(u, gens):
    out = []
    for bits in product((0, 1), repeat=len(gens)):
        v = u
        for b, g in zip(bits, gens):
            if b:
                v = add(v, g)
        out.append(v)
    return out


def cells(member, Q, allow_origin=False, maxdim=None):
    k = len(Q)
    maxdim = k if maxdim is None else maxdim
    box = list(product(*[range(q + 1) for q in Q]))
    F = {v for v in box if member(v) and (allow_origin or any(v))}
    G = [g for g in graver_region(member, Q) if lexpos(g)]
    out = []
    for u in sorted(F):
        out.append((u, ()))
        c1 = [g for g in G if add(u, g) in F]
        for j in range(1, maxdim + 1):
            for gs in combinations(c1, j):
                if rank(gs) < j:
                    continue
                if all(c in F for c in corners(u, gs)):
                    out.append((u, gs))
    return out, F, G


def params(base, gens, p):
    """exact parameters t with p = base + sum t_i g_i  (Gram system), or None if p is not in the affine hull"""
    m = len(gens)
    d = [Fr(x) - Fr(y) for x, y in zip(p, base)]
    if m == 0:
        return [] if not any(d) else None
    G = [[sum(Fr(a) * Fr(b) for a, b in zip(g, h)) for h in gens] for g in gens]
    rhs = [sum(Fr(a) * x for a, x in zip(g, d)) for g in gens]
    A = [row[:] + [r] for row, r in zip(G, rhs)]
    for c in range(m):
        piv = next((i for i in range(c, m) if A[i][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for i in range(m):
            if i != c and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    t = [A[i][m] for i in range(m)]
    for j in range(len(d)):
        if sum(t[i] * gens[i][j] for i in range(m)) != d[j]:
            return None
    return t


def in_cell(base, gens, p):
    t = params(base, gens, p)
    return t is not None and all(0 <= x <= 1 for x in t)


def in_union(cell_list, p):
    p = tuple(Fr(x) for x in p)
    for base, gens in cell_list:
        lo = [base[c] + sum(min(g[c], 0) for g in gens) for c in range(len(base))]
        hi = [base[c] + sum(max(g[c], 0) for g in gens) for c in range(len(base))]
        if all(lo[c] <= p[c] <= hi[c] for c in range(len(base))) and in_cell(base, gens, p):
            return True
    return False


def is_cell_of(member, Q, base, gens, allow_origin=False):
    """verify from the definitions that P(base;gens) is a cell of U(member,Q)"""
    G = set(graver_region(member, Q))
    if rank(gens) < len(gens):
        return False, "dependent generators"
    for g in gens:
        if tuple(g) not in G and tuple(-x for x in g) not in G:
            return False, "generator %r not Graver in the region" % (g,)
    for c in corners(tuple(base), [tuple(g) for g in gens]):
        if not member(c) or any(x < 0 or x > q for x, q in zip(c, Q)) or (not allow_origin and not any(c)):
            return False, "corner %r not in F" % (c,)
    return True, "ok"
