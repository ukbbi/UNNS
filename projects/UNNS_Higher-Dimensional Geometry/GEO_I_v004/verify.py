#!/usr/bin/env python3
"""GEO-I v004 verifier.     python3 verify.py --smoke   (a few minutes)       python3 verify.py   (full)
CORE checks use only files inside this release (so the count is identical after a clean unzip).  OPTIONAL sibling-release integrity checks
(v001-v003 folders beside this one) are reported separately and never change the core count.  Exact integer/rational arithmetic throughout;
resource-limited items are reported UNAVAILABLE, never silently skipped."""
import os, sys, json, time, hashlib, subprocess, itertools, collections, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(ROOT, d))
ap = argparse.ArgumentParser(); ap.add_argument('--smoke', action='store_true'); ARGS = ap.parse_args(); SMOKE = ARGS.smoke; MODE = 'smoke' if SMOKE else 'full'
from fractions import Fraction as Fr
from math import gcd
from realization import fibre_complex, fibre_complex_data, cover_cells
from validation import audit, edge_level_audit, cell_level_audit
from subdivision import planar_subdivision, planar_cells_for_homology
from chain_complex import betti
from homology_compare import betti_abs, betti_nerve
from arith import order_mod, group_order, graver_complete
from lattice_model import Lat, U_betti, complex_data
from coverage import is_hull_covered
from stabilization import data_to_pure, predicted_beta1, realize
from obstruction_templates import Lattice, LatticeFromLat, obstruction_atlas, embedded_by_templates, templates, classify, min_boxes
from arithmetic_criteria import invariants
import benchmarks as B, validate_templates as VT, high_dimensional as HD, counterexample_search as CE, essential_dimension as ED, klein_four as K4
import stabilization_certificate as SC
from obstruction_atlas import validate

OUT = os.path.join(ROOT, 'output'); DATA = os.path.join(OUT, 'data')
REP = os.path.join(OUT, 'smoke' if SMOKE else 'reports'); os.makedirs(REP, exist_ok=True)
CHECKS = []; FAILS = 0; RES = {'mode': MODE}; T0 = time.time()


def check(name, ok, detail=None, optional=False):
    global FAILS
    try: json.dumps(detail, default=str)
    except TypeError: detail = str(detail)
    CHECKS.append({'name': name, 'ok': bool(ok), 'optional': optional, 'detail': detail}); FAILS += (not ok and not optional)
    try: dd = detail if isinstance(detail, str) else json.dumps(detail, default=str)
    except TypeError: dd = str(detail)
    d = '' if detail is None else '   [' + dd[:170] + ']'
    print(('PASS  ' if ok else ('WARN  ' if optional else 'FAIL  ')) + ('(optional) ' if optional else '') + name + d, flush=True)


def sha(path): return hashlib.sha256(open(path, 'rb').read()).hexdigest()
def load_jsonl(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
def pad(b, n=3): return tuple(b) + (0,) * (n - len(b))
def _clean(o):
    if isinstance(o, dict): return {(k if isinstance(k, (str, int, float, bool)) or k is None else str(k)): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)): return [_clean(v) for v in o]
    return o
def dump(name, obj):
    with open(os.path.join(REP, name), 'w') as f: json.dump(_clean(obj), f, indent=1, default=str)

