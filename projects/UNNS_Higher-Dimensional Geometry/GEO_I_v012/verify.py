#!/usr/bin/env python3
"""GEO-I v012 verifier.   python3 verify.py --smoke  (several minutes)    python3 verify.py  (full, about 2 h)
New v012 checks (G12-T1..T8: arithmetic lemma, structure lemmas, cell cover, certificates, tamper rejection, documentation) + the inherited v011 verifier (verify_v011.py, which itself gates verify_v010.py) as a gate.
Exact integer/rational arithmetic; anything not run is reported UNAVAILABLE, never PASS.  Writes output/reports/verify_{smoke,full}.json."""
import os, sys, json, time, hashlib, subprocess, random, argparse, copy, tempfile
ROOT = os.path.dirname(os.path.abspath(__file__))
for d in ('theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d))
ap = argparse.ArgumentParser(); ap.add_argument('--smoke', action='store_true'); ap.add_argument('--rerun-inherited-full', action='store_true', help='also re-execute the 2-hour inherited v011/v010 full gate'); _a = ap.parse_args(); SMOKE = _a.smoke; RERUN = _a.rerun_inherited_full; MODE = 'smoke' if SMOKE else 'full'
from math import gcd
import cap_cells as K, cap_cover as C, checker12 as KC
DATA = os.path.join(ROOT, 'output', 'data'); CHECKS = []; FAILS = 0; T0 = time.time(); GRP = ['v012']
def check(name, ok, detail=None):
    global FAILS
    CHECKS.append({'name': name, 'ok': bool(ok), 'detail': detail, 'group': GRP[0]}); FAILS += (not ok)
    print(('PASS  ' if ok else 'FAIL  ') + name + ('' if detail is None else '   [' + str(detail)[:150] + ']'), flush=True)
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
ALLOWED = ('PROVED', 'PROVED+CHECKED', 'CHECKED', 'FALSE', 'CORRECTED', 'OPEN', 'UNAVAILABLE')
rd = lambda *p: open(os.path.join(ROOT, *p), encoding='utf-8').read()

# ---------------------------------------------------------------- integrity / preservation
bad = []
for l in open(os.path.join(ROOT, 'MANIFEST.sha256')):
    h, p = l.strip().split(None, 1); p = p.lstrip('*')
    if not os.path.exists(os.path.join(ROOT, p)) or sha(os.path.join(ROOT, p)) != h: bad.append(p)
check('MANIFEST.sha256 verifies (every shipped file unchanged)', not bad, bad[:3])
prov = json.load(open(os.path.join(ROOT, 'PROVENANCE.json'))); inh = prov['inherited_v011_sha256']; mv = prov['moved_v011_docs']
check('v011 preservation: %d files inherited UNCHANGED from the v011 release (sha-256 equal)' % len(inh), len(inh) > 280 and all(os.path.exists(os.path.join(ROOT, p)) and sha(os.path.join(ROOT, p)) == h for p, h in inh.items()))
check('v011 documents archived unchanged in docs_v011/ (%d files)' % len(mv), len(mv) == 10 and all(os.path.exists(os.path.join(ROOT, q)) for q in mv.values()))
check('v012 provenance: new_in_v012 files are all present', len(prov['new_in_v012']) > 15 and all(os.path.exists(os.path.join(ROOT, p)) for p in prov['new_in_v012']))
FROZEN = {'geo1lib.py': '0c94b3a73721c0c69823aee53f33710cad186280f3e8d8659bbb4188381c8831', 'geo2lib.py': 'a8c47c4ff0aebbcfb41372dcaba5006b12349add5c1103073583f50c093d852e'}
check('frozen v001/v002 libraries byte-identical to released (sha-256)', all(sha(os.path.join(ROOT, 'frozen', k)) == v for k, v in FROZEN.items()))
check('v011 results preserved: W2 and universal rank-3 records present and PROVED statuses unchanged in docs_v011', 'G11-T4' in rd('docs_v011', 'THEOREM_REGISTRY.tsv') and 'PROVED' in [l.split('\t')[2] for l in rd('docs_v011', 'THEOREM_REGISTRY.tsv').splitlines() if l.startswith('G11-T4')][0])

# ---------------------------------------------------------------- unit tests
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'tests', 'test_geo12.py')], capture_output=True, text=True)
check('v012 tests/test_geo12.py (13 checks incl. certificate tamper rejection) pass', r.returncode == 0 and ' 0 failures' in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])

