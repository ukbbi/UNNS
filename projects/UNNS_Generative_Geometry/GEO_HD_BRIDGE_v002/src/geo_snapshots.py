"""G2-A: geometric state record G(m) for an integer state m, built from the FROZEN GEO-I engine (src/frozen/geo2lib.py,
pinned) plus closed forms proved in theory/GEOMETRIC_HISTORIES.md.  For an integer m (denominator 1) the relation lattice is
Z^P, the Graver basis is {+-e_i}, K_axis = K_move, and F(m) = box \\ {0}, box = prod [0, q_p], q_p = floor(v_p(m)/2).
Components that are undefined are reported as undefined (no analogue is manufactured)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'frozen'))
from math import prod
from geo1lib import factor, fibre
from geo2lib import analyse


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p; k += 1
    return k


def qvec(m):
    """{p: floor(v_p(m)/2)} restricted to q_p >= 1 (the active coordinates of the exponent box)."""
    return {p: e // 2 for p, e in sorted(factor(m).items()) if e // 2 >= 1}


def s_of(m):
    return prod(p ** q for p, q in qvec(m).items())


def closed_form(m):
    """k, q, |F|, total cell count, Euler characteristic of K(m) -- Theorem B2-T1."""
    q = qvec(m); k = len(q)
    if k == 0:
        return None
    return {'k': k, 'primes': sorted(q), 'q': [q[p] for p in sorted(q)], 'nF': prod(x + 1 for x in q.values()) - 1,
            'ncells': prod(2 * x + 1 for x in q.values()) - 2 ** k, 'chi': 1, 'sigma': s_of(m),
            'd_aff': 0 if (k == 1 and list(q.values())[0] == 1) else k}


def state_record(m, frozen=True):
    """G(m) = (D, F, Lambda, cells C, region U, invariants I).  Undefined components are flagged."""
    cf = closed_form(m)
    if cf is None:
        return {'m': m, 'defined': False, 'reason': 'D(m) is empty (no p with v_p(m) >= 2)'}
    rec = {'m': m, 'defined': True, 'D_size': cf['nF'], 'lattice': 'Z^%d (b=1)' % cf['k'], 'closed': cf}
    if frozen:
        a = analyse(m)
        rec['frozen'] = {'primes': a['primes'], 'q': a['q'], 'R': a['R'], 'd_aff': a['d_aff'], 'graver': a['graver_region_size'],
                         'axis_cells': a['axis']['cells_per_dim'], 'move_cells': a['move']['cells_per_dim'],
                         'components': a['move']['components'], 'betti_gf2': a['move']['betti']['2'], 'd2_zero': a['move']['d2_zero']}
    return rec


def persists(m, mp):
    """K(m) is a subcomplex of K(m') iff q(m) <= q(m') coordinatewise iff D(m) subset D(m')."""
    a, b = qvec(m), qvec(mp)
    return all(b.get(p, 0) >= q for p, q in a.items())
