"""E2-P3 exact containment engine (BUILDER side).  Pure standard library, exact rational arithmetic only.

Objects.  A *cell* is a parallelotope  P(base; g_1..g_m) = { base + sum t_i g_i : 0 <= t_i <= 1 }  with integer base and
linearly independent integer generators (m = 0 point, 1 segment, ...), living in R^k.
A *halfspace* is (a, c) meaning  a . x <= c  (a: tuple of Fractions, c: Fraction).

Decision problem.  Given a source cell C and target cells T_1..T_n, decide  C <= T_1 u ... u T_n  exactly.
Method (closed splitting).  Maintain a polytope P (H-representation, root = C).  Let V = vertices(P).
  * If all of V lies in one T_j then P <= T_j (T_j convex)                          -> covered leaf.
  * Else if some inequality (a,c) of some T_j is CUT by V (a.v < c < a.v' for vertices v, v')   -> split
        P = P^- u P^+,   P^- = P n {a.x <= c},  P^+ = P n {a.x >= c}   (closed halves; no strictness issue).
  * Else no inequality of any T_j is cut: for every T_j either P <= T_j or some inequality has a.v >= c for all
    vertices with strict '>' at one vertex; then the CENTROID m of V (a relative-interior point of P) satisfies
    a.m > c, so m is not in T_j.  If P is in no T_j, m is a point of P outside the union: NONCONTAINMENT witness.
Termination: a hyperplane that has been used on a branch is never cut again on that branch.
Because all pieces are closed and the covering is of closed sets by closed sets, the verdicts are exact; no tolerance.
"""
from fractions import Fraction as Fr
from itertools import combinations
from math import gcd

# ----------------------------------------------------------------------------------------------- linear algebra
def _solve(M, rhs):
    """Solve the square system M x = rhs exactly (Fractions).  Return list or None if singular."""
    n = len(M)
    A = [[Fr(v) for v in row] + [Fr(r)] for row, r in zip(M, rhs)]
    for c in range(n):
        piv = next((r for r in range(c, n) if A[r][c] != 0), None)
        if piv is None:
            return None
        A[c], A[piv] = A[piv], A[c]
        inv = 1 / A[c][c]
        A[c] = [v * inv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[r][n] for r in range(n)]


