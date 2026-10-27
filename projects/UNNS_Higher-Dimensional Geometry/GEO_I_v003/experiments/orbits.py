"""E9: C-map orbits of v002 (never combined with SELECT-II).  Same seven orbits, 60 steps."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d))
from fractions import Fraction as Fr
from math import prod
from geo1lib import Cstep
import rational_corpus as rc
from realization import fibre_complex, cover_cells
from validation import audit
from homology_compare import betti_abs, betti_nerve, betti_clique


def orbit_states(x0, steps):
    xs = [Fr(x0)]
    for _ in range(steps - 1):
        y = Cstep(xs[-1])
        if y is None: break
        xs.append(Fr(y))
    return xs


def orbit_specs(smoke=False):
    specs = {'72 [C, G=1]': 72, 'g11 benchmark 67500^2/11 [C]': Fr(67500 ** 2, 11)}
    if not smoke:
        for g, E in ((11, (1, 3, 4)), (13, (1, 3, 4)), (17, (2, 3, 5)), (19, (2, 3, 5)), (23, (2, 3, 5))):
            pr = [p for p in (2, 3, 5, 7) if g % p][:len(E)]; Lq = prod(p ** e for p, e in zip(pr, E))
            specs['g=%d L=%s [C]' % (g, '*'.join('%d^%d' % (p, e) for p, e in zip(pr, E)))] = Fr(Lq * Lq, g)
    return specs


from validation import edge_level_audit, cell_level_audit
from realization import fibre_complex, cover_cells
from homology_compare import betti_abs, betti_nerve, betti_clique
import rational_corpus as rc


def state_record(n, x, nerve_lp=20000, full_nerve_cover=25, full_nerve_lp=250000):
    t0 = time.time()
    fc = fibre_complex(x)
    ea = edge_level_audit(fc['cells'])
    ca = cell_level_audit(fc['cells'], lp_budget=400000, stop_at_first=True)
    cls = 'EMBEDDED' if ca['status'] == 'embedded' else ('UNRESOLVED_RESOURCE_LIMIT' if ca['status'] == 'resource_limited' else
          ('NON_EMBEDDED_EDGE_CROSSING' if ea['relations'].get('interior_cross', 0) else 'NON_EMBEDDED_CELL_ONLY'))
    rec = {'n': n, 'x': str(x) if len(str(x)) < 40 else str(x)[:18] + '...', 'b': fc['b'], 'k': fc['k'], 'q': fc['q'], 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']],
           'class': cls, 'edge_relations': ea['relations'], 'n_crossing_points': len(ea['crossing_points']), 'n_crossing_pairs': len(ea['crossing_pairs'])}
    ba = betti_abs(fc['cells']); rec['betti_abs_Q'] = ba[0]; rec['abs_d2_euler'] = [ba[1], ba[2]]
    cb, info = betti_clique(fc['F'], fc['G'], 3); rec['betti_clique_Q'] = cb; rec['clique_trusted_degrees'] = len(cb)
    cov = cover_cells(fc['cells']); rec['cover'] = len(cov)
    if cls == 'EMBEDDED':
        rec['betti_U'] = ba[0]; rec['U_method'] = 'theorem (embedded => homeomorphic)'; rec['U_trusted_degrees'] = len(ba[0])
    elif fc['k'] == 2:
        bU, sub = rc.planar_U_betti(fc, cov); rec['betti_U'] = bU; rec['U_method'] = 'planar subdivision (exact)'; rec['U_trusted_degrees'] = len(bU)
    else:
        done = False
        if len(cov) <= full_nerve_cover:
            bn3, inf3 = betti_nerve(cov, maxdim=3, max_lp=full_nerve_lp)
            if bn3 is not None:
                rec['betti_U'] = bn3; rec['U_method'] = 'nerve (4-fold intersections)'; rec['U_trusted_degrees'] = inf3['trusted_degrees']; done = True
        if not done:
            bn, inf = betti_nerve(cov, maxdim=2, max_lp=nerve_lp)
            if bn is None:
                rec['betti_U'] = None; rec['U_method'] = 'UNAVAILABLE: nerve LP budget exceeded (%d)' % nerve_lp; rec['U_trusted_degrees'] = 0
            else:
                rec['betti_U'] = bn; rec['U_method'] = 'nerve (triple intersections; beta_0, beta_1 only)'; rec['U_trusted_degrees'] = inf['trusted_degrees']
    rec['seconds'] = round(time.time() - t0, 1)
    return rec


def run_orbit(name, x0, steps, **kw):
    return [state_record(n, x, **kw) for n, x in enumerate(orbit_states(x0, steps))]
