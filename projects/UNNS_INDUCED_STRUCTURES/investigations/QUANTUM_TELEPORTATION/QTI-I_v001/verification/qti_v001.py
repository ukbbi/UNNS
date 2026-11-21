#!/usr/bin/env python3
"""QTI-I v001: audit of the QTEL v001 gap records, exact history theorems, and a deeper-history baseline.

Input : the three *_gaps.csv files written by QUANTUM_TELEPORTATION/scripts/RUN_PROBE.py (raw .pt files not needed).
Output: qti_v001_results.json (deterministic; seed fixed).  Needs numpy, sympy.  Usage: python3 qti_v001.py [csv_dir]
Definitions (all exact):  incoming edges of d: m>=2 with m^2 | d, predecessor d(m-1)/m^2   [T_N with N = m-1]
  F(d) = 1 + sum_{m^2|d, m>=2} F(d(m-1)/m^2)   = number of admissible histories ending at d (empty history included)
  depth(d) = longest history length;  A(d) = set of distinct ancestors;  merger excess = F(d) - |A(d)| - 1 + ... (see code)
"""
import csv, json, hashlib, math, sys, itertools, random
from functools import lru_cache
from pathlib import Path
import numpy as np
from sympy import factorint

CSV_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/mnt/user-data/uploads/UNNS_INDUCED_STRUCTURES/investigations/QUANTUM_TELEPORTATION/results')
FILES = ['iPsiM_156p45_tot', 'iPsiP_156p45_tot', 'iPsiM_156p95_tot']
SEED = 20261121
rng = np.random.default_rng(SEED); random.seed(SEED)
results = {}
def rec(name, ok, **kw):
    results[name] = dict(ok=bool(ok), **kw)
    print(("PASS " if ok else "FAIL ") + name, {k: v for k, v in kw.items() if not isinstance(v, (list, dict))})

_fc = {}
def fac(n):
    r = _fc.get(n)
    if r is None: r = _fc[n] = factorint(n)
    return r