# ================================================================================================== G7 preservation / G5 integrity (self-contained)
FROZEN = {'geo1lib.py': '0c94b3a73721c0c69823aee53f33710cad186280f3e8d8659bbb4188381c8831', 'geo2lib.py': 'a8c47c4ff0aebbcfb41372dcaba5006b12349add5c1103073583f50c093d852e'}
check('G7: frozen v001/v002 arithmetic libraries are byte-identical to the released ones (sha-256)', all(sha(os.path.join(ROOT, 'frozen', k)) == v for k, v in FROZEN.items()))
mf = os.path.join(ROOT, 'MANIFEST.sha256')
if os.path.exists(mf):
    bad = []
    for l in open(mf):
        h, p = l.strip().split(None, 1); p = p.lstrip('*')
        if not os.path.exists(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h: bad.append(p)
    check('G6: MANIFEST.sha256 verifies (every shipped source/data file unchanged)', not bad, bad[:3])
else:
    check('G6: MANIFEST.sha256 present', False, 'missing')
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo3.py')], capture_output=True, text=True)
check('tests/test_geo3.py (inherited exact-geometry tests, 24 checks) pass', r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo4.py')], capture_output=True, text=True)
check('tests/test_geo4.py (v004 theory tests, 72 checks) pass', r.returncode == 0 and '72 checks' in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

# ================================================================================================== nine mandatory benchmarks
e1 = B.e1()
check('BM-5  82944/5: F={(1,1),(2,2),(4,0),(5,1)}, edges (1,1)-(5,1) and (2,2)-(4,0) cross exactly at (3,1) (not in Lambda), NON-EMBEDDED; Betti K_abs (1,2,0) vs embedded image (1,0,0)',
      sorted(e1['F']) == [(1, 1), (2, 2), (4, 0), (5, 1)] and e1['crossing']['point'] == ['3', '1'] and not e1['crossing']['in_F'] and e1['audit']['status'] == 'non_embedded' and e1['betti_abs_Q'] == [1, 2, 0] and e1['betti_embedded_Q'] == [1, 0, 0])
e3 = B.e3()
check('BM-4  2304/5: two vertices, one primitive-move edge (3,-1), embedded', e3['F'] == [(1, 1), (4, 0)] and e3['edge'] == [((1, 1), ((3, -1),))] and e3['status'] == 'embedded')
e456 = B.e456()
x4, x5, x6 = e456['E4_3600'], e456['E5_44100'], e456['E6_210pow4']
check('BM-1  3600: cells 11/17/8/1, embedded, Betti (1,0,0,0)', x4['cells'] == [11, 17, 8, 1] and x4['status'] == 'embedded' and x4['betti_abs'] == [1, 0, 0, 0])
check('BM-3  44100: 15 points, cells 15/28/18/4 (no 4-cell), embedded', x5['cells'] == [15, 28, 18, 4] and x5['status'] == 'embedded')
check('BM-2  210^4: cells 80/212/210/92/15, embedded, every maximal-cell pair meets in a common face', x6['cells'] == [80, 212, 210, 92, 15] and x6['status'] == 'embedded' and x6['cell_pairs']['non_face'] == 0)
T = 8 if SMOKE else 16
e2 = B.e2(T)
check('BM-6  x_t = 2^(10+2t) 3^4/5, t=0..%d: non-embedded (witness crossing (3,1)), beta1(K_abs)=2, beta2(K_abs)=floor(t/4) unbounded, embedded image (1,0,0)' % T,
      all(r['status'] == 'non_embedded' and r['has_witness_crossing'] and pad(r['betti_abs'])[1] == 2 and pad(r['betti_abs'])[2] == r['t'] // 4 and r['betti_U'] == [1, 0, 0] for r in e2))
b7 = {}
for nm, x in (('27348890625/8', Fr(27348890625, 8)), ('5489031744/5', Fr(5489031744, 5))):
    fc = fibre_complex(x); a = audit(fc); b7[nm] = {'ps': fc['ps'], 'b': fc['b'], 'q': fc['q'], 'R': len(fc['F']), 'cells': [len(c) for c in fc['cells']], 'status': a['status'],
                                                   'edge': a['edge']['relations'], 'pairs': a['cell']['pairs']}
k4 = b7['27348890625/8']
latk = Lattice((3, 5, 7), 8); _, ak = obstruction_atlas(latk)
check('BM-7  27348890625/8 (b=8, primes 3,5,7, q=(3,3,2)): NO interior edge crossing yet NON-EMBEDDED; the template atlas predicts it ((3,2,1) <= q is a minimal obstruction box)',
      k4['status'] == 'non_embedded' and k4['edge'].get('interior_cross', 0) == 0 and k4['q'] == [3, 3, 2] and not embedded_by_templates(ak, tuple(k4['q'])) and (3, 2, 1) in [tuple(a) for a in ak])
k8 = b7['5489031744/5']; lat8 = Lattice((2, 3, 7 % 5), 5)
_, a8 = obstruction_atlas(lat8, maxdim=1)          # edge-level templates (O-E/parallel): the 30 interior crossings are edge-level obstructions
check('BM-8  5489031744/5 (b=5, primes 2,3,7, q=(3,3,3)): non-embedded with 30 interior edge crossings; edge-level templates (maxdim=1) already predict non-embedded',
      k8['status'] == 'non_embedded' and k8['edge'].get('interior_cross', 0) == 30 and not embedded_by_templates(a8, tuple(k8['q'])), {'minimal': sorted(a8)[:8]})
res5 = (2, 3); fcq = fibre_complex_data(res5, (4, 4), 5); aq = audit(fcq)
lat5 = Lattice(res5, 5)
o2 = [t for t in templates(lat5) if [tuple(g) for g in t['A']] == [(1, -3), (3, -1)] and [tuple(g) for g in t['B']] == [(2, -2)] and t['delta'] == (0, 0)]
o2_box = min_boxes(lat5, o2[0]['A'], o2[0]['B'], o2[0]['delta']) if o2 else None
fc34 = {q: cell_level_audit(fibre_complex_data(res5, q, 5)['cells'], lp_budget=100000, stop_at_first=True)['status'] for q in ((3, 4), (4, 3), (4, 4))}
check('BM-9  O2 (b=5, residues (2,3), q=(4,4)): no interior edge crossing, 4 non-face cell pairs; mechanism = Graver edge [0,(2,-2)] inside the 2-cell P(0;(1,-3),(3,-1)) (centre, O-T), realized exactly at box (4,4); (3,4),(4,3) embedded',
      aq['status'] == 'non_embedded' and aq['edge']['relations'].get('interior_cross', 0) == 0 and aq['cell']['pairs']['non_face'] == 4 and o2 and classify(lat5, o2[0]['A'], o2[0]['B'], o2[0]['delta']) == 'O-T'
      and o2_box == [(4, 4)] and fc34 == {(3, 4): 'embedded', (4, 3): 'embedded', (4, 4): 'non_embedded'}, {'o2_box': o2_box, 'status': fc34})
RES['benchmarks'] = {'e1': {k: v for k, v in e1.items() if k not in ('subdivision',)}, 'e3': e3, 'e456': e456, 'x_t': e2, 'klein_and_5489': b7}

# ================================================================================================== Programme A: planar stabilization (G1)
def v003_betti(res, b, q):
    fc = fibre_complex_data(res, q, b); cov = cover_cells(fc['cells']); allc = [c for d in fc['cells'] for c in d]
    sub = planar_subdivision(cov, fc['F'], refine=allc); cl, bd = planar_cells_for_homology(sub); return betti(cl, bd)[0], fc
rng_cases = []
import random
rnd = random.Random(4)
nS1 = 25 if SMOKE else 120; badS1 = []; nS1done = 0; seenS1 = set()
while nS1done < nS1:
    b = rnd.randint(5, 80); us = [r for r in range(2, b) if gcd(r, b) == 1]
    if len(us) < 2: continue
    r1, r2 = rnd.choice(us), rnd.choice(us); q = (rnd.randint(1, 9), rnd.randint(1, 9))
    if (b, r1, r2, q) in seenS1: continue
    seenS1.add((b, r1, r2, q))
    o1, o2 = order_mod(r1, b), order_mod(r2, b)
    D = {pow(r1, i, b) for i in range(o1)} & {pow(r2, j, b) for j in range(o2)}; d = len(D)
    # s is determined by the lattice: find s with (a,c*s...) membership
    a, c = o1 // d, o2 // d; s = None
    for ss in (range(1, d + 1) if d > 1 else [1]):
        if d > 1 and gcd(ss, d) != 1: continue
        if all(((x, y) in Lat(o1, o2, d, ss)) == (pow(r1, x, b) * pow(r2, y, b) % b == 1 % b) for x in range(0, o1 + 1) for y in range(0, o2 + 1)): s = ss; break
    if s is None: badS1.append(('no s', b, r1, r2)); nS1done += 1; continue
    fc = fibre_complex_data((r1, r2), q, b)
    if not fc['F']: continue
    nS1done += 1
    bU, _ = v003_betti((r1, r2), b, q); Lp, Qs = data_to_pure(o1, o2, d, s, q); bp, _ = U_betti(Lp, Qs)
    if bp is None or list(pad(bU, 3)) != list(pad(bp, 3)): badS1.append((b, r1, r2, q, bU, bp))
    epure = cell_level_audit(complex_data(Lp, Qs)['cells'], lp_budget=100000, stop_at_first=True)['status']
    eorig = cell_level_audit(fc['cells'], lp_budget=100000, stop_at_first=True)['status']
    if epure != eorig: badS1.append(('embedded-status', b, r1, r2, q, epure, eorig))
check('S1 scaling reduction: on %d random (b,p1,p2,q) the original lattice and the pure model L(d,s) at Q=(floor(q1/a),floor(q2/c)) have identical beta(U) and identical embedded status' % nS1, not badS1, badS1[:3])

ce = load_jsonl(os.path.join(DATA, 'counterexamples_g4c1.jsonl'))
ce_re = CE.run(models=((2, 2, 2), (3, 2, 2), (2, 2, 3)) if SMOKE else ((2, 2, 2), (3, 2, 2), (4, 2, 2), (2, 2, 3), (3, 2, 3), (2, 3, 3)))
check('G4-C1 REFUTATION of the v003 guess "q_i > o_i => beta1(U)=0": %d certified counterexamples (b=15, primes (2,7), q=(5,5), x = 2^10 7^10/15 is the simplest); three independent exact routes (v003 pipeline over Q, pure model, nerve over Q) agree and equal the predicted beta1' % len(ce_re),
      all(r.get('q_gt_o') and r['x_matches_fibre'] and r['betti_U_pipeline_v003'][1] == r['betti_U_pure_model'][1] == r['predicted_beta1'] >= 2 and r['betti_nerve_Q'][1] == r['predicted_beta1'] for r in ce_re) and len(ce_re) >= 4, [(r['b'], r['primes'], r['q'], r['betti_U_pipeline_v003']) for r in ce_re[:3]])
check('G4-C1 shipped counterexample table (%d rows) is internally consistent: every row has q_i > o_i and beta1 >= 2' % len(ce), len(ce) >= 13 and all(r['q_gt_o'] and r['betti_U_pipeline_v003'][1] >= 2 for r in ce))
x15 = Fr(2 ** 10 * 7 ** 10, 15); fc = fibre_complex(x15)
check('G4-C1 explicit example x = 2^10 7^10/15 = 289254654976/15 (b=15, primes 2,7, orders (4,4), box q=(5,5) > o): F has 4 points, K_abs embedded, beta(U) = beta(K_abs) = (1,2,0)', fc['b'] == 15 and list(fc['q']) == [5, 5] and len(fc['F']) == 4 and audit(fc)['status'] == 'embedded' and pad(betti_abs(fc['cells'])[0]) == (1, 2, 0) and v003_betti((2, 7), 15, (5, 5))[0] == [1, 2, 0], (fc['b'], fc['q'], len(fc['F'])))

scan = load_jsonl(os.path.join(DATA, 'planar_scan_general_lattices.jsonl'))
mm = []; nin = 0; nviol = 0; nhol = 0
for r in scan:
    (o1, o2), d, s_, q = r['o'], r['d'], r['s'], r['q']; a_, c_ = o1 // d, o2 // d; Qs = (q[0] // a_, q[1] // c_); p_ = predicted_beta1(d, s_, Qs)
    if p_ is None: continue
    nin += 1; nhol += (Qs == (d, d)); nviol += (q[0] > o1 and q[1] > o2 and r['betti_U'][1] != 0)
    if r['betti_U'][1] != p_: mm.append((o1, o2, d, s_, q, r['betti_U'], p_))
rs = random.Random(9); samp = rs.sample(scan, 12 if SMOKE else 60); rc = []
for r in samp:
    (o1, o2), d, s_, q = r['o'], r['d'], r['s'], r['q']
    bb, _ = U_betti(Lat(o1, o2, d, s_), tuple(q))
    if list(pad(bb, 3)) != list(pad(r['betti_U'], 3)): rc.append((o1, o2, d, s_, q))
check('G4-C1 general-lattice scan (shipped, exact): %d boxes over all lattices with orders <= 10; in the scope Q>=(d,d) (%d boxes, %d of them at the hollow box) beta1(U) equals the corrected statement in EVERY box; %d boxes have q_i > o_i yet beta1 != 0 (refuting the v003 guess); %d recomputed boxes agree' % (len(scan), nin, nhol, nviol, len(samp)),
      not mm and not rc and nviol > 0 and len(scan) > 3000, (mm[:2], rc[:2]))
DS = 7 if SMOKE else 10
SCrows = []
for d in range(2, DS + 1):
    for s in range(1, d):
        if gcd(s, d) != 1: continue
        if SC.inv(s, d) < s: continue
        SCrows.append(SC.certify(d, s))
stored = load_jsonl(os.path.join(DATA, 'stabilization_certificates.jsonl'))
check('G4-C1 STABILIZATION (corrected): for every (d,s), 2<=d<=%d, every box Q in [d,3d-1]^2 other than (d,d) has U = conv(F) (exact polygon subtraction), and (d,d) is hollow: %d lattices recomputed' % (DS, len(SCrows)),
      all(not r['violations'] and r['hollow_at_dd'] for r in SCrows), [r['d'] for r in SCrows if r['violations']])
need = {(d, s) for d in range(2, 14) for s in range(1, d) if gcd(s, d) == 1 and SC.inv(s, d) >= s}
have = {(r['d'], r['s']) for r in stored if not r['violations'] and r['hollow_at_dd'] and r['d'] > 1}
check('G4-C1 shipped base-window certificates: complete for ALL (d,s) with 2<=d<=13 (%d lattice classes, %d boxes), zero violations; by Lemma S4 this proves U=conv(F) for ALL boxes Q>=(d,d), Q!=(d,d), for these d' % (len(need), sum(r['boxes'] for r in stored if r['d'] > 1)),
      need <= have, sorted(need - have)[:5])
DB = 8 if SMOKE else 12
tab = {}
for d in range(2, DB + 1):
    for s in range(1, d):
        if gcd(s, d) == 1: tab[(d, s)] = U_betti(Lat(d, d, d, s), (d, d))[0][1]
check('G4-C1 hollow value B(d,s) = beta1(U at Q=(d,d)) = d for s = -1 and = 2 otherwise, for all d in [2,%d] incl. composite d (%d pairs)' % (DB, len(tab)),
      all(v == (d if (s + 1) % d == 0 else 2) for (d, s), v in tab.items()), {k: v for k, v in tab.items() if v != (k[0] if (k[1] + 1) % k[0] == 0 else 2)})
RES['stabilization'] = {'B_table': {'%d,%d' % k: v for k, v in tab.items()}, 'certified_d_max_shipped': 13}
# Lemma S4 horizontal chord property, checked numerically
bad = []
for d in (2, 3, 4, 5, 6):
    for s in range(1, d):
        if gcd(s, d) != 1: continue
        for Q1 in range(2 * d, 2 * d + 3):
            L = Lat(d, d, d, s)
            for j in range(0, d + 3):
                row = [i for i in range(0, Q1 + 1) if (i, j) in L and (i or j)]
                if len(row) < 2: bad.append((d, s, Q1, j))
check('Lemma S4 (translation): every lattice row of the box [0,Q1], Q1>=2d, contains >= 2 fibre points (so horizontal chords of conv(F) have length >= d)', not bad, bad[:3])
cov_bad = []; ncov = 0
for d, s in ((3, 1), (3, 2), (4, 1), (4, 3), (5, 2)):
    for q1 in range(1, d + 3):
        for q2 in range(1, d + 3):
            if q1 < d or q2 < d or (q1, q2) == (d, d): continue
            ncov += 1
            if not is_hull_covered(Lat(d, d, d, s), (q1, q2)) or U_betti(Lat(d, d, d, s), (q1, q2))[0][1] != 0: cov_bad.append((d, s, q1, q2))
check('E1 independent route: the fast polygon-subtraction test and the full arrangement homology agree on %d boxes (U = conv(F), beta1 = 0)' % ncov, not cov_bad, cov_bad[:3])

# ================================================================================================== Programme B (G2, G3, G4)
VB, VM = (7, 5) if SMOKE else (10, 7)
tot = bad = nn = 0; badboxes = []
for b, res in VT.residue_classes(2, range(2, VB + 1)):
    lat = Lattice(res, b); boxes = list(itertools.product(range(1, min(2 * lat.o[0] + 2, VM) + 1), range(1, min(2 * lat.o[1] + 2, VM) + 1)))
    n, bd, ne, _, mm = validate(res, b, boxes); tot += n; bad += bd; nn += ne; badboxes += [(b, res, m) for m in mm]
check('T-FIN (G4-T3) validation, k=2: finite-template prediction equals the exhaustive polyhedral audit on %d (residues,box) cases (%d non-embedded), 0 disagreements; the two code paths share no code' % (tot, nn), bad == 0 and tot > 100, badboxes[:3])
t3 = 0; bad3 = 0; nn3 = 0
for b, res in VT.residue_classes(3, range(2, 5)):
    lat = Lattice(res, b); boxes = list(itertools.product(*[range(1, min(2 * o + 2, 4) + 1) for o in lat.o]))
    n, bd, ne, _, mm = validate(res, b, boxes); t3 += n; bad3 += bd; nn3 += ne
check('T-FIN (G4-T3) validation, k=3: template prediction equals the audit on %d (residues,box) cases (%d non-embedded), 0 disagreements' % (t3, nn3), bad3 == 0 and t3 > 100)
for fn, k, want in (('validation_k2_templates.jsonl', 2, 5000), ('validation_k3_templates.jsonl', 3, 1000)):
    rows = load_jsonl(os.path.join(DATA, fn))
    check('T-FIN shipped large validation run (k=%d): %d residue classes, %d boxes, 0 mismatches' % (k, len(rows), sum(r['boxes'] for r in rows)), rows and sum(r['mismatches'] for r in rows) == 0 and sum(r['boxes'] for r in rows) >= want)
kf = K4.run(bs=(8,)) if SMOKE else K4.run(bs=(8, 15))
abc = [tuple(map(tuple, r['minimal_boxes'])) for r in kf['abc']]; aab = [tuple(map(tuple, r['minimal_boxes'])) for r in kf['aab']]
ABC = ((1, 1, 4), (1, 2, 3), (1, 3, 2), (1, 4, 1), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1), (4, 1, 1))
check('G4-T4 Klein-four classification (Z^3 -> Z2^2, residues a,b,ab pairwise distinct): the atlas is the same antichain of 9 minimal boxes (all permutations of (1,1,4),(1,2,3)) for every modulus/residue triple tested (%d triples); (2,2,2) is NOT an obstruction' % len(abc),
      all(a == ABC for a in abc) and ABC and len(set(abc)) == 1)
check('G4-T4 type (a,a,b): minimal boxes {(1,3,2),(3,1,2),(2,2,2) + 2D boxes (1,4,0),(2,3,0),(3,2,0),(4,1,0)} for repeated-residue positions 1,2; other positions are coordinate permutations (%d triples)' % len(aab),
      all(set(a) in ({(1, 3, 2), (3, 1, 2), (2, 2, 2), (1, 4, 0), (2, 3, 0), (3, 2, 0), (4, 1, 0)}, {(0, 1, 4), (0, 2, 3), (0, 3, 2), (0, 4, 1), (2, 1, 3), (2, 2, 2), (2, 3, 1)}) for a in aab))
audit_ok = True; det = []
for m in ABC:
    st = cell_level_audit(fibre_complex_data((3, 5, 7), m, 8)['cells'], lp_budget=200000, stop_at_first=True)['status']
    below = [tuple(m[j] - (j == i) for j in range(3)) for i in range(3) if m[i] > 0]
    sb = []
    for q in below:
        if not any(q): continue
        fc_ = fibre_complex_data((3, 5, 7), q, 8)
        sb.append('empty' if not fc_['F'] else cell_level_audit(fc_['cells'], lp_budget=200000, stop_at_first=True)['status'])
    ok_ = st == 'non_embedded' and all(s in ('embedded', 'empty') or any(all(x[j] <= q[j] for j in range(3)) for x in ABC if x != m) for s, q in zip(sb, below))
    audit_ok &= ok_; det.append((m, st, sb))
check('G4-T4 two-direction check by exhaustive audit: each of the 9 minimal boxes is non-embedded and every box one unit lower is embedded (b=8, residues (3,5,7))', audit_ok, det[:3])
check('G4-T4 erratum to v003 (recorded, v003 untouched): v003 stated non-embedded "from q>=(3,3,2)"; that is true but not sharp - the sharp threshold is the 9-box antichain above (e.g. (3,2,1) and (4,1,1) already fail)',
      embedded_by_templates(ak, (3, 3, 2)) is False and embedded_by_templates(ak, (2, 2, 2)) is True and embedded_by_templates(ak, (3, 2, 1)) is False)
# essential dimensionality
ess = [ED.compare(res, b) for b, res in VT.residue_classes(2, range(2, 6 if SMOKE else 7))]
check('G4-T6 essential dimensionality (k=2 -> 3, %d classes): adjoining a residue-1 prime NEVER changes whether the complex is embedded for all boxes, every base obstruction persists, but it LOWERS the obstruction threshold in %d classes, always at height q_3 = 1 (so it is not essential for classification, but not inert for thresholds)' % (len(ess), sum(r['lowered_threshold'] for r in ess)),
      all(r['class_same'] and r['persist'] and r['max_new_height'] <= 1 for r in ess) and any(r['lowered_threshold'] for r in ess))
es_s = load_jsonl(os.path.join(DATA, 'essential_dimension_k2.jsonl'))
check('G4-T6 shipped run: %d classes (b<=12): classification unchanged in all, persistence in all, thresholds lowered in %d (exactly the non-direct classes), max new height %d' % (len(es_s), sum(r['lowered_threshold'] for r in es_s), max([r['max_new_height'] for r in es_s] or [0])),
      es_s and all(r['class_same'] and r['persist'] and r['max_new_height'] <= 1 for r in es_s) and len(es_s) >= 100 and all(r['lowered_threshold'] == (not r['direct0']) for r in es_s))
# 3D / 4D genuine obstructions
par = {q: HD.audit_box((2, 2, 2), 3, q)['status'] for q in ((1, 1, 1), (2, 1, 1), (2, 2, 1))}
_, apar = obstruction_atlas(Lattice((2, 2, 2), 3)) if not SMOKE else (None, [(1, 1, 2)])
p4 = {q: HD.audit_box((2, 2, 2, 2), 3, q)['status'] for q in ((1, 1, 1, 0), (1, 1, 1, 1), (2, 1, 1, 0))}
check('G3 parity lattices Lambda_n={sum even} (b=3): n=3 first obstruction at (2,1,1) (full support, plane (1,1,0)/(1,0,1)), n=4 has a NEW pure-4D obstruction at (1,1,1,1) that no 3D box (2,1,1,0) accounts for',
      par == {(1, 1, 1): 'embedded', (2, 1, 1): 'non_embedded', (2, 2, 1): 'non_embedded'} and p4[(1, 1, 1, 0)] == 'embedded' and p4[(1, 1, 1, 1)] == 'non_embedded' and p4[(2, 1, 1, 0)] == 'non_embedded')
fd = HD.four_d(3 if SMOKE else 4)
check('G3 4D example b=24, residues (5,7,13,23) (all coordinates same parity; H=Z2^3, |H|=8 < 16): every box <= (2,2,2,2) is embedded; first obstructions (sorted) at (3,2,1,1) and (4,1,1,1); edges never cross there',
      all(r['status'] in ('embedded', 'empty_fibre') for r in fd['boxes'] if max(r['q']) <= 2) and ([3, 2, 1, 1] in fd['minimal_nonembedded_sorted'] or SMOKE) and all((r.get('edge_interior_crossings') or 0) == 0 for r in fd['boxes']), fd['minimal_nonembedded_sorted'])
RES['higher_dimensional'] = {'parity3': par, 'parity4': p4, 'four_d_minimal_sorted': fd['minimal_nonembedded_sorted'], 'klein': kf}
atl = load_jsonl(os.path.join(DATA, 'k2_atlas_pure.jsonl'))
sm1 = [r for r in atl if r['d'] >= 4 and r['s'] == 1]; sm_1 = [r for r in atl if r['d'] >= 3 and r['s'] == r['d'] - 1]
check('E3 k=2 atlas (pure lattices d<=7): s=1 -> minimal boxes {(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}; s=-1 -> the antidiagonal {Q1+Q2=2d+1}  (observed, d<=7; stated as a conjecture, NOT proved)',
      all(sorted(map(tuple, r['minimal_boxes'])) == sorted([(1, 2 * r['d']), (2, r['d'] + 1), (r['d'], r['d']), (r['d'] + 1, 2), (2 * r['d'], 1)]) for r in sm1) and
      all(sorted(map(tuple, r['minimal_boxes'])) == sorted((i, 2 * r['d'] + 1 - i) for i in range(1, 2 * r['d'] + 1)) for r in sm_1) and len(sm1) >= 3)
check('G4-C1/G4-T5 coupling: for L(d,1) the O2 box (d,d) is the hollow box of the stabilization theorem (both are minimal exceptional boxes), e.g. b=5 (2,3) at q=(4,4)',
      [tuple(r['minimal_boxes'][2]) for r in atl if r['d'] == 4 and r['s'] == 1] == [(4, 4)] and tab.get((4, 1)) == 2)

# ================================================================================================== sibling releases (OPTIONAL; do not change the core count)
for name in ('GEO_I_v001', 'GEO_I_v002', 'GEO_I_v003'):
    d = os.path.join(ROOT, '..', name); mfp = os.path.join(d, 'MANIFEST.sha256')
    if os.path.exists(mfp):
        r = subprocess.run(['sha256sum', '-c', 'MANIFEST.sha256'], cwd=d, capture_output=True, text=True)
        badl = [l for l in r.stdout.splitlines() if not l.endswith(': OK')]
        check('sibling release %s verifies against its own manifest (unchanged, read-only)' % name, not badl, badl[:2], optional=True)
    else: print('NOTE  sibling %s not present beside this release (optional check not run; core count unaffected)' % name)

core = [c for c in CHECKS if not c['optional']]
RES.update({'core_checks': len(core), 'core_pass': sum(c['ok'] for c in core), 'optional_checks': len(CHECKS) - len(core), 'seconds': round(time.time() - T0, 1), 'checks': CHECKS})
dump('verify_%s.json' % MODE, RES)
print('\n%s: CORE %d/%d PASS%s   (%.0f s)' % (MODE.upper(), RES['core_pass'], RES['core_checks'], ('   optional sibling checks: %d' % RES['optional_checks']) if RES['optional_checks'] else '', RES['seconds']))
sys.exit(1 if FAILS else 0)
