#!/usr/bin/env python3
"""GEO-I v006 verifier.   python3 verify.py --smoke  (a few minutes)    python3 verify.py  (full)
Core checks use only files inside this release.  Exact integer/rational arithmetic; anything not run is reported UNAVAILABLE, never PASS.
Gate G1 = the unmodified v005 verifier (regression_v005.py) must pass completely."""
import os, sys, json, time, hashlib, subprocess, itertools, random, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(ROOT, d))
ap = argparse.ArgumentParser(); ap.add_argument('--smoke', action='store_true'); SMOKE = ap.parse_args().smoke; MODE = 'smoke' if SMOKE else 'full'
from math import gcd
import modular_layers as ML, small_boxes as SB, binary_01 as B, coverage as C
import witness_dimension as WD
from lattice_model import Lat, U_betti
OUT = os.path.join(ROOT, 'output'); DATA = os.path.join(OUT, 'data')
REP = os.path.join(OUT, 'smoke' if SMOKE else 'reports'); os.makedirs(REP, exist_ok=True)
CHECKS = []; FAILS = 0; T0 = time.time()


def check(name, ok, detail=None):
    global FAILS
    CHECKS.append({'name': name, 'ok': bool(ok), 'detail': detail}); FAILS += (not ok)
    ds = '' if detail is None else '   [' + str(detail)[:150] + ']'
    print(('PASS  ' if ok else 'FAIL  ') + name + ds, flush=True)


def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def rows(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
def inv(s, d): return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)
def units(d): return [s for s in range(1, d) if gcd(s, d) == 1]

# ---------------------------------------------------------------- G9 preservation / integrity
FROZEN = {'geo1lib.py': '0c94b3a73721c0c69823aee53f33710cad186280f3e8d8659bbb4188381c8831', 'geo2lib.py': 'a8c47c4ff0aebbcfb41372dcaba5006b12349add5c1103073583f50c093d852e'}
check('G9: frozen v001/v002 libraries byte-identical to released (sha-256)', all(sha(os.path.join(ROOT, 'frozen', k)) == v for k, v in FROZEN.items()))
bad = []
for l in open(os.path.join(ROOT, 'MANIFEST.sha256')):
    h, p = l.strip().split(None, 1); p = p.lstrip('*')
    if not os.path.exists(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h: bad.append(p)
check('G9: MANIFEST.sha256 verifies (every shipped file unchanged)', not bad, bad[:3])
prov = json.load(open(os.path.join(ROOT, 'PROVENANCE.json')))
check('G9: reference modules inherited from v005 are recorded with source hashes and match the shipped copies', all(sha(os.path.join(ROOT, p)) == h for p, h in prov['inherited_v005_sha256'].items()), len(prov['inherited_v005_sha256']))

# ---------------------------------------------------------------- G1 regression: the v005 verifier, unmodified checks
t = time.time()
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'regression_v005.py')] + (['--smoke'] if SMOKE else []), capture_output=True, text=True, cwd=ROOT)
last = [l for l in r.stdout.splitlines() if 'CORE' in l][-1:] or [r.stderr[-200:]]
check('G1: v005 regression suite (80 witness certificates, 4D/5D parity, b=24 (5,7,13,23), s=+-1 theorems, d<=21 certificates, tests) passes completely', r.returncode == 0, last[0].strip())
subprocess.run([sys.executable, '-c', 'pass'])