def _nullspace(rows, k):
    """Rational basis of {n : rows . n = 0} in R^k."""
    A = [[Fr(v) for v in r] for r in rows]
    piv_cols, r = [], 0
    for c in range(k):
        p = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        inv = 1 / A[r][c]
        A[r] = [v * inv for v in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
        if r == len(A):
            break
    free = [c for c in range(k) if c not in piv_cols]
    basis = []
    for f in free:
        v = [Fr(0)] * k
        v[f] = Fr(1)
        for i, pc in enumerate(piv_cols):
            v[pc] = -A[i][f]
        basis.append(v)
    return basis


def _rank_int(vs):
    """rank of a short list of integer vectors (exact)"""
    rows = [[Fr(c) for c in v] for v in vs]
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
        if r == len(rows):
            break
    return r


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _normalize(a, c):
    """Scale (a,c) by a positive rational to a primitive integer vector (orientation preserved)."""
    den = 1
    for v in list(a) + [c]:
        den = den * Fr(v).denominator // gcd(den, Fr(v).denominator)
    ai = [int(Fr(v) * den) for v in a]
    ci = int(Fr(c) * den)
    g = 0
    for v in ai + [ci]:
        g = gcd(g, abs(v))
    g = g or 1
    return tuple(Fr(v // g) for v in ai), Fr(ci // g)


# ----------------------------------------------------------------------------------------------- cells
def cell_vertices(base, gens):
    out = []
    for bits in range(1 << len(gens)):
        v = list(base)
        for i, g in enumerate(gens):
            if bits >> i & 1:
                v = [x + y for x, y in zip(v, g)]
        out.append(tuple(v))
    return sorted(out)


def cell_params(base, gens, point):
    """Return the unique t with point = base + sum t_i g_i (list of Fractions) or None if point is off the affine hull."""
    m = len(gens)
    d = [Fr(p) - b for p, b in zip(point, base)]
    if m == 0:
        return [] if all(x == 0 for x in d) else None
    G = [[dot(gi, gj) for gj in gens] for gi in gens]
    t = _solve(G, [dot(gi, d) for gi in gens])
    if t is None:
        return None
    for j in range(len(d)):
        if sum(t[i] * gens[i][j] for i in range(m)) != d[j]:
            return None
    return t


def in_cell(base, gens, point):
    t = cell_params(base, gens, point)
    return t is not None and all(0 <= x <= 1 for x in t)


def cell_halfspaces(base, gens, k):
    """Complete exact H-description of a cell (affine-hull equalities as paired inequalities)."""
    m = len(gens)
    hs = []
    base = tuple(Fr(x) for x in base)
    if m:
        G = [[dot(gi, gj) for gj in gens] for gi in gens]
        for i in range(m):
            e = [Fr(1 if j == i else 0) for j in range(m)]
            coef = _solve(G, e)                      # y_i = sum_j coef_j g_j, y_i . g_j = delta_ij
            y = tuple(sum(coef[j] * gens[j][c] for j in range(m)) for c in range(k))
            hs.append(_normalize(tuple(-v for v in y), -dot(y, base)))              # y.(x-base) >= 0
            hs.append(_normalize(y, dot(y, base) + 1))                              # y.(x-base) <= 1
    for n in _nullspace(gens, k) if m else [[Fr(int(i == j)) for j in range(k)] for i in range(k)]:
        hs.append(_normalize(tuple(n), dot(n, base)))
        hs.append(_normalize(tuple(-v for v in n), -dot(n, base)))
    return _dedupe(hs)


def _dedupe(hs):
    seen, out = set(), []
    for a, c in hs:
        key = (tuple(a), c)
        if key not in seen:
            seen.add(key)
            out.append((tuple(a), c))
    return out


# ----------------------------------------------------------------------------------------------- polytopes
def vertices(hs, k):
    """All vertices of the bounded polytope {x : a.x <= c for (a,c) in hs} (brute force over k-subsets)."""
    V = set()
    for sub in combinations(range(len(hs)), k):
        x = _solve([hs[i][0] for i in sub], [hs[i][1] for i in sub])
        if x is None:
            continue
        if all(dot(a, x) <= c for a, c in hs):
            V.add(tuple(x))
    return sorted(V)


def hull_halfspaces(points, k):
    """Facet description of conv(points) (full-dimensional case) by brute force."""
    pts = sorted(set(tuple(p) for p in points))
    hs = set()
    for sub in combinations(pts, k):
        rows = [[Fr(s[j]) - Fr(sub[0][j]) for j in range(k)] for s in sub[1:]]
        ns = _nullspace(rows, k) if rows else []
        if len(ns) != 1:
            continue
        n = ns[0]
        c = dot(n, sub[0])
        vals = [dot(n, p) - c for p in pts]
        if all(v <= 0 for v in vals):
            hs.add(_normalize(tuple(n), c))
        elif all(v >= 0 for v in vals):
            hs.add(_normalize(tuple(-x for x in n), -c))
    return sorted(hs)


def polygon_area(V):
    """Exact area of a convex polygon given its vertex set (any order)."""
    if len(V) < 3:
        return Fr(0)
    cx = sum(v[0] for v in V) / len(V)
    cy = sum(v[1] for v in V) / len(V)
    import math as _m
    pts = sorted(V, key=lambda v: _m.atan2(float(v[1] - cy), float(v[0] - cx)))
    s = Fr(0)
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def centroid(V):
    n = len(V)
    return tuple(sum(v[j] for v in V) / n for j in range(len(V[0])))


class Target:
    """Target cell with cached vertices and halfspaces."""
    def __init__(self, base, gens, k):
        self.base, self.gens, self.k = tuple(base), tuple(tuple(g) for g in gens), k
        self.verts = cell_vertices(self.base, self.gens)
        self.hs = cell_halfspaces(self.base, self.gens, k)
        self.lo = tuple(min(v[j] for v in self.verts) for j in range(k))
        self.hi = tuple(max(v[j] for v in self.verts) for j in range(k))
        # every halfspace must be valid on every vertex (self-check of the H-description)
        for a, c in self.hs:
            for v in self.verts:
                assert dot(a, v) <= c

    def contains(self, p):
        return in_cell(self.base, self.gens, p)

    def as_json(self):
        return {"base": list(self.base), "gens": [list(g) for g in self.gens]}


def geometric_maximal(cells, k):
    """Remove cells whose vertices all lie in another (kept) cell.  cells: list of (base,gens).  Deterministic."""
    cells = sorted(set((tuple(b), tuple(tuple(g) for g in gs)) for b, gs in cells),
                   key=lambda c: (-len(c[1]), c))
    kept = []
    for b, gs in cells:
        vs = cell_vertices(b, gs)
        if not any(len(g2) >= len(gs) and all(in_cell(b2, g2, v) for v in vs) for b2, g2 in kept):
            kept.append((b, gs))
    return kept


# ----------------------------------------------------------------------------------------------- the decision procedure
class Exhausted(Exception):
    pass


def _cands(V, targets):
    lo = [min(v[j] for v in V) for j in range(len(V[0]))]
    hi = [max(v[j] for v in V) for j in range(len(V[0]))]
    return [i for i, t in enumerate(targets)
            if all(t.lo[j] <= hi[j] and t.hi[j] >= lo[j] for j in range(len(lo)))]


def decide_cell(base, gens, targets, k, node_limit=20000, first_witness=True):
    """Decide base+gens <= union(targets).  Returns dict:
         {"verdict": "CONTAINED", "tree": node}  or  {"verdict": "NOT_CONTAINED", "witness": w, "leaf_hs": hs, ...}
       Tree node: {"leaf": j} | {"empty": true} | {"split": [a, c], "lo": node, "hi": node}   (a,c as strings)."""
    root = cell_halfspaces(base, gens, k)
    counter = [0]
    witnesses = []

    def rec(hs):
        counter[0] += 1
        if counter[0] > node_limit:
            raise Exhausted("node limit %d" % node_limit)
        V = vertices(hs, k)
        if not V:
            return {"empty": True}
        cand = _cands(V, targets)
        best, bestn = None, -1
        for j in cand:
            n = sum(1 for v in V if targets[j].contains(v))
            if n == len(V):
                return {"leaf": j}
            if n > bestn:
                best, bestn = j, n
        # find a cut among candidate targets, preferring the target holding the most vertices
        order = sorted(cand, key=lambda j: -sum(1 for v in V if targets[j].contains(v)))
        for j in order:
            for a, c in targets[j].hs:
                vals = [dot(a, v) - c for v in V]
                if min(vals) < 0 < max(vals):
                    lo = rec(_dedupe(hs + [(a, c)]))
                    if first_witness and witnesses:
                        return {"abort": True}
                    hi = rec(_dedupe(hs + [(tuple(-x for x in a), -c)]))
                    return {"split": [[str(x) for x in a], str(c)], "lo": lo, "hi": hi}
        m = centroid(V)
        witnesses.append({"point": m, "leaf_hs": hs, "leaf_vertices": V})
        return {"witness": True}

    tree = rec(root)
    if witnesses:
        w = witnesses[0]
        return {"verdict": "NOT_CONTAINED", "witness": w["point"], "leaf_vertices": w["leaf_vertices"], "nodes": counter[0]}
    return {"verdict": "CONTAINED", "tree": tree, "nodes": counter[0]}


def noncontainment_certificate(base, gens, w, targets_all, k):
    """Assemble the checkable certificate  w in P(c)  and  w not in Q_j for every target cell Q_j."""
    t = cell_params(base, gens, w)
    assert t is not None and all(0 <= x <= 1 for x in t), "witness must lie in the source cell"
    per = []
    for j, T in enumerate(targets_all):
        found = None
        for a, c in T.hs:
            if dot(a, w) > c:
                found = (a, c)
                break
        assert found is not None, "witness lies in target cell %d" % j
        per.append({"target": j, "a": [str(x) for x in found[0]], "c": str(found[1]), "value": str(dot(found[0], w) - found[1])})
    return {"kind": "NONCONTAINMENT", "source_cell": {"base": list(base), "gens": [list(g) for g in gens]},
            "witness": [str(x) for x in w], "params": [str(x) for x in t], "violations": per}


def containment_certificate(base, gens, decision):
    return {"kind": "CONTAINMENT", "source_cell": {"base": list(base), "gens": [list(g) for g in gens]},
            "tree": decision["tree"]}


def decide_union(source_cells, target_cells, k, node_limit=20000):
    """Decide U <= U' where both are given as lists of (base,gens).  Returns summary + list of per-cell certificates.
    Source cells already vertex-contained in a single target cell are certified by a one-leaf tree (still checked)."""
    S = geometric_maximal(source_cells, k)
    Tmax = geometric_maximal(target_cells, k)
    targets = [Target(b, gs, k) for b, gs in Tmax]
    certs, bad = [], []
    for b, gs in S:
        dec = decide_cell(b, gs, targets, k, node_limit)
        if dec["verdict"] == "CONTAINED":
            certs.append(containment_certificate(b, gs, dec))
        else:
            bad.append((b, gs, dec))
    out = {"source_maximal": [{"base": list(b), "gens": [list(g) for g in gs]} for b, gs in S],
           "target_maximal": [t.as_json() for t in targets], "n_source_maximal": len(S), "n_target_maximal": len(targets)}
    if bad:
        b, gs, dec = bad[0]
        out["verdict"] = "NOT_CONTAINED"
        out["n_noncontained_source_cells"] = len(bad)
        out["certificate"] = noncontainment_certificate(b, gs, dec["witness"], targets, k)
        out["all_failing_cells"] = [{"base": list(b2), "gens": [list(g) for g in g2]} for b2, g2, _ in bad]
    else:
        out["verdict"] = "CONTAINED"
        out["certificates"] = certs
    return out


# ----------------------------------------------------------------------------------------------- coverage gap
def violation_list(w, targets):
    per = []
    for j, T in enumerate(targets):
        found = next(((a, c) for a, c in T.hs if dot(a, w) > c), None)
        if found is None:
            return None
        per.append({"target": j, "a": [str(x) for x in found[0]], "c": str(found[1])})
    return per


def gap_decomposition(points_F, target_cells, k, node_limit=50000):
    """Exact decomposition of H' = conv(F') into closed pieces, each either inside ONE target cell (covered) or such that the
    relative interior of the piece misses U'  (a piece of the coverage gap G' = H' \\ U').
    Returns the splitting tree (checkable by certificate_check.verify_hull_tree) plus summary data."""
    Tmax = geometric_maximal(target_cells, k)
    targets = [Target(b, gs, k) for b, gs in Tmax]
    hull = hull_halfspaces(points_F, k)
    if not hull:
        raise Exhausted("hull not full-dimensional")
    gap, counter, ncov = [], [0], [0]

    def rec(hs):
        counter[0] += 1
        if counter[0] > node_limit:
            raise Exhausted("gap node limit")
        V = vertices(hs, k)
        if not V:
            return {"empty": True}
        cand = _cands(V, targets)
        for j in cand:
            if all(targets[j].contains(v) for v in V):
                ncov[0] += 1
                return {"leaf": j}
        order = sorted(cand, key=lambda j: -sum(1 for v in V if targets[j].contains(v)))
        for j in order:
            for a, c in targets[j].hs:
                vals = [dot(a, v) - c for v in V]
                if min(vals) < 0 < max(vals):
                    lo = rec(_dedupe(hs + [(a, c)]))
                    hi = rec(_dedupe(hs + [(tuple(-x for x in a), -c)]))
                    return {"split": [[str(x) for x in a], str(c)], "lo": lo, "hi": hi}
        m = centroid(V)
        viol = violation_list(m, targets)
        assert viol is not None
        gap.append({"vertices": V})
        return {"gap": {"point": [str(x) for x in m], "violations": viol}}

    tree = rec(hull)
    out = []
    for g in gap:
        V = g["vertices"]
        a = polygon_area(V) if k == 2 else None
        out.append({"vertices": [[str(x) for x in v] for v in V], "area": (str(a) if a is not None else None),
                    "full_dimensional": (a is not None and a > 0)})
    return {"covered_pieces": ncov[0], "gap_pieces": out, "nodes": counter[0], "tree": tree,
            "target_maximal": [t.as_json() for t in targets],
            "hull_halfspaces": [[[str(x) for x in a], str(c)] for a, c in hull]}
