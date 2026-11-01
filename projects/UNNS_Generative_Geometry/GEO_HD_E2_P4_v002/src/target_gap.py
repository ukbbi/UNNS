"""Target coverage gap for the coupled target Lambda_3 = E_3 = {a+b+c even} and the general-m lemmas behind P4-T1 / P4-T2."""
from fractions import Fraction as Fr
from itertools import product

import _boot  # noqa: F401
import coverage_gap as cg

P = (2, 5, 11)


def e3_fibre(n):
    return [a for a in product(range(n + 1), repeat=3) if any(a) and sum(a) % 2 == 0]


def is_graver_e3(v):
    """v is conformally minimal in E_3 \\ {0}: no nonzero w in E_3, w != v, w conformal-<= v (|w_i|<=|v_i|, same sign)."""
    ranges = [range(0, x + 1) if x >= 0 else range(x, 1) for x in v]
    for w in product(*ranges):
        if any(w) and w != tuple(v) and sum(w) % 2 == 0:
            return False
    return sum(v) % 2 == 0 and any(v)


def cube_tiling_lemma(n):
    """n even.  For every w in (2Z)^3 cap [0,n-2]^3 with w != 0: the 8 vertices of the cube w + [0,2]^3 lie in F(E_3,n) (even sum, in the box,
    nonzero) and its generators 2e_1, 2e_2, 2e_3 are Graver moves of E_3, so the cube is a 3-cell of K_abs.  The cubes tile [0,n]^3.
    Returns (ok, details)."""
    assert n % 2 == 0 and n >= 2
    gens_ok = all(is_graver_e3(g) for g in ((2, 0, 0), (0, 2, 0), (0, 0, 2)))
    F = set(e3_fibre(n))
    bad = []
    count = 0
    for w in product(range(0, n - 1, 2), repeat=3):
        if w == (0, 0, 0):
            continue
        count += 1
        for e in product((0, 2), repeat=3):
            v = tuple(a + b for a, b in zip(w, e))
            if v not in F:
                bad.append((w, v))
    return gens_ok and not bad, {"n": n, "n_cubes": count, "generators_graver": gens_ok, "bad": bad[:5]}


def hull_halfspaces_e3(n):
    """H' = conv F(E_3, n) = { z in [0,n]^3 : z1+z2+z3 >= 2 }  (n even >= 2).  Returns (halfspaces as (a,c) meaning a.z <= c, vertex list).
    The vertex list consists of the 7 cube vertices other than 0 plus (2,0,0),(0,2,0),(0,0,2) -- all lattice points of F -- and the claim
    'conv = polytope' is checked by exact vertex enumeration of the stated inequalities."""
    hs = []
    for i in range(3):
        e = [0, 0, 0]
        e[i] = 1
        hs.append((tuple(e), Fr(n)))
        e2 = [0, 0, 0]
        e2[i] = -1
        hs.append((tuple(e2), Fr(0)))
    hs.append(((-1, -1, -1), Fr(-2)))
    return hs


def hull_check_e3(n):
    """Exact: the vertices of the polytope hull_halfspaces_e3(n) are lattice points of F(E_3,n) and every F-point satisfies the inequalities."""
    from itertools import combinations
    hs = hull_halfspaces_e3(n)
    verts = set()
    for tri in combinations(range(len(hs)), 3):
        A = [[Fr(x) for x in hs[i][0]] for i in tri]
        rhs = [hs[i][1] for i in tri]
        # solve 3x3 by Cramer (exact)
        def det(M):
            return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                    + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        d = det(A)
        if d == 0:
            continue
        sol = []
        for c in range(3):
            M = [row[:] for row in A]
            for r in range(3):
                M[r][c] = rhs[r]
            sol.append(det(M) / d)
        if all(sum(a * s for a, s in zip(h[0], sol)) <= h[1] for h in hs):
            verts.add(tuple(sol))
    F = set(e3_fibre(n))
    verts_in_F = all(all(x.denominator == 1 for x in v) and tuple(int(x) for x in v) in F for v in verts)
    F_in_poly = all(all(sum(a * x for a, x in zip(h[0], v)) <= h[1] for h in hs) for v in F)
    return verts_in_F and F_in_poly, sorted(tuple(str(x) for x in v) for v in verts)


def cell_vertex_sets(n):
    """Set of (vertex-set, generators) of every abstract cell of E_3 in the box [0,n]^3 (builder-side derivation)."""
    F, G, cells = cg.cells_of(P, 3, (n,) * 3)
    import e1_cell_transport as ct0
    out = set()
    for base, gens in cells:
        c = ct0.Cell(base, gens)
        out.add((c.key, tuple(sorted(gens))))
    return out


def graver_equal(n1, n2):
    import graver_transport as gt
    return sorted(gt.graver_fast(P, 3, (n1,) * 3)) == sorted(gt.graver_fast(P, 3, (n2,) * 3))
