"""E10: active 3D and 4D modular fibres.  Exact audit of every fibre; concrete rational realizations."""
import os, sys, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d))
from fractions import Fraction as Fr
from math import gcd
import intersections as X
from realization import fibre_complex_data, fibre_complex, cover_cells
from validation import edge_level_audit, cell_level_audit
from arith import crossing_free_for_all_boxes, group_order, order_mod
from homology_compare import betti_abs, betti_nerve, betti_clique
from geo1lib import is_prime
from theorems import units, direct_product, graph_identity


def primes_in_class(r, b, avoid, count=1):
    out = []; p = 2
    while len(out) < count:
        if is_prime(p) and p % b == r % b and p not in avoid and gcd(p, b) == 1: out.append(p)
        p += 1
    return out


def realize(res, q, b):
    """concrete x = prod p_i^(2 q_i) / b with p_i prime, p_i = res_i mod b, distinct, coprime to b.  (b=1 unused here)"""
    used = []; ps = []
    for r in res:
        p = primes_in_class(r, b, used + [p for p in range(2, b + 1) if b % p == 0])[0]; used.append(p); ps.append(p)
    a = 1
    for p, e in zip(ps, q): a *= p ** (2 * e)
    return Fr(a, b), ps


def crossing_geometry(a, fc):
    """for each crossing pair, whether the plane spanned lies in a coordinate plane (product-like) and the support of the edge vectors."""
    k = fc['k']; rows = []
    for pr in a['crossing_pairs']:
        (e1, e2) = tuple(pr)
        g = X.sub(e1[1], e1[0]); h = X.sub(e2[1], e2[0])
        supp = sorted({i for i in range(k) if g[i] or h[i]})
        rows.append({'g': g, 'h': h, 'support': supp, 'coordinate_plane': len(supp) == 2})
    return rows


def survey(k, bs, boxes, lp_budget=4000, max_res=None):
    out = []
    for b in bs:
        for res in itertools.combinations_with_replacement(units(b), k):
            if all(r == 1 for r in res): continue
            for q in boxes:
                fc = fibre_complex_data(res, q, b)
                if not fc['F']: continue
                ea = edge_level_audit(fc['cells'])
                ca = cell_level_audit(fc['cells'], lp_budget=lp_budget, stop_at_first=True)
                cross = ea['relations'].get('interior_cross', 0) > 0
                cls = 'EMBEDDED' if ca['status'] == 'embedded' else ('UNRESOLVED_RESOURCE_LIMIT' if ca['status'] == 'resource_limited' else
                      ('NON_EMBEDDED_EDGE_CROSSING' if cross else 'NON_EMBEDDED_CELL_ONLY'))
                rec = {'b': b, 'res': list(res), 'q': list(q), 'k': k, 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']], 'class': cls,
                       'direct_product': direct_product(res, b), 'has_unit_residue': any(r == 1 for r in res), 'n_crossing_pairs': len(ea['crossing_pairs']),
                       'lp_calls': ca['lp_calls']}
                if cross:
                    cg = crossing_geometry(ea, fc)
                    rec['crossing_nonplanar_in_coords'] = any(not r['coordinate_plane'] for r in cg)
                    rec['example_crossing'] = {'g': cg[0]['g'], 'h': cg[0]['h'], 'support': cg[0]['support']}
                out.append(rec)
    return out


def example_record(label, res, q, b, x=None, nerve_lp=150000):
    if x is None: x, ps = realize(res, q, b)
    else: ps = None
    fc = fibre_complex(x)
    ea = edge_level_audit(fc['cells'])
    ca = cell_level_audit(fc['cells'], lp_budget=60000)
    cov = cover_cells(fc['cells'])
    ba = betti_abs(fc['cells'])
    rec = {'label': label, 'x': str(x), 'primes': fc['ps'], 'exponent_boxes_q': fc['q'], 'b': fc['b'], 'k': fc['k'], 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']],
           'status': ca['status'], 'edge_relations': ea['relations'], 'cell_pairs': ca['pairs'], 'non_face_by_dims': ca['non_face_by_dims'],
           'maximal_by_dim': ca['maximal_by_dim'], 'involved_by_dim': ca['involved_by_dim'], 'betti_abs_Q': ba[0], 'abs_d2_euler': [ba[1], ba[2]],
           'cover_size': len(cov), 'crossing_points': sorted(['(' + ','.join(c) + ')' for c in ea['crossing_points']])[:6]}
    if ca['status'] == 'embedded':
        rec['betti_U'] = ba[0]; rec['U_method'] = 'theorem (embedded)'
    else:
        bn, inf = betti_nerve(cov, maxdim=3, max_lp=nerve_lp)
        if bn is None:
            bn, inf = betti_nerve(cov, maxdim=2, max_lp=nerve_lp)
        rec['betti_U'] = bn; rec['U_method'] = ('nerve; trusted degrees %d' % inf.get('trusted_degrees', 0)) if bn is not None else 'UNAVAILABLE (budget)'
    cb, ci = betti_clique(fc['F'], fc['G'], 3); rec['betti_clique_Q'] = cb
    return rec