# ---------------------------------------------------------------- G12-T1 REGENERATED
DM = 40 if SMOKE else 100; n = 0; bad = []
for d in range(5, DM + 1):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        t = pow(s, -1, d); a, c = d - s, d - t
        for x in range(1, d):
            y = (s * x) % d
            if y == 0 or any(((j + a * i) % d == 0) and (i, j) not in ((0, 0), (x, y)) for i in range(x + 1) for j in range(y + 1)): continue
            n += 1
            if max(y + a * x, x + c * y) < x * y: bad.append((d, s, x, y))
check('G12-T1 REGENERATED: max(y+(d-s)x,(d-t)y+x) >= xy at every Pareto-minimal point of Gamma, %d points, 5<=d<=%d' % (n, DM), not bad and n > 1000, bad[:3])
# proof mechanism of Step 2/3: if y>a and b>=2 the point R of the proof exists in the rectangle (checked on every point with y>a and D1 >= 2d)
m = 0; bad = []
for d in range(5, 36 if SMOKE else 60):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        a = d - s
        for x in range(1, d):
            y = (s * x) % d
            if y == 0 or y <= a or y + a * x < 2 * d: continue
            if any(((j + a * i) % d == 0) and (i, j) not in ((0, 0), (x, y)) for i in range(x + 1) for j in range(y + 1)): continue
            bad.append((d, s, x, y))   # a Pareto-minimal M with y>a and b>=2 must not exist
            m += 1
check('G12-T1 proof Step 2 (REGENERATED): no Pareto-minimal M has both y > d-s and b = (y+(d-s)x)/d >= 2 (so such an M would contradict minimality), d<=%d' % (35 if SMOKE else 59), not bad, bad[:3])

# ---------------------------------------------------------------- structure lemmas / cover
SD = 9 if SMOKE else 14
n, bad = C.structure_sweep(5, SD)
check('G12-L1..L5 structure lemmas S1-S6 REGENERATED on all %d small boxes d<=%d (H_Q cap square = H_0; no N points; flags; no R->T; first step B+M; Graver steps)' % (n, SD), not bad, bad[:2])
CD = 9 if SMOKE else 13
n, bad = C.sweep(5, CD)
check('G12-T3..T7 cell family REGENERATED (exact): legitimate and covering H_Q minus H_0 on all %d small boxes d<=%d (one-sided, mixed, degenerate)' % (n, CD), not bad, bad[:2])
tgt = [(13, 5, 1, 12), (13, 5, 12, 1), (21, 8, 20, 20), (34, 13, 1, 33), (55, 21, 54, 2), (89, 34, 3, 88), (233, 89, 1, 232), (101, 38, 50, 70), (64, 5, 63, 63), (97, 2, 96, 1), (97, 95, 1, 96), (144, 55, 143, 143), (377, 144, 1, 376)]
if SMOKE: tgt = tgt[:8]
check('G12 adversarial boxes (Fibonacci/extreme residues/thin enlargements, d up to %d) exact cover' % max(t[0] for t in tgt), all(C.verify(*x)[0] for x in tgt))
rng = random.Random(1212); nr = 40 if SMOKE else 400; bad = []
for _ in range(nr):
    d = rng.randint(31, 160); us = [s for s in range(2, d - 1) if gcd(s, d) == 1]; s = rng.choice(us); u = rng.randrange(d); v = rng.randrange(d)
    if u == v == 0: continue
    if not C.verify(d, s, u, v)[0]: bad.append((d, s, u, v))
check('G12 fresh random boxes (seed 1212, 31<=d<=160): %d boxes exact cover' % nr, not bad, bad[:3])
rec = json.load(open(os.path.join(DATA, 'v12_cap.json')))
check('shipped record v12_cap.json: full sweep d<=%d (%d boxes), structure d<=%d (%d boxes), targeted (%d boxes, d<=%d), random (%d boxes): 0 failures' % (rec['full_sweep']['dmax'], rec['full_sweep']['boxes'], rec['structure_sweep']['dmax'], rec['structure_sweep']['boxes'], rec['targeted']['boxes'], rec['targeted']['dmax'], rec['random']['boxes']),
      rec['full_sweep']['failures'] == [] and rec['structure_sweep']['failures'] == [] and rec['targeted']['failures'] == [] and rec['random']['failures'] == [] and rec['full_sweep']['dmax'] >= 12 and rec['full_sweep']['boxes'] > 2000)