def sqdivs(d):
    """all m>=2 with m^2 | d"""
    f = fac(d); ps = [(p, e // 2) for p, e in f.items() if e >= 2]
    ms = [1]
    for p, e in ps: ms = [m * p ** k for m in ms for k in range(e + 1)]
    return sorted(m for m in ms if m > 1)
def R_q(d):
    f = fac(d); R = 1; q = 1
    for p, e in f.items(): R *= e // 2 + 1; q *= p ** (e // 2)
    return R - 1, q
@lru_cache(maxsize=None)
def hist(d):
    """(F, depth, frozenset of ancestors) for d"""
    F = 1; depth = 0; anc = set()
    for m in sqdivs(d):
        p = d * (m - 1) // (m * m)
        Fp, dp, ap = hist(p)
        F += Fp; depth = max(depth, dp + 1); anc.add(p); anc |= ap
    return F, depth, frozenset(anc)

# ---------------------------------------------------------------- load
data = {}
for fn in FILES:
    rows = list(csv.DictReader(open(CSV_DIR / (fn + '_gaps.csv'))))
    data[fn] = rows
inc = {fn: [r for r in rows if r['included'] == 'yes'] for fn, rows in data.items()}

# ---------------------------------------------------------------- Part 1: audit from the CSVs
res_json = json.load(open(CSV_DIR / 'results.json'))
ok = True; n = 0; audit = {}
for fn in FILES:
    h = [int(r['inferred_counter_gap']) for r in inc[fn]]
    Rs = [R_q(x)[0] for x in h]; qs = [R_q(x)[1] for x in h]
    ok &= Rs == [int(r['UNNS_R']) for r in inc[fn]] and qs == [int(r['max_square_root_divisor']) for r in inc[fn]]
    key = fn + '.pt'; ref = res_json['files'][key]
    ok &= len(h) == ref['gaps_analyzed']
    ok &= abs(np.mean(np.array(Rs) > 0) - ref['counter_R_positive_rate']) < 1e-12
    ok &= abs(np.mean(Rs) - ref['counter_R_mean']) < 1e-12
    ok &= max(Rs) == ref['counter_R_max']
    n += len(h)
    raw = np.array([int(r['raw_gap']) for r in inc[fn]]); hh = np.array(h)
    audit[fn] = dict(gaps=len(h), raw_all_divisible_by_4=bool(np.all(raw % 4 == 0)),
                     max_abs_raw_minus_312p5_h=float(np.max(np.abs(raw - 312.5 * hh))))
rec("A1_independent_recomputation_of_R_q_and_summaries_from_CSV", ok, gaps_recomputed=n, per_stream=audit,
    note="R, q, positive rate, mean R, max R and counts agree with archived results.json; raw gaps all divisible by 4")
ok = all(a['raw_all_divisible_by_4'] and a['max_abs_raw_minus_312p5_h'] <= 5 + 1e-9 for a in audit.values())
rec("A2_grid_statement_consistent_with_CSV", ok, note="raw gap = 312.5*counter gap within the +-5 unit round-off of two rounded timestamps")

# ---------------------------------------------------------------- Part 2: exact theorems
# T2: recursion F equals brute-force forward enumeration
X = 3000
# histories = (start x, forward word); every state of every history is an endpoint of its prefix:
# count, for every start x, all forward paths; number of paths ending at d  == F(d)
paths_end = {d: 0 for d in range(1, X + 1)}
def walk(x):
    paths_end[x] += 1
    for N in range(1, x + 1):
        if x % N == 0:
            y = x * (N + 1) ** 2 // N
            if y <= X: walk(y)
# a history ending at d is determined by its start s and word; enumerate by starting from every s
# (to avoid double counting: paths_end[x] counts paths from the current start only)
tot = {d: 0 for d in range(1, X + 1)}
for s in range(1, X + 1):
    paths_end = {d: 0 for d in range(1, X + 1)}
    walk(s)
    for d, c in paths_end.items(): tot[d] += c
ok = all(tot[d] == hist(d)[0] for d in range(1, X + 1))
rec("T2_history_count_recursion_matches_forward_enumeration", ok, checked_d_up_to=X,
    note="F(d) = 1 + sum F(d(m-1)/m^2) over m>=2, m^2|d; depth <= log_4 d because each predecessor is at most d(m-1)/m^2 <= d/ ... (m^2/(m-1) >= 4)")
# depth bound: m^2/(m-1) >= 4
ok = all(hist(d)[1] <= math.log(d, 4) + 1e-9 for d in range(1, X + 1))
rec("T2b_depth_bounded_by_log4_d", ok)

# T1: clock-unit lift W(d) subset W(hd): same m-sequences are admissible at hd
def mseqs(d):
    out = [()]
    for m in sqdivs(d):
        p = d * (m - 1) // (m * m)
        out += [(m,) + s for s in mseqs(p)]
    return out
ok = True; strict = 0; tot_pairs = 0; ex = []
for d in range(1, 91):
    base = set(mseqs(d))
    for h in range(1, 61):
        lift = set(mseqs(h * d)); tot_pairs += 1
        ok &= base <= lift
        if len(lift) > len(base): strict += 1
        elif h > 1 and len(ex) < 4: ex.append((d, h))
rec("T1_clock_lift_inclusion_W(d)_subset_W(hd)", ok, pairs=tot_pairs, strict_inclusions=strict,
    equal_cases_examples=ex, note="inclusion exact on every pair; strictness is not universal (e.g. d=1,h=2 equal)")
rec("T1b_example_1_vs_4", hist(1)[0] == 1 and hist(4)[0] == 2, F_1=hist(1)[0], F_4=hist(4)[0])
# T1c: mapping raw = 4*y always carries the incoming edge m=2 (N=1): every raw gap has R>=1
ok = all(R_q(4 * y)[0] >= 1 for y in range(1, 5000)); rec("T1c_multiples_of_4_always_have_incoming_edge", ok)

# ---------------------------------------------------------------- Part 3: baseline on the observed counter gaps
def stats_of(vals):
    Rs = []; Fs = []; Ds = []
    for d in vals:
        F, D, A = hist(d)
        Rs.append(R_q(d)[0]); Fs.append(F); Ds.append(D)
    Rs = np.array(Rs); Fs = np.array(Fs); Ds = np.array(Ds)
    return dict(n=len(Rs), P_R_pos=float(np.mean(Rs > 0)), mean_R=float(np.mean(Rs)), mean_F=float(np.mean(Fs)),
                mean_logF=float(np.mean(np.log(Fs))), P_depth_ge2=float(np.mean(Ds >= 2)), mean_depth=float(np.mean(Ds)),
                max_F=int(np.max(Fs)), max_depth=int(np.max(Ds)))
# merger excess: histories that reach the same ancestor by different words: F-1 paths vs |A| distinct ancestors
def merger_excess(d):
    F, D, A = hist(d); return (F - 1) - len(A)
def stats(vals):
    s = stats_of(vals); me = np.array([merger_excess(d) for d in vals])
    s['P_merger'] = float(np.mean(me > 0)); s['mean_merger_excess'] = float(np.mean(me)); return s

obs = {fn: stats([int(r['inferred_counter_gap']) for r in inc[fn]]) for fn in FILES}
# control C1: magnitude-matched integers (each draw: pick an observed gap, uniform integer within +-10%)
pool = {}
NPOOL = 12000
for fn in FILES:
    h = np.array([int(r['inferred_counter_gap']) for r in inc[fn]], dtype=np.int64)
    pick = rng.choice(h, size=NPOOL)
    lo = (pick * 9) // 10; hi = (pick * 11) // 10
    sur = [int(rng.integers(l, u + 1)) for l, u in zip(lo, hi)]
    pool[fn] = sur
# bootstrap null: resample n draws from the pool, 300 times
def boot(sur, n, B=300):
    me_all = np.array([merger_excess(d) for d in sur]); R_all = np.array([R_q(d)[0] for d in sur])
    F_all = np.array([hist(d)[0] for d in sur]); D_all = np.array([hist(d)[1] for d in sur])
    out = {k: [] for k in ('P_R_pos', 'mean_F', 'mean_logF', 'P_depth_ge2', 'P_merger')}
    for _ in range(B):
        ix = rng.integers(0, len(sur), size=n)
        out['P_R_pos'].append(np.mean(R_all[ix] > 0)); out['mean_F'].append(np.mean(F_all[ix]))
        out['mean_logF'].append(np.mean(np.log(F_all[ix]))); out['P_depth_ge2'].append(np.mean(D_all[ix] >= 2))
        out['P_merger'].append(np.mean(me_all[ix] > 0))
    return {k: (float(np.mean(v)), float(np.std(v, ddof=1))) for k, v in out.items()}
ctrl = {fn: boot(pool[fn], obs[fn]['n']) for fn in FILES}
zs = {}
for fn in FILES:
    zs[fn] = {k: float((obs[fn][k] - ctrl[fn][k][0]) / ctrl[fn][k][1]) for k in ctrl[fn]}
maxz = max(abs(v) for fn in zs for v in zs[fn].values())
rec("B1_observed_vs_magnitude_matched_integer_baseline", maxz < 4, observed=obs, control_mean_sd=ctrl, z_scores=zs, max_abs_z=round(maxz, 3),
    note="5 statistics x 3 streams; no preregistered threshold beyond |z|<4 here; exploratory")

# clock-lift ladder on observed gaps (representation sensitivity): subsample for speed
ladder = {}
for fn in FILES:
    h = [int(r['inferred_counter_gap']) for r in inc[fn]]
    sub = [h[i] for i in rng.choice(len(h), size=1500, replace=False)]
    row = {}
    for hh in (1, 2, 3, 4, 6, 8, 12, 16):
        vals = [hh * x for x in sub]
        Fs = np.array([hist(v)[0] for v in vals]); Rs = np.array([R_q(v)[0] for v in vals])
        row[hh] = dict(P_R_pos=float(np.mean(Rs > 0)), mean_F=float(np.mean(Fs)))
    ladder[fn] = row
mono = all(ladder[fn][b]['mean_F'] >= ladder[fn][a]['mean_F'] - 1e-9 and ladder[fn][b]['P_R_pos'] >= ladder[fn][a]['P_R_pos'] - 1e-9
           for fn in FILES for a, b in ((1, 2), (1, 3), (1, 4), (2, 4), (2, 6), (4, 8), (4, 12), (8, 16), (1, 8), (1, 16)))
rec("B2_clock_lift_ladder_on_observed_gaps_is_monotone", mono, ladder=ladder,
    note="multiplying gaps by h (same events, other unit) increases or preserves activation/history counts, as T1 requires; h=4 reproduces raw-unit universality")

# raw-unit artefact: raw gaps/4 are the integer units that make raw = 4*y
raw4 = {}
for fn in FILES:
    y = [int(r['raw_gap']) // 4 for r in inc[fn][:2000]]
    raw4[fn] = dict(P_R_pos_of_raw=float(np.mean([R_q(4 * v)[0] > 0 for v in y])), P_R_pos_of_raw_over_4=float(np.mean([R_q(v)[0] > 0 for v in y])))
rec("B3_raw_unit_artefact", all(v['P_R_pos_of_raw'] == 1.0 for v in raw4.values()), raw_units=raw4)

# channel-aware comparison: two-sample KS on F and depth between streams (exploratory)
from scipy.stats import ks_2samp
cmp = {}
for a, b in itertools.combinations(FILES, 2):
    Fa = [hist(int(r['inferred_counter_gap']))[0] for r in inc[a]]; Fb = [hist(int(r['inferred_counter_gap']))[0] for r in inc[b]]
    t = ks_2samp(Fa, Fb); cmp[a + ' / ' + b] = dict(D=float(t.statistic), p=float(t.pvalue))
rec("B4_between_stream_comparison_of_history_counts", True, ks=cmp, note="descriptive; streams differ in rate/setting, no channel timing used")


# B5: sensitivity of the multiplicity statistics to the control; pooled comparison
def pm(vals):
    me = np.array([merger_excess(d) for d in vals]); R = np.array([R_q(d)[0] for d in vals])
    return float(np.mean(me > 0)), float(np.mean(R >= 2))
sens = {}; ctrl_pm = []
for fn in FILES:
    h = np.array([int(r['inferred_counter_gap']) for r in inc[fn]], dtype=np.int64)
    o = pm([int(x) for x in h]); row = dict(observed=dict(P_merger=o[0], P_R_ge2=o[1], n=len(h)))
    for w in (0.01, 0.1, 0.3):
        pick = rng.choice(h, size=20000)
        lo = (pick * int(100 * (1 - w))) // 100; hi = (pick * int(100 * (1 + w))) // 100
        sur = [int(rng.integers(l, u + 1)) for l, u in zip(lo, hi)]
        c = pm(sur); row['jitter_%g' % w] = dict(P_merger=c[0], P_R_ge2=c[1]); ctrl_pm.append(c)
    mean_ = float(h.mean()); sur = [max(1, int(x)) for x in rng.exponential(mean_, size=20000)]
    c = pm(sur); row['exponential_same_mean'] = dict(P_merger=c[0], P_R_ge2=c[1]); ctrl_pm.append(c)
    sens[fn] = row
N_all = sum(sens[f]['observed']['n'] for f in FILES)
obs_m = sum(sens[f]['observed']['P_merger'] * sens[f]['observed']['n'] for f in FILES) / N_all
obs_r = sum(sens[f]['observed']['P_R_ge2'] * sens[f]['observed']['n'] for f in FILES) / N_all
ctrl_m = float(np.mean([c[0] for c in ctrl_pm])); ctrl_r = float(np.mean([c[1] for c in ctrl_pm]))
z_m = (obs_m - ctrl_m) / math.sqrt(ctrl_m * (1 - ctrl_m) / N_all); z_r = (obs_r - ctrl_r) / math.sqrt(ctrl_r * (1 - ctrl_r) / N_all)
rec("B5_multiplicity_statistics_across_controls_pooled", abs(z_m) < 4 and abs(z_r) < 4, per_stream=sens,
    pooled=dict(N=N_all, obs_P_merger=obs_m, ctrl_P_merger=ctrl_m, z_merger=z_m, obs_P_R_ge2=obs_r, ctrl_P_R_ge2=ctrl_r, z_R_ge2=z_r),
    note="the three streams lie at or slightly below nearly all controls in P(R>=2) and P(merger); pooled z about -1.7 and -1.8; exploratory, no multiplicity correction")

blob = json.dumps(results, sort_keys=True, default=str, indent=1)
open('qti_v001_results.json', 'w').write(blob)
print("sha256", hashlib.sha256(blob.encode()).hexdigest())
print("ALL PASS" if all(v['ok'] for v in results.values()) else "SOME FAIL")
