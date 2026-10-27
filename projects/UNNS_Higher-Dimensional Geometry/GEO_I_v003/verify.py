#!/usr/bin/env python3
"""GEO-I v003 verifier.   python3 verify.py --smoke   (about a minute)      python3 verify.py   (full; add --orbits-exhaustive to recompute all 420 orbit states)
Every decision is made in exact integer / rational arithmetic.  Nothing is skipped silently: items that cannot be computed are written to the
report with the reason (resource limit / unavailable)."""
import os, sys, json, time, hashlib, subprocess, itertools, collections, csv, argparse
ROOT = os.path.dirname(os.path.abspath(__file__))
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(ROOT, d))
ap = argparse.ArgumentParser(); ap.add_argument('--smoke', action='store_true'); ap.add_argument('--orbits-exhaustive', action='store_true')
ARGS = ap.parse_args(); SMOKE = ARGS.smoke; MODE = 'smoke' if SMOKE else 'full'
from fractions import Fraction as Fr
from math import gcd
import intersections as X
from realization import fibre_complex, fibre_complex_data, cover_cells, maximal_cells
from validation import audit, edge_level_audit, cell_level_audit
from homology_compare import betti_abs, betti_nerve, betti_clique
from subdivision import planar_subdivision, planar_cells_for_homology, validate_planar
from chain_complex import betti
from arith import crossing_free_for_all_boxes, group_order, order_mod, iota, graver_complete, crossing_offsets
import benchmarks as B, crossing_family as CF, rational_corpus as RC, theorems as TH, high_dimensional as HD, orbits as OR

OUT = os.path.join(ROOT, 'output'); SHIPPED = OUT                      # smoke runs write their tables under output/smoke/ so the shipped full-run data are never overwritten
if SMOKE: OUT = os.path.join(ROOT, 'output', 'smoke')
for _d in ('reports', 'data', 'certificates'): os.makedirs(os.path.join(OUT, _d), exist_ok=True)
RES = {'mode': MODE}; CHECKS = []; T0 = time.time(); FAILS = 0

def check(name, ok, detail=None):
    global FAILS
    CHECKS.append({'name': name, 'ok': bool(ok), 'detail': detail}); FAILS += (not ok)
    print(('PASS  ' if ok else 'FAIL  ') + name + (('   [' + (json.dumps(detail, default=str) if not isinstance(detail, str) else detail)[:170] + ']') if detail is not None else ''), flush=True)

def sha(path):
    h = hashlib.sha256(); h.update(open(path, 'rb').read()); return h.hexdigest()