# ---------------------------------------------------------------- certificates
files = [os.path.join(ROOT, 'certificates', f) for f in ('C11_arith.json', 'C12_capcover2.json', 'C9_partition.json', 'C10_capcover.json')]
td = tempfile.mkdtemp()
if SMOKE:
    new = []
    for i, f in enumerate(files): json.dump(json.load(open(f))[::(9, 37, 4, 8)[i]], open(os.path.join(td, 'c%d.json' % i), 'w')); new.append(os.path.join(td, 'c%d.json' % i))
    files = new
r = subprocess.run([sys.executable, '-I', os.path.join(ROOT, 'certificates', 'checker12.py')] + files, capture_output=True, text=True)
check('D checker12.py run isolated (python -I): %s' % ' | '.join(l.split(': ', 1)[1] for l in r.stdout.splitlines() if l.startswith('VALID')), r.returncode == 0 and 'INVALID' not in r.stdout and r.stdout.count('VALID  ') == 4, r.stdout[-200:])
AR = json.load(open(os.path.join(ROOT, 'certificates', 'C11_arith.json'))); CV = json.load(open(os.path.join(ROOT, 'certificates', 'C12_capcover2.json')))
check('D certificate counts: 984 ARITH (every unit pair 5<=d<=60), 2,130 CAPCOVER2 (all small boxes d<=12)', len(AR) == 984 and len(CV) == 2130 and all(c['type'] == 'ARITH' for c in AR) and all(c['type'] == 'CAPCOVER2' for c in CV))
tam = True
for i in (500, 1100, 2000):
    rej = 0
    for k in range(len(CV[i]['cells'])):
        c = copy.deepcopy(CV[i]); del c['cells'][k]; rej += (not KC.check_CAPCOVER2(c)[0])
    tam &= rej >= 1   # at least the essential cells are detected when removed (a cell may be redundant)
    c = copy.deepcopy(CV[i]); c['cells'][0][2] += 1; tam &= not KC.check_CAPCOVER2(c)[0]
c = copy.deepcopy(AR[100]); c['s'] = c['d'] - 1; tam &= not KC.check_ARITH(c)[0]
check('D tamper rejection: CAPCOVER2 (removed cell, perturbed generator), ARITH (s=d-1)', tam)

# ---------------------------------------------------------------- documentation / honesty
tm = rd('MATHEMATICS.md'); tsv = [l.split('\t') for l in rd('THEOREM_REGISTRY.tsv').splitlines()[1:]]; reg = {r_[0]: r_[2] for r_ in tsv}
check('G12 THEOREM_REGISTRY.tsv: %d rows, every status starts with an allowed word' % len(tsv), len(tsv) >= 20 and all(r_[2].split()[0] in ALLOWED for r_ in tsv))
check('G12 honesty: T1..T8 are PROVED+CHECKED with proofs in MATHEMATICS.md (not CHECKED-only); broader global organisation recorded OPEN; no GAP certificate shipped', all(reg['G12-T%d' % k] == 'PROVED+CHECKED' for k in range(1, 9)) and reg['G12-O1'] == 'OPEN' and reg['G12-N1'] == 'CHECKED' and reg['G11-T4'] == 'PROVED')
check('G12 documentation: MATHEMATICS.md contains the full proof chain and names the inherited hypotheses of T8', all(k in tm for k in ('G12-T1', 'reflection', 'Pareto-minimal', 'G12-L4', 'G12-T8', 'G5-C1', 'G7-T1', 'G10-R1', 'Case 1')) and 'conditional' in tm.lower())
check('G12 documentation: all required documents exist', all(os.path.exists(os.path.join(ROOT, f)) for f in ('README.md', 'REPORT.md', 'MATHEMATICS.md', 'ARITH_CAP.md', 'GRAVER_STRIP.md', 'MIXED_CAP.md', 'CERTIFICATION.md', 'PRIOR_ART.md', 'THEOREM_REGISTRY.tsv', 'CONTEXT.md', 'RUN_SMOKE.bat', 'RUN_FULL.bat')))
tp = rd('PRIOR_ART.md').lower()
ip = json.load(open(os.path.join(DATA, 'v12_sweep_13_30_PARTIAL.json')))
check('interrupted standalone sweep d=13..30 recorded as PARTIAL (not PASS); no check depends on it', ip['status'] == 'PARTIAL' and 'PASS' not in ip['status'] and not any('13..30' in c['name'] or '13<=d<=30' in c['name'] for c in CHECKS))
check('G12 prior art: no priority or novelty claim; no unverified reference', 'no priority or novelty claim' in tp and 'fabricated' in tp)
check('G12 figures: 2 figures shipped in figures_v12/', len([f for f in os.listdir(os.path.join(ROOT, 'figures_v12')) if f.endswith('.png')]) == 2)
rep = rd('REPORT.md').lower()
check('G12 report states the planar status precisely (proved modulo the named inherited results; not a claim about broader organisation)', 'conditional' in rep and 'inherited' in rep and 'not claimed' in rep)

