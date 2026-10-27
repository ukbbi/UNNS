"""E2: the infinite family x_t = 2^(10+2t) 3^4 / 5.  Proof certificates for Props G3-P1 and G3-P2 (see MATHEMATICS.md)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(HERE, '..', d))
from fractions import Fraction as Fr
import intersections as X
from realization import fibre_complex, cover_cells
from validation import edge_level_audit
from arith import in_lambda, graver_complete
from homology_compare import betti_abs
import rational_corpus as rc


def x_t(t): return Fr(2 ** (10 + 2 * t) * 3 ** 4, 5)


def p1_certificate(t):
    """Prop G3-P1 for one t: witness vertices in F, witness vectors Graver, crossing exact, crossing point not in Lambda."""
    fc = fibre_complex(x_t(t)); F = set(fc['F']); G = set(graver_complete((2, 3), 5))
    pts = [(1, 1), (5, 1), (2, 2), (4, 0)]
    edge1 = X.sub((5, 1), (1, 1)); edge2 = X.sub((4, 0), (2, 2))
    kind, pt = X.seg_relation((1, 1), (5, 1), (2, 2), (4, 0))
    return {'t': t, 'q': fc['q'], 'witness_in_F': all(p in F for p in pts), 'vectors_graver': edge1 in G and edge2 in G,
            'crossing': kind == 'interior_cross' and pt == (Fr(3), Fr(1)), 'crossing_not_in_Lambda': not in_lambda((2, 3), 5, (3, 1)), 'crossing_not_in_F': (3, 1) not in F,
            'edges_present_in_complex': all(any((u == a and X.add(u, g[0]) == b) or (u == b and X.add(u, g[0]) == a) for (u, g) in fc['cells'][1]) for (a, b) in (((1, 1), (5, 1)), ((2, 2), (4, 0))))}


def counts(t):
    fc = fibre_complex(x_t(t)); n = [len(c) for c in fc['cells']]
    return n


def p2_period_check(tmin=6, tmax=30):
    """Prop G3-P2: for q1 >= 11 (t >= 6) the (R, #edges, #squares) increase by exactly (3, 8, 6) per period of 4, so chi increases by 1."""
    cs = {t: counts(t) for t in range(tmin, tmax + 1)}
    bad = [t for t in range(tmin, tmax + 1 - 4) if [cs[t + 4][j] - cs[t][j] for j in range(3)] != [3, 8, 6]]
    chi = {t: cs[t][0] - cs[t][1] + cs[t][2] for t in cs}
    return {'bad_periods': bad, 'chi_increment_ok': all(chi[t + 4] - chi[t] == 1 for t in range(tmin, tmax + 1 - 4))}