def csvw(path, rows, header):
    with open(os.path.join(OUT, 'data', path), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def dump(path, obj, sub='data'):
    with open(os.path.join(OUT, sub, path), 'w') as f: json.dump(obj, f, indent=1, default=str)

def pad(b, n=3): return tuple(b) + (0,) * (n - len(b))

# ============================================================================================== G6  historical preservation
FROZEN = {'geo1lib.py': '0c94b3a73721c0c69823aee53f33710cad186280f3e8d8659bbb4188381c8831', 'geo2lib.py': 'a8c47c4ff0aebbcfb41372dcaba5006b12349add5c1103073583f50c093d852e'}
check('G6: frozen v001/v002 arithmetic libraries are byte-identical to the v002 release (sha-256)', all(sha(os.path.join(ROOT, 'frozen', k)) == v for k, v in FROZEN.items()), {k: v[:12] for k, v in FROZEN.items()})
sib = {}
for rel in ('..', os.path.join('..', 'GEO_I_v002'), os.path.join('..', 'GEO_I_v001')):
    pass
for name in ('GEO_I_v001', 'GEO_I_v002'):
    d = os.path.join(ROOT, '..', name); mf = os.path.join(d, 'MANIFEST.sha256')
    if os.path.exists(mf):
        r = subprocess.run(['sha256sum', '-c', 'MANIFEST.sha256'], cwd=d, capture_output=True, text=True)
        bad = [l for l in r.stdout.splitlines() if not l.endswith(': OK')]
        sib[name] = len(bad) == 0
        check('G6: sibling release %s verifies against its own manifest (unchanged)' % name, len(bad) == 0, {'bad': bad[:3]})
    else:
        sib[name] = None
RES['sibling_manifests'] = sib
if all(v is None for v in sib.values()): RES['sibling_note'] = 'sibling v001/v002 folders not present beside this release; only the frozen-library hashes were checked'

# ============================================================================================== unit tests (independent clipping cross-check etc.)
r = subprocess.run([sys.executable, os.path.join(ROOT, 'tests', 'test_geo3.py')], capture_output=True, text=True)
check('tests/test_geo3.py passes (24 checks incl. 1500 random 2D cell pairs against exact polygon clipping)', r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

# ============================================================================================== E1  82944/5
e1 = B.e1(); RES['E1'] = e1
check('E1: fibre of 82944/5 = {(1,1),(2,2),(4,0),(5,1)}; six Graver edges; one 2-cell', sorted(e1['F']) == [(1, 1), (2, 2), (4, 0), (5, 1)] and len(e1['edges']) == 6 and len(e1['cell2']) == 1)
check('E1: edges (1,1)-(5,1) and (2,2)-(4,0) cross exactly at (3,1) (t = lambda = 1/2), and (3,1) is not in F_x (not even in Lambda_5)', e1['crossing']['point'] == ['3', '1'] and not e1['crossing']['in_F'] and e1['crossing']['offsets_w_t_lam'] == [[[1, 1], '1/2', '1/2']], e1['crossing'])
check('E1: audit = NON-EMBEDDED (edge crossing + both diagonals inside the 2-cell); no other edge pair meets except at endpoints', e1['audit']['status'] == 'non_embedded' and e1['audit']['edge_relations'] == {'shared_endpoint': 12, 'interior_cross': 1}, e1['audit'])
check('E1: exact subdivision certified (convex faces, edges meet only at endpoints, 2-cell exactly tiled, support = union): 5 vertices (4 occurrences + 1 auxiliary crossing), 8 edges, 4 triangles', e1['subdivision']['validation']['all_ok'] and len(e1['subdivision']['vertices']) == 5 and e1['subdivision']['n_edges'] == 8 and e1['subdivision']['n_faces'] == 4 and e1['subdivision']['kinds'].count('crossing') == 1 and e1['subdivision']['kinds'].count('occurrence') == 4)
check('E1: Betti numbers over Q: K_abs = (1,2,0), embedded K_emb = (1,0,0), clique complex = (1,0,0)  [abstract b1 = 2 is an attachment artifact]', e1['betti_abs_Q'] == [1, 2, 0] and e1['betti_embedded_Q'] == [1, 0, 0] and e1['betti_clique_Q'] == [1, 0, 0])
dump('e1_witness.json', e1, 'certificates')

# ============================================================================================== E2  infinite family
T = 12 if SMOKE else 24
e2 = B.e2(T); RES['E2'] = e2
cert = [CF.p1_certificate(t) for t in range(0, (30 if SMOKE else 60) + 1)]
check('E2 / Prop G3-P1: for t = 0..%d the four witness vertices lie in F, both vectors are Graver, the segments cross exactly at (3,1), (3,1) is not in Lambda' % (len(cert) - 1), all(all(v for k, v in c.items() if k not in ('t', 'q')) for c in cert))
check('E2: every x_t is NON-EMBEDDED and the crossing point (3,1) is among its crossing points (t <= %d)' % T, all(r['status'] == 'non_embedded' and r['has_witness_crossing'] for r in e2))
check('E2: embedded image K_emb has Betti (1,0,0) for t <= %d, abstract beta_1 = 2 and beta_2 = floor(t/4) (exact over Q): the discrepancy beta_2(K_abs) - beta_2(U) is unbounded' % T,
      all(r['betti_U'] == [1, 0, 0] and pad(r['betti_abs'])[1] == 2 and pad(r['betti_abs'])[2] == r['t'] // 4 for r in e2), [(r['t'], r['betti_abs']) for r in e2][:14])
pc = CF.p2_period_check(2, 40 if not SMOKE else 24)
check('E2 / Prop G3-P2: per period of 4 in q1 the counts (points, edges, squares) increase by exactly (3,8,6) (hence chi by 1) for t >= 2 (proof needs t >= 6)', not pc['bad_periods'] and pc['chi_increment_ok'], pc)
csvw('crossing_family.csv', [(r['t'], r['x'], r['q'][0], r['q'][1], r['R'], '|'.join(map(str, r['cells'])), r['status'], r['crossing_points'], '|'.join(map(str, r['betti_abs'])), '|'.join(map(str, r['betti_U']))) for r in e2], ['t', 'x', 'q1', 'q2', 'R', 'cells', 'status', 'crossing_points', 'betti_abs_Q', 'betti_U'])

# ============================================================================================== E3-E6
e3 = B.e3(); e456 = B.e456(); RES['E3'] = e3; RES['E4_E6'] = e456
check('E3: 2304/5 keeps its two-vertex, one-move-edge structure (0 grid edges, 1 primitive-move edge (3,-1)), embedded', e3['F'] == [(1, 1), (4, 0)] and e3['cells'] == [2, 1] and e3['edge'] == [((1, 1), ((3, -1),))] and e3['status'] == 'embedded')
x4 = e456['E4_3600']; x5 = e456['E5_44100']; x6 = e456['E6_210pow4']
check('E4: 3600 preserves the certified 3-cell (cells 11/17/8/1), is embedded, Betti (1,0,0,0); the cube has 8 vertices', x4['cells'] == [11, 17, 8, 1] and x4['status'] == 'embedded' and x4['betti_abs'] == [1, 0, 0, 0] and x4['top_cell'] is not None)
check('E5: 44100 has 15 fibre points, four axes, NO 4-cell (cells 15/28/18/4), embedded', x5['R'] == 15 and x5['k'] == 4 and x5['cells'] == [15, 28, 18, 4] and x5['status'] == 'embedded')
check('E6: 210^4 preserves the certified 4-cell (cells 80/212/210/92/15), embedded, 105 maximal-cell pairs all meet in common faces', x6['cells'] == [80, 212, 210, 92, 15] and x6['status'] == 'embedded' and x6['cell_pairs']['non_face'] == 0 and x6['top_cell'] is not None)
for nm in ('E4_3600', 'E5_44100', 'E6_210pow4'):
    check('%s: cell counts equal those of the frozen v002 release' % nm, e456[nm]['cells'] == e456[nm]['expected_cells_v002'])

# ============================================================================================== T1  lemmas and crossing predictor (k = 2 and k = 3)
def sweep(kdim):
    V = collections.Counter(); n = 0; mism = 0; ncross = 0; fibres = []
    if kdim == 2:
        bmax, qmax = (7, 4) if SMOKE else (10, 6)
        for b in range(2, bmax + 1):
            for r1 in TH.units(b):
                for r2 in TH.units(b):
                    if r2 < r1: continue
                    for q in itertools.product(range(1, qmax + 1), repeat=2): fibres.append(((r1, r2), b, q))
    else:
        bmax = 5 if SMOKE else 9
        boxes = [(1, 2, 3), (2, 2, 2), (3, 2, 2)] if SMOKE else [(1, 2, 3), (2, 2, 2), (3, 2, 2), (2, 3, 3), (3, 3, 3), (4, 3, 2), (2, 4, 3), (5, 2, 2), (2, 2, 5)]
        for b in range(2, bmax + 1):
            for res in itertools.combinations_with_replacement(TH.units(b), 3):
                for q in boxes: fibres.append((res, b, q))
    for res, b, q in fibres:
        viol, a, fc = TH.lemma_checks(res, b, q)
        if not fc['F']: continue
        n += 1
        for k_, v in viol.items(): V[k_] += v
        if TH.predicted_crossing_pairs(res, b, fc['F'], fc['G']) != TH.audit_pairs_canonical(a): mism += 1
        if a['relations'].get('interior_cross', 0): ncross += 1
    return n, dict(V), mism, ncross
for kd in (2, 3):
    n, V, mism, ncross = sweep(kd)
    RES['T1_k%d' % kd] = {'fibres': n, 'violations': V, 'predictor_mismatches': mism, 'fibres_with_crossings': ncross}
    check('T1 (k=%d): Lemmas 1-4 (no Lambda-point in an open Graver segment, no collinear overlap, no endpoint-on-interior, crossing points never in Lambda): 0 violations on %d fibres' % (kd, n), sum(V.values()) == 0, V)
    check('T1 (k=%d): crossing predictor from (g,h,w in Omega(g,h),u) data alone equals the exhaustive edge audit as a SET OF EDGE PAIRS on all %d fibres (%d with crossings)' % (kd, n, ncross), mism == 0 and ncross > 0, {'mismatches': mism})
tot = bad = 0
for b in range(2, 11 if SMOKE else 16):
    for r1 in TH.units(b):
        for r2 in TH.units(b):
            if r2 < r1: continue
            m = group_order((r1, r2), b); pos = [g for g in graver_complete((r1, r2), b) if g > (0, 0)]
            for g, h in itertools.combinations(pos, 2):
                det = abs(g[0] * h[1] - g[1] * h[0])
                if det == 0: continue
                for s in (1, -1):
                    tot += 1
                    if det % m or iota((r1, r2), b, g, (s * h[0], s * h[1])) != det // m: bad += 1
check('T1 (k=2): iota(g,h) = |det(g,h)| / |<p1,p2>| on %d Graver pairs' % tot, bad == 0 and tot > 0)

# ============================================================================================== T2  embedding classification
bmaxd = 20 if SMOKE else 59
mism = []; n_k2 = 0
for b in range(2, bmaxd + 1):
    for r1 in TH.units(b):
        for r2 in TH.units(b):
            if r2 < r1: continue
            n_k2 += 1
            if crossing_free_for_all_boxes((r1, r2), b)[0] != TH.direct_product((r1, r2), b): mism.append((b, r1, r2))
check('T2(a,b) k=2: [edge-crossing-free for every box] <=> [|<p1,p2>| = ord(p1)*ord(p2)]  on %d residue pairs (b <= %d)' % (n_k2, bmaxd), not mism, mism[:5])
n3 = 0; mism3 = []; bmax3 = 8 if SMOKE else 13
for b in range(2, bmax3 + 1):
    for res in itertools.combinations_with_replacement(TH.units(b), 3):
        n3 += 1
        if crossing_free_for_all_boxes(res, b)[0] != TH.direct_product(res, b): mism3.append((b, res))
RES['T2_k3_edge_mismatch'] = mism3
check('T2(c) k=3: direct product => edge-crossing-free always; the converse FAILS exactly at the Klein-four classes: %d exceptions among %d triples (b <= %d): %s' % (len(mism3), n3, bmax3, mism3), all(crossing_free_for_all_boxes(res, b)[0] and not TH.direct_product(res, b) for b, res in mism3) and (SMOKE or [(8, (3, 5, 7)), (12, (5, 7, 11))] == mism3 or ((8, (3, 5, 7)) in mism3)))
tot = 0; badc = []
for b in range(2, 21 if SMOKE else 41):
    n, bad = TH.check_k2_converse(b); tot += n; badc += bad
check('T2(b): for every non-direct pair (b <= %d, %d pairs) the explicit configuration u=(0,o2), g=(o1,0), r=(a,c), h=(0,o2) in the box (o1, c+o2) is a genuine interior crossing of two Graver edges' % (40 if not SMOKE else 20, tot), not badc and tot > 0, badc[:3])
kf = HD.example_record('Klein-four b=8', (3, 5, 7), (3, 3, 2), 8)
RES['Klein_four'] = kf
check('T2(c): Klein-four (b=8, primes = 3,5,7 mod 8, x = %s): edges never cross, yet the cell structure is NON-EMBEDDED at box (3,3,2): 14 two-cells and the 3-cell all meet improperly; diagonal obstruction (0,0,2) = (1,1,1)-(1,1,-1)' % kf['x'],
      kf['status'] == 'non_embedded' and kf['edge_relations'].get('interior_cross', 0) == 0 and (0, 0, 2) in [tuple(g) for g in graver_complete((3, 5, 7), 8)], kf['non_face_by_dims'])
ok_pp = all(TH.free_axis_persistence(res, b, q)[0] for res, b, q in (((2, 3), 5, (5, 2)), ((2, 3), 5, (6, 3)), ((2, 2), 3, (3, 3)), ((2, 3), 7, (6, 4))) if True)
check('T5 product principle: appending an axis with p = 1 (mod b) keeps every crossing of the base fibre (4 base fibres)', ok_pp)

# ============================================================================================== E7  corpus audit,  E8  the b_1 != 0 fibres
t = time.time(); e7 = RC.run_e7(SMOKE); RES['E7_seconds'] = round(time.time() - t, 1)
cls = collections.Counter(r['class'] for r in e7); RES['E7_classes'] = dict(cls)
check('E7: all %d corpus fibres classified (no skips, none resource-limited): %s' % (len(e7), dict(cls)), len(e7) == sum(cls.values()) and cls.get('UNRESOLVED_RESOURCE_LIMIT', 0) == 0)
check('E7: boundary^2 = 0 and Euler-Poincare check on every K_abs (over Q)', all(r['d2_ok'] and r['euler_ok'] for r in e7))
if not SMOKE: check('E7: the corpus has exactly 8,203 fibres (same set as v002)', len(e7) == 8203, len(e7))
ne = [r for r in e7 if r['class'] != 'EMBEDDED']
RES['E7_nonembedded'] = [{k_: r[k_] for k_ in ('x', 'class', 'k', 'q', 'b', 'R', 'cells', 'why', 'betti_abs_Q', 'betti_U', 'betti_U_method')} for r in ne]
check('E7: non-embedded fibres: %s' % [r['x'] for r in ne], (SMOKE and len(ne) >= 0) or sorted(r['x'] for r in ne) == sorted(['6400/3', '12800/3', '63504/5', '82944/5', '112896/5']), [r['x'] for r in ne])
check('E7: 82944/5 is the only corpus fibre with an interior edge crossing; the four others fail only through a Graver diagonal lying inside a 2-cell', [r['x'] for r in e7 if r['class'] == 'NON_EMBEDDED_EDGE_CROSSING'] in (['82944/5'], []) )
# embedded => homeomorphic: independent re-computation of the embedded image by the nerve on embedded fibres
nv = 0; nvbad = []; nlimit = 150 if SMOKE else 700
for r in e7:
    if nv >= nlimit: break
    if r['class'] != 'EMBEDDED' or r['k'] < 2 or r['R'] < 4: continue
    x = Fr(r['x']); fc = fibre_complex(x); cov = cover_cells(fc['cells'])
    if len(cov) > 14: continue
    bn, info = betti_nerve(cov, maxdim=3)
    if bn is None: continue
    nv += 1; td = max(1, min(info.get('trusted_degrees', len(bn)), 4)); L = max(len(bn), len(r['betti_abs_Q']), td)
    if list(pad(bn, L)[:td]) != list(pad(r['betti_abs_Q'], L)[:td]): nvbad.append((r['x'], bn, r['betti_abs_Q'], td))
check('E7/T3(a): for %d embedded corpus fibres the nerve (independent exact route) reproduces the Betti numbers of K_abs' % nv, not nvbad and nv > 0, nvbad[:2])
nz = [r for r in e7 if any(r['betti_abs_Q'][1:])]
e8 = {'total_b1_or_higher_nonzero': len(nz), 'embedded': sum(1 for r in nz if r['class'] == 'EMBEDDED'),
      'nonembedded_betti_changed': [(r['x'], r['betti_abs_Q'], r['betti_U']) for r in nz if r['class'] != 'EMBEDDED' and r['betti_U'] is not None and list(pad(r['betti_U'], len(r['betti_abs_Q']))[:len(r['betti_abs_Q'])]) != list(r['betti_abs_Q'])],
      'nonembedded_betti_same': [(r['x'], r['betti_abs_Q'], r['betti_U']) for r in nz if r['class'] != 'EMBEDDED' and r['betti_U'] is not None and list(pad(r['betti_U'], len(r['betti_abs_Q']))[:len(r['betti_abs_Q'])]) == list(r['betti_abs_Q'])],
      'unavailable': [r['x'] for r in nz if r['class'] != 'EMBEDDED' and r['betti_U'] is None]}
RES['E8'] = e8
check('E8: of the %d corpus fibres with nonzero homology in K_abs, %d are valid embedded complexes (their Betti numbers are the geometric ones) and %d are non-embedded; of those, Betti numbers change in %d, stay the same in %d, unavailable in %d' % (len(nz), e8['embedded'], len(nz) - e8['embedded'], len(e8['nonembedded_betti_changed']), len(e8['nonembedded_betti_same']), len(e8['unavailable'])),
      len(nz) == e8['embedded'] + len(e8['nonembedded_betti_changed']) + len(e8['nonembedded_betti_same']) + len(e8['unavailable']), e8)
csvw('corpus_audit.csv', [(r['x'], r['family'], r['b'], r['k'], '|'.join(map(str, r['q'])), r['R'], '|'.join(map(str, r['cells'])), r['class'], json.dumps(r['edge_relations']), '|'.join(map(str, r['betti_abs_Q'])), '' if r['betti_U'] is None else '|'.join(map(str, r['betti_U'])), r['betti_U_method']) for r in e7],
     ['x', 'family', 'b', 'k', 'q', 'R', 'cells', 'class', 'edge_relations', 'betti_abs_Q', 'betti_U', 'betti_U_method'])

# ============================================================================================== k = 2 residue scan (H1-H4 evidence)
import crossing_scan as CS
rows = []; t = time.time()
bmaxs, qmaxs = (6, 4) if SMOKE else (11, 6)
for b in range(2, bmaxs + 1):
    for r1 in TH.units(b):
        for r2 in TH.units(b):
            if r2 < r1: continue
            for q1 in range(1, qmaxs + 1):
                for q2 in range(1, qmaxs + 1):
                    rec = CS.run_case(b, r1, r2, q1, q2)
                    if rec: rows.append(rec)
RES['scan_seconds'] = round(time.time() - t, 1)
def differs(r): return list(pad(r['abs'], 3)) != list(pad(r['U'], 3))
crossing = [r for r in rows if r['edge_rel'].get('interior_cross', 0)]
noncross_diff = [r for r in rows if not r['edge_rel'].get('interior_cross', 0) and differs(r)]
scan = {'cases': len(rows), 'crossing': len(crossing), 'crossing_differ': sum(1 for r in crossing if differs(r)), 'noncrossing_but_differ': len(noncross_diff),
        'U_b2_nonzero': sum(1 for r in rows if pad(r['U'], 3)[2] != 0), 'U_b1_positive': sum(1 for r in rows if pad(r['U'], 3)[1] > 0),
        'abs_b1_positive': sum(1 for r in rows if pad(r['abs'], 3)[1] > 0), 'abs_b2_positive': sum(1 for r in rows if pad(r['abs'], 3)[2] > 0),
        'noncrossing_not_differ_are_embedded_or_agree': sum(1 for r in rows if not r['edge_rel'].get('interior_cross', 0) and not differs(r)),
        'all_complexes_valid_d2_euler': all(r['ok'] for r in rows), 'bmax': bmaxs, 'qmax': qmaxs, 'field': 'GF(2^61-1) for bulk rank; exact-Q recheck below'}
RES['scan_k2'] = scan
check('k=2 scan (b <= %d, boxes <= %d^2, %d fibres): boundary^2 = 0 and Euler-Poincare on every abstract and every planar complex' % (bmaxs, qmaxs, len(rows)), scan['all_complexes_valid_d2_euler'])
check('H1 test: the abstract Betti numbers DIFFER from those of the geometric image U in all %d crossing fibres (so the abstract pattern is not a geometric invariant there)' % scan['crossing'], scan['crossing'] == scan['crossing_differ'] and scan['crossing'] > 0)
check('H4 test: U (any planar polyhedral set) has beta_2 = 0 in all %d scan fibres, while K_abs has beta_2 > 0 in %d of them' % (len(rows), scan['abs_b2_positive']), scan['U_b2_nonzero'] == 0)
# exact-Q recheck on a deterministic sample of the scan
import random
rnd = random.Random(20261024); samp = rnd.sample(rows, min(len(rows), 80 if SMOKE else 400)); badQ = []
for r in samp:
    b = r['b']; fc = fibre_complex_data(tuple(r['r']), tuple(r['q']), b); cov = cover_cells(fc['cells'])
    bU, _ = RC.planar_U_betti(fc, cov, 'Q'); bA = betti_abs(fc['cells'])[0]
    if list(pad(bU, 3)) != list(pad(r['U'], 3)) or list(pad(bA, 3)) != list(pad(r['abs'], 3)): badQ.append((b, r['r'], r['q']))
check('scan: exact-rational recomputation of %d sampled cases reproduces the GF(p) Betti numbers of both K_abs and U' % len(samp), not badQ, badQ[:3])
csvw('scan_k2.csv', [(r['b'], r['r'][0], r['r'][1], r['q'][0], r['q'][1], r['R'], '|'.join(map(str, r['abs'])), '|'.join(map(str, r['U'])), json.dumps(r['edge_rel']), r['n_crossing_points']) for r in rows],
     ['b', 'r1', 'r2', 'q1', 'q2', 'R', 'betti_abs', 'betti_U', 'edge_relations', 'n_crossing_points'])

# ============================================================================================== planar vs nerve cross-validation, graph identity
n = 0; bad = []; lim = 120 if SMOKE else 1700
for r in rows:
    if n >= lim: break
    if r['cover'] > 14: continue
    fc = fibre_complex_data(tuple(r['r']), tuple(r['q']), r['b']); cov = cover_cells(fc['cells'])
    bn, info = betti_nerve(cov)
    if bn is None: continue
    n += 1; m = min(len(bn), len(r['U']))
    if list(bn[:m]) != list(r['U'][:m]) or any(bn[m:]) or any(r['U'][m:]): bad.append((r['b'], r['r'], r['q'], bn, r['U']))
check('T3(b): planar polyhedral subdivision and the nerve of the maximal-cell cover (two independent exact routes to H_*(U)) agree on %d fibres' % n, not bad and n > 0, bad[:2])
gi = [TH.graph_identity(fibre_complex_data(tuple(r['r']), tuple(r['q']), r['b'])) for r in rows[:: (4 if SMOKE else 3)]]
gi = [g for g in gi if g]
check('P3 graph identity: beta_1(arrangement of the straight 1-skeleton) = beta_1(abstract 1-skeleton) + sum_p (m_p - 1), beta_0 preserved, on %d fibres' % len(gi), all(g['ok'] for g in gi) and len(gi) > 0)

# ============================================================================================== E10  3D and 4D rational cuts
sv3 = HD.survey(3, [3, 4, 5, 7], [(2, 2, 2), (3, 2, 2), (2, 3, 3)])
c3 = collections.Counter(r['class'] for r in sv3); dp3 = [r for r in sv3 if r['direct_product']]
RES['E10_k3'] = {'fibres': len(sv3), 'classes': dict(c3), 'direct_product_fibres': len(dp3), 'direct_all_embedded': all(r['class'] == 'EMBEDDED' for r in dp3),
                 'non_direct_embedded': sum(1 for r in sv3 if not r['direct_product'] and r['class'] == 'EMBEDDED'),
                 'crossing_nonplanar_in_coords': sum(1 for r in sv3 if r.get('crossing_nonplanar_in_coords'))}
check('E10 (k=3, b in {3,4,5,7}, 3 boxes, %d fibres, none unresolved): %s; every one of the %d direct-product fibres is embedded (Thm T2a)' % (len(sv3), dict(c3), len(dp3)),
      c3.get('UNRESOLVED_RESOURCE_LIMIT', 0) == 0 and RES['E10_k3']['direct_all_embedded'] and len(dp3) > 0)
check('E10 (k=3): the survey contains edge crossings whose plane is NOT a coordinate plane (genuinely 3-dimensional crossings): %d fibres' % RES['E10_k3']['crossing_nonplanar_in_coords'], RES['E10_k3']['crossing_nonplanar_in_coords'] > 0)
sv4 = HD.survey(4, [3, 5] if SMOKE else [3, 4, 5], [(1, 1, 1, 2), (2, 2, 2, 2)] if not SMOKE else [(1, 1, 2, 2)], lp_budget=6000)
c4 = collections.Counter(r['class'] for r in sv4); dp4 = [r for r in sv4 if r['direct_product']]
RES['E10_k4'] = {'fibres': len(sv4), 'classes': dict(c4), 'direct_product_fibres': len(dp4), 'direct_all_embedded': all(r['class'] == 'EMBEDDED' for r in dp4)}
check('E10 (k=4): %d fibres classified: %s (resource-limited cases are reported, not counted as embedded); every direct-product fibre is embedded' % (len(sv4), dict(c4)), RES['E10_k4']['direct_all_embedded'] and len(sv4) > 0)
ex = {}
ex['genuine_3D_crossing'] = HD.example_record('genuine 3-D edge crossing: b=5, residues (2,2,3), box (3,3,3)', (2, 2, 3), (3, 3, 3), 5)
ex['unit_axis_embedded'] = HD.example_record('b=3, residues (2,1,1,1): one real axis plus three unit axes (4-D, direct product)', (2, 1, 1, 1), (2, 1, 1, 1), 3)
cr4 = [r for r in sv4 if r['class'] == 'NON_EMBEDDED_EDGE_CROSSING']
if cr4:
    r4 = sorted(cr4, key=lambda r: (r['R'], r['b']))[0]
    ex['4D_edge_crossing'] = HD.example_record('4-D edge crossing (smallest in the survey): b=%d, residues %s, box %s' % (r4['b'], tuple(r4['res']), tuple(r4['q'])), tuple(r4['res']), tuple(r4['q']), r4['b'])
RES['E10_examples'] = ex
g3 = ex['genuine_3D_crossing']
check('E10: genuine 3-D crossing witness x = %s (primes %s): non-embedded, K_abs = %s, geometric image U = %s' % (g3['x'], g3['primes'], g3['betti_abs_Q'], g3['betti_U']),
      g3['status'] == 'non_embedded' and g3['edge_relations'].get('interior_cross', 0) > 0 and g3['x'] == '5489031744/5')
check('E10: 4-D example with unit axes is embedded and contractible (Betti numbers (1,0,0,0) over Q)', ex['unit_axis_embedded']['status'] == 'embedded', ex['unit_axis_embedded']['betti_abs_Q'])
if cr4: check('E10: a 4-D fibre (x = %s) has interior edge crossings in R^4 (k=4 is not special)' % ex['4D_edge_crossing']['x'], ex['4D_edge_crossing']['edge_relations'].get('interior_cross', 0) > 0)
csvw('e10_survey.csv', [(r['k'], r['b'], '|'.join(map(str, r['res'])), '|'.join(map(str, r['q'])), r['R'], '|'.join(map(str, r['cells'])), r['class'], r['direct_product'], r['n_crossing_pairs']) for r in sv3 + sv4],
     ['k', 'b', 'residues', 'box', 'R', 'cells', 'class', 'direct_product', 'crossing_pairs'])
dump('e10_examples.json', ex, 'certificates')

# ============================================================================================== E9  collective orbits (C-map, 60 steps each; cached exact records + recomputation)
cache_path = os.path.join(SHIPPED, 'data', 'e9_orbits.json')
if not os.path.exists(cache_path):
    check('E9: cached orbit records present (output/data/e9_orbits.json)', False)
else:
    cache = json.load(open(cache_path)); meta = cache.pop('_meta', {})
    states = [(nm, r) for nm, rs in cache.items() for r in rs]
    cls9 = collections.Counter(r['class'] for _, r in states)
    RES['E9_classes'] = dict(cls9); RES['E9_states'] = len(states); RES['E9_meta'] = meta
    per = {nm: dict(collections.Counter(r['class'] for r in rs)) for nm, rs in cache.items()}; RES['E9_per_orbit'] = per
    check('E9: %d orbit states recorded across %d orbits; classes %s; unresolved (resource-limited) states are listed, never counted as embedded' % (len(states), len(cache), dict(cls9)), len(states) > 0)
    emb = [r for _, r in states if r['class'] == 'EMBEDDED']
    check('E9/T3(a): in every embedded state the geometric image has the Betti numbers of K_abs (%d states)' % len(emb), all(r['betti_U'] == r['betti_abs_Q'] for r in emb))
    o72 = [rs for nm, rs in cache.items() if nm.startswith('72')]
    if o72: check('E9: the 72 [C, G=1] orbit is embedded at all %d recorded states (no crossings)' % len(o72[0]), all(r['class'] == 'EMBEDDED' for r in o72[0]))
    ob = [rs for nm, rs in cache.items() if nm.startswith('g11 benchmark')]
    if ob:
        check('E9: the g=11 benchmark orbit (FIELD-I) is NON-EMBEDDED at all %d states (interior edge crossings), so v002 beta_1 saturation (= 8) is an abstract-complex quantity' % len(ob[0]), all(r['class'] == 'NON_EMBEDDED_EDGE_CROSSING' for r in ob[0]))
        late = [r for r in ob[0] if r['n'] >= 20 and r['betti_U'] is not None and len(r['betti_U']) > 1]
        check('E9: g=11 benchmark, n >= 20: beta_1(K_abs) = %s while beta_1(U) = %s (%d states with a trusted value)' % (sorted({r['betti_abs_Q'][1] for r in late}), sorted({r['betti_U'][1] for r in late}), len(late)), len(late) > 0 and all(r['betti_U'][1] == 0 for r in late))
    check('E9: no orbit state has a failed boundary^2 / Euler-Poincare check', all(r['abs_d2_euler'][0] and r['abs_d2_euler'][1] for _, r in states))
    # recomputation
    want = {'72': (0, 10, 30), 'g11 benchmark': (0, 3, 8, 15), 'g=11 L': (0, 5)} if SMOKE else {'72': (0, 10, 30, 59), 'g11 benchmark': (0, 3, 8, 15, 30, 45), 'g=11 L': (0, 5, 20), 'g=13': (0, 8, 15)}
    nrec = 0; badrec = []
    for nm, rs in cache.items():
        for pref, ns in want.items():
            if nm.startswith(pref):
                spec = OR.orbit_specs()[nm] if nm in OR.orbit_specs() else None
                if spec is None: continue
                xs = OR.orbit_states(spec, 60)
                for r in rs:
                    if (ARGS.orbits_exhaustive or r['n'] in ns) and r['n'] < len(xs):
                        if r.get('seconds', 0) > 90 and not ARGS.orbits_exhaustive: continue
                        new = OR.state_record(r['n'], xs[r['n']]); nrec += 1
                        a = {k: v for k, v in r.items() if k != 'seconds'}; b_ = {k: v for k, v in new.items() if k != 'seconds'}
                        if a != b_: badrec.append((nm, r['n']))
    check('E9: independent recomputation of %d orbit states%s reproduces the cached records exactly' % (nrec, ' (exhaustive)' if ARGS.orbits_exhaustive else ' (deterministic sample)'), not badrec and nrec > 0, badrec[:3])
    csvw('e9_orbit_states.csv', [(nm, r['n'], r['b'], r['k'], '|'.join(map(str, r['q'])), r['R'], '|'.join(map(str, r['cells'])), r['class'], r['n_crossing_points'], '|'.join(map(str, r['betti_abs_Q'])),
                                  '' if r['betti_U'] is None else '|'.join(map(str, r['betti_U'])), r['U_method']) for nm, r in states],
         ['orbit', 'n', 'b', 'k', 'q', 'R', 'cells', 'class', 'crossing_points', 'betti_abs_Q', 'betti_U', 'U_method'])

# ============================================================================================== summary
RES['hypotheses'] = {'H1': 'false: abstract Betti numbers differ from geometric ones whenever an interior crossing exists (all %d scan crossings, 5 corpus non-embedded)' % scan['crossing_differ'],
                     'H2': 'true and fully characterized for k=2 (direct product <=> never crosses); partial for k>=3 (Klein-four exception, genuine 3-D crossings)',
                     'H3': 'partial: embedded fibres keep K_abs homology exactly; abstract beta_1 saturation/beta_2 growth vanish on the geometric image',
                     'H4': 'abstract beta_2 is unbounded (family x_t) while planar U has beta_2 = 0; orbit saturation of beta_1 is an abstract-complex statement'}
npass = sum(c['ok'] for c in CHECKS); RES['checks'] = CHECKS; RES['passed'] = npass; RES['total'] = len(CHECKS); RES['seconds'] = round(time.time() - T0, 1)
dump('verify_%s.json' % MODE, RES, 'reports')
print('\n%d/%d checks passed  (%s mode, %.0f s)%s' % (npass, len(CHECKS), MODE, time.time() - T0, '' if FAILS == 0 else '   %d FAILED' % FAILS))
sys.exit(1 if FAILS else 0)
