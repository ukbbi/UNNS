"""GEO-I v010 unit tests (exact).  python3 tests/test_geo10.py"""
import os, sys, json, copy, itertools, pickle, random, shutil, subprocess, tempfile
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory', 'certificates', 'experiments', 'tests'): sys.path.insert(0, os.path.join(ROOT, d))
import binary5 as B5, binary6 as B6, checker10 as K, modular_sail as MS
from math import gcd
N = 0; F = 0
def t(name, ok, detail=None):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name + ('' if ok or detail is None else '   [%s]' % (detail,)))
D = os.path.join(ROOT, 'output', 'data')
def spanning_affine(m): o = pickle.load(open(os.path.join(D, 'v10_affine_orbits_m%d.pkl' % m), 'rb')); return [R for s in sorted(o) for R in o[s] if B5.rank_of(list(R)) == m + 1]
# --- G10-E1: criterion equals the cell/collision engine
for k in (3, 4):
    sp = spanning_affine(k - 1); bad = 0
    for R in sp:
        C = B5.code_masks(list(R)); bad += (B6.non_embedded(C) != (not B5.embedded(C)))
    t('G10-E1: partition criterion == cell-collision engine on all %d spanning affine classes of nullity %d' % (len(sp), k), bad == 0)
rng = random.Random(10); sp5 = spanning_affine(4); bad = 0
for R in rng.sample(sp5, 12):
    C = B5.code_masks(list(R)); bad += (B6.non_embedded(C) != (not B5.embedded(C)))
t('G10-E1: criterion == engine on 12 random spanning classes of nullity 5', bad == 0)
# --- G10-A1 / orbit counts
bs = {2: 5, 3: 10, 4: 32, 5: 382}
tot = {m: sum(len(v) for v in pickle.load(open(os.path.join(D, 'v10_affine_orbits_m%d.pkl' % m), 'rb')).values()) for m in bs}
t('affine orbit generator: non-empty orbit counts + empty set = Burnside counts 5, 10, 32, 382 for AG(m,2), m=2..5', all(tot[m] + 1 == bs[m] for m in bs), tot)
if shutil.which('gcc'):
    tmp = tempfile.mkdtemp(); exe = os.path.join(tmp, 'ba'); subprocess.run(['gcc', '-O2', '-o', exe, os.path.join(ROOT, 'tools', 'burnside_affine.c')], check=True)
    out3 = subprocess.run([exe, '3'], capture_output=True, text=True).stdout; out4 = subprocess.run([exe, '4'], capture_output=True, text=True).stdout
    t('Burnside program (AGL(m,2)) re-run: m=3 -> 10, m=4 -> 32 orbits including the empty set', 'orbits_incl_empty=10' in out3.replace(' ', '') and 'orbits_incl_empty=32' in out4.replace(' ', ''), (out3.strip()[-40:], out4.strip()[-40:]))
else: print('UNAVAILABLE  gcc not found: Burnside re-run skipped (shipped record checked above)')
# --- classification records
res = {k: json.load(open(os.path.join(D, 'v10_binary%d.json' % k))) for k in (3, 4, 5, 6)}
t('reduced-box classes of nullity 3,4,5 from the affine route: 1, 3, 12 minimal (= v008/v009 classifications)', [len(res[k]['minimal']) for k in (3, 4, 5)] == [1, 3, 12])
t('nullity 6 (G10-T4): 381 affine orbits, 350 spanning, 349 non-embedded, 215 minimal, every minimum witness rank 3', (res[6]['affine_orbits_nonempty'], res[6]['spanning'], res[6]['non_embedded'], len(res[6]['minimal'])) == (381, 350, 349, 215) and all(m['min_rank'] == 3 for m in res[6]['minimal']))
t('nullity 6: all 215 minimal classes satisfy W2 (>=2 two-circuit partitions of the full set); minimum count is 16 = 2^(k-2)', all(m['W2'] for m in res[6]['minimal']) and min(m['two_circuit_partitions_of_1'] for m in res[6]['minimal']) == 16)
cc = {k: json.load(open(os.path.join(D, 'v10_binary%d_crosscheck.json' % k))) for k in (3, 4, 5, 6)}
t('cell-engine cross-check record: every spanning class, nullity 3..6, 0 disagreements (6: 350 classes)', all(cc[k]['disagreements'] == 0 for k in cc) and cc[6]['checked'] == 350)
# --- G10-F1 / G10-R on all 215
ok_f1 = ok_rig = ok_ident = ok_aff = True
for m in res[6]['minimal']:
    sig = m['support']; C = B5.code_masks(sig); n = len(sig); full = (1 << n) - 1
    ok_f1 &= full in C and B6.minimal_criterion(C, n)
    cnt, tot_f = B6.decomposition_profile(C, n)
    ok_rig &= all(v == 1 for u, v in cnt.items() if u != full) and len(cnt) == len(C) - 1
    ok_ident &= (tot_f == len(C) - 2 + cnt.get(full, 0))
    u0 = [u for u in range(1, 1 << 6) if all(bin(u & s).count('1') & 1 for s in sig)]
    ok_aff &= len(u0) == 1
