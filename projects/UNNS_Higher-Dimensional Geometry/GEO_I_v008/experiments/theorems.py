"""Exhaustive checks of the proved statements of GEO-I v003 (MATHEMATICS.md): Lemmas 1-4, Thm T1 (crossing predictor and iota),
T2 (direct product <=> crossing-freeness in k=2; Klein-four exception in k=3), plus the planted constructions."""
import os, sys, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen'): sys.path.insert(0, os.path.join(HERE, '..', d))
from math import gcd
from fractions import Fraction as Fr
import intersections as X
from realization import fibre_complex_data
from validation import edge_level_audit, audit
from arith import (graver_complete, crossing_offsets, in_lambda, order_mod, group_order, crossing_free_for_all_boxes, iota)


def units(b): return [r for r in range(1, b) if gcd(r, b) == 1] or [1]


def lemma_checks(res, b, q):
    """Lemmas 1-4 on one fibre.  returns dict of violation counts."""
    fc = fibre_complex_data(res, q, b)
    F = set(fc['F']); G = fc['G']; viol = {'L1_open_segment_hits_Lambda': 0, 'L2_collinear_overlap': 0, 'L3_endpoint_on_interior': 0, 'L4_crossing_point_in_Lambda': 0}
    # Lemma 1: no point of Lambda in the open segment (u, u+g) for u in F, u+g in F  (also for all lattice u, not only fibre points)
    for g in G:
        d = 0
        for c in g: d = gcd(d, abs(c))
        for j in range(1, d):
            step = tuple(c * j // d for c in g)       # integer points of the open segment from 0
            if in_lambda(res, b, step): viol['L1_open_segment_hits_Lambda'] += 1
    a = edge_level_audit(fc['cells'])
    viol['L2_collinear_overlap'] = a['relations'].get('collinear_overlap', 0)
    viol['L3_endpoint_on_interior'] = a['relations'].get('endpoint_on_interior', 0)
    for ptstr in a['crossing_points']:
        pt = tuple(Fr(c) for c in ptstr)
        if all(c.denominator == 1 for c in pt) and in_lambda(res, b, tuple(int(c) for c in pt)): viol['L4_crossing_point_in_Lambda'] += 1
    return viol, a, fc


def predicted_crossing_pairs(res, b, F, G):
    """T1 predictor: all unordered pairs of edges that cross, from (g, h, w in Omega(g,h), u) data alone."""
    Fs = set(F); pairs = set()
    for g in G:
        for h in G:
            for (w, t, lam) in crossing_offsets(res, b, g, h):
                for u in F:
                    ug = X.add(u, g)
                    if ug not in Fs: continue
                    r = X.add(u, w); rh = X.add(r, h)
                    if r in Fs and rh in Fs:
                        pairs.add(frozenset((tuple(sorted((u, ug))), tuple(sorted((r, rh))))))
    return pairs


def audit_pairs_canonical(a):
    return {frozenset(tuple(sorted(e)) for e in pr) for pr in a['crossing_pairs']}


def direct_product(res, b):
    return group_order(res, b) == _prod([order_mod(r, b) for r in res])


def _prod(xs):
    p = 1
    for x in xs: p *= x
    return p


def k2_converse_construction(res, b):
    """for a non-direct pair (r1,r2): returns the explicit box and crossing configuration from the proof of T2(b)."""
    o1, o2 = order_mod(res[0], b), order_mod(res[1], b)
    best = None
    for a in range(1, o1):
        for c in range(1, o2):
            if in_lambda(res, b, (a, c)):
                if best is None or c < best[1]: best = (a, c)
    if best is None: return None
    a, c = best
    return {'o': (o1, o2), 'w': (a, c), 'box': (o1, c + o2), 'u': (0, o2), 'g': (o1, 0), 'h': (0, o2), 'r': (a, c)}


# ------------------------------------------------------------------ graph-level homology identity (T3b)
from subdivision import graph_subdivision
from chain_complex import betti


def graph_betti(vertices, edges):
    idx = {v: i for i, v in enumerate(vertices)}
    cells = [[(0, i) for i in range(len(vertices))], [(1, j) for j in range(len(edges))]]
    def bd(c):
        if c[0] == 0: return {}
        a, b = edges[c[1]]
        return {(0, idx[b]): 1, (0, idx[a]): -1}
    return betti(cells, bd)[0]


def graph_identity(fc):
    """beta_1(arrangement graph of the straight-line 1-skeleton) = beta_1(abstract 1-skeleton) + sum_p (m_p - 1)."""
    E = [(u, X.add(u, g)) for (u, (g,)) in (fc['cells'][1] if len(fc['cells']) > 1 else [])]
    Vs = list(fc['F'])
    babs = graph_betti(Vs, E)
    if not E: return None
    sub = graph_subdivision(E)
    bsub = graph_betti(sub['vertices'], sub['edges'])
    extra = sum(len(s) - 1 for s in sub['crossings'].values())      # sum_p (m_p - 1): m_p = number of edges crossing at p
    return {'b0_abs': babs[0], 'b1_abs': babs[1], 'b0_sub': bsub[0], 'b1_sub': bsub[1], 'extra': extra, 'ok': bsub[1] == babs[1] + extra and bsub[0] == babs[0]}


def check_k2_converse(b):
    """T2(b): for every non-direct pair (r1,r2) mod b, the explicit configuration of the proof is a genuine interior crossing."""
    n = 0; bad = []
    for r1 in units(b):
        for r2 in units(b):
            if r2 < r1: continue
            if direct_product((r1, r2), b): continue
            cons = k2_converse_construction((r1, r2), b)
            if cons is None: bad.append((b, r1, r2, 'no w')); continue
            box = cons['box']
            fc = fibre_complex_data((r1, r2), box, b)
            F = set(fc['F']); u, g, h, r = cons['u'], cons['g'], cons['h'], cons['r']
            pts = [u, X.add(u, g), r, X.add(r, h)]
            n += 1
            if not all(p in F for p in pts): bad.append((b, r1, r2, 'endpoints not in F')); continue
            kind, pt = X.seg_relation(u, X.add(u, g), r, X.add(r, h))
            if kind != 'interior_cross': bad.append((b, r1, r2, kind)); continue
            # both are edges of the complex
            E = {frozenset(((e[0]), X.add(e[0], e[1][0]))) for e in fc['cells'][1]}
            if frozenset((u, X.add(u, g))) not in E or frozenset((r, X.add(r, h))) not in E: bad.append((b, r1, r2, 'not Graver edges'))
    return n, bad


def free_axis_persistence(res, b, q, extra_q=2):
    """product principle: appending an axis with p = 1 (mod b) keeps every crossing of the base fibre (slice c = 0)."""
    base = fibre_complex_data(res, q, b); ab = edge_level_audit(base['cells'])['crossing_pairs']
    big = fibre_complex_data(tuple(res) + (1,), tuple(q) + (extra_q,), b); a2 = edge_level_audit(big['cells'])['crossing_pairs']
    lifted = {frozenset(tuple(tuple(list(p) + [0]) for p in e) for e in pr) for pr in ab}
    lifted = {frozenset(tuple(sorted(e)) for e in pr) for pr in lifted}
    got = {frozenset(tuple(sorted(e)) for e in pr) for pr in a2}
    return lifted <= got, len(ab), len(a2)
