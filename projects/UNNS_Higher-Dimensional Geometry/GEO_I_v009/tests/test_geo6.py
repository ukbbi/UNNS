"""GEO-I v006 unit tests (exact arithmetic).  python3 tests/test_geo6.py"""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(ROOT, d))
import binary_01 as B, modular_layers as ML, small_boxes as SB, coverage as C
from lattice_model import Lat
N = 0; F = 0
def t(name, ok):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name)
# binary 0/1 engine
t('rank_int basic', B.rank_int([[1, 0, 1], [0, 1, 1], [1, 1, 2]]) == 2)
cw = B.codewords([1, 1, 1, 1]); t('parity4 codewords = 7 even-weight vectors', len(cw) == 7 and all(bin(x).count('1') % 2 == 0 for x in cw))
t('parity4 circuits: 6 pairs', len(B.circuits_of(cw)) == 6)
a = B.analyse([1, 1, 1, 1]); t('parity4: 3 witnesses all span 3, minimal', a['n_witnesses'] == 3 and a['span_hist'] == {3: 3} and B.minimal_nonembedded([1] * 4))
t('parity3 embedded', B.is_embedded([1, 1, 1]))
t('parity5 not minimal (deletion gives parity4 shape)', not B.minimal_nonembedded([1] * 5))
t('independent columns -> trivial lattice embedded', B.is_embedded([1, 2, 4, 8]))
t('theorem B2: parity4 has ONE shared centre (1/2,1/2,1/2,1/2) carrying 3 square cells (-> 3 witness pairs)', {k: len(v) for k, v in B.cells_01([1] * 4)[0].items() if len(v) > 1} == {(15, 0): 3})
t('deletion of a coordinate: parity4 minus coord 0 embedded', B.is_embedded([1, 1, 1, 1], 0b1110))
# modular layers
t('graver basis of (5,2) contains (1,2),(0,5),(5,0)', {(1, 2), (0, 5), (5, 0)} <= ML.graver_set(5, 2))
t('fibre size (5,2) box (7,7)', len(ML.fibre(5, 2, (7, 7))) == len([1 for i in range(8) for j in range(8) if (i or j) and (j - 2 * i) % 5 == 0]))
t('proof cells cover box (7,3) Q=(14,14)', ML.verify_box(7, 3, (14, 14))['ok'] is True)
t('proof cells cover thin box (11,4) Q=(15,30)', ML.verify_box(11, 4, (15, 30))['ok'] is True)
t('proof cells cover thin-y box (11,4) Q=(30,15)', ML.verify_box(11, 4, (30, 15))['ok'] is True)
t('small box regime has no proof cells', ML.proof_cells(7, 2, (9, 11))[1] == 'small')
t('small-box certification (7,2) Q=(10,12)', SB.certify_box(7, 2, (10, 12))['ok'])
t('hollow box (7,2): hull NOT covered at (d,d)', len(C.uncovered(Lat(7, 7, 7, 2), (7, 7))) > 0)
t('hollow area = d (area2 = 2d), s=3,d=7', sum(abs(C.area2(p)) for p in C.uncovered(Lat(7, 7, 7, 3), (7, 7))) == 14)
t('non-hollow: (7,3) Q=(8,7) covered', len(C.uncovered(Lat(7, 7, 7, 3), (8, 7))) == 0)
print('GEO-I v006 tests: %d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
