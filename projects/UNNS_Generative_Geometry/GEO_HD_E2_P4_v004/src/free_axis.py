"""P4-S2 (v003): exact decision of U(Lambda,Q) <= U(Lambda',Q) when the target Lambda' has a free coordinate i (e_i in Lambda'),
WITHOUT building the spatial target complex.  Theorem P4-S2: with Lambda' = Lambda'_2 (+) Z e_i, q_i >= 1,
   (x',c) in U(Lambda',Q)  <=>  ( c < 1 and x' in U(Lambda'_2,Q') )  or  ( c >= 1 and x' in U0(Lambda'_2,Q') ),
where U0 is the planar union of Graver cells with all corners in Lambda'_2 cap Q' (origin ALLOWED as a corner).
The decision runs the pinned closed-splitting procedure on  C cap {c<=1}  against the cylinders  C2 x [0,q_i]  (C2 cells of U) and on  C cap {c>=1}  against cylinders over U0."""
from itertools import combinations, product

import _boot  # noqa: F401
import exact_containment as ec
import lattice_model as lm
import coverage_gap as cg


def planar_cells0(inL2, q2, zero_allowed):
    """Graver cells of a planar lattice; corners must lie in Lambda cap Q (0 allowed iff zero_allowed)."""
    pts = [v for v in product(*[range(m + 1) for m in q2]) if inL2(v) and (zero_allowed or any(v))]
    Fs = set(pts)
    Lall = [v for v in product(*[range(-m, m + 1) for m in q2]) if any(v) and inL2(v)]
    def conf(h, g):
        return all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(h, g))
    G = [g for g in Lall if not any(h != g and conf(h, g) for h in Lall)]
    Go = sorted(g for g in G if next(x for x in g if x) > 0)
    cells = {}
    for v in pts:
        cells[(v,)] = (v, ())
    for m in (1, 2):
        for gens in combinations(Go, m):
            if m == 2 and gens[0][0] * gens[1][1] - gens[0][1] * gens[1][0] == 0:
                continue
            for u in pts:
                vs = []
                for bits in product((0, 1), repeat=m):
                    w = list(u)
                    for bit, g in zip(bits, gens):
                        if bit:
                            w = [a + b for a, b in zip(w, g)]
                    vs.append(tuple(w))
                if all(w in Fs for w in vs):
                    cells.setdefault(tuple(sorted(vs)), (u, tuple(gens)))
    return list(cells.values())


def _embed(cell2, i, hi):
    rest = [j for j in range(3) if j != i]
    def put(v2, c):
        out = [0, 0, 0]
        out[rest[0]], out[rest[1]], out[i] = v2[0], v2[1], c
        return tuple(out)
    base = put(cell2[0], 0)
    gens = [put(g, 0) for g in cell2[1]] + [put((0, 0), hi)]
    return base, gens


def decide_poly(hs, targets, k, node_limit=60000):
    """closed splitting from an arbitrary root polytope hs (same procedure as engine decide_cell)."""
    counter = [0]
    wit = []

    def rec(h):
        counter[0] += 1
        if counter[0] > node_limit:
            raise ec.Exhausted("node limit")
        V = ec.vertices(h, k)
        if not V:
            return
        cand = ec._cands(V, targets)
        order = sorted(cand, key=lambda j: -sum(1 for v in V if targets[j].contains(v)))
        for j in order:
            if all(targets[j].contains(v) for v in V):
                return
        for j in order:
            for a, c in targets[j].hs:
                vals = [ec.dot(a, v) - c for v in V]
                if min(vals) < 0 < max(vals):
                    rec(ec._dedupe(h + [(a, c)]))
                    if wit:
                        return
                    rec(ec._dedupe(h + [(tuple(-x for x in a), -c)]))
                    return
        wit.append(ec.centroid(V))
    rec(hs)
    return (wit[0] if wit else None), counter[0]


def decide_free_axis(source_max, inT, q, i, node_limit=60000):
    """source_max: maximal source cells [(base,gens)]; inT: 3D target membership with e_i in the target; q: box.
    Returns {'verdict','witness','part':'S0'|'S1'}."""
    rest = [j for j in range(3) if j != i]
    inT2 = lambda v: inT(tuple(v[rest.index(j)] if j != i else 0 for j in range(3)))  # noqa: E731
    q2 = tuple(q[j] for j in rest)
    T0 = [ec.Target(*_embed(c, i, q[i]), 3) for c in planar_cells0(inT2, q2, False)]
    T1 = [ec.Target(*_embed(c, i, q[i]), 3) for c in planar_cells0(inT2, q2, True)]
    nodes = 0
    for base, gens in source_max:
        root = ec.cell_halfspaces(base, gens, 3)
        e = [Fr(0)] * 3
        for part, targets, sign in (("S0", T0, 1), ("S1", T1, -1)):
            a = [0, 0, 0]
            a[i] = sign
            hs = ec._dedupe(root + [(tuple(ec.Fr(x) for x in a), ec.Fr(sign * 1))])  # S0: c <= 1 ; S1: -c <= -1
            V = ec.vertices(hs, 3)
            if not V or (part == "S0" and all(v[i] >= 1 for v in V)):
                continue
            w, n = decide_poly(hs, targets, 3, node_limit)
            nodes += n
            if w is not None:
                return {"verdict": "NOT_CONTAINED", "witness": [str(x) for x in w], "part": part, "cell": {"base": list(base), "gens": [list(g) for g in gens]}, "nodes": nodes}
    return {"verdict": "CONTAINED", "nodes": nodes}


from fractions import Fraction as Fr  # noqa: E402
