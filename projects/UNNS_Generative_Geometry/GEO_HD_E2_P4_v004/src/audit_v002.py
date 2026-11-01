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


# ---- v003: independent corroboration of the P4-S2 formula and of the 21 formerly UNAVAILABLE rows ---------------------
def s2_formula_member(inT2_cells, inT2_cells0, i, qi, p):
    """Predicted membership in U(Lambda') from the planar unions: U(L2) for c<1, U0(L2) for c>=1."""
    rest = [j for j in range(3) if j != i]
    x = (p[rest[0]], p[rest[1]])
    return in_cells(inT2_cells if p[i] < 1 else inT2_cells0, x)


def planar_union(inL2, q2, zero_allowed):
    pts = [v for v in product(*[range(m + 1) for m in q2]) if inL2(v) and (zero_allowed or any(v))]
    Fs = set(pts)
    Lall = [v for v in product(*[range(-m, m + 1) for m in q2]) if any(v) and inL2(v)]
    G = [g for g in Lall if not any(h != g and ga.conf(h, g) for h in Lall)]
    Go = sorted(g for g in G if ga.lex_pos(g))
    cells = {}
    for v in pts:
        cells[(v,)] = (v, ())
    for m in (1, 2):
        for gens in combinations(Go, m):
            if au._rank(gens) != m:
                continue
            for u in pts:
                vs = [tuple(u[c] + sum(b * g[c] for b, g in zip(bits, gens)) for c in range(2)) for bits in product((0, 1), repeat=m)]
                if all(w in Fs for w in vs):
                    cells.setdefault(tuple(sorted(vs)), (u, tuple(gens)))
    return list(cells.values())


def s2_check_row(P, b, b2, q, den=3):
    """(a) every grid point (denominator den) of every independently derived source cell lies in the 3D target union (independent cells),
    (b) on a rational grid the 3D target union membership equals the P4-S2 formula.  Returns (ok_a, ok_b, n_points)."""
    inS, inT = chi_member(P, b), chi_member(P, b2)
    free = [i for i in range(3) if inT(tuple(1 if j == i else 0 for j in range(3)))]
    i = free[0]
    rest = [j for j in range(3) if j != i]
    pl = chi_member([P[j] for j in rest], b2)
    q2 = tuple(q[j] for j in rest)
    U2, U20 = planar_union(pl, q2, False), planar_union(pl, q2, True)
    F, T = cells_from_member(inT, tuple(q))
    F0, S = cells_from_member(inS, tuple(q))
    ok_a = True
    n = 0
    for base, gens in S:
        for ss in product(range(den + 1), repeat=len(gens)):
            pt = tuple(Fr(base[c]) + sum(Fr(s, den) * g[c] for s, g in zip(ss, gens)) for c in range(3))
            n += 1
            if not in_cells(T, pt):
                ok_a = False
    ok_b = True
    grid = [Fr(k, 2) for k in range(0, 2 * q[0] + 1)]
    for pt in product([Fr(k, 2) for k in range(0, 2 * q[0] + 1)], [Fr(k, 2) for k in range(0, 2 * q[1] + 1)], [Fr(k, 2) for k in range(0, 2 * q[2] + 1)]):
        if in_cells(T, pt) != s2_formula_member(U2, U20, i, q[i], pt):
            ok_b = False
    return ok_a, ok_b, n


# ---- v004: independent checks of P4-Z2 and of the structure of hard cells (P4-P1) -------------------------------------------
def zv_explicit_ind(base, gens, inLp):
    """P4-Z2 re-stated independently: min corner = 0 and negative parts of the generators in the target."""
    k = len(base)
    mn = [base[c] + sum(min(g[c], 0) for g in gens) for c in range(k)]
    return all(x == 0 for x in mn) and all(inLp(tuple(min(x, 0) for x in g)) for g in gens)


def hard_ind(base, gens, inLp):
    k = len(base)
    mn = [base[c] + sum(min(g[c], 0) for g in gens) for c in range(k)]
    return all(x == 0 for x in mn) and all(inLp(tuple(min(x, 0) for x in g)) and inLp(tuple(max(x, 0) for x in g)) for g in gens)