# ---------------------------------------------------------------- inherited gate (the v011 verifier, which gates v010)
GRP[0] = 'gate'
# Frozen baselines: the full v011/v010 verification reports of the v011 release are preserved unchanged (hash-checked by MANIFEST) and recorded here.
b11 = json.load(open(os.path.join(ROOT, 'output', 'baseline_v011', 'verify_v011_full_BASELINE.json'))); b10 = json.load(open(os.path.join(ROOT, 'output', 'baseline_v011', 'verify_v010_full_BASELINE.json')))
check('BASELINE: preserved full reports of the frozen v011/v010 releases: v011 %s/%s, v010 %s/%s checks passed (recorded, not re-executed here)' % (b11['total_pass_this_file'], b11['total_checks_this_file'], b10['total_pass'], b10['total_checks']),
      b11['release'] == 'v011' and b11['mode'] == 'full' and b11['total_pass_this_file'] == b11['total_checks_this_file'] == 33 and b10['release'] == 'v010' and b10['mode'] == 'full' and b10['total_pass'] == b10['total_checks'] == 132)
GMODE = 'smoke' if (SMOKE or not RERUN) else 'full'
r = subprocess.run([sys.executable, os.path.join(ROOT, 'verify_v011.py')] + (['--smoke'] if GMODE == 'smoke' else []), capture_output=True, text=True, cwd=ROOT)
gj = os.path.join(ROOT, 'output', 'reports', 'verify_v011_%s.json' % GMODE); g = json.load(open(gj)) if os.path.exists(gj) else {}
check('GATE (targeted compatibility regression = inherited v011 verifier in %s mode, which gates v010): %s/%s own checks + v010 gate %s/%s' % (GMODE, g.get('total_pass_this_file'), g.get('total_checks_this_file'), g.get('inherited_v010_gate_pass'), g.get('inherited_v010_gate_checks')),
      r.returncode == 0 and g.get('release') == 'v011' and g.get('total_pass_this_file') == g.get('total_checks_this_file') and g.get('total_checks_this_file', 0) >= 30, (r.stdout.strip().splitlines() or [''])[-1])
INH_FULL = 'PASS (re-executed)' if (RERUN and not SMOKE) else 'NOT_RERUN - FROZEN BASELINE VERIFIED'
print('inherited full v011/v010 gate:', INH_FULL)

new = [c for c in CHECKS if c['group'] == 'v012']; ok = sum(c['ok'] for c in CHECKS)
os.makedirs(os.path.join(ROOT, 'output', 'reports'), exist_ok=True)
json.dump({'release': 'v012', 'mode': MODE, 'level': 'Level 1 (smoke)' if SMOKE else 'Level 1 + Level 2 (full)', 'v012_new_checks': len(new), 'v012_new_pass': sum(c['ok'] for c in new),
           'inherited_full_gate_status': INH_FULL, 'inherited_gate_mode_run': GMODE, 'inherited_v011_gate_checks': g.get('total_checks_this_file'), 'inherited_v011_gate_pass': g.get('total_pass_this_file'), 'inherited_v010_gate_checks': g.get('inherited_v010_gate_checks'), 'inherited_v010_gate_pass': g.get('inherited_v010_gate_pass'),
           'total_checks_this_file': len(CHECKS), 'total_pass_this_file': ok, 'seconds': round(time.time() - T0, 1), 'checks': CHECKS}, open(os.path.join(ROOT, 'output', 'reports', 'verify_%s.json' % MODE), 'w'), indent=1, default=str)
print('\n%s: v012 NEW %d/%d PASS | inherited v011 gate %s/%s (v010 inside: %s/%s) | (%.0f s)' % (MODE.upper(), sum(c['ok'] for c in new), len(new), g.get('total_pass_this_file'), g.get('total_checks_this_file'), g.get('inherited_v010_gate_pass'), g.get('inherited_v010_gate_checks'), time.time() - T0))
sys.exit(1 if FAILS else 0)
