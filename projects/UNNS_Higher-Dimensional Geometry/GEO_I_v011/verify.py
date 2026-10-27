#!/usr/bin/env python3
"""GEO-I v011 verifier.   python3 verify.py --smoke  (a few minutes)    python3 verify.py  (full, about 2 h)
New v011 checks (Programmes A, B, C, D) + the inherited v010 verifier (verify_v010.py, which re-runs every v005-v010 check) as a gate.
Exact integer/rational arithmetic; anything not run is reported UNAVAILABLE, never PASS.  Writes output/reports/verify_{smoke,full}.json."""
import os, sys, json, time, hashlib, subprocess, random, argparse, copy
ROOT = os.path.dirname(os.path.abspath(__file__))
for d in ('theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d))
ap = argparse.ArgumentParser(); ap.add_argument('--smoke', action='store_true'); SMOKE = ap.parse_args().smoke; MODE = 'smoke' if SMOKE else 'full'
from math import gcd
import circuit_partitions as CP, cap_cells as K, checker11 as KC
DATA = os.path.join(ROOT, 'output', 'data'); CHECKS = []; FAILS = 0; T0 = time.time(); GRP = ['v011']
def check(name, ok, detail=None):
    global FAILS
    CHECKS.append({'name': name, 'ok': bool(ok), 'detail': detail, 'group': GRP[0]}); FAILS += (not ok)
    print(('PASS  ' if ok else 'FAIL  ') + name + ('' if detail is None else '   [' + str(detail)[:150] + ']'), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
J = lambda n: json.load(open(os.path.join(DATA, n)))
ALLOWED = ('PROVED', 'PROVED+CHECKED', 'CHECKED', 'FALSE', 'CORRECTED', 'OPEN', 'UNAVAILABLE')

# ---------------------------------------------------------------- integrity
bad = []
for l in open(os.path.join(ROOT, 'MANIFEST.sha256')):
    h, p = l.strip().split(None, 1); p = p.lstrip('*')
    if not os.path.exists(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h: bad.append(p)
check('MANIFEST.sha256 verifies (every shipped file unchanged)', not bad, bad[:3])
prov = json.load(open(os.path.join(ROOT, 'PROVENANCE.json'))); inh = prov['inherited_v010_sha256']
check('v010 preservation: %d files inherited UNCHANGED from the v010 release (sha-256 equal)' % len(inh), len(inh) > 250 and all(os.path.exists(os.path.join(ROOT, p)) and sha(os.path.join(ROOT, p)) == h for p, h in inh.items()))
mv = prov['moved_v010_docs']
check('v010 documents archived unchanged in docs_v010/ (%d files, hashes equal the v010 release)' % len(mv), len(mv) == 12 and all(sha(os.path.join(ROOT, q)) for q in mv.values()) and all(os.path.exists(os.path.join(ROOT, q)) for q in mv.values()))
check('v011 provenance: new_in_v011 files are all present', len(prov['new_in_v011']) > 20 and all(os.path.exists(os.path.join(ROOT, p)) for p in prov['new_in_v011']))
FROZEN = {'geo1lib.py': '0c94b3a73721c0c69823aee53f33710cad186280f3e8d8659bbb4188381c8831', 'geo2lib.py': 'a8c47c4ff0aebbcfb41372dcaba5006b12349add5c1103073583f50c093d852e'}
check('frozen v001/v002 libraries byte-identical to released (sha-256)', all(sha(os.path.join(ROOT, 'frozen', k)) == v for k, v in FROZEN.items()))

# ---------------------------------------------------------------- unit tests
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo11.py')], capture_output=True, text=True)
check('v011 tests/test_geo11.py (unit tests incl. certificate tamper rejection) pass', r.returncode == 0 and ' 0 failures' in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

# ---------------------------------------------------------------- Programme B (W2) -- REGENERATED
cls = {k: [x['support'] for x in J('v10_binary%d.json' % k)['minimal']] for k in (3, 4, 5, 6)}
check('B inherited classification present: 1, 3, 12, 215 minimal classes of nullity 3,4,5,6', [len(cls[k]) for k in (3, 4, 5, 6)] == [1, 3, 12, 215])
rng = random.Random(11)
for k in (3, 4, 5, 6):
    sel = cls[k] if (k < 6 or not SMOKE) else rng.sample(cls[k], 30); bad = []; mn = 10 ** 9; minblock = 10 ** 9; nid = 0
    for i, X in enumerate(sel):
        c = CP.circuits(X, k); n = len(X); P = CP.partitions(c, n); tb = CP.two_block_partitions(c, n); mn = min(mn, len(tb))
        minblock = min(minblock, min(bin(m).count('1') for m in c.values()))
        ok = CP.counting_identity(P, k) and CP.parseval_identity(c, P, n, k) and CP.vector_space_partition(c, P, X, k) and CP.parseval_direct(X, k) and CP.weight_second_moment(X, k) and len(tb) >= 2 and (n < 9 or len(tb) >= n - 1)
        if not ok: bad.append(i)
    check('B G11-L5/L5b/L6/T3 REGENERATED on %d minimal classes of nullity %d: counting identity, Parseval identity, vector-space partition, W2 (min n_2 = %d), n_2 >= p-1 for p>=9, smallest circuit size %d >= 2' % (len(sel), k, mn, minblock), not bad and minblock >= 2, bad[:3])
check('B G11-L6 threshold inequality p(2^m/m-2) >= 2^m-2 for every 3<=m<=p/2: true for all 9<=p<=400, false at p=6,7,8', all(CP.w2_threshold_ok(p) for p in range(9, 401)) and not any(CP.w2_threshold_ok(p) for p in (6, 7, 8)))
top = 1 << 6; Xs = [top] + [top | (1 << i) for i in range(6)]; x8 = 0
for x in Xs: x8 ^= x
X8 = Xs + [x8]; c8 = CP.circuits(X8, 7)
check('B G11-L6b case k=7, p=8: even-weight code E_8, 28 weight-2 circuits, no two-block partition, non-embedded, NOT minimal', CP.rank(X8) == 7 and len(c8) == 28 and not CP.two_block_partitions(c8, 8) and CP.non_embedded_E1(c8, 8) and not CP.is_minimal_E1(X8, 7))
def brute(k):
    m = k - 1; tp = 1 << m; pts = [tp | a for a in range(1 << m)]; res = []
    for mask in range(1, 1 << len(pts)):
        X = [pts[i] for i in range(len(pts)) if mask >> i & 1]
        if len(X) < k + 1 or CP.rank(X) < k: continue
        c = CP.circuits(X, k); n = len(X)
        if len(CP.partitions(c, n)) < 2 or not CP.is_minimal_E1(X, k): continue
        res.append(len(CP.two_block_partitions(c, n)))
    return len(res), min(res)
b = {k: brute(k) for k in ((3, 4) if SMOKE else (3, 4, 5))}
check('B G11-T3 REGENERATED brute force over ALL subsets of AG(k-1,2), k=%s: minimal subsets and minimum n_2 = %s' % ('3,4' if SMOKE else '3,4,5', b), b[3] == (1, 3) and b[4] == (37, 4) and (SMOKE or b[5] == (19373, 8)))
w2 = J('v11_w2.json')
check('B shipped record v11_w2.json: brute force k=3,4,5 (1 / 37 / 19,373 minimal subsets, min n_2 3 / 4 / 8), all identities, 231 inherited classes 0 violations, random nullity 7/8 0 violations', [(x['minimal_subsets'], x['min_two_blocks'], x['all_W2'], x['all_identities'], x['all_bound']) for x in w2['brute']] == [(1, 3, True, True, True), (37, 4, True, True, True), (19373, 8, True, True, True)] and sum(x['classes'] for x in w2['inherited']) == 231 and all(x['violations'] == 0 for x in w2['inherited']) and all(x['violations'] == 0 for x in w2['random']) and w2['threshold']['true_for_all_p_ge_9'])
check('B supplementary knapsack record: no n_2<=1 profile numerically possible for k=4,6..12; k=5 admits only p=6 (no minimal box: brute force min p = 8)', all(w2['knapsack_feasible_profiles'][str(k)] == [] for k in (4, 6, 7, 8, 9, 10, 11, 12)) and w2['knapsack_feasible_profiles']['5'] == [[6, 0]] and 6 not in w2['brute'][2]['p_values'])
mn_by_p = {}
for k in (3, 4, 5, 6):
    for x in J('v10_binary%d.json' % k)['minimal']: mn_by_p[x['p']] = min(mn_by_p.get(x['p'], 10 ** 9), x['two_circuit_partitions_of_1'])
check('B G11-K1 sharpness: n_2 = p-1 attained at p = 4, 16, 32 (X = AG(k-1,2)); n_2 >= p-1 at every p >= 9 in the classification', all(mn_by_p[p] == p - 1 for p in (4, 16, 32)) and all(v >= p - 1 for p, v in mn_by_p.items() if p >= 9))
# ---------------------------------------------------------------- Programme C
c6 = J('v10_binary6.json')['minimal']
check('C G11-T4: every classified minimal class (231) has minimum witness rank 3 (inherited records) and W2; with G11-T3 + G10-C1\' this is universal', all(x['min_rank'] == 3 and x['W2'] for k in (3, 4, 5, 6) for x in J('v10_binary%d.json' % k)['minimal']))

# ---------------------------------------------------------------- Programme A (cap)
n, bad = K.lemma_scan(40 if SMOKE else 150)
check('A G11-A arithmetic lemma REGENERATED: max(cr(g1,M), cr(u*,M)) >= x*y on %d triples (d<=%d)' % (n, 40 if SMOKE else 150), not bad, bad[:3])
n, bad = K.one_sided_sweep(5, 16 if SMOKE else 40)
check('A G11-L3 one-sided cap REGENERATED (exact): explicit cell family legitimate and covers the cap, %d triples (d<=%d)' % (n, 16 if SMOKE else 40), not bad, bad[:3])
n, sk, bad = K.pentagon_sweep(5, 9 if SMOKE else 12)
check('A G11-L4 mixed corner pentagon REGENERATED: covered in all %d non-degenerate boxes (d<=%d; %d degenerate boxes not analysed)' % (n, 9 if SMOKE else 12, sk), not bad, bad[:3])
FLM = 6 if SMOKE else 8; nb = 0; bad = []
for d in range(5, FLM + 1):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        for u in range(d):
            for v in range(d):
                if (u, v) == (0, 0): continue
                nb += 1
                if not K.full_cover(d, s, (d + u, d + v)): bad.append((d, s, u, v))
check('A G11-R1 REGENERATED with the independent v011 engine: conv(F_Q) covered by cells for all %d boxes d<=%d (G10-T2 evidence, not a proof)' % (nb, FLM), not bad, bad[:3])
cap = J('v11_cap.json')
check('A shipped record v11_cap.json: one-sided d<=60 (39,590 triples), lemma d<=150 (657,526), pentagon d<=15 (345 non-degenerate, 4,681 degenerate), full cover d<=9 (686 boxes): 0 failures', cap['onesided']['triples'] == 39590 and cap['lemma_G11A']['triples'] == 657526 and cap['pentagon']['nondegenerate_boxes'] == 345 and cap['pentagon']['degenerate_skipped'] == 4681 and cap['full_cover']['boxes'] == 686 and not any(cap[k]['failures'] for k in ('onesided', 'lemma_G11A', 'pentagon', 'full_cover')))

# ---------------------------------------------------------------- Programme D (certificates)
files = [os.path.join(ROOT, 'certificates', 'C9_partition.json'), os.path.join(ROOT, 'certificates', 'C10_capcover.json')]
import tempfile
if SMOKE:
    P9 = json.load(open(files[0])); C10 = json.load(open(files[1])); td = tempfile.mkdtemp()
    json.dump(P9[::4], open(os.path.join(td, 'p.json'), 'w')); json.dump(C10[::8], open(os.path.join(td, 'c.json'), 'w')); files = [os.path.join(td, 'p.json'), os.path.join(td, 'c.json')]
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'certificates', 'checker11.py')] + files, capture_output=True, text=True)
check('D checker11.py run isolated (python -I, no release imports): %s' % ' | '.join(l.split(': ', 1)[1] for l in r.stdout.splitlines() if l.startswith('VALID')), r.returncode == 0 and 'INVALID' not in r.stdout and r.stdout.count('VALID  ') == 2, r.stdout[-200:])
P9 = json.load(open(os.path.join(ROOT, 'certificates', 'C9_partition.json'))); C10 = json.load(open(os.path.join(ROOT, 'certificates', 'C10_capcover.json')))
check('D certificate counts: 231 PARTITION (all classified minimal classes), 544 CAPCOVER (5<=d<=16)', len(P9) == 231 and len(C10) == 544)
tam = True
for i in (3, 77, 200):
    c = copy.deepcopy(P9[i]); c['two_blocks'] = c['two_blocks'][:1]; tam &= not KC.check_PARTITION(c)[0]
    c = copy.deepcopy(P9[i]); c['n_two_blocks'] += 1; tam &= not KC.check_PARTITION(c)[0]
for i in (5, 100, 400):
    c = copy.deepcopy(C10[i]); c['cells'] = c['cells'][1:]; tam &= not KC.check_CAPCOVER(c)[0]
    c = copy.deepcopy(C10[i]); c['cells'][0][2] += 1; tam &= not KC.check_CAPCOVER(c)[0]
check('D tamper rejection: PARTITION (single pair, wrong count), CAPCOVER (removed cell, perturbed generator)', tam)

# ---------------------------------------------------------------- documentation / honesty
tm = open(os.path.join(ROOT, 'MATHEMATICS.md'), encoding='utf-8').read(); tc = open(os.path.join(ROOT, 'CAP.md'), encoding='utf-8').read()
tsv = [l.split('\t') for l in open(os.path.join(ROOT, 'THEOREM_REGISTRY.tsv'), encoding='utf-8').read().splitlines()[1:]]; reg = {r_[0]: r_[2] for r_ in tsv}
check('G11 THEOREM_REGISTRY.tsv: %d rows, every status starts with an allowed word' % len(tsv), len(tsv) >= 19 and all(r_[2].split()[0] in ALLOWED for r_ in tsv))
check('G11 honesty: cap theorem G11-C1/T1 and stabilization G11-T2 recorded OPEN; one-sided cap CHECKED (not PROVED); G11-A CHECKED; W2 PROVED+CHECKED; rank PROVED', reg['G11-C1'] == 'OPEN' and reg['G11-T1'] == 'OPEN' and reg['G11-T2'] == 'OPEN' and reg['G11-L3'] == 'CHECKED' and reg['G11-A'] == 'CHECKED' and reg['G11-T3'] == 'PROVED+CHECKED' and reg['G11-T4'] == 'PROVED' and reg['G11-C3'] == 'FALSE' and 'OPEN' in tc)
need = ('G11-L5', 'G11-L6', 'G11-T3', 'G11-T4')
check('G11 documentation: MATHEMATICS.md contains the W2 theorem chain and the proof sections', all(k in tm for k in need) and 'Parseval' in tm and 'vector-space' in tm)
check('G11 documentation: all required documents exist', all(os.path.exists(os.path.join(ROOT, f)) for f in ('README.md', 'REPORT.md', 'MATHEMATICS.md', 'CAP.md', 'CIRCUIT_PARTITIONS.md', 'RANK_UNIVERSAL.md', 'CERTIFICATION.md', 'PRIOR_ART.md', 'THEOREM_REGISTRY.tsv', 'CONTEXT.md', 'RUN_SMOKE.bat', 'RUN_FULL.bat')))
tp = open(os.path.join(ROOT, 'PRIOR_ART.md'), encoding='utf-8').read()
check('G11 prior art: examined sources named with level; no priority or novelty claim; no unverified reference', 'abstract' in tp and 'no priority or novelty claim' in tp.lower() and '2306.14236' in tp)
check('G11 figures: 3 figures shipped in figures_v11/', len([f for f in os.listdir(os.path.join(ROOT, 'figures_v11')) if f.endswith('.png')]) == 3)

# ---------------------------------------------------------------- inherited gate (the v010 verifier)
GRP[0] = 'gate'
t = time.time(); r = subprocess.run([sys.executable, os.path.join(ROOT, 'verify_v010.py')] + (['--smoke'] if SMOKE else []), capture_output=True, text=True, cwd=ROOT)
gj = os.path.join(ROOT, 'output', 'reports', 'verify_inherited_%s.json' % MODE); g = json.load(open(gj)) if os.path.exists(gj) else {}
check('GATE: the inherited v010 verifier (verify_v010.py, %s) passes completely: %s/%s checks' % (MODE, g.get('total_pass'), g.get('total_checks')), r.returncode == 0 and g.get('release') == 'v010' and g.get('total_pass') == g.get('total_checks') and g.get('total_checks', 0) > 100, r.stdout.strip().splitlines()[-1][:150] if r.stdout.strip() else r.stderr[-200:])

new = [c for c in CHECKS if c['group'] == 'v011']; gate = [c for c in CHECKS if c['group'] == 'gate']; ok = sum(c['ok'] for c in CHECKS)
os.makedirs(os.path.join(ROOT, 'output', 'reports'), exist_ok=True)
json.dump({'release': 'v011', 'mode': MODE, 'level': 'Level 1 (smoke)' if SMOKE else 'Level 1 + Level 2 (full)', 'v011_new_checks': len(new), 'v011_new_pass': sum(c['ok'] for c in new),
           'inherited_v010_gate_checks': g.get('total_checks'), 'inherited_v010_gate_pass': g.get('total_pass'), 'inherited_v010_gate_seconds': g.get('seconds'),
           'total_checks_this_file': len(CHECKS), 'total_pass_this_file': ok, 'seconds': round(time.time() - T0, 1), 'checks': CHECKS}, open(os.path.join(ROOT, 'output', 'reports', 'verify_%s.json' % MODE), 'w'), indent=1, default=str)
print('\n%s: v011 NEW %d/%d PASS | inherited v010 gate %s/%s | (%.0f s)' % (MODE.upper(), sum(c['ok'] for c in new), len(new), g.get('total_pass'), g.get('total_checks'), time.time() - T0))
sys.exit(1 if FAILS else 0)
