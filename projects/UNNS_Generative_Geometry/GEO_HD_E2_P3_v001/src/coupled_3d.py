"""E2-P3 / P3-E3: three-coordinate (k = 3) FIELD-I transitions: exact containment verdicts, essentiality analysis.

Essentiality (spec 6.2), all three computed exactly for every witnessed failure:
  coordinate support  : coordinates i for which some vertex of the failing source cell has v_i != 0   (need all three)
  geometric dimension : affine dimension of the failing cell (1, 2 or 3) and, when the loss region is measured, of the lost piece
  irreducibility      : the transition restricted to each coordinate face {x_i = 0} (primes P minus p_i, same b, b', box q minus q_i,
                        i.e. the planar FIELD-I-lattice transition on the remaining two coordinates) is CONTAINED, for every i."""
import math
import os
import sys
from collections import Counter
from fractions import Fraction as Fr
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coverage_gap as cg  # noqa: E402
import exact_containment as ec  # noqa: E402
import planar_residual as pr  # noqa: E402

lt, ft = cg.lt, cg.ft


def face_restriction_verdicts(P, q, b, b2):
    """Verdict of the transition restricted to each coordinate face x_i = 0 (a k=2 lattice transition on the other two primes)."""
    out = {}
    for i in range(3):
        keep = [j for j in range(3) if j != i]
        P2 = tuple(P[j] for j in keep)
        q2 = tuple(q[j] for j in keep)
        res, F2, c2 = cg.geometric_verdict(P2, b, b2, q2)
        out[str(i)] = {"primes": list(P2), "box": list(q2), "verdict": res["verdict"],
                       "source_lattice_index": lt.describe(P2, b)["index"], "target_lattice_index": lt.describe(P2, b2)["index"]}
    return out


def support_of(cell):
    base, gens = cell["base"], cell["gens"]
    verts = ec.cell_vertices(base, gens)
    return sorted(i for i in range(len(base)) if any(v[i] != 0 for v in verts))


def evaluate_3d(row, node_limit=30000):
    P, q, b, b2 = tuple(row["primes"]), tuple(row["box"]), row["b"], row["b_next"]
    out = dict(row)
    out["coupled_source"] = bool(lt.coupled(P, b))
    out["coupled_target"] = bool(lt.coupled(P, b2)) if b2 > 1 else False
    out["both_nontrivial"] = row["index_source"] > 1 and row["index_target"] > 1
    try:
        res, F2, c2 = cg.geometric_verdict(P, b, b2, q, node_limit)
    except ec.Exhausted as e:
        out["verdict"] = "UNAVAILABLE"
        out["reason"] = str(e)
        return out
    out["verdict"] = res["verdict"]
    out["n_source_maximal"], out["n_target_maximal"] = res["n_source_maximal"], res["n_target_maximal"]
    if res["verdict"] == "NOT_CONTAINED":
        cert = res["certificate"]
        out["n_noncontained_source_cells"] = res["n_noncontained_source_cells"]
        out["witness"] = cert["witness"]
        out["witness_cell"] = cert["source_cell"]
        failing = res["all_failing_cells"]
        sup = [support_of(c) for c in failing]
        dims = [len(c["gens"]) for c in failing]
        out["failing_cells"] = failing
        out["essentiality"] = {
            "witness_cell_support": support_of(cert["source_cell"]),
            "witness_cell_dimension": len(cert["source_cell"]["gens"]),
            "any_failing_cell_with_full_support": any(len(s) == 3 for s in sup),
            "failing_cell_dimensions": sorted(set(dims)),
            "face_restrictions": face_restriction_verdicts(P, q, b, b2)}
        e = out["essentiality"]
        e["irreducible_to_faces"] = all(v["verdict"] == "CONTAINED" for v in e["face_restrictions"].values())
        e["full_support"] = len(e["witness_cell_support"]) == 3
        out["certificate"] = cert
        out["target_maximal"] = res["target_maximal"]
        out["essential_3d"] = bool(e["full_support"] and e["irreducible_to_faces"] and e["witness_cell_dimension"] >= 2
                                   and out["both_nontrivial"] and out["coupled_source"])
    return out


def sweep3(pool, qmax, bmax, start=0, stop=None, progress=None, odd=True):
    return pr.sweep(pool, qmax, bmax, 3, start, stop, progress, odd)


