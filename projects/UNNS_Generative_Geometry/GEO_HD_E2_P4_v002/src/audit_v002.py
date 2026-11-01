"""E2-P4 v002 independent audit.  Imports only the independent engine pieces (audit_p3, certificate_check, geometry_audit) -- NOT the builder modules
(lattice_model, zero_vertex, slab_law, build_p4_v002).  Lattice cells are re-derived from first principles from a membership predicate."""
from fractions import Fraction as Fr
from itertools import combinations, product

import _boot  # noqa: F401
import audit_p3 as au
import certificate_check as cc
import geometry_audit as ga


# ---- independent lattice membership -------------------------------------------------------------
def in_hnf(B, v):
    """v in the lattice with upper-triangular basis rows B (back-substitution from the first coordinate)."""
    v = list(v)
    for i, row in enumerate(B):
        d = row[i]
        if v[i] % d:
            return False
        t = v[i] // d
        for j in range(i, len(v)):
            v[j] -= t * row[j]
    return all(x == 0 for x in v)


def chi_member(P, b):
    def f(v):
        r = 1
        for p, e in zip(P, v):
            r = r * (pow(p, e, b) if e >= 0 else pow(pow(p, -1, b), -e, b)) % b
        return r == 1 % b
    return f


def cells_from_member(inL, q):
    """Same definition as audit_p3.independent_cells, but from a membership predicate."""
    k = len(q)
    F = [v for v in product(*[range(m + 1) for m in q]) if any(v) and inL(v)]
    Fs = set(F)
    Lall = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and inL(v)]
    G = [g for g in Lall if not any(h != g and ga.conf(h, g) for h in Lall)]
    Go = sorted(g for g in G if ga.lex_pos(g))
    cells = {}
    for v in F:
        cells[(v,)] = (v, ())
    for m in range(1, k + 1):
        for gens in combinations(Go, m):
            if au._rank(gens) != m:
                continue
            for u in F:
                vs = []
                for bits in product((0, 1), repeat=m):
                    w = list(u)
                    for bit, g in zip(bits, gens):
                        if bit:
                            w = [x + y for x, y in zip(w, g)]
                    vs.append(tuple(w))
                if all(w in Fs for w in vs):
                    cells.setdefault(tuple(sorted(vs)), (u, tuple(gens)))
    return F, au.maximal_cells(list(cells.values()))


def in_cells(cells, p):
    return any(cc._in(c[0], [list(g) for g in c[1]], p) for c in cells)


def cell_ok(inL, q, cell, w=None):
    """source cell: corners all in F (member, nonzero, inside the box) and generators independent; optionally w inside."""
    base, gens = cell["base"], [list(g) for g in cell["gens"]]
    for v in cc._verts(base, gens):
        if not (any(v) and inL(tuple(int(x) for x in v)) and all(0 <= x <= m for x, m in zip(v, q))):
            return False
    if gens and not cc._independent(gens):
        return False
    return True if w is None else cc._in(base, gens, tuple(Fr(x) for x in w))


