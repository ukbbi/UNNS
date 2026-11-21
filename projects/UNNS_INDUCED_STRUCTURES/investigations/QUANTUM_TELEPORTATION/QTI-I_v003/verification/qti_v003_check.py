#!/usr/bin/env python3
"""QTI-I v003 structure checks (exact timestamp relations) + aggregation of results/parts/*.json.  Needs numpy.
Writes ../results/qti_v003_analysis.json; prints PASS/FAIL per check."""
import json, glob, zipfile, hashlib, sys, math, time
from collections import defaultdict
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'results'; RAW = HERE.parents[1] / 'data' / 'raw'
CACHE = RES / 'structure_cache.json'; W = 6e5; T0 = time.time(); BUDGET = 130
out = {}; ok_all = True
def rec(name, ok, **kw):
    global ok_all; ok_all &= bool(ok); out[name] = dict(ok=bool(ok), **kw); print('PASS' if ok else 'FAIL', name, {k: v for k, v in kw.items() if not isinstance(v, (dict, list))})
def load(z, m): return np.frombuffer(z.read(m), dtype='<u8').astype(np.int64)
def near(T, X, excl_self=False):
    i = np.searchsorted(T, X); a = T[np.clip(i - 1, 0, len(T) - 1)]
    b = T[np.clip(i + (1 if excl_self else 0), 0, len(T) - 1)]; return np.minimum(np.abs(X - a), np.abs(b - X))
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
for zn in ['Short distance.zip', '1 km.zip']:
    z = zipfile.ZipFile(RAW / zn); G = defaultdict(dict)
    for info in z.infolist():
        if info.filename.endswith('.pt'):
            f, fn = info.filename.split('/'); c, s = fn[:-3].split('_', 1); G[(f, s)][c] = info.filename
    for (f, s), mem in sorted(G.items()):
        key = zn + '|' + f + '|' + s
        if key in cache: continue
        if time.time() - T0 > BUDGET: print('BUDGET: rerun'); CACHE.write_text(json.dumps(cache)); sys.exit(2)
        ch = {c: load(z, mem[c]) for c in ('ps', 'iPsiM', 'iPsiP', 'i1', 'i2')}; M, P, ps, i1, i2 = ch['iPsiM'], ch['iPsiP'], ch['ps'], ch['i1'], ch['i2']
        r = {}
        r['M_exact_in_i1_or_i2'] = float(np.mean(np.isin(M, i1) | np.isin(M, i2))); r['P_exact_in_i1_or_i2'] = float(np.mean(np.isin(P, i1) | np.isin(P, i2)))
        r['M_in_i1_exact'] = float(np.mean(np.isin(M, i1))); r['M_in_i2_exact'] = float(np.mean(np.isin(M, i2)))
        r['M_other_detector_partner_within'] = float(np.mean((near(i1, M) <= W) & (near(i2, M) <= W)))
        P1 = P[np.isin(P, i1)]; P2 = P[np.isin(P, i2)]
        r['P_same_detector_partner_within'] = float(np.mean(np.r_[near(i1, P1, True) <= W, near(i2, P2, True) <= W]))
        r['P_other_detector_partner_within'] = float(np.mean(np.r_[near(i2, P1) <= W, near(i1, P2) <= W]))
        rs = np.random.default_rng(7); R1 = i1[rs.choice(len(i1), 5000, replace=False)]
        r['baseline_i1_i2_pair_within'] = float(np.mean(near(i2, R1) <= W)); r['baseline_i1_same_detector_pair_within'] = float(np.mean(near(i1, R1, True) <= W))
        r['M_in_P_exact'] = float(np.mean(np.isin(M, P))); r['n'] = dict(M=int(len(M)), P=int(len(P)), ps=int(len(ps)))
        r['ps_mod_20000_unique'] = int(len(np.unique(ps % 20000)))
        # ps trials without an M partner: what lies 7e6..1.2e7 earlier?
        lo = np.searchsorted(M, ps - 1.25e7); hi = np.searchsorted(M, ps - 7e6); hasM = (hi - lo) > 0
        um = ps[~hasM]; r['ps_without_M_partner'] = int(len(um)); r['ps_without_M_fraction'] = float(len(um) / len(ps))
        cnt = {}
        for nm, T in (('i1', i1), ('i2', i2), ('P', P)):
            lo = np.searchsorted(T, um - 1.25e7); hi = np.searchsorted(T, um - 7e6); cnt[nm] = float(np.mean((hi - lo) > 0)) if len(um) else None
        r['ps_without_M_window_has'] = cnt
        # chance level for that window: rate*5.5e6
        r['chance_window_i1'] = float(len(i1) / ((i1[-1] - i1[0]) / 5.5e6))
        cache[key] = r; print('done', key, round(time.time() - T0), flush=True)