def planar_pairs(nmax):
    """all (B, Bp) with Lambda < Lambda' in Z^2, index <= nmax (HNF written independently)."""
    def hnf(n):
        return [((a, x), (0, n // a)) for a in range(1, n + 1) if n % a == 0 for x in range(n // a)]
    lats = [(n, B) for n in range(1, nmax + 1) for B in hnf(n)]
    out = []
    for n, B in lats:
        for n2, Bp in lats:
            if n2 < n and n % n2 == 0 and all(in_hnf(Bp, r) for r in B):
                out.append((B, Bp))
    return out


def check_z2_and_hard(nmax, boxes):
    """returns (n_cells, n_zv_mismatch, n_hard, n_structure_violations, n_hard_not_in_target_grid_test)"""
    cells_n = mism = hard = viol = notin = 0
    for B, Bp in planar_pairs(nmax):
        inS = lambda v, B=B: in_hnf(B, v)  # noqa: E731
        inT = lambda v, Bp=Bp: in_hnf(Bp, v)  # noqa: E731
        kp = next(k for k in range(1, 10 ** 4) if inT((k, 0)))
        lp = next(l for l in range(1, 10 ** 4) if inT((0, l)))
        for q in boxes:
            F, S = cells_from_member(inS, q)
            T = None
            for base, gens in S:
                if len(gens) == 0:
                    continue
                cells_n += 1
                brute = zv_flag(base, gens, inT)
                mism += (brute != zv_explicit_ind(base, gens, inT))
                if len(gens) == 2 and hard_ind(base, gens, inT):
                    hard += 1
                    V = cc._verts(base, [list(g) for g in gens])
                    A = [v for v in V if v[0] == 0 and v[1] > 0]
                    Bc = [v for v in V if v[1] == 0 and v[0] > 0]
                    ok = bool(A) and bool(Bc)
                    if ok:
                        A, Bc = A[0], Bc[0]
                        oth = [v for v in V if v != A and v != Bc]
                        ok = (len(oth) == 2 and A[0] + Bc[0] == oth[0][0] + oth[1][0] and A[1] + Bc[1] == oth[0][1] + oth[1][1]
                              and all(v[0] >= kp and v[1] >= lp for v in oth) and all(Fr(v[0], kp) + Fr(v[1], lp) >= 2 for v in V))
                    viol += (not ok)
                    if T is None:
                        T = cells_from_member(inT, q)[1]
                    pts = [tuple(Fr(base[c]) + sum(Fr(s, 4) * g[c] for s, g in zip(ss, gens)) for c in range(2)) for ss in product(range(5), repeat=2)]
                    notin += (not all(in_cells(T, p) for p in pts))
    return cells_n, mism, hard, viol, notin


def counterexample_K1():
    """v003 assessment: Lambda = {a even, b-a = 0 mod 6, c even}, Lambda' = E_3, Q = (6,6,2), cell (0,6,0);(2,-4,0),(4,-2,0).
    The cell lies in the plane z3 = 0; there the target is E_2 (even sum) in box (6,6) and Graver cells of the plane lattice are Graver cells of E_3.
    Returns (corners in F(Lambda), zero-vertex explicit criterion holds, grid points of the cell in the planar target union, target has no free coordinate)."""
    inS = lambda v: v[0] % 2 == 0 and (v[1] - v[0]) % 6 == 0 and v[2] % 2 == 0  # noqa: E731
    inT = lambda v: sum(v) % 2 == 0  # noqa: E731
    base, gens = (0, 6, 0), [(2, -4, 0), (4, -2, 0)]
    corners_ok = all(any(v) and inS(tuple(int(x) for x in v)) and all(0 <= x <= m for x, m in zip(v, (6, 6, 2))) for v in cc._verts(base, [list(g) for g in gens]))
    zv = zv_explicit_ind(base, gens, inT)
    F, T = cells_from_member(lambda v: sum(v) % 2 == 0, (6, 6))
    pts = [tuple(Fr(base[c]) + sum(Fr(s, 6) * g[c] for s, g in zip(ss, gens)) for c in range(2)) for ss in product(range(7), repeat=2)]
    nofree = not any(inT(tuple(1 if j == i else 0 for j in range(3))) for i in range(3))
    return corners_ok, zv, all(in_cells(T, p) for p in pts), nofree
