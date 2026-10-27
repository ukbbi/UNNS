"""Deterministic unit tests for GEO-I v004 (python3 tests/test_geo4.py).  Self-contained: needs only this release."""
import os, sys, itertools, random
HERE = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d))
from math import gcd
from lattice_model import Lat, complex_data, U_betti
from coverage import uncovered, is_hull_covered, hull, area2
from obstruction_templates import Lattice, LatticeFromLat, obstruction_atlas, embedded_by_templates, in_open_zonotope, rank, lexpos
from arithmetic_criteria import invariants, drop_unit_residues, essential_dimension
from stabilization import predicted_beta1, realize, prime_in_class, data_to_pure
from arith import order_mod, group_order, in_lambda, graver_complete
from realization import fibre_complex_data
from validation import cell_level_audit

n = 0
def ok(name, cond):
    global n
    assert cond, 'FAILED: ' + name
    n += 1

# --- lattice model: membership agrees with the modular definition (scaling reduction S1)
for (o1, o2, d, s) in [(4, 4, 4, 1), (6, 6, 3, 2), (4, 6, 2, 1), (8, 8, 4, 3)]:
    r = realize(o1, o2, d, s, 200)
    ok('realize %s' % ((o1, o2, d, s),), r is not None and order_mod(r['res'][0], r['b']) == o1 and order_mod(r['res'][1], r['b']) == o2)
    L = Lat(o1, o2, d, s)
    ok('membership %s' % ((o1, o2, d, s),), all(in_lambda(r['res'], r['b'], (x, y)) == ((x, y) in L) for x in range(-o1, o1 + 1) for y in range(-o2, o2 + 1)))
    ok('index = |H|', L.index == group_order(r['res'], r['b']))
    ok('prime reps', all(p % r['b'] == r['res'][i] % r['b'] for i, p in enumerate(r['primes'])) and r['primes'][0] != r['primes'][1])

# --- Graver completeness (conformal minimality) in the pure model
L = Lat(5, 5, 5, 2); G = L.graver_complete()
ok('graver in lattice', all(g in L for g in G))
ok('graver minimal', not any(h != g and h[0] * g[0] >= 0 and h[1] * g[1] >= 0 and abs(h[0]) <= abs(g[0]) and abs(h[1]) <= abs(g[1]) for g in G for h in G if h in L and any(h)))
ok('Lemma0 |g_i| <= o_i', all(abs(g[0]) <= 5 and abs(g[1]) <= 5 for g in G))

# --- polygon tools
ok('hull square', len(hull([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])) == 4)
ok('area2', area2([(0, 0), (2, 0), (2, 2), (0, 2)]) == 8)

# --- planar stabilization data points (exact)
ok('hollow (3,2)@(3,3) beta1=2', U_betti(Lat(3, 3, 3, 1), (3, 3))[0][1] == 2)
ok('s=-1: beta1 = d at (d,d)', all(U_betti(Lat(d, d, d, d - 1), (d, d))[0][1] == d for d in (3, 4, 5, 6)))
ok('stabilized (4,3)', U_betti(Lat(4, 4, 4, 1), (5, 4))[0][1] == 0 and is_hull_covered(Lat(4, 4, 4, 1), (5, 4)))
ok('(d,d) never hull covered', not any(is_hull_covered(Lat(d, d, d, s), (d, d)) for d in (2, 3, 4, 5) for s in range(1, d) if gcd(s, d) == 1))
ok('coverage == homology on 40 boxes', all((U_betti(Lat(d, d, d, s), (q1, q2))[0][1] == 0) == is_hull_covered(Lat(d, d, d, s), (q1, q2))
    for d, s in ((3, 1), (3, 2), (4, 1), (4, 3)) for q1 in range(d, d + 3) for q2 in range(d, d + 3) if (q1, q2) != (d, d)) )
ok('predicted beta1', predicted_beta1(5, 4, (5, 5)) == 5 and predicted_beta1(5, 2, (5, 5)) == 2 and predicted_beta1(5, 2, (6, 5)) == 0 and predicted_beta1(1, 1, (1, 1)) == 0)
ok('d=1 contractible (Z^2 box)', all(U_betti(Lat(1, 1, 1, 1), (a, b))[0][1:] == [0, 0] for a in (1, 2, 3) for b in (1, 2, 3)))

# --- templates: b=5, (2,3): minimal boxes and agreement with the exhaustive audit
lat = Lattice((2, 3), 5); ts, anti = obstruction_atlas(lat)
ok('b=5 (2,3) atlas', sorted(anti) == [(1, 8), (2, 5), (4, 4), (5, 2), (8, 1)])
for q in itertools.product(range(1, 7), repeat=2):
    fc = fibre_complex_data((2, 3), q, 5)
    if not fc['F']: continue
    a = cell_level_audit(fc['cells'], lp_budget=100000, stop_at_first=True)
    ok('template == audit at %s' % (q,), (a['status'] == 'embedded') == embedded_by_templates(anti, q))
ok('LatticeFromLat == modular lattice atlas', sorted(obstruction_atlas(LatticeFromLat(Lat(4, 4, 4, 1)))[1]) == sorted(anti))
ok('direct product => empty atlas', invariants((2, 6), 7)['direct_product'] and obstruction_atlas(Lattice((2, 6), 7))[1] == [])
ok('zonotope membership', in_open_zonotope((1, 1), [(2, 0), (0, 2)]) and not in_open_zonotope((2, 2), [(2, 0), (0, 2)]))
ok('rank', rank([(1, 0), (0, 1), (1, 1)]) == 2 and lexpos((0, 1)) and not lexpos((0, -1)))

# --- arithmetic criteria
ok('invariants', invariants((2, 3), 5)['H'] == 4 and not invariants((2, 3), 5)['direct_product'] and invariants((2, 3), 7)['direct_product'] is False)
ok('essential dimension', essential_dimension((2, 3, 1), 5) == 2 and drop_unit_residues((2, 1, 3))[0] == (2, 3))
ok('prime_in_class', prime_in_class(5, 24) == 5 and prime_in_class(1, 24) == 73)
print('test_geo4: %d checks passed' % n)
