#!/usr/bin/env python3
"""GEO-I v005 unit tests (exact arithmetic).  python3 tests/test_geo5.py"""
import os, sys, itertools, copy
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(ROOT, d))
from fractions import Fraction as Fr
from math import gcd
N = [0, 0]
def ok(name, cond):
    N[0] += 1
    if not cond: N[1] += 1; print('FAIL', name)
import pure_lattice as PL, planar_embed as PE, symbolic_atlas as SA, uniform_coverage as UC, hollow_box as HB
import witness_dimension as WD, certificates as CE
from obstruction_templates import Lattice, LatticeFromLat
from lattice_model import Lat

# ---- pure lattice / explicit Graver sets
for d in (2, 3, 5, 8, 12):
    ok('graver s=+1 d=%d' % d, set(PL.graver(d, 1)) == PL.graver_s_plus(d))
    ok('graver s=-1 d=%d' % d, set(PL.graver(d, d - 1)) == PL.graver_s_minus(d))
ok('inv', PL.inv(2, 5) == 3 and PL.inv(1, 7) == 1)
ok('fibre excludes origin', (0, 0) not in PL.fibre(5, 2, (5, 5)) and (5, 0) in PL.fibre(5, 2, (5, 5)))
# ---- independent planar test: known hand cases
ok('d=2,s=1 box (2,2) embedded (hand case)', PE.embedded(2, 1, (2, 2)))
ok('d=3,s=1 box (3,3) non-embedded (parallelogram with diagonal edge)', not PE.embedded(3, 1, (3, 3)))
ok('d=3,s=1 box (2,3) embedded', PE.embedded(3, 1, (2, 3)))
ok('d=4,s=3 box (4,5) non-embedded', not PE.embedded(4, 3, (4, 5)))
ok('d=4,s=3 box (4,4) embedded', PE.embedded(4, 3, (4, 4)))
# planar test vs template route (independent code paths) on a block of boxes
mis = 0
for d, s in ((3, 1), (3, 2), (4, 1), (4, 3), (5, 2)):
    lat = LatticeFromLat(Lat(d, d, d, s))
    for q1 in range(1, 2 * d + 2):
        for q2 in range(1, 2 * d + 2):
            if PE.embedded(d, s, (q1, q2)) != WD.embedded(lat, (q1, q2)): mis += 1
ok('planar exact test == template route on 5 lattices x all boxes', mis == 0)
# ---- G5-T3 / G5-T4
for d in (2, 3, 4, 7, 11):
    ok('T3 d=%d ingredients' % d, SA.check_T3(d, brute=d <= 4)['ok'])
for d in (3, 4, 5, 8, 11):
    ok('T4 d=%d ingredients' % d, SA.check_T4(d, brute=d <= 5)['ok'])
ok('T3 staircase', SA.staircase_ok(SA.claimed_T3(6), SA.maximal_T3(6), 6, [(i, j) for i in range(1, 20) for j in range(1, 20)])[0])
ok('T4 staircase', SA.staircase_ok(SA.claimed_T4(6), SA.maximal_T4(6), 6, [(i, j) for i in range(1, 20) for j in range(1, 20)])[0])
ok('T4 d=3 five minimal boxes by brute force', sorted(SA.brute_obs(3, 1, 8)) == sorted(SA.claimed_T4(3)))
ok('T3 d=3 minimal boxes are the antidiagonal Q1+Q2=7', sorted(SA.brute_obs(3, 2, 8)) == sorted(SA.claimed_T3(3)))
# ---- layer construction (G5-C1 s=+-1)
for s in (-1, 1):
    for d in (2, 3, 5):
        allok = all(UC.verify_box(d, s, (q1, q2))['ok'] for q1 in range(d, 3 * d + 1) for q2 in range(d, 3 * d + 1) if (q1, q2) != (d, d))
        ok('layer cover s=%+d d=%d all boxes in [d,3d]^2' % (s, d), allok)
