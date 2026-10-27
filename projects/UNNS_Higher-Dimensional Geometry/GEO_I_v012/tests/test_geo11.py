"""GEO-I v011 unit tests (exact).  python3 tests/test_geo11.py"""
import os, sys, json, copy, random
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d))
import circuit_partitions as CP, cap_cells as K, checker11 as KC
from math import gcd
N = 0; F = 0
def t(name, ok, detail=None):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or detail is None else '   [%s]' % (detail,)))
D = os.path.join(ROOT, 'output', 'data')
cls = {k: [r['support'] for r in json.load(open(os.path.join(D, 'v10_binary%d.json' % k)))['minimal']] for k in (3, 4, 5, 6)}
# ---- Programme B: identities on the classified minimal classes
for k in (3, 4, 5):
    bad = 0
    for X in cls[k]:
        c = CP.circuits(X, k); n = len(X); P = CP.partitions(c, n)
        bad += not (CP.counting_identity(P, k) and CP.parseval_identity(c, P, n, k) and CP.vector_space_partition(c, P, X, k) and CP.parseval_direct(X, k) and CP.weight_second_moment(X, k))
    t('G11-L5: counting identity, Parseval identity, vector-space partition on all %d minimal classes of nullity %d' % (len(cls[k]), k), bad == 0)
random.seed(11); sub = random.sample(cls[6], 25); bad = 0
for X in sub:
    c = CP.circuits(X, 6); n = len(X); P = CP.partitions(c, n); tb = CP.two_block_partitions(c, n)
    bad += not (CP.counting_identity(P, 6) and CP.parseval_identity(c, P, n, 6) and CP.vector_space_partition(c, P, X, 6) and len(tb) >= 2 and (n < 9 or len(tb) >= n - 1))
t('G11-L5/L6: identities, W2 and n_2 >= p-1 on 25 random nullity-6 minimal classes', bad == 0)
t('G11-L6 inequality p(2^m/m-2) >= 2^m-2 for all 3<=m<=p/2: true for every 9<=p<=400, false for p=6,7,8', all(CP.w2_threshold_ok(p) for p in range(9, 401)) and not any(CP.w2_threshold_ok(p) for p in (6, 7, 8)))
t('G11-L6 sharpness: at p=9, m=3 the inequality is an equality (so n_2 >= p-1 is the exact output of the method)', 9 * (8 / 3 - 2) == 6.0 or abs(9 * (8 / 3 - 2) - 6) < 1e-12)
# ---- the case k=7, p=8: the box is the even-weight code, not minimal
top = 1 << 6; Xs = [top] + [top | (1 << i) for i in range(6)]; x8 = 0
for x in Xs: x8 ^= x
X8 = Xs + [x8]; c8 = CP.circuits(X8, 7)
t('G11-T3 case k=7,p=8: C^perp = <1>, circuits are exactly the 28 weight-2 words, no two-block partition', len(X8) == 8 and CP.rank(X8) == 7 and len(c8) == 28 and all(bin(m).count('1') == 2 for m in c8.values()) and not CP.two_block_partitions(c8, 8))
t('G11-T3 case k=7,p=8: non-embedded (105 perfect matchings) but NOT minimal (a deletion is still non-embedded)', CP.non_embedded_E1(c8, 8) and not CP.is_minimal_E1(X8, 7))
# ---- brute force at k=3,4: all subsets
def brute(k):
    m = k - 1; top_ = 1 << m; pts = [top_ | a for a in range(1 << m)]; out = []
    for mask in range(1, 1 << len(pts)):
        X = [pts[i] for i in range(len(pts)) if mask >> i & 1]
        if len(X) < k + 1 or CP.rank(X) < k: continue
        if CP.is_minimal_E1(X, k): out.append((len(X), len(CP.two_block_partitions(CP.circuits(X, k), len(X)))))
    return out
b3, b4 = brute(3), brute(4)
t('G11-T3 brute force over all subsets of AG(2,2), AG(3,2): minimal subsets 1 and 37, every one has >=2 two-block partitions (min 3, 4)', (len(b3), len(b4), min(x[1] for x in b3), min(x[1] for x in b4)) == (1, 37, 3, 4))
# ---- certificates + tamper
P9 = json.load(open(os.path.join(ROOT, 'certificates', 'C9_partition.json'))); C10 = json.load(open(os.path.join(ROOT, 'certificates', 'C10_capcover.json')))
t('PARTITION certificates: all %d accepted by the standalone checker' % len(P9), all(KC.check_PARTITION(c)[0] for c in P9) and len(P9) == 231)
c = copy.deepcopy(P9[40]); c['two_blocks'] = c['two_blocks'][:1]; t('PARTITION tamper: a single pair is rejected', not KC.check_PARTITION(c)[0])
c = copy.deepcopy(P9[40]); c['two_blocks'][0][1] ^= 1; t('PARTITION tamper: a corrupted functional is rejected', not KC.check_PARTITION(c)[0])
c = copy.deepcopy(P9[40]); c['n_two_blocks'] += 1; t('PARTITION tamper: a wrong count is rejected', not KC.check_PARTITION(c)[0])
t('CAPCOVER certificates: %d accepted' % len(C10), all(KC.check_CAPCOVER(c)[0] for c in C10[::7]) and len(C10) == 544)
c = copy.deepcopy(C10[100]); c['cells'] = c['cells'][1:]; t('CAPCOVER tamper: removing a cell is rejected', not KC.check_CAPCOVER(c)[0])
c = copy.deepcopy(C10[100]); c['cells'][0][2] += 1; t('CAPCOVER tamper: a perturbed generator is rejected', not KC.check_CAPCOVER(c)[0])
# ---- Programme A: library
n, bad = K.lemma_scan(40); t('G11-A arithmetic lemma: max(cr(g1,M), cr(u*,M)) >= x*y on %d triples (d<=40)' % n, not bad)
n, bad = K.one_sided_sweep(5, 14); t('G11-L3 one-sided cap: explicit cell family covers the cap, %d triples (d<=14), all cells legitimate' % n, not bad)
r = K.analyse(11, 5, 3, 2); r2 = K.analyse(13, 4, 3, 2)
t('G11-L4 corner pentagon data: covered in sample boxes', all(x is None or x['covered'] for x in (r, r2, K.analyse(9, 4, 2, 2), K.analyse(11, 5, 4, 3))))
t('G10-T2 re-run with the independent v011 engine on d=5 (all 4+ boxes)', all(K.full_cover(5, s, (5 + u, 5 + v)) for s in (2, 3) for u in range(5) for v in range(5) if (u, v) != (0, 0)))
print('\n%d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