t('G10-F1: every minimal class of nullity 6 contains the all-ones word', ok_f1)
t('G10-R rigidity: every word other than 0, 1 has exactly one decomposition into disjoint circuits (215 classes)', ok_rig)
t('G10-R counting identity: #non-empty disjoint circuit families = 2^k - 2 + #blocks (215 classes)', ok_ident)
t('G10-A1: u0 with u0.s = 1 on the whole support exists and is unique (215 classes)', ok_aff)
# --- G10-L5 explicit witness validated by the cell engine for nullity <= 5
bad = 0
for R in spanning_affine(4):
    C = B5.code_masks(list(R)); n = len(R)
    if B5.embedded(C) or not all(B5.embedded(B5.delete(C, i)) for i in range(n)): continue
    w = B6.rank3_witness(C, n); U, S, T, x = None, w[1], w[2], w[3]
    keys = {(c[1], c[2], c[3], c[4]) for c in B5.collisions(C)}
    bad += not any(set(c[2]) == set(S) and set(c[4]) == set(T) or set(c[2]) == set(T) and set(c[4]) == set(S) for c in B5.collisions(C))
t('G10-L5: the explicit common-base collision built from a double 2-decomposition is a collision of the cell engine (12 classes of nullity 5)', bad == 0)
# --- K_{2,t}
rows = json.load(open(os.path.join(D, 'v10_k2t.json')))
t('G10-K: cut space of K_{2,t}, t=2..10: non-embedded, minimal, rank 3; two-blocks = 2^(t-1) for t>=3 (3 for t=2)', [r['t'] for r in rows] == list(range(2, 11)) and all(r['non_embedded'] and r['minimal'] and r['witness_rank'] == 3 for r in rows) and all(r['two_blocks'] == 2 ** (r['t'] - 1) for r in rows if r['t'] >= 3))
ok = True
for tt in (2, 3, 4, 5):
    C = B6.cut_space_k2t(tt); n = 2 * tt; ok &= (B6.non_embedded(C) == (not B5.embedded(C))) and B6.minimal_criterion(C, n) and B5.minimal(C, n)
t('G10-K recomputed by both engines for t=2..5', ok)
# --- certificates and tamper
c6 = json.load(open(os.path.join(ROOT, 'certificates', 'C6_rank6.json'))); c7 = json.load(open(os.path.join(ROOT, 'certificates', 'C7_k2t.json')))
t('certificates: 215 RANK6 (nullity 6) and 7 RANK6 (K_{2,t}, t=2..8) accepted by the standalone checker10', len(c6) == 215 and len(c7) == 7 and all(K.check_RANK6(c)[0] for c in c6 + c7))
c = copy.deepcopy(c6[5]); c['min_rank'] = 4; t('RANK6 tamper: claimed rank 4 rejected', not K.check_RANK6(c)[0])
c = copy.deepcopy(c6[5]); c['witness']['T'] = c['witness']['S']; t('RANK6 tamper: S == T (not a collision) rejected', not K.check_RANK6(c)[0])
c = copy.deepcopy(c6[5]); a = c['witness']['S'][0]; c['witness']['x'] = a; t('RANK6 tamper: base x inside span(S) rejected', not K.check_RANK6(c)[0])
c = copy.deepcopy(c6[5]); c['support'] = c['support'][:-1]; t('RANK6 tamper: dropped support point (no longer spanning/valid) rejected', not K.check_RANK6(c)[0])
big = next(c for c in c6 if len(c['support']) >= 20); d = copy.deepcopy(big); extra = next(p for p in range(1, 64) if p not in d['support'] and p & 32); d['support'].append(extra)
t('RANK6 tamper: adding a support point to a minimal class (box no longer minimal or witness invalid) rejected', not K.check_RANK6(d)[0])