ok('layer construction correctly does NOT cover the hollow box (4,4), s=+1 and s=-1', not UC.verify_box(4, 1, (4, 4))['ok'] and not UC.verify_box(4, -1, (4, 4))['ok'])
L, pt, e, band = UC.layers(4, -1, (6, 7))
ok('layers s=-1 structure', sorted(L) == [1, 2, 3] and L[1] == (0, 4) and pt(2, 3) == (3, 5) and band == (0, 4))
# ---- hollow box (G5-C2)
for d in (3, 6, 9): ok('hollow s=+1 d=%d' % d, HB.check_s_plus(d)['ok'])
for d in (2, 5, 8): ok('hollow s=-1 d=%d beta1=%d' % (d, d), HB.check_s_minus(d)['beta1'] == d)
from lattice_model import U_betti
ok('beta1(U) hollow s=1 d=5 via arrangement == 2', U_betti(Lat(5, 5, 5, 1), (5, 5))[0][1] == 2)
ok('beta1(U) hollow s=2 d=5 == 2', U_betti(Lat(5, 5, 5, 2), (5, 5))[0][1] == 2)
# ---- witness dimension (G5-C3)
lat = Lattice((3, 5, 7), 8)
ok('Klein-four (1,2,3): 1 witness, span 2 support 3', (lambda W: len(W) == 1 and W[0]['d_span'] == 2 and W[0]['d_support'] == 3)(WD.witnesses_from_cells((3, 5, 7), 8, (1, 2, 3), lat)))
ok('cells route == template route at Klein (2,2,3)', {WD.canon(w) for w in WD.witnesses_from_cells((3, 5, 7), 8, (2, 2, 3), lat)} == {WD.canon(w) for w in WD.witnesses(lat, (2, 2, 3))})
ok('Klein (1,1,3) embedded, (1,1,4) not', WD.embedded(lat, (1, 1, 3)) and not WD.embedded(lat, (1, 1, 4)))
lat4 = Lattice((2, 2, 2, 2), 3)
W4 = WD.witnesses_from_cells((2, 2, 2, 2), 3, (1, 1, 1, 1), lat4)
ok('parity4 (1,1,1,1): exactly 3 witnesses', len(W4) == 3)
ok('parity4 (1,1,1,1): every witness has d_span 3, support 4, intersection 1', all(w['d_span'] == 3 and w['d_support'] == 4 and w['d_intersection'] == 1 for w in W4))
W4t = WD.witnesses(lat4, (1, 1, 1, 1), maxdim=2)
ok('parity4 (1,1,1,1): template route (cell dim <= 2, complete since |F|=7<8) gives the same 3 witnesses', {WD.canon(w) for w in W4t} == {WD.canon(w) for w in W4})
ok('parity4: all 4 coordinate restrictions of (1,1,1,1) embedded (essential)', WD.analyse_box_cells((2, 2, 2, 2), 3, (1, 1, 1, 1))['essential_coordinate'])
ok('weak G5-C3 FALSE at parity4 (1,1,1,1)', not any(w['d_span'] <= 2 for w in W4))
fl = WD.irreducibility(W4)
ok('parity4 witnesses are irreducible', all(fl))
m24 = WD.analyse_box_cells((5, 7, 13, 23), 24, (4, 1, 1, 1))
ok('mod-24 (4,1,1,1): single witness, d_span 2, d_support 4, essential', m24['n_witnesses'] == 1 and m24['min_span'] == 2 and m24['min_support'] == 4 and m24['essential_coordinate'])
cub = WD.analyse_box_cells((5, 7, 11, 13), 24, (2, 2, 2, 2))
ok('b=24 (5,7,11,13) box (2,2,2,2): all 9 witnesses d_span 3, support 3 (4th coordinate is only a lift off the origin)', cub['n_witnesses'] == 9 and cub['span_histogram'] == {'3': 9} and cub['support_histogram'] == {'3': 9} and cub['essential_coordinate'])
# ---- certificates
c = CE.make_certificate((2, 2, 2, 2), 3, (1, 1, 1, 1), W4[0]); good, info = CE.verify_certificate(c)
ok('certificate verifies', good and info['d_span'] == 3)
bad = copy.deepcopy(c); bad['q'] = [1, 1, 1, 0]
ok('certificate with box too small rejected', not CE.verify_certificate(bad)[0])
bad = copy.deepcopy(c); bad['t'][0] = '1'
ok('certificate with coefficient 1 rejected', not CE.verify_certificate(bad)[0])
bad = copy.deepcopy(c); bad['A'][0] = [2, 0, 0, 0]
ok('certificate with non-Graver generator rejected', not CE.verify_certificate(bad)[0])
print('GEO-I v005 tests: %d checks, %d failures' % tuple(N))
sys.exit(1 if N[1] else 0)