# =====================================================================================================================
# Rectangular targets: corner-cube criterion (P3-T3) and predictor (P3-T4)
# =====================================================================================================================
def rectangular_data(P, b2, q):
    """If Lambda_{b2} = (o_1 Z) x ... x (o_k Z) (i.e. index = prod of the orders o_i = ord_{b2}(p_i); b2 = 1 gives o = 1)
    return (o, Qtilde = floor(q/o)); else None."""
    if b2 == 1:
        o = tuple(1 for _ in P)
    else:
        o = tuple(lt.orders(P, b2))
        if lt.describe(P, b2)["index"] != math.prod(o):
            return None
    return o, tuple(qi // oi for qi, oi in zip(q, o))


def max_slack(base, gens, o):
    """max s such that some z = base + sum t_j g_j (0 <= t_j <= 1) has z_i + s*o_i <= o_i for all i  (LP, exact, by vertex
    enumeration in the variables (t, s)).  The cell meets the open corner cube {z_i < o_i for all i} iff the optimum is > 0."""
    k, m = len(base), len(gens)
    nv = m + 1
    rows = []
    for i in range(k):                       # sum_j t_j g_ji + s o_i <= o_i - base_i
        rows.append(([Fr(g[i]) for g in gens] + [Fr(o[i])], Fr(o[i] - base[i])))
    for j in range(m):
        e = [Fr(0)] * nv
        e[j] = Fr(1)
        rows.append((e, Fr(1)))
        rows.append(([-x for x in e], Fr(0)))
    best = None
    for sub in combinations(range(len(rows)), nv):
        x = ec._solve([rows[i][0] for i in sub], [rows[i][1] for i in sub])
        if x is None:
            continue
        if all(ec.dot(a, x) <= c for a, c in rows):
            if best is None or x[-1] > best[0]:
                best = (x[-1], x[:-1])
    return best


def corner_cube_predict_full(P, q, b, b2):
    """Reference implementation: build the whole SOURCE complex, test every maximal cell (slow; used to cross-check the fast one)."""
    rd = rectangular_data(P, b2, q)
    if rd is None:
        return None
    o, Qt = rd
    if min(Qt) < 1:
        return {"verdict": "UNAVAILABLE", "reason": "scaled target box has a zero coordinate (U' not of corner-cube form)"}
    F, G, cells = cg.cells_of(P, b, q)
    for base, gens in ec.geometric_maximal(cells, len(q)):
        r = max_slack(base, gens, o)
        if r is not None and r[0] > 0:
            return _predict_hit(base, gens, r, o, Qt)
    return {"verdict": "CONTAINED", "orders": list(o), "scaled_box": list(Qt)}


def _predict_hit(base, gens, r, o, Qt):
    t = r[1]
    z = tuple(Fr(base[i]) + sum(t[j] * gens[j][i] for j in range(len(gens))) for i in range(len(base)))
    return {"verdict": "NOT_CONTAINED", "witness": [str(x) for x in z], "cell": {"base": list(base), "gens": [list(g) for g in gens]},
            "slack": str(r[0]), "orders": list(o), "scaled_box": list(Qt)}


def corner_cube_predict(P, q, b, b2):
    """P3-T4 predictor (fast).  Uses only the SOURCE fibre and Graver set and the target orders.  By P3-T3 (c),(d),(f) a cell meeting
    the corner cube may be taken 2-dimensional (k = 3; for general k a (k-1)-dimensional face is not enumerated here, so k is
    restricted to 2 and 3) and must have a vertex of scaled L1 norm <= k-1; only such cells are tested."""
    rd = rectangular_data(P, b2, q)
    if rd is None:
        return None
    o, Qt = rd
    k = len(q)
    if min(Qt) < 1:
        return {"verdict": "UNAVAILABLE", "reason": "scaled target box has a zero coordinate (U' not of corner-cube form)"}
    if k != 3:
        return corner_cube_predict_full(P, q, b, b2)
    F = cg.fibre_of(P, b, q)
    Fs = set(F)
    Go = ft.oriented(cg.gt.graver_fast(P, b, q))
    small = [v for v in F if sum(Fr(vi, oi) for vi, oi in zip(v, o)) <= k - 1]
    seen = set()
    for v in small:
        for g, h in combinations(Go, 2):
            if ec._rank_int([g, h]) != 2:
                continue
            for s1 in (1, -1):
                for s2 in (1, -1):
                    gg = tuple(s1 * x for x in g)
                    hh = tuple(s2 * x for x in h)
                    verts = [v, tuple(a + b_ for a, b_ in zip(v, gg)), tuple(a + b_ for a, b_ in zip(v, hh)),
                             tuple(a + b_ + c_ for a, b_, c_ in zip(v, gg, hh))]
                    if not all(w in Fs for w in verts):
                        continue
                    key = tuple(sorted(verts))
                    if key in seen:
                        continue
                    seen.add(key)
                    r = max_slack(v, [gg, hh], o)
                    if r is not None and r[0] > 0:
                        return _predict_hit(v, [gg, hh], r, o, Qt)
    return {"verdict": "CONTAINED", "orders": list(o), "scaled_box": list(Qt), "cells_tested": len(seen)}


def short_vector_screen(P, q, b, b2):
    """Necessary condition for failure (proved in THEOREMS P3-T3(c)): the SCALED source lattice contains a nonzero vector v >= 0
    with |v|_1 <= k-1.  Returns True when failure is still possible.  Cheap: no complex is built."""
    rd = rectangular_data(P, b2, q)
    if rd is None:
        return None
    o, Qt = rd
    k = len(q)
    for v in product(*[range(0, min(k - 1, qi // 1) + 1) for qi in Qt]):
        if any(v) and sum(v) <= k - 1 and lt.in_lambda(tuple(vi * oi for vi, oi in zip(v, o)), P, b):
            if all(vi * oi <= qi for vi, oi, qi in zip(v, o, q)):
                return True
    return False
