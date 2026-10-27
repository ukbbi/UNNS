"""GEO-I v008 unit tests (exact arithmetic).  python3 tests/test_geo8.py"""
import os, sys, json, copy, itertools
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory', 'certificates', 'experiments', 'tests'): sys.path.insert(0, os.path.join(ROOT, d))
from math import gcd
import small_box as SB, hollow as H, cell_cover as CCv, binary_min as BM, rank_reduce as RRd, binary_01 as B, centre_collisions as CC, rank_reduction as RR
import coverage as C, checker8 as K
from lattice_model import Lat, U_betti
N = 0; F = 0
def t(name, ok):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name)
units = SB.units
# --- Programme A: staircase theorem G8-S
t('G8-S staircase equals definition (d=9,s=2) on every small box', all(SB.squareless(9, 2, (9 + u, 9 + v)) == SB.squareless_staircase(9, 2, (9 + u, 9 + v)) for u in range(9) for v in range(9) if (u, v) != (0, 0)))
t('G8-S count formula: N_sq(7,3) equals enumeration', SB.n_squareless(7, 3) == sum(SB.squareless(7, 3, (7 + u, 7 + v)) for u in range(7) for v in range(7) if (u, v) != (0, 0)))
t('record minimum is non-increasing', all(all(a >= b for a, b in zip(m, m[1:])) for m in (SB.record_min(d, s) for d in range(3, 20) for s in units(d))))
R, T, K_ = SB.extension_points(7, 2, (10, 11)); t('extension points of (7,2,(10,11)): K has (7+1,7+2)', (8, 9) in K_ and len(R) == 3 and len(T) == 4)
t('region labels', [SB.region(7, 3, Q) for Q in ((7, 7), (9, 7), (7, 9), (9, 9))] == ['hollow', 'bottom', 'left', 'interior'])
# --- Programme B: filling lemma
t('G8-T1 filling cells valid for all d<=60, all units (exact)', all(all(H.check_filling(d, s).values()) for d in range(3, 61) for s in units(d)))
t('G8-T1: negative control, R2 does NOT lie in the hollow box (needs Q2>=d+1): corner (t,d+1) outside', all(H.filling_cells(d, 1 if d == 3 else 2 if d % 2 else 3)['R2'][0] for d in (5, 7)) and (lambda d, s: H.corners(H.filling_cells(d, s)['R2'][0])[1][1] == d + 1)(5, 2))
ok = True
for d, s in [(5, 2), (7, 3), (6, 5), (8, 3)]:
    for Q in ((d, d + 1), (d + 1, d)):
        pcs = C.uncovered(Lat(d, d, d, s), Q)
        T1, T2 = H.hollow_triangles(d, s)
        # no leftover piece may meet int T1 or int T2: leftover must be empty
        ok &= (pcs == [])
