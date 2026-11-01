"""v005: verification of Theorem P5-S4 (generalised slab law) for SPLIT targets  Lambda' = Lambda'_2 (+) k Z e_3  (coordinate 3 split with period k).
  U(Lambda',Q) = [U(Lambda'_2,Q') x [0,k]]  union  [U0(Lambda'_2,Q') x [k,kJ]],  J = floor(q_3/k)   (J = 0: U x {0}).
  C <= U(Lambda',Q)  <=>  proj( C cap {z <= k} ) <= U(Lambda'_2,Q')     (for a source cell C of U(Lambda,Q), Lambda <= Lambda').
Checks: (I) pointwise identity of the union on a rational grid (mini.py, brute force);  (II) the criterion against the pinned exact engine, cell by cell."""
import sys, os, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mini, geo3
import planar_audit as pa


def split_basis(L2, k):
    (a, x), (_, b) = L2
    return ((a, x, 0), (0, b, 0), (0, 0, k))


def formula_member(U2, U02, k, J, p):
    z = p[2]; pl = (p[0], p[1])
    if J == 0:
        return z == 0 and mini.in_union(U2, pl)
    if z <= k and mini.in_union(U2, pl): return True
    if k <= z <= k * J and mini.in_union(U02, pl): return True
    return False


def check_identity(L2, k, Q, denom=3):
    """pointwise: mini 3D union == formula, on the grid (1/denom Z)^3 inside the box"""
    Bp = split_basis(L2, k); mBp = lambda v: geo3.member(Bp, v)
    c3, _, _ = mini.cells(mBp, Q)
    Q2 = (Q[0], Q[1]); m2 = pa.member2(L2)
    U2, _, _ = mini.cells(m2, Q2, maxdim=2); U02, _, _ = mini.cells(m2, Q2, allow_origin=True, maxdim=2)
    J = Q[2] // k
    bad = 0; n = 0
    for p in itertools.product(*[[Fr(t, denom) for t in range(q * denom + 1)] for q in Q]):
        n += 1
        if mini.in_union(c3, p) != formula_member(U2, U02, k, J, p): bad += 1
    return n, bad


# ---------------------------------------------------------------- planar convex hull / truncation of a source cell
def hull2(points):
    pts = sorted(set(points))
    if len(pts) <= 2: return pts
    def cross(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def truncated_projection(base, gens, k):
    """vertices of proj_{xy}( C cap {z <= k} ) as Fractions (C a parallelotope with integer data)"""
    V = mini.corners(tuple(base), [tuple(g) for g in gens])
    pts = [(Fr(v[0]), Fr(v[1])) for v in V if v[2] <= k]
    n = len(gens)
    for bits in itertools.product((0, 1), repeat=n):
        for i in range(n):
            if bits[i]: continue
            P = list(base)
            for b, g in zip(bits, gens):
                if b: P = [x + y for x, y in zip(P, g)]
            g = gens[i]; Pz = P[2]; Rz = Pz + g[2]
            if (Pz < k < Rz) or (Rz < k < Pz):
                t = Fr(k - Pz, g[2])
                pts.append((P[0] + t * g[0], P[1] + t * g[1]))
    return hull2(pts)


def criterion_contained(base, gens, k, U2polys):
    """P5-S4 criterion for the source cell: planar projection of C cap {z<=k} lies in U(Lambda'_2,Q')"""
    hull = truncated_projection(base, gens, k)
    if len(hull) == 0: return True
    if len(hull) < 3:
        # degenerate (segment/point): test endpoints and midpoint exactly against planar cells
        pts = list(hull) + ([((hull[0][0] + hull[-1][0]) / 2, (hull[0][1] + hull[-1][1]) / 2)] if len(hull) == 2 else [])
        return all(mini.in_union(U2polys['cells'], p) for p in pts)
    pieces = [hull]
    sb = pa.bbox_poly(hull)
    for tb, tp in U2polys['polys']:
        if tb[0] > sb[2] or tb[2] < sb[0] or tb[1] > sb[3] or tb[3] < sb[1]: continue
        pieces = pa.subtract(pieces, tp)
        if not pieces: return True
    return False


def _planar_context(L2, Qxy, cache):
    key = (L2, Qxy)
    if key not in cache:
        m2 = pa.member2(L2)
        U2, _, _ = mini.cells(m2, Qxy, maxdim=2)
        polys = [(pa.bbox_poly(p), p) for p in (pa.parallelogram(b, g[0], g[1]) for b, g in U2 if len(g) == 2)]
        cache[key] = dict(cells=U2, polys=polys)
    return cache[key]


def check_criterion(L2, k, m_list=(2, 3, 4), cap=(8, 8, 9), time_budget=None, stats=None):
    """criterion (P5-S4) vs the pinned exact engine, for every hard cell of every source Lambda of index m in Lambda' = L2 (+) kZ, box Qmax and its own box Q_C"""
    import time
    import _boot
    ec = _boot.p4("lattice_model").ec
    lm = _boot.p4("lattice_model")
    t0 = time.time()
    Bp = split_basis(L2, k)
    ko = geo3.axis_orders(Bp)
    Qmax = tuple(min(3 * ko[i], cap[i]) for i in range(3))
    stats = stats if stats is not None else dict(hard=0, agree=0, disagree=0, noncontained=0)
    bad = []
    pcache = {}; ecache = {}
    for m in m_list:
        for M in geo3.hnf3_enum(m):
            B = geo3.sublattice(Bp, M)
            G = geo3.lexpos(geo3.graver(B, Qmax))
            for u, gens in geo3.hard_cells(G, B, Bp, Qmax):
                if time_budget and time.time() - t0 > time_budget: return stats, bad
                import numpy as np
                QC = tuple(int(x) for x in (np.array(u) + sum((np.maximum(g, 0) for g in gens), np.zeros(3, dtype=np.int64))))
                base = tuple(int(x) for x in u); gs = [tuple(int(x) for x in g) for g in gens]
                crit = criterion_contained(base, gs, k, _planar_context(L2, (QC[0], QC[1]), pcache))
                if QC not in ecache:
                    F, cs = lm.cells_of_member(lambda v: geo3.member(Bp, v), QC)
                    ecache[QC] = [ec.Target(b, g, 3) for b, g in ec.geometric_maximal(cs, 3)]
                dec = ec.decide_cell(base, tuple(gs), ecache[QC], 3, node_limit=50000)
                eng = dec["verdict"] == "CONTAINED"
                stats['hard'] += 1
                stats['noncontained'] += (not eng)
                if crit == eng: stats['agree'] += 1
                else: stats['disagree'] += 1; bad.append(dict(L2=L2, k=k, B=B, base=base, gens=gs, QC=QC, criterion=crit, engine=dec["verdict"]))
    return stats, bad
