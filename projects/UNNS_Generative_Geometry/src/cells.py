"""EXPERIMENTAL higher-k corner-admissible parallelotopes (not inherited Paper A theorem).

Defines a proposed grammar: choose r linearly independent Graver directions, a lattice
vertex as base, and all 2**r translated corner vertices in a finite occurrence fibre.
This gives candidate r-cells. Checking face-to-face embedding and homology is separate.
"""
from fractions import Fraction
from itertools import combinations, product


def rational_rank(vectors):
    if not vectors:
        return 0
    a = [[Fraction(v) for v in row] for row in vectors]
    m, n, r = len(a), len(a[0]), 0
    for j in range(n):
        piv = next((i for i in range(r, m) if a[i][j]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        q = a[r][j]
        a[r] = [x / q for x in a[r]]
        for i in range(m):
            if i != r and a[i][j]:
                f = a[i][j]
                a[i] = [u - f * v for u, v in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def admissible_cells(points, oriented_directions, dimension):
    """Sets of distinct corner tuples for the stated EXACT candidate cell grammar."""
    P = set(points)
    if not P:
        return ()
    k = len(next(iter(P)))
    cells = set()
    for ds in combinations(oriented_directions, dimension):
        if rational_rank(ds) != dimension:
            continue
        for a in P:
            verts = frozenset(tuple(a[i] + sum(bits[j] * ds[j][i] for j in range(dimension)) for i in range(k))
                              for bits in product((0, 1), repeat=dimension))
            if verts <= P:
                cells.add(tuple(sorted(verts)))
    return tuple(sorted(cells))


def coordinate_hull_contains(u, Q):
    """Hull of all lattice points of [0,Q] except origin, k>=2, Q_i>=1."""
    assert len(u) == len(Q) >= 2 and all(q >= 1 for q in Q)
    return all(0 <= v <= q for v, q in zip(u, Q)) and sum(u) >= 1


def coordinate_cell_union_contains(u, Q):
    """Union of corner-admissible axis-aligned unit coordinate cells."""
    assert len(u) == len(Q) >= 2 and all(q >= 1 for q in Q)
    return all(0 <= v <= q for v, q in zip(u, Q)) and max(u) >= 1