t('G8-T1 independent path: exact leftover empty at Q=(d,d+1),(d+1,d) for 4 types incl. s=-1', ok)
t('hollow box: leftover area d (G7-T3 regression, both paths)', all(sum(abs(C.area2(p)) for p in C.uncovered(Lat(d, d, d, s), (d, d))) == 2 * d for d, s in [(5, 2), (7, 3), (9, 2)]))
t('s=-1 hollow box beta1=d and beta1=0 after one enlargement (d=5)', U_betti(Lat(5, 5, 5, 4), (5, 5))[0][1] == 5 and U_betti(Lat(5, 5, 5, 4), (5, 6))[0][1] == 0)
# --- Programme C
t('B-SERIES: parallel classes of parity-4 blow-up (2,1,1,1) are 4', len(BM.classes_of(BM.blowup_parity_columns([2, 3, 4, 5], [2, 1, 1, 1]))) == 4)
t('nullity-3 classification: exactly one orbit, p=4, min rank 3', (lambda r: len(r['minimal_reduced_orbits']) == 1 and r['minimal_reduced_orbits'][0]['p'] == 4 and r['min_rank_histogram'] == {3: 1})(BM.classify_nullity(3)))
r4 = BM.classify_nullity(4); t('nullity-4 classification: p in (6,7,8), all min rank 3', sorted(o['p'] for o in r4['minimal_reduced_orbits']) == [6, 7, 8] and r4['min_rank_histogram'] == {3: 3})
t('B-SERIES invariance on a blow-up (3,1,2,1) of parity 4', (lambda r: r['embedded_equal'] and r['minimal_equal'] and r['rank_sets_equal'] and r['collision_counts_equal'])(RRd.check_series_invariance(BM.blowup_parity_columns([2, 3, 4, 5], [3, 1, 2, 1]))))
t('B-NULL prime: every non-embedded box of n<=6 has nullity>=3', all(len(B.codewords(c)) >= 7 for n in range(3, 7) for c in itertools.combinations_with_replacement(range(1, 8), n) if not B.is_embedded(list(c))))
t('B-BASIS: basis+extras enumeration covers all GL classes: counts for n=5,m=2', sum(1 for _ in __import__('rank_attack').basis_sets(5, 2)) == len(list(itertools.combinations_with_replacement(range(1, 4), 3))))
sys.path.insert(0, os.path.join(ROOT, 'tests'))
# --- certificates: positive and negative
def load(n): return json.load(open(os.path.join(ROOT, 'certificates', n)))
t('C1 COVER certificates all VALID', all(K.check_COVER(c)[0] for c in load('C1_cover.json')))
t('C2 GAP certificates all VALID', all(K.check_GAP(c)[0] for c in load('C2_gap.json')))
t('C3 HOMOLOGY certificates all VALID', all(K.check_HOMOLOGY(c)[0] for c in load('C3_homology.json')))
t('C4 RANK certificates all VALID', all(K.check_RANK(c)[0] for c in load('C4_rank.json')))
c = copy.deepcopy(load('C1_cover.json')[0]); c['pieces'][0]['poly'][0] = ['100', '100']; t('COVER tampered piece rejected', not K.check_COVER(c)[0])
c = copy.deepcopy(load('C1_cover.json')[0]); c['hull'] = c['hull'][:-1]; t('COVER tampered hull rejected', not K.check_COVER(c)[0])
c = copy.deepcopy(load('C1_cover.json')[0]); c['cells'][0][1] = [1, 1]; t('COVER non-Graver generator rejected', not K.check_COVER(c)[0])
g = copy.deepcopy(load('C2_gap.json')[0]); g['z'] = ['0', '10']; t('GAP point outside hull rejected', not K.check_GAP(g)[0])
g = copy.deepcopy(load('C2_gap.json')[0]); g['Q'] = [g['Q'][0] + 1, g['Q'][1]]; t('GAP rejected after enlarging the box (the hole is filled, G8-T1)', not K.check_GAP(g)[0])
h = copy.deepcopy(load('C3_homology.json')[0]); h['betti'] = [1, 1, 0]; t('HOMOLOGY wrong Betti rejected', not K.check_HOMOLOGY(h)[0])
h = copy.deepcopy(load('C3_homology.json')[0]); h['faces'][0] = h['faces'][0][:-1]; t('HOMOLOGY broken face cycle rejected', not K.check_HOMOLOGY(h)[0])
r = copy.deepcopy(load('C4_rank.json')[0]); r['min_rank'] = 4; t('RANK wrong min_rank rejected', not K.check_RANK(r)[0])
r = copy.deepcopy(load('C4_rank.json')[0]); r['nullity'] = 4; t('RANK wrong nullity rejected', not K.check_RANK(r)[0])
r = copy.deepcopy(load('C4_rank.json')[0]); r['columns'] = [1, 2, 3, 4]; t('RANK embedded box rejected', not K.check_RANK(r)[0])
t('legacy D1-D3 still accepted by checker8', all(K.KINDS[c['kind']](c)[0] for f in ('D1_coverage.json', 'D2_rank.json', 'D3_hollow.json') for c in load(f)))
print('\n%d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
