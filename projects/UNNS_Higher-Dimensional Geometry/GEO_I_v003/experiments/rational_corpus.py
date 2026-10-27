"""Exactly the v002 rational corpus (E5 of v002 = E7 of v003): b<=31, a<=20000, plus L^2/g reset states."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'geometry')); sys.path.insert(0, os.path.join(HERE, '..', 'frozen'))
from fractions import Fraction as Fr
from math import gcd
from geo2lib import coords, fibre_points

def corpus(smoke=False):
    BMAX, AMAX = (13, 3000) if smoke else (31, 20000)
    items = []
    for b in range(2, BMAX + 1):
        for a in range(2, AMAX + 1):
            if gcd(a, b) == 1: items.append((Fr(a, b), 'F1_small_denominator'))
    GS = (5, 7, 11, 13, 17, 19, 23) if smoke else (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 15, 21, 35, 39, 25, 33)
    LMAX = 120 if smoke else 400
    for g in GS:
        for L in range(2, LMAX):
            if gcd(L, g) == 1: items.append((Fr(L * L, g), 'F2_reset_states_L2_over_g'))
    out = []
    for x, fam in items:
        ps, q, b = coords(x)
        if not ps: continue
        F = fibre_points(ps, q, b)
        if not F: continue
        out.append((x, fam))
    return out

if __name__ == '__main__':
    c = corpus(); print(len(c))


# ---------------------------------------------------------------------------------------------- E7 / E8 runner
import time, json
from realization import fibre_complex, cover_cells
from validation import audit
from homology_compare import betti_abs, betti_nerve, betti_clique
from subdivision import planar_subdivision, planar_cells_for_homology
from chain_complex import betti


def planar_U_betti(fc, cover, field='Q'):
    allc = [c for d in fc['cells'] for c in d]
    sub = planar_subdivision(cover, fc['F'], refine=allc)
    cl, bd = planar_cells_for_homology(sub)
    return betti(cl, bd, field)[0], sub


def classify(fc, a):
    ed = a['edge']['relations']
    cross = ed.get('interior_cross', 0) > 0
    if a['status'] == 'embedded': return 'EMBEDDED'
    if a['status'] == 'resource_limited': return 'UNRESOLVED_RESOURCE_LIMIT'
    return 'NON_EMBEDDED_EDGE_CROSSING' if cross else 'NON_EMBEDDED_CELL_ONLY'


def e7_record(x, fam, nerve_budget=40):
    fc = fibre_complex(x)
    a = audit(fc)
    rec = {'x': str(x), 'family': fam, 'b': fc['b'], 'k': fc['k'], 'q': fc['q'], 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']],
           'class': classify(fc, a), 'edge_relations': a['edge']['relations'], 'cell_pairs': a['cell']['pairs'], 'why': a['cell']['why'],
           'n_crossing_points': len(a['edge']['crossing_points']), 'seconds_audit': a['seconds']}
    babs = betti_abs(fc['cells'])
    rec['betti_abs_Q'] = babs[0]; rec['d2_ok'] = babs[1]; rec['euler_ok'] = babs[2]
    if rec['class'] == 'EMBEDDED':
        rec['betti_U'] = babs[0]; rec['betti_U_method'] = 'theorem (embedded => homeomorphic)'
    elif fc['k'] == 2:
        cov = cover_cells(fc['cells']); bU, sub = planar_U_betti(fc, cov)
        rec['betti_U'] = bU; rec['betti_U_method'] = 'planar subdivision (exact, validated)'
        rec['sub'] = [len(sub['vertices']), len(sub['edges']), len(sub['faces'])]
    else:
        cov = cover_cells(fc['cells'])
        if len(cov) <= nerve_budget:
            bn, info = betti_nerve(cov)
            if bn is None: rec['betti_U'] = None; rec['betti_U_method'] = 'UNAVAILABLE: nerve resource limit'
            else: rec['betti_U'] = bn; rec['betti_U_method'] = 'nerve of closed convex cover (trusted degrees %d)' % info['trusted_degrees']
        else:
            rec['betti_U'] = None; rec['betti_U_method'] = 'UNAVAILABLE: cover has %d members (> %d)' % (len(cov), nerve_budget)
    return rec


def run_e7(smoke=False, progress=None):
    t = time.time(); out = []
    items = corpus(smoke)
    for i, (x, fam) in enumerate(items):
        out.append(e7_record(x, fam))
        if progress and i % 1000 == 0: progress(i, len(items), time.time() - t)
    return out
