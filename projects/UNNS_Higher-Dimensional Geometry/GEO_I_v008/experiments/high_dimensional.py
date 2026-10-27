"""E5/G3: genuinely higher-dimensional benchmarks (k = 3, 4).  Exact audits of the v003 polyhedral realization.
 * Klein-four (b=8, 3,5,7)             : edges never cross, cells do.
 * parity lattices Lambda_n = {sum alpha_i even} (b=3, residues (2,)*n) : obstructions live in a non-coordinate 2-plane with full support.
 * 4D example b=24, residues (5,7,13,23) (H = (Z/24)^x of order 8, orders (2,2,2,2)).
usage: high_dimensional.py  (prints JSON)"""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from realization import fibre_complex_data
from validation import cell_level_audit, edge_level_audit
from arithmetic_criteria import invariants


def audit_box(res, b, q, budget=200000):
    fc = fibre_complex_data(res, q, b)
    if not fc['F']: return {'q': list(q), 'status': 'empty_fibre'}
    ea = edge_level_audit(fc['cells'])
    ca = cell_level_audit(fc['cells'], lp_budget=budget, stop_at_first=True)
    return {'q': list(q), 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']], 'status': ca['status'],
            'edge_interior_crossings': ea['relations'].get('interior_cross', 0)}


def parity_scan(n, qmax=2, b=3):
    res = (2,) * n; out = []
    for q in itertools.product(range(0, qmax + 1), repeat=n):
        if list(q) != sorted(q, reverse=True) or not any(q): continue          # symmetric under permutations of the coordinates
        out.append(audit_box(res, b, q))
    return out


def minimal_nonembedded(rows):
    bad = [r['q'] for r in rows if r.get('status') == 'non_embedded']
    return sorted(q for q in bad if not any(o != q and all(o[i] <= q[i] for i in range(len(q))) for o in bad))


def four_d(qmax=4):
    """Lambda = {alpha in Z^4 : all coordinates have the same parity}  (b=24, residues 5,7,13,23; symmetric in the 4 coordinates)."""
    res, b = (5, 7, 13, 23), 24; inv = invariants(res, b); out = []
    for q in itertools.product(range(0, qmax + 1), repeat=4):
        if list(q) != sorted(q, reverse=True) or not any(q): continue
        out.append(audit_box(res, b, q))
    return {'invariants': inv, 'boxes': out, 'minimal_nonembedded_sorted': minimal_nonembedded(out)}


if __name__ == '__main__':
    print(json.dumps({'parity3': parity_scan(3, 2), 'parity4': parity_scan(4, 2), 'four_d': four_d(2)}, default=str))