CACHE.write_text(json.dumps(cache))
C = cache; keys = sorted(C)
rec('S1_time_base_exact_timestamp_identity', all(C[k]['M_exact_in_i1_or_i2'] == 1.0 and C[k]['P_exact_in_i1_or_i2'] == 1.0 for k in keys), datasets=len(keys),
    note='every iPsiM and iPsiP timestamp equals an i1 or i2 timestamp exactly (offset 0): the channels share one time coordinate')
rec('S2_iPsiM_is_two_detector_pair', all(C[k]['M_other_detector_partner_within'] == 1.0 for k in keys),
    min_frac=min(C[k]['M_other_detector_partner_within'] for k in keys), baseline_max=max(C[k]['baseline_i1_i2_pair_within'] for k in keys), window=W)
rec('S3_iPsiP_is_same_detector_pair', all(C[k]['P_same_detector_partner_within'] == 1.0 for k in keys),
    min_frac=min(C[k]['P_same_detector_partner_within'] for k in keys), other_detector_max=max(C[k]['P_other_detector_partner_within'] for k in keys), baseline_max=max(C[k]['baseline_i1_same_detector_pair_within'] for k in keys))
rec('S4_iPsiM_iPsiP_nearly_disjoint', max(C[k]['M_in_P_exact'] for k in keys) < 0.01, max_overlap=max(C[k]['M_in_P_exact'] for k in keys))
rec('S5_ps_timestamps_on_few_20000_grid_phases', all(C[k]['ps_mod_20000_unique'] <= 4 for k in keys), phases_per_dataset={k: C[k]['ps_mod_20000_unique'] for k in keys}, note='ps timestamps take 1-4 distinct residues mod 20000 per data set (6 of 12 data sets have one); more than one phase is not explained here')
rec('S6_ps_trials_without_iPsiM_partner', True, fractions={k: round(C[k]['ps_without_M_fraction'], 3) for k in keys}, window_has_events={k: C[k]['ps_without_M_window_has'] for k in keys},
    note='descriptive: 11-36% of ps have no iPsiM partner; in 11 of 12 data sets >=97% of those have i1 and i2 events in the delay window (chance ~1e-3), in 1 km dataL only 36%; what they are is open')
# aggregate parts
P = [json.load(open(f)) for f in sorted(glob.glob(str(RES / 'parts' / '*.json')))]
rec('N0_all_12_datasets', len(P) == 12 and len(keys) == 12, parts=len(P))
def g(r, k, f): return r['pair_tests'][k][f]
rec('N1_iPsiM_ps_survives_channel_aware_nulls', all(g(r, 'iPsiM->ps', 'obs_frac') > 0.99 and g(r, 'iPsiM->ps', 'obs_frac') > 100 * max(g(r, 'iPsiM->ps', 'shift_null_max'), g(r, 'iPsiM->ps', 'rotation_null_max'), 1e-5) and g(r, 'iPsiM->ps', 'poisson_z') > 100 for r in P),
    obs_min=min(g(r, 'iPsiM->ps', 'obs_frac') for r in P), shift_null_max=max(g(r, 'iPsiM->ps', 'shift_null_max') for r in P), rotation_null_max=max(g(r, 'iPsiM->ps', 'rotation_null_max') for r in P),
    poisson_z_min=min(g(r, 'iPsiM->ps', 'poisson_z') for r in P), shift_p_resolution=1 / 201, note='null draws 200 shifts / 25 window rotations; p<=0.005 is the resolution limit')