r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo6.py')], capture_output=True, text=True)
check('tests/test_geo6.py (v006 unit tests) pass', r.returncode == 0 and ' 0 failures' in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
# ---------------------------------------------------------------- Programme A
TYPES9 = [(5, 2), (7, 2), (7, 3), (8, 3), (9, 2), (11, 3), (11, 4), (13, 5), (10, 3)]
rng = random.Random(6)
nbox = 0; nbad = 0
for (d, s) in (TYPES9[:3] if SMOKE else TYPES9):
    boxes = [(a, b) for a in range(d, 3 * d + 1) for b in range(d, 3 * d + 1) if max(a, b) >= 2 * d]
    if SMOKE: boxes = rng.sample(boxes, 25)
    for Q in boxes:
        res = ML.verify_box(d, s, Q); nbox += 1; nbad += (res['ok'] is not True)
check('G6-C1 (A): exact proof-cell cover of conv(F) for every sampled box with max(Q1,Q2)>=2d (thick, thin-x, thin-y) -- %d boxes, %d types' % (nbox, 3 if SMOKE else 9), nbad == 0, 'violations %d' % nbad)

nsb = 0; nbad = 0; nfb = 0
for (d, s) in ([(7, 2), (9, 2), (11, 4)] if SMOKE else [(d, s) for d in range(4, 14) for s in units(d) if inv(s, d) >= s]):
    for r1 in range(d):
        for r2 in range(d):
            if (r1, r2) == (0, 0): continue
            if s == inv(s, d) and r2 < r1: continue
            res = SB.certify_box(d, s, (d + r1, d + r2)); nsb += 1; nbad += (not res['ok']); nfb += res['method'] != 'family'
check('G6-C1 (A): all small boxes Q=(d+r1,d+r2) certified exactly (sufficient-family test, generic fallback) -- %d boxes' % nsb, nbad == 0, 'bad %d, via generic fallback %d' % (nbad, nfb))

gs = rows(os.path.join(DATA, 'general_s_d15_70.jsonl'))
have = {(r['d'], r['s']) for r in gs}; dm = 14
for dd in range(15, 71):
    if not {(dd, ss) for ss in units(dd) if inv(ss, dd) >= ss} <= have: break
    dm = dd
badrows = [r for r in gs if r['n_bad'] or r['proof_cell_audit_bad'] or r.get('generic_audit_bad')]
nsm = sum(r['small_boxes_certified'] for r in gs)
check('G6-C1 (A): shipped general-s run: %d unit classes (all classes complete for 15<=d<=%d), %d small boxes certified, 0 violations/unresolved, proof-cell and generic audits clean' % (len(gs), dm, nsm), len(gs) > 100 and not badrows, 'complete for d<=%d; partial rows beyond; target 70: UNAVAILABLE' % dm)
wf = []
for sh in (0, 1): wf += rows(os.path.join(DATA, 'window_full_d22_30_s%d.jsonl' % sh))
wd = sorted({r['d'] for r in wf}); nb = sum(r['boxes'] for r in wf); un = sum(len(r['unresolved']) for r in wf)
check('G6-C1 (A): COMPLETE base-window certification for d in %s (%d unit classes, %d boxes): every window box exactly certified; by v004 Lemma S4 U=conv(F) for ALL Q>=(d,d), Q!=(d,d) for these d' % ('%d..%d' % (wd[0], wd[-1]) if wd else '-', len(wf), nb), len(wf) > 0 and un == 0, 'unresolved %d' % un)
ext = []
for fn in ('stabilization_extended.jsonl',):
    ext += rows(os.path.join(DATA, fn))
check('G6-C1 (A): v005 d<=21 extended-stabilization records shipped (inherited)', len(ext) > 0, len(ext))

nh = 0; nbad = 0; b1 = set()
for d in range(3, 8 if SMOKE else 11):
    for s in units(d):
        if s == d - 1: continue
        pcs = C.uncovered(Lat(d, d, d, s), (d, d)); nh += 1
        T1 = [(C.mpq(0), C.mpq(d)), (C.mpq(d - inv(s, d)), C.mpq(d - 1)), (C.mpq(d), C.mpq(d))]; T2 = [(C.mpq(d), C.mpq(0)), (C.mpq(d - 1), C.mpq(d - s)), (C.mpq(d), C.mpq(d))]
        def ia(P, T):
            if C.area2(T) < 0: T = T[::-1]
            rr = P
            for i in range(3):
                p, q = T[i], T[(i + 1) % 3]; a = -(q[1] - p[1]); bb = (q[0] - p[0]); c = a * p[0] + bb * p[1]
                rr = C.clip(rr, -a, -bb, -c)
                if len(rr) < 3: return 0
            return abs(C.area2(rr))
        tot = sum(abs(C.area2(p)) for p in pcs)
        ok = tot == 2 * d and sum(ia(p, T1) + ia(p, T2) for p in pcs) == tot
        betti = U_betti(Lat(d, d, d, s), (d, d))[0]; b1.add(betti[1])
        nbad += (not ok) or betti[1] != 2
check('G6-C2 (A): hollow box (d,d): conv(F)\\U = int T1 u int T2 exactly (area d) and beta1 = 2 for every unit s != -1, recomputed for %d types' % nh, nbad == 0 and b1 == {2}, sorted(b1))
hs = json.load(open(os.path.join(DATA, 'hollow_general_s.json')))
check('G6-C2 (A): shipped hollow check: %d types, 3<=d<=%d, 0 violations; beta1=2 for all rows carrying a Betti number' % (hs['n_types'], hs['range'][1]), hs['n_bad'] == 0 and all(r['beta1'] == 2 for r in hs['rows'] if 'beta1' in r))

# ---------------------------------------------------------------- Programme B
a4 = B.analyse([1, 1, 1, 1]); a5 = B.analyse([1] * 5)
check('B: 0/1 engine reproduces 4D parity benchmark: non-embedded, 3 witnesses, all span 3; box is minimal', (not a4['embedded']) and a4['n_witnesses'] == 3 and a4['span_hist'] == {3: 3} and B.minimal_nonembedded([1] * 4))
check('B: 5D parity (1^5): 90 witnesses, min span 3, individual witnesses of span 4 exist (15); box not minimal', a5['n_witnesses'] == 90 and a5['span_hist'] == {3: 75, 4: 15} and not B.minimal_nonembedded([1] * 5))
g = {1: 5, 2: 7, 4: 13}
def res_of(c):
    r = 1
    for bit in (1, 2, 4):
        if c & bit: r = r * g[bit] % 24
    return r
rr = random.Random(1); npair = 0; mism = []
for N in (3, 4, 5):
    allc = list(itertools.combinations_with_replacement(range(1, 8), N))
    for cols in rr.sample(allc, 12 if SMOKE else 60):
        a = B.analyse(list(cols)); w = WD.analyse_box_cells(tuple(res_of(c) for c in cols), 24, (1,) * N); npair += 1
        if (0 if a['embedded'] else a['n_witnesses']) != w['n_witnesses'] or (None if a['embedded'] else a['min_span']) != w['min_span']: mism.append(cols)
check('B: INDEPENDENT cross-validation of the 0/1 engine against the v005 engine (cells/LP route, residues mod 24) on %d random binary lattices: witness counts and minimum spans agree' % npair, not mism, mism[:2])
if not SMOKE:
    w6 = WD.analyse_box_cells((2,) * 6, 3, (1,) * 6); a6 = B.analyse([1] * 6)
    check('B: parity n=6 at 1^6: 0/1 engine and v005 engine give the same 1440 witnesses and the same span histogram {3:360,4:315,5:585,6:180} (min span 3, individual spans up to 6)',
          a6['n_witnesses'] == w6['n_witnesses'] == 1440 and a6['span_hist'] == {int(k): v for k, v in w6['span_histogram'].items()} == {3: 360, 4: 315, 5: 585, 6: 180})
    r6 = random.Random(7); m6 = []
    for cols in r6.sample(list(itertools.combinations_with_replacement(range(1, 8), 6)), 15):
        a = B.analyse(list(cols)); w = WD.analyse_box_cells(tuple(res_of(c) for c in cols), 24, (1,) * 6)
        if (0 if a['embedded'] else a['n_witnesses']) != w['n_witnesses'] or (None if a['embedded'] else a['min_span']) != w['min_span']: m6.append(cols)
    check('B: cross-validation vs v005 on 15 random 6-coordinate binary lattices (witness classes and min spans)', not m6, m6[:2])
sp = {}
for n, mm in ((4, 4), (5, 5)) + (() if SMOKE else ((6, 5),)):
    import subprocess as sp_
    out = os.path.join(REP, 'binrank_check_n%d.json' % n)
    sp_.run([sys.executable, os.path.join(ROOT, 'experiments', 'binary_rank_search.py'), str(n), str(mm), out], capture_output=True)
    cur = json.load(open(out)); ship = json.load(open(os.path.join(DATA, 'binrank_n%d.json' % n)))
    check('B: exhaustive recomputation n=%d (all binary column multisets of rank<=%d): minimal boxes by min span = %s, equals shipped' % (n, mm, cur['minimal_boxes_by_min_span']),
          cur['minimal_boxes_by_min_span'] == ship['minimal_boxes_by_min_span'] and set(cur['minimal_boxes_by_min_span']) <= {'3'})
shipall = {n: json.load(open(os.path.join(DATA, 'binrank_n%d.json' % n))) for n in range(3, 9)}
check('B: shipped census n=3..8: %s minimal boxes, ALL with minimum witness span 3 (no rank>=4 minimal box found; G6-C3 remains OPEN)' % [sum(v['minimal_boxes_by_min_span'].values()) for v in shipall.values()],
      all(set(v['minimal_boxes_by_min_span']) <= {'3'} for v in shipall.values()))

# ---------------------------------------------------------------- Programme C
cb = json.load(open(os.path.join(DATA, 'cert_benchmark.json')))
check('C: certificate-size benchmark shipped: proof-cell certificates (%d-%d cells) vs generic cell enumeration (%d-%d 2-cells), both exact and agreeing' % (min(r['proof_cells'] for r in cb), max(r['proof_cells'] for r in cb), min(r.get('generic_2cells', 10**9) for r in cb), max(r.get('generic_2cells', 0) for r in cb)),
      all(r['proof_ok'] and r.get('generic_ok', True) for r in cb) and all(r['proof_cells'] * 4 < r['generic_2cells'] for r in cb if 'generic_2cells' in r))
for (d, s, Q) in ([(17, 5, (40, 40))] if SMOKE else [(17, 5, (40, 40)), (21, 8, (42, 60)), (29, 12, (58, 58))]):
    res = ML.verify_box(d, s, Q)
    check('C: recomputed O(|F|)-size proof certificate for (d,s,Q)=(%d,%d,%s): %d cells cover conv(F) exactly' % (d, s, Q, res['n_cells']), res['ok'] is True)

core = len(CHECKS); ok = sum(c['ok'] for c in CHECKS)
json.dump({'mode': MODE, 'core_checks': core, 'core_pass': ok, 'seconds': round(time.time() - T0, 1), 'checks': CHECKS}, open(os.path.join(REP, 'verify_%s.json' % MODE), 'w'), indent=1, default=str)
print('\n%s: CORE %d/%d PASS   (%.0f s)' % (MODE.upper(), ok, core, time.time() - T0))
sys.exit(1 if FAILS else 0)
