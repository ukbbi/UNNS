"""GEO-I v007 unit tests (exact arithmetic).  python3 tests/test_geo7.py"""
import os, sys, json, subprocess, copy
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d))
import binary_01 as B, binary_circuits as BC, centre_collisions as CC, rank_reduction as RR, corner_sail as CS, coverage_lemmas as CL, hollow_geometry as HG
import modular_layers as ML, coverage as C, checker as K
N = 0; F = 0
def t(name, ok):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name)
# --- Programme A
t('columns(7,3,(9,14)): column 0 bottom is d (origin removed)', CS.columns(7, 3, (9, 14))[0][0] == 7)
r = CS.verify_col_box(7, 3, (9, 14)); t('A-COL (7,3,(9,14)) exact cover', r['ok'] and all(r['lemmas'].values()))
try: CS.strip_cells(7, 3, (20, 9)); ok = False
except AssertionError: ok = True
t('strip_cells refuses Q2<2d (assertion)', ok)
t('A-COL s=-1 (hull edge (0,d)-(d,0) is the exception): (7,6,(9,14)) cover', CS.verify_col_box(7, 6, (9, 14))['ok'])
t('A-COL composite d=12, s=5', CS.verify_col_box(12, 5, (14, 24))['ok'])
t('A-COL d=2', CS.verify_col_box(2, 1, (3, 4))['ok'])
t('lower_pieces: collinear intermediate points kept', CS.lower_pieces([(0, 2), (1, 1), (2, 0), (3, 3)]) == [((0, 2), (1, 1)), ((1, 1), (2, 0)), ((2, 0), (3, 3))])
t('squareless: (7,3) Q=(8,7): r=(1,0), no nonzero Gamma point in [0,1]x[0,0]', CL.squareless(7, 3, (8, 7)))
t('squareless false when Gamma point in [0,r1]x[0,r2]: (7,2),(10,11)? point (1,2)', not CL.squareless(7, 2, (10, 11)))
t('HYP-LL stays FALSE: step failure exists for (5,1,(5,7))', len(CL.hypll_step_failures(5, 1, (5, 7))) > 0)
t('HYP-LL failures never coexist with r1>0,r2>0 and max(Q)>=2d (d<=8)', all(not CL.hypll_step_failures(d, s, (a, b)) for d in range(3, 9) for s in CL.units(d) for a in range(d + 1, 3 * d) for b in range(d + 1, 3 * d) if max(a, b) >= 2 * d))
# --- Programme B
t('B-DELTA on parity4', RR.check_box([1, 1, 1, 1])['delta_in_span'])
t('B-COSET full-support cells of parity4: 3 partitions x 1 nonzero coset', len(BC.full_support_cells([1, 1, 1, 1])) == 3)
t('B-COSET cross-check with cells_01 on [1,1,2,2,3,3]', CC.check_facts([1, 1, 2, 2, 3, 3])['coset_description'])
t('B-NULL nullity of [1,1,1,1] is 3', BC.nullity([1, 1, 1, 1]) == 3)
t('B-NULL: nullity>=3 whenever full-support collision (spot)', all(CC.check_facts(c)['F3'] for c in ([1, 1, 1, 1, 1], [1, 1, 2, 2, 3, 3], [1, 2, 3, 1, 2, 3, 1])))
t('F1: no segment collisions in [1,1,1,1,1]', CC.check_facts([1] * 5)['F1'])
t('collision type (3,2) exists in [1,1,2,2,3,3]', any(sorted((len(a[2]), len(b[2]))) == [2, 3] for _, a, b in CC.collisions([1, 1, 2, 2, 3, 3])))
t('atom criterion agrees with ranks on [1,1,2,2,3,4,7]', RR.check_box([1, 1, 2, 2, 3, 4, 7])['atom_ok'])
t('minimal box [1,1,2,2,4,4,7,7] has min witness rank 3', RR.check_box([1, 1, 2, 2, 4, 4, 7, 7])['min_rank'] == 3)
t('embedded box has no collisions: [1,2,4,8]', CC.collisions([1, 2, 4, 8]) == [])
# --- Programme C
t('hollow certificate d=7 s=3', HG.check_hollow(7, 3)['ok'])
t('hollow certificate s=-1 d=7 (beta1>=2; true beta1=d)', HG.check_hollow(7, 6)['ok'])
t('hollow F structure d=9 s=2', HG.check_hollow(9, 2)['F_structure'])
t('triangle edge-meets test: segment through open triangle detected', HG.seg_meets_open_tri([(0, 0), (4, 0), (0, 4)], (-1, 1), (3, 1)))
t('triangle edge-meets test: boundary segment not interior', not HG.seg_meets_open_tri([(0, 0), (4, 0), (0, 4)], (0, 0), (4, 0)))
# --- Programme D: checker accepts / rejects
D1 = json.load(open(os.path.join(ROOT, 'certificates', 'D1_coverage.json')))
t('D1 certificates valid', all(K.check_D1(c)[0] for c in D1))
bad = copy.deepcopy(D1[0]); bad['pieces'].pop()
t('D1 checker rejects a certificate with a missing piece (area mismatch)', not K.check_D1(bad)[0])
bad = copy.deepcopy(D1[0]); u, g, h = bad['cells'][0]; bad['cells'][0] = [u, [g[0] * 2, g[1] * 2], h]
t('D1 checker rejects a cell with a non-Graver generator', not K.check_D1(bad)[0])
t('D2 checker rejects embedded box [1,2,4,8]', not K.check_D2({'columns': [1, 2, 4, 8], 'min_rank': 3})[0])
t('D2 checker rejects non-minimal box [1,1,1,1,1]', not K.check_D2({'columns': [1] * 5, 'min_rank': 3})[0])
t('D2 checker rejects wrong min rank', not K.check_D2({'columns': [1, 1, 1, 1], 'min_rank': 4})[0])
t('D3 checker rejects non-unit s', not K.check_D3({'d': 8, 's': 2})[0])
print('GEO-I v007 tests: %d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