rec('N2_iPsiP_ps_not_associated', all(g(r, 'iPsiP->ps', 'obs_frac') < 0.01 for r in P), obs_max=max(g(r, 'iPsiP->ps', 'obs_frac') for r in P), wide_lag_1e12_peak_max=max(g(r, 'iPsiP->ps_wide1e12', 'peak_count') for r in P),
    note='within +-1e12 (1e6 bins) the only iPsiP-ps peak lies at the iPsiM delay with 4-18 events (<=0.5% of iPsiP), consistent with the 0.1-0.7% iPsiM/iPsiP overlap; no other lag shows a peak')
rc = lambda a, b: [r['rate_profile_corr']['pairs'][a + '~' + b]['lag0'] for r in P]
rec('N3_rate_profile_correlations', True, ps_M=[round(min(rc('ps', 'iPsiM')), 2), round(max(rc('ps', 'iPsiM')), 2)], ps_P=[round(min(rc('ps', 'iPsiP')), 2), round(max(rc('ps', 'iPsiP')), 2)],
    M_P=[round(min(rc('iPsiM', 'iPsiP')), 2), round(max(rc('iPsiM', 'iPsiP')), 2)], i12_M=[round(min(rc('i12', 'iPsiM')), 2), round(max(rc('i12', 'iPsiM')), 2)], i12_P=[round(min(rc('i12', 'iPsiP')), 2), round(max(rc('i12', 'iPsiP')), 2)])
# joint UNNS geometry
rk = [v['pw2']['rank_F'] for r in P for v in r['delay_lift_histories'].values()]; rk3 = [v['pw3']['rank_F'] for r in P for v in r['delay_lift_histories'].values()]
rec('J1_delay_lift_histories_within_integer_baseline', max(rk) < 0.99 and max(rk3) < 0.99, n_delays=len(rk), max_rank_F_pw2=max(rk), max_rank_F_pw3=max(rk3), n_rank_ge_095_pw2=int(sum(x >= 0.95 for x in rk)), n_rank_ge_095_pw3=int(sum(x >= 0.95 for x in rk3)),
    note='rank of F(counter delay) among 1500 integers in [c/2,2c]; no delay is extreme; 36 delays x 2 grammars, exploratory')
bsat = [r['joint_gap_structure']['pw2']['observed']['P_b'] for r in P]; pa = [r['joint_gap_structure']['pw2']['observed']['P_a'] for r in P]
rec('J2_joint_gap_structure_degenerate_ps_saturated', min(bsat) > 0.99, ps_P_R_pos_range=[min(bsat), max(bsat)], iPsiM_P_R_pos_range=[min(pa), max(pa)], phi_values=[r['joint_gap_structure']['pw2']['observed']['phi'] for r in P],
    note='ps gaps are squareful (clock grid) in all data sets, so the conditional P(R_ps>0 | R_M>0) carries no information; cubic grammar likewise saturated/zero')
eq = [r['joint_gap_structure']['frac_equal'] for r in P]
rec('J3_synchronized_gaps_nearly_equal_not_nested', max(eq) < 0.01, frac_equal_max=max(eq), median_abs_diff_range=[min(r['joint_gap_structure']['median_abs_diff'] for r in P), max(r['joint_gap_structure']['median_abs_diff'] for r in P)],
    note='counter gaps of iPsiM and of the matched ps differ by ~150-225 ticks (delay jitter); ratio ~1, so no T_N relation (ratio>=4) links the two channels')
blob = json.dumps(out, sort_keys=True, indent=1, default=str); (RES / 'qti_v003_analysis.json').write_text(blob)
print('sha256', hashlib.sha256(blob.encode()).hexdigest()); print('ALL PASS' if ok_all else 'SOME FAIL')