# ---- P4-C1 correction ------------------------------------------------------------------------------
def c1_check(n=4):
    q = (n, n, n)
    inL = lambda v: all(x % 2 == 0 for x in v)  # noqa: E731
    F, S = cells_from_member(inL, q)
    inE = lambda v: sum(v) % 2 == 0  # noqa: E731
    FE, T = cells_from_member(inE, q)
    pt = (Fr(1), Fr(1), Fr(1))
    wit = (Fr(4, 7), Fr(4, 7), Fr(10, 7))
    verts = {(a, b, c) for a in (0, n) for b in (0, n) for c in (0, n)} | {(1, 1, 0) for _ in [0]}
    hull10 = [v for v in product((0, n), repeat=3) if sum(v) >= 2] + [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
    return {"n_F_source": len(F), "ten_hull_vertices_in_F": all(tuple(v) in set(F) for v in hull10) and len(set(hull10)) == 10,
            "(1,1,1)_in_source_union": in_cells(S, pt), "(1,1,1)_in_E3_union": in_cells(T, pt),
            "witness_in_E3_union": in_cells(T, wit), "witness_in_source_union": in_cells(S, wit),
            "source_equals_box_minus_origin_cube": all(in_cells(S, p) == (max(p) >= 2) for p in product([Fr(0), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(3), Fr(n)], repeat=3)),
            "every_source_cell_has_vertex_max_ge_2": all(any(max(v) >= 2 for v in cc._verts(c[0], [list(g) for g in c[1]])) for c in S)}


# ---- zero-vertex decomposition re-verification -----------------------------------------------------------
def zv_decomposition_ok(inLp, ex):
    """ex = {'base','gens','decomposition'}: verify s_i in lattice, s_i conformally below g_i, and base + sum s_i = 0."""
    base, gens, dec = ex["base"], ex["gens"], ex["decomposition"]
    if len(dec) != len(gens):
        return False
    tot = list(base)
    for s, g in zip(dec, gens):
        if not inLp(tuple(s)) or not ga.conf(tuple(s), tuple(g)):
            return False
        tot = [a + b for a, b in zip(tot, s)]
    return all(x == 0 for x in tot)


# ---- noncontainment witnesses ------------------------------------------------------------------------------
def noncontained_ok(inS, inT, q, cell, w):
    """source cell legitimate, witness inside it, witness in none of the independently derived maximal target cells."""
    if not cell_ok(inS, q, cell, w):
        return False, "source cell invalid or witness not inside"
    F, T = cells_from_member(inT, q)
    if in_cells(T, tuple(Fr(x) for x in w)):
        return False, "witness lies in the target union"
    return True, "ok (%d target maximal cells)" % len(T)


def slab_ok(inT, q, w, i, planar_inL):
    """free coordinate i: e_i in lattice; 0<w_i<1; planar part of w outside the independently derived planar union."""
    e = [0, 0, 0]
    e[i] = 1
    if not inT(tuple(e)):
        return False, "coordinate %d is not free" % i
    wf = [Fr(x) for x in w]
    if not (0 < wf[i] < 1):
        return False, "witness not in the thin slab"
    rest = [j for j in range(3) if j != i]
    F2, T2 = cells_from_member(planar_inL, tuple(q[j] for j in rest))
    if in_cells(T2, (wf[rest[0]], wf[rest[1]])):
        return False, "planar part lies in planar target union"
    return True, "ok"


def slab_lemma_check(n=2):
    """Finite check of the slab lemma for E2 (+) Z in the box (n,n,n): for c in {1/4,1/2,3/4} and a 1/4-grid of planar points,
    (x,c) in U(E2 (+) Z) <=> x in U(E2)."""
    inE2 = lambda v: (v[0] + v[1]) % 2 == 0  # noqa: E731
    inT = lambda v: (v[0] + v[1]) % 2 == 0  # noqa: E731  (third coordinate free)
    _, T3 = cells_from_member(inT, (n, n, n))
    _, T2 = cells_from_member(inE2, (n, n))
    bad, tot = 0, 0
    for c in (Fr(1, 4), Fr(1, 2), Fr(3, 4)):
        for x in product([Fr(i, 4) for i in range(0, 4 * n + 1)], repeat=2):
            tot += 1
            if in_cells(T3, (x[0], x[1], c)) != in_cells(T2, x):
                bad += 1
    return tot, bad


# ---- independent zero-vertex screen (brute force, no shared code with zero_vertex.py) ---------------------------
def zv_flag(base, gens, inLp):
    """True iff there are s_i in the lattice, each conformally below g_i (componentwise between 0 and g_i), with base + sum s_i = 0."""
    k = len(base)
    opts = []
    for g in gens:
        rng = [range(min(0, x), max(0, x) + 1) for x in g]
        opts.append([s for s in product(*rng) if inLp(s)])
    for combo in product(*opts):
        if all(base[c] + sum(s[c] for s in combo) == 0 for c in range(k)):
            return True
    return False


def zv_rescreen(P, b, b2, q):
    """Independent cells of the source lattice ker chi_b; zero-vertex flag count against ker chi_b2.  Returns (n_maximal, n_flagged)."""
    F, S = au.independent_cells(P, tuple(q), b)
    S = au.maximal_cells(S)
    inLp = chi_member(P, b2)
    return len(S), sum(1 for c in S if c[1] and zv_flag(c[0], c[1], inLp))
