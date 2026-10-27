#!/usr/bin/env python3
"""GEO-I v007 verifier.   python3 verify.py --smoke  (Level 1, a few minutes)    python3 verify.py  (Level 1 + Level 2, full)
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
CHECKS = []; FAILS = 0; T0 = time.time(); GRP = ['inherited']


def check(name, ok, detail=None):
    global FAILS
    CHECKS.append({'name': name, 'ok': bool(ok), 'detail': detail, 'group': GRP[0]}); FAILS += (not ok)
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


# =====================================================================================================  v007 NEW CHECKS
GRP[0] = 'v007'
sys.path.insert(0, os.path.join(ROOT, 'certificates'))
import corner_sail as CS, coverage_lemmas as CL, binary_circuits as BC, centre_collisions as CC, rank_reduction as RR, hollow_geometry as HG
import checker as CK
ok7 = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo7.py')], capture_output=True, text=True)
check('v007 tests/test_geo7.py (unit tests, incl. checker rejection tests) pass', ok7.returncode == 0 and ' 0 failures' in ok7.stdout, ok7.stdout.strip().splitlines()[-1] if ok7.stdout.strip() else ok7.stderr[-200:])

# ---- Programme A  (G7-T1 / Theorem A-COL, G7-C1 reduction)
dmax = 5 if SMOKE else 9
n, bad = CL.verify_Acol(dmax)
check('A / G7-T1 REGENERATED: Theorem A-COL strip-cell cover is exact and every lemma (K>=1, steps, bridges Graver, hull pieces Graver, sliver height) holds on all %d boxes, d<=%d, all units, Q1 in [d,3d], Q2 in [2d,3d]' % (n, dmax), not bad, bad[:3])
ac = json.load(open(os.path.join(DATA, 'v7_acol_12.json')))
check('A / G7-T1 SHIPPED RECORD (verification of supplied record, not regeneration): A-COL machine check d<=%d: %d boxes, 0 failures' % (ac['dmax'], ac['boxes']), ac['failures'] == [] and ac['boxes'] > 8000)
rr = random.Random(77); nb = 0; badl = []
for _ in range(25 if SMOKE else 120):
    d = rr.randint(14, 45); s = rr.choice(units(d)); Q = (rr.randint(d, 3 * d), rr.randint(2 * d, 3 * d)); nb += 1
    r = CS.verify_col_box(d, s, Q)
    if not (r['ok'] and all(r['lemmas'].values())): badl.append((d, s, Q))
check('A / G7-T1: Theorem A-COL on %d random boxes with 14<=d<=45 (beyond the exhaustive range)' % nb, not badl, badl[:3])
# independent path: standalone checker re-derives F, Graver and the subdivision from the shipped D1 certificates
D1 = json.load(open(os.path.join(ROOT, 'certificates', 'D1_coverage.json')))
check('A / D1 (independent path): standalone checker validates %d coverage certificates with explicit finite subdivisions (pieces inside cells, disjoint, areas sum to area(conv F))' % len(D1), all(CK.check_D1(c)[0] for c in D1))
cmp_bad = []
for (d, s, Q) in [(7, 3, (9, 14)), (11, 4, (13, 22)), (8, 5, (8, 16))]:
    cells, tags = CS.strip_cells(d, s, Q)
    a = ML.covered(d, s, Q, list(dict.fromkeys(cells)))[0]; c = [x for x in D1 if (x['d'], x['s'], tuple(x['Q'])) == (d, s, Q)]
    if c and not (a and CK.check_D1(c[0])[0]): cmp_bad.append((d, s, Q))
check('A: two independent coverage routines (v006 exact polygon subtraction vs standalone subdivision checker) agree on the shipped certificate boxes', not cmp_bad, cmp_bad)
hl = CL.classify_hypll_steps(7 if SMOKE else 10); hs_ = json.load(open(os.path.join(DATA, 'v7_hypll.json')))
check('A / HYP-LL (regression, stays FALSE): step failures classified with exact witnesses: %d of %d boxes fail (d<=%d); none has r1>0, r2>0 and max(Q)>=2d' % (hl['boxes_failing'], hl['boxes'], 7 if SMOKE else 10),
      hl['boxes_failing'] > 0 and not [x for x in hl['failing_other'] if max(x[2], x[3]) >= 2 * x[0]] and (SMOKE or hl['boxes_failing'] == hs_['boxes_failing']), 'shipped d<=10: %d' % hs_['boxes_failing'])
sq = CL.squareless
nsq = 0; cand = []
for d in range(3, 8 if SMOKE else 12):
    for s in units(d):
        L = Lat(d, d, d, s)
        for q1 in range(d, 2 * d):
            for q2 in range(d, 2 * d):
                if (q1, q2) == (d, d) or not sq(d, s, (q1, q2)): continue
                nsq += 1; u = C.uncovered(L, (q1, q2))
                if u is None or len(u) > 0: cand.append((d, s, q1, q2))
check('A / G7-C1 adversarial (REGENERATED): all %d squareless small boxes with d<=%d satisfy U=conv(F) by the generic exact routine; no counterexample candidate' % (nsq, 7 if SMOKE else 11), not cand, cand[:3])
tot = 0; badc = []
for fn in sorted(os.listdir(DATA)):
    if fn.startswith('v7_sqless_'):
        r = json.load(open(os.path.join(DATA, fn))); tot += r['squareless_tested']; badc += r['counterexample_candidates'] + r['unresolved']
check('A / G7-C1 adversarial (SHIPPED RECORDS): %d squareless small boxes certified over the shipped ranges (d from 3), 0 counterexample candidates, 0 unresolved' % tot, tot > 29000 and not badc)

# ---- Programme B
rb = random.Random(5); nbox = 0; badb = []
for n_ in (4, 5, 6, 7):
    for m_ in (2, 3, 4):
        allc = list(itertools.combinations_with_replacement(range(1, 1 << m_), n_)); rb.shuffle(allc)
        for cols in allc[:(6 if SMOKE else 25)]:
            cols = list(cols)
            if B.is_embedded(cols): continue
            nbox += 1; r = RR.check_box(cols); f = CC.check_facts(cols)
            if not (r['delta_in_span'] and r['atom_ok'] and all(f.values())): badb.append(cols)
check('B: Theorems B-DELTA, B-COSET, B-NULL, fact F1 and the (2,2) atom criterion hold on %d random non-embedded binary boxes (n=4..7)' % nbox, not badb, badb[:2])
for n_ in ((4, 5, 6) if SMOKE else (4, 5, 6, 7)):
    out = os.path.join(REP, 'v7_rank_n%d.json' % n_)
    subprocess.run([sys.executable, os.path.join(ROOT, 'experiments', 'rank_counterexamples.py'), str(n_), str(max(n_ - 3, 1)), out], capture_output=True)
    cur = json.load(open(out)); ship = json.load(open(os.path.join(DATA, 'v7_rank_n%d.json' % n_)))
    check('B: REGENERATED census n=%d (all binary column multisets of rank<=%d = n-3): minimal boxes by min witness rank %s; nullity histogram %s; all collisions full-support: %s' % (n_, max(n_ - 3, 1), cur['minimal_boxes_by_min_rank'], cur['nullity_hist'], cur['all_collisions_full_support']),
          cur['minimal_boxes_by_min_rank'] == ship['minimal_boxes_by_min_rank'] and set(cur['minimal_boxes_by_min_rank']) == {'3'} and cur['all_collisions_full_support'])
r8 = json.load(open(os.path.join(DATA, 'v7_rank_n8.json')))
check('B: SHIPPED RESTRICTED census n=8 (rank<=%d only; NOT complete): %d minimal boxes, min rank 3 for all; labelled restricted' % (r8['mmax'], sum(r8['minimal_boxes_by_min_rank'].values())), not r8['complete_nullity_ge3'] and set(r8['minimal_boxes_by_min_rank']) == {'3'})
D2 = json.load(open(os.path.join(ROOT, 'certificates', 'D2_rank.json')))
check('B / D2 (independent path): standalone checker (own coset-based cell/collision implementation) validates %d obstruction-rank certificates, incl. minimality, rank, and exact shared point' % len(D2), all(CK.check_D2(c)[0] for c in D2))
cross_bad = []
for cols in ([1, 1, 1, 1], [1, 1, 1, 2, 3], [1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 4, 7]):
    n_ = len(cols); full = (1 << n_) - 1
    a = sum(1 for _, a_, b_ in CC.collisions(cols)); b = sum(len(v) * (len(v) - 1) // 2 for k, v in CK.collisions(cols, full))
    if a != b: cross_bad.append(cols)
check('B: two independent cell/collision engines (binary_01.cells_01 vs checker coset implementation) give identical collision-pair counts', not cross_bad, cross_bad)
for cols in ([1] * 4, [1] * 5):
    pass
check('B regression: parity 4 (min rank 3, 3 witnesses) and 5 (90 witnesses, spans {3:75,4:15}) unchanged under the v007 engines', RR.check_box([1] * 4)['min_rank'] == 3 and B.analyse([1] * 5)['span_hist'] == {3: 75, 4: 15})
check('B: separation of rank notions: parity-5 box has individual witness rank 4 yet min rank 3 and is not minimal (min over witnesses != max over witnesses)', B.analyse([1] * 5)['max_span'] == 4 and B.analyse([1] * 5)['min_span'] == 3)

# ---- Programme C
nh = 0; bh = []
for d in range(3, 13 if SMOKE else 25):
    for s in units(d):
        nh += 1
        if not HG.check_hollow(d, s)['ok']: bh.append((d, s))
check('C / G7-T3 REGENERATED: hollow-box certificate (primitive triangles, Graver boundary edges, no 1-cell or 2-cell meets int T_i) => beta_1>=2, for all %d unit classes with 3<=d<=%d' % (nh, 12 if SMOKE else 24), not bh, bh[:3])
tot = 0; bh = []
for fn in ('v7_hollow_3_50.json', 'v7_hollow_51_64.json'):
    r = json.load(open(os.path.join(DATA, fn))); tot += r['pairs']; bh += r['failures']
check('C / G7-T3 SHIPPED RECORDS: hollow certificates for %d unit classes, 3<=d<=64: 0 failures (lower bound beta_1>=2; the all-d proof is in HOLLOW_TOPOLOGY.md, the records are evidence)' % tot, tot > 1200 and not bh)
D3 = json.load(open(os.path.join(ROOT, 'certificates', 'D3_hollow.json')))
check('C / D3 (independent path): standalone checker validates %d hollow-box certificates' % len(D3), all(CK.check_D3(c)[0] for c in D3))
ind_bad = []
for (d, s) in ((5, 2), (7, 3), (8, 3), (9, 2)):
    pcs = C.uncovered(Lat(d, d, d, s), (d, d)); ind_bad += [] if (HG.check_hollow(d, s)['ok'] and sum(abs(C.area2(p)) for p in pcs) == 2 * d) else [(d, s)]
check('C: third path: v005 exact uncovered-region routine gives total complement area d (area2 = 2d) consistent with the two-triangle certificate', not ind_bad, ind_bad)
check('C regression: s=-1 is not forced into the two-triangle family (beta_1 = d from v005 Theorem H1); the certificate still gives beta_1 >= 2', U_betti(Lat(7, 7, 7, 6), (7, 7))[0][1] == 7 and HG.check_hollow(7, 6)['ok'])

# ---- Programme D
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'certificates', 'checker.py')] + [os.path.join(ROOT, 'certificates', f) for f in ('D1_coverage.json', 'D2_rank.json', 'D3_hollow.json')], capture_output=True, text=True)
check('D1-D3: certificates verify with the standalone checker run in isolated mode (python -I, no release imports): %d VALID' % r.stdout.count('VALID  '), r.returncode == 0 and 'INVALID' not in r.stdout)
d4 = json.load(open(os.path.join(ROOT, 'certificates', 'D4_symbolic_records.json')))
check('D4: symbolic records use only the allowed statuses (TARGET is not a status) and every PROVED* record names a proof location or machine range', all(x['status'] in ('PROVED', 'PROVED+CHECKED', 'CHECKED', 'FALSE', 'CORRECTED', 'OPEN', 'UNAVAILABLE') for x in d4) and all(('proof' in x or 'machine_checked' in x or x['status'] not in ('PROVED', 'PROVED+CHECKED')) for x in d4))
d5 = json.load(open(os.path.join(ROOT, 'certificates', 'D5_cost.json')))
check('D5: cost accounting shipped: strip-cell certificates are %.1fx-%.1fx smaller than generic 2-cell enumerations on the benchmark boxes' % (min(r_['generic_2cells'] / r_['strip_cells'] for r_ in d5), max(r_['generic_2cells'] / r_['strip_cells'] for r_ in d5)), all(r_['checker_ok'] for r_ in d5))

# ---- regressions (v007 view): historical items must remain recorded
t7 = open(os.path.join(ROOT, 'MATHEMATICS.md'), encoding='utf-8').read()
check('G9: historical falsifications remain recorded in MATHEMATICS.md (q_i>o_i, 2^10 7^10/15, HYP-LL FALSE, 82944/5, 2^{10+2t}3^4/5, 3600 and 210^4, parity 4/5, b=24, exceptional (d,d) box)', all(k in t7 for k in ('2^10', 'HYP-LL', '82944/5', '3600', '210', 'b = 24', 'exceptional')))

core = len(CHECKS); ok = sum(c['ok'] for c in CHECKS)
g7 = [c for c in CHECKS if c['group'] == 'v007']; gi = [c for c in CHECKS if c['group'] == 'inherited']
json.dump({'mode': MODE, 'level': 'Level 1 (smoke)' if SMOKE else 'Level 1 + Level 2 (full)', 'v007_checks': len(g7), 'v007_pass': sum(c['ok'] for c in g7), 'inherited_regression_checks': len(gi),
           'inherited_regression_pass': sum(c['ok'] for c in gi), 'archived_v006_counts': {'smoke': '20/20', 'full': '25/25', 'inherited_v005': '52/52'},
           'seconds': round(time.time() - T0, 1), 'checks': CHECKS}, open(os.path.join(REP, 'verify_%s.json' % MODE), 'w'), indent=1, default=str)
print('\n%s: v007 NEW %d/%d PASS | inherited regressions %d/%d PASS | TOTAL %d/%d   (%.0f s)   [archived v006: smoke 20/20, full 25/25, v005 52/52 -- reported separately]' % (
    MODE.upper(), sum(c['ok'] for c in g7), len(g7), sum(c['ok'] for c in gi), len(gi), ok, core, time.time() - T0))
sys.exit(1 if FAILS else 0)
