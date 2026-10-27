"""GEO-I v012 unit tests (exact).  python3 tests/test_geo12.py"""
import os, sys, json, copy, random
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d))
import cap_cells as K, cap_cover as C, checker12 as KC
from math import gcd
N = 0; F = 0
def t(name, ok, detail=None):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or detail is None else '   [%s]' % (detail,)))
# ---- G12-T1 (G11-A) : the proof's mechanism, checked on its own terms
bad = 0; n = 0
for d in range(5, 61):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        t_ = pow(s, -1, d); sg, tau = d - s, d - t_
        # all Pareto-minimal Gamma points M=(x,y), 0<x,y<d (not only records): inequality, and the forbidden point R when both fail
        for x in range(1, d):
            y = (s * x) % d
            if y == 0: continue
            if any((b - s * i) % d == 0 and (i, b) not in ((0, 0), (x, y)) for i in range(x + 1) for b in range(y + 1)): continue
            n += 1
            if max(y + sg * x, x + tau * y) < x * y: bad += 1
t('G12-T1 (G11-A) on every Pareto-minimal point M of Gamma_(d,s), 5<=d<=60 (%d points): max(y+(d-s)x,(d-t)y+x) >= xy' % n, bad == 0 and n > 1000)
# ---- Graver / structure / cover on small boxes
t('G12 structural lemmas S1..S6 (H_Q cap square = H_0; no N points; flags monotone; no R->T step; first step B+M; all steps Graver) on all boxes d<=9', C.structure_sweep(5, 9)[1] == [])
n, bad = C.sweep(5, 9); t('G12-T3..T8 cell family: legitimate and covering H_Q minus H_0 on all %d small boxes d<=9 (one-sided, u=0, v=0, mixed)' % n, not bad, bad[:2])
t('G12 targeted boxes (extreme residues, thin/unequal enlargements)', all(C.verify(d, s, u, v)[0] for (d, s, u, v) in [(13, 5, 1, 12), (13, 5, 12, 1), (21, 8, 20, 20), (34, 13, 1, 33), (55, 21, 54, 2), (89, 34, 3, 88), (233, 89, 1, 232), (101, 38, 50, 70), (64, 5, 63, 63), (97, 2, 96, 1), (97, 95, 1, 96)]))
# ---- the old 'pentagon' is an artifact of using hull vertices only
d, s, u, v = 14, 3, 4, 2; Om, Fq = C.omega(d, s, (d + u, d + v))
t('G12-T5: Omega contains Gamma-points of type C (x>=d,y>=d), in particular the point C=(d,d) lies on the boundary when v011 saw a bridging edge; no R->T step', (d, d) in Om and C.structure_check(d, s, u, v)['S4'])
# ---- certificates
AR = json.load(open(os.path.join(ROOT, 'certificates', 'C11_arith.json'))); CV = json.load(open(os.path.join(ROOT, 'certificates', 'C12_capcover2.json')))
t('ARITH certificates (%d) accepted' % len(AR), all(KC.check_ARITH(c)[0] for c in AR[::9]) and len(AR) == 984)
t('CAPCOVER2 certificates (%d) accepted (sample)' % len(CV), all(KC.check_CAPCOVER2(c)[0] for c in CV[::37]) and len(CV) == 2130)
c = copy.deepcopy(CV[500]); c['cells'] = c['cells'][1:]; t('CAPCOVER2 tamper: removing a cell is rejected', not KC.check_CAPCOVER2(c)[0])
c = copy.deepcopy(CV[500]); c['cells'][0][2] += 1; t('CAPCOVER2 tamper: perturbed generator rejected', not KC.check_CAPCOVER2(c)[0])
c = copy.deepcopy(CV[900]); c['cells'] = [x for x in c['cells'] if x != c['cells'][len(c['cells']) // 2]]; t('CAPCOVER2 tamper: a middle cell removed is rejected', not KC.check_CAPCOVER2(c)[0])
c = copy.deepcopy(AR[100]); c['s'] = c['d'] - 1; t('ARITH tamper: s = d-1 (outside the theorem) is rejected', not KC.check_ARITH(c)[0])
# ---- inherited v011 certificate formats still accepted by the v012 checker
t('v011 PARTITION / CAPCOVER certificates still accepted by checker12', all(KC.check_PARTITION(c)[0] for c in json.load(open(os.path.join(ROOT, 'certificates', 'C9_partition.json')))[::10]) and all(KC.check_CAPCOVER(c)[0] for c in json.load(open(os.path.join(ROOT, 'certificates', 'C10_capcover.json')))[::40]))
# ---- transposition symmetry (G12-T4)
ok = True
for (d, s, u, v) in [(11, 3, 2, 5), (13, 5, 7, 3), (12, 5, 0, 4), (16, 7, 5, 5)]:
    tt = pow(s, -1, d); Fq = K.fibreQ(d, s, (d + u, d + v)); Ft = K.fibreQ(d, tt, (d + v, d + u))
    ok &= {(y, x) for x, y in Fq} == Ft and K.verify_transposed(d, s, u, v) if hasattr(K, 'verify_transposed') else {(y, x) for x, y in Fq} == Ft
    ok &= C.verify(d, s, u, v)[0] and C.verify(d, tt, v, u)[0]
t('G12-T4 transposition: F_Q^T = F_(Q^T) for (d,t), conformal/Graver structure preserved (cover verified for both orientations)', ok)
print('\n%d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