# --- Programme A: explicit modular-sail covers (G10-S1, G10-S2)
pairs = [(d, s) for d in range(5, 41) for s in range(2, d - 1) if gcd(d, s) == 1]
bad = [(d, s) for d, s in pairs if not (lambda v: v['cells_valid'] and v['remainder_area2'] == 0)(MS.verify_general(d, s))]
t('G10-Z: zonogon cover valid for ALL %d unit pairs 5 <= d <= 40, 2 <= s <= d-2 (cells valid, conv(F) minus (T1 u T2 u cells) has area 0)' % len(pairs), not bad and len(pairs) > 400, bad[:3])
pairs12 = [(d, s) for d, s in pairs if MS.sail_cover(d, s) is not None]
bad = [(d, s) for d, s in pairs12 if not (lambda v: v['cells_valid'] and v['remainder_area2'] == 0)(MS.verify_cover(d, s))]
t('G10-S1/S2 (explicit corollaries): exact covers valid for all %d covered pairs 5 <= d <= 40' % len(pairs12), not bad and len(pairs12) > 150, bad[:3])
sf = json.load(open(os.path.join(D, 'v10_sail_families.json')))
t('G10-Z record: d <= %d: %d unit pairs, 0 failures; S1/S2 explicit %d pairs, 0 failures; engine agreement on %d pairs (d <= %d), 0 failures' % (sf['dmax'], sf['pairs'], sf['explicit_S1_S2_pairs'], sf['engine_checked'], sf['engine_max']), sf['pairs'] > 5000 and not sf['failures'] and not sf['explicit_failures'] and not sf['engine_failures'] and sf['engine_checked'] > 100)
import hollow_check as HC
t('G10-Z vs v005/v009 engine: conv(F) minus U0 = int T1 u int T2 (exact) for (13,3), (11,3), (17,4), (19,5), (9,2)', all(HC.check(d, s)[0] for d, s in ((13, 3), (11, 3), (17, 4), (19, 5), (9, 2))))
t('G10-S2 zonotope identity: g + h4 + h = (d,-d) for the three generators of the hexagon (s,M) in 3..9', all((1 + (M - 1) + (s * M - 1 - M), (s - (s * M - 1)) + (1 - s) - 1) == (s * M - 1, -(s * M - 1)) for s in range(3, 10) for M in range(3, 10)))
cb = json.load(open(os.path.join(ROOT, 'certificates', 'C8_boundary.json')))
sample = cb[::9]
t('BOUNDARY certificates: %d of %d (every 9th) accepted by checker10 (the full list is checked by verify.py)' % (len(sample), len(cb)), len(cb) == 453 and all(K.check_BOUNDARY(c)[0] for c in sample))
c = copy.deepcopy(cb[40]); c['cells'] = c['cells'][1:]; t('BOUNDARY tamper: a cell removed (cover incomplete) rejected', not K.check_BOUNDARY(c)[0])
c = copy.deepcopy(cb[40]); c['cells'][0][1] = [c['cells'][0][1][0] + 1, c['cells'][0][1][1]]; t('BOUNDARY tamper: a generator changed (not a lattice vector / not Graver) rejected', not K.check_BOUNDARY(c)[0])
c = copy.deepcopy(cb[40]); c['s'] = c['s'] + 1 if gcd(c['d'], c['s'] + 1) == 1 else c['s'] + 2; t('BOUNDARY tamper: different s with the same cells rejected', not K.check_BOUNDARY(c)[0])
ok_neg = K.check_BOUNDARY({'kind': 'BOUNDARY', 'd': 8, 's': 3, 'cells': [[list(x[0]), list(x[1]), list(x[2])] for x in MS.sail_cover(13, 3)[1]]})
t('BOUNDARY: cells of another pair do not certify (8,3)', not ok_neg[0])
# --- planar record
sa = json.load(open(os.path.join(D, 'v10_sail_attack.json')))
t('G10-L2 negative record: R-SYM holds on all %d pairs; R-MIR, R-EUC, R-LAT are FALSE with stored counterexamples' % sa['pairs'], sa['rules']['R-SYM']['holds'] and not any(sa['rules'][r]['holds'] for r in ('R-MIR', 'R-EUC', 'R-LAT')) and all(sa['rules'][r]['counterexamples'] for r in ('R-MIR', 'R-EUC', 'R-LAT')))
print('\n%d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
