#!/usr/bin/env python3
"""QTI-I v003: channel-conditioned analysis (research release; Substrate unchanged; v001/v002 untouched).
Per data set (zip, folder, setting) with channels ps, iPsiM, iPsiP, i1, i2, s:
 E1 time-coordinate compatibility + channel-aware nulls (global shift, window-rotation, local-rate Poisson),
 E2 iPsiP diagnosis (wide lag search, rate-profile correlation, i1/i2 membership, overlap with iPsiM),
 E3 joint UNNS geometry on synchronized iPsiM-ps pairs (delay-lift histories, joint gap structure) with index-lag/jitter controls and a cubic grammar.
Reads raw zips in place.  Resumable (results/parts).  Usage: python3 qti_v003.py   (rerun until summary prints)
"""
import sys, json, hashlib, math, zipfile, time, csv
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import numpy as np
from sympy import factorint
HERE = Path(__file__).resolve().parent; RAW = HERE.parents[1] / 'data' / 'raw'; OUT = HERE.parent / 'results'; PARTS = OUT / 'parts'
PARTS.mkdir(parents=True, exist_ok=True); T0 = time.time(); BUDGET = 130
ZIPS = ['Short distance.zip', '1 km.zip']; TOL = 2e6; CH = ['ps', 'iPsiM', 'iPsiP', 'i1', 'i2', 's']

_fc = {}
def fac(n):
    r = _fc.get(n)
    if r is None: r = _fc[n] = factorint(n)
    return r
def sqdivs(d, pw=2):
    ps = [(p, e // pw) for p, e in fac(d).items() if e >= pw]; ms = [1]
    for p, e in ps: ms = [m * p ** k for m in ms for k in range(e + 1)]
    return sorted(m for m in ms if m > 1)
@lru_cache(maxsize=None)
def hist(d, pw=2):
    F = 1; depth = 0; anc = set()
    for m in sqdivs(d, pw):
        p = d * (m - 1) // m ** pw; Fp, dp, ap = hist(p, pw); F += Fp; depth = max(depth, dp + 1); anc.add(p); anc |= ap
    return F, depth, frozenset(anc)
def Rn(d, pw=2): return len(sqdivs(d, pw))

def mf(T, Xq, off, tol=TOL):
    q = Xq + off; i = np.searchsorted(T, q); a = T[np.clip(i, 0, len(T) - 1)]; b = T[np.clip(i - 1, 0, len(T) - 1)]
    return np.minimum(np.abs(a - q), np.abs(b - q)) <= tol
def offsets(X, T, W, nmax, rng):
    Xs = X if len(X) <= nmax else X[np.sort(rng.choice(len(X), nmax, replace=False))]
    lo = np.searchsorted(T, Xs - W); hi = np.searchsorted(T, Xs + W)
    parts = [T[a:b] - x for a, b, x in zip(lo, hi, Xs) if b > a]
    return np.concatenate(parts) if parts else np.zeros(0, np.int64), len(Xs)
def pair_test(X, T, rng, W=2e9, B=1e6, nmax=3000, nshift=200, nrot=25):
    d, ns = offsets(X, T, W, nmax, rng); out = dict(n_X=int(len(X)), n_T=int(len(T)), window=W)
    if len(d) == 0: out.update(n_pairs=0, significant=False, obs_frac=0.0); return out
    bins = np.round(d / B).astype(np.int64); u, c = np.unique(bins, return_counts=True); k = int(np.argmax(c))
    exp = len(d) / (2 * W / B); mode = float(np.median(d[bins == u[k]]))
    sig = bool(c[k] > 8 * exp + 8)
    out.update(n_pairs=int(len(d)), peak_offset=mode, peak_count=int(c[k]), peak_count_expected_per_bin=float(exp), significant=sig)
    obs = float(mf(T, X, mode).mean()); out['obs_frac'] = obs
    sh = []
    for _ in range(nshift):
        dl = rng.uniform(1e10, 2e12) * rng.choice([-1, 1]); sh.append(float(mf(T, X + dl, mode).mean()))
    out['shift_null_mean'] = float(np.mean(sh)); out['shift_null_max'] = float(np.max(sh))
    out['shift_p_ge_obs'] = float((1 + sum(1 for v in sh if v >= obs)) / (1 + nshift))
    # local-rate Poisson expectation (window +-5e12)
    q = X + mode; lo = np.searchsorted(T, q - 5e12); hi = np.searchsorted(T, q + 5e12); lam = (hi - lo) / 1e13
    p = 1 - np.exp(-2 * TOL * lam); out['poisson_expected_frac'] = float(p.mean()); out['poisson_z'] = float((obs * len(X) - p.sum()) / math.sqrt(max((p * (1 - p)).sum(), 1e-12)))
    if len(T) <= 3_000_000 and nrot:
        Wn = 5e13; t0 = T[0]; w = ((T - t0) // Wn).astype(np.int64); rv = []
        for _ in range(nrot):
            r = rng.integers(0, int(Wn), size=int(w.max()) + 1); T2 = np.sort(w * int(Wn) + ((T - t0 - w * int(Wn)) + r[w]) % int(Wn) + t0)
            rv.append(float(mf(T2, X, mode).mean()))
        out['rotation_null_mean'] = float(np.mean(rv)); out['rotation_null_max'] = float(np.max(rv))
    return out

def stat_pair(a, b):
    a = np.asarray(a, bool); b = np.asarray(b, bool)
    return dict(P_b_given_a=float(b[a].mean()) if a.any() else None, P_b_given_not_a=float(b[~a].mean()) if (~a).any() else None, P_a=float(a.mean()), P_b=float(b.mean()),
                phi=float(np.corrcoef(a, b)[0, 1]) if a.std() > 0 and b.std() > 0 else None)

def analyse(zn, folder, suf, mem, z):
    seed = int(hashlib.sha256((zn + folder + suf).encode()).hexdigest(), 16) % 2**32; rng = np.random.default_rng(seed)
    ch = {c: np.frombuffer(z.read(mem[c]), dtype='<u8').astype(np.int64) for c in CH}
    R = dict(zip=zn, dataset=folder, suffix=suf, members={c: mem[c] for c in CH}, events={c: int(len(x)) for c, x in ch.items()},
             span={c: [int(x[0]), int(x[-1])] for c, x in ch.items()}, rate_per_1e12={c: float(len(x) / ((x[-1] - x[0]) / 1e12)) for c, x in ch.items()})
    M, P, ps, i1, i2, s = ch['iPsiM'], ch['iPsiP'], ch['ps'], ch['i1'], ch['i2'], ch['s']
    # E1/E2 pair tests
    pt = {}
    for src in ('iPsiM', 'iPsiP'):
        for tgt in ('ps', 'i1', 'i2', 's'):
            pt[src + '->' + tgt] = pair_test(ch[src], ch[tgt], rng, nrot=(25 if tgt != 's' else 0))
    pt['iPsiM->iPsiP'] = pair_test(M, P, rng, W=2e9, nrot=0); pt['i1->i2'] = pair_test(i1, i2, rng, W=2e9, nrot=0)
    pt['iPsiP->ps_wide1e12'] = pair_test(P, ps, rng, W=1e12, nrot=0, nshift=100)
    pt['iPsiM->ps_wide1e12'] = pair_test(M, ps, rng, W=1e12, nrot=0, nshift=100)
    R['pair_tests'] = pt
    # rate-profile correlations (2e12 bins)
    t0 = min(x[0] for x in ch.values()); t1 = max(x[-1] for x in ch.values()); Bn = 2e12; nb = int((t1 - t0) / Bn) + 1
    H = {c: np.bincount(((x - t0) / Bn).astype(int), minlength=nb).astype(float) for c, x in ch.items()}; H['i12'] = H['i1'] + H['i2']
    def xc(a, b, lag):
        if lag > 0: a, b = a[lag:], b[:-lag]
        elif lag < 0: a, b = a[:lag], b[-lag:]
        return float(np.corrcoef(a, b)[0, 1])
    rp = {}
    for a, b in (('ps', 'iPsiM'), ('ps', 'iPsiP'), ('iPsiM', 'iPsiP'), ('i12', 'iPsiM'), ('i12', 'iPsiP'), ('s', 'iPsiM'), ('s', 'iPsiP'), ('ps', 'i12')):
        lags = [xc(H[a], H[b], l) for l in range(-40, 41) if l != 0]
        rp[a + '~' + b] = dict(lag0=xc(H[a], H[b], 0), max_abs_nonzero_lag=float(np.max(np.abs(lags))), noise_sd=float(1 / math.sqrt(nb)))
    R['rate_profile_corr'] = dict(bins=nb, bin=Bn, pairs=rp)
    # class matrix of iPsiM / iPsiP membership
    def flag(src, tgt):
        r = pt[src + '->' + tgt]
        return mf(ch[tgt], ch[src], r['peak_offset']) if r.get('significant') else np.zeros(len(ch[src]), bool)
    cls = {}
    for src in ('iPsiM', 'iPsiP'):
        f = {t: flag(src, t) for t in ('ps', 'i1', 'i2', 's')}; keys = defaultdict(int)
        for k in zip(f['i1'], f['i2'], f['ps']): keys['i1=%d,i2=%d,ps=%d' % tuple(map(int, k))] += 1
        cls[src] = dict(n=int(len(ch[src])), classes=dict(keys), frac_in_i1_or_i2=float(np.mean(f['i1'] | f['i2'])), frac_ps=float(f['ps'].mean()))
    R['membership'] = cls
    # ps coverage by iPsiM and vice versa
    pm = pt['iPsiM->ps']
    if pm.get('significant'):
        offm = pm['peak_offset']; covered = mf(M, ps, -offm)  # ps events that have an M event at -offset
        R['ps_events_with_iPsiM_partner'] = float(covered.mean()) if False else float(mf(M, ps, -offm).mean())
        # offset structure & joint geometry
        i = np.searchsorted(ps, M + offm); i = np.clip(i, 0, len(ps) - 1); j = np.clip(i - 1, 0, len(ps) - 1)
        near = np.where(np.abs(ps[i] - (M + offm)) <= np.abs(ps[j] - (M + offm)), i, j); ok = np.abs(ps[near] - (M + offm)) <= TOL
        ok &= np.r_[True, np.diff(near) > 0] if len(near) > 1 else ok
        Mj = M[ok]; psj = ps[near[ok]]; off = psj - Mj; R['n_synchronized_pairs'] = int(len(Mj))
        fi1 = flag('iPsiM', 'i1')[ok]; fi2 = flag('iPsiM', 'i2')[ok]
        u, c = np.unique(np.round(off / 1e5).astype(np.int64), return_counts=True); top = np.argsort(-c)[:4]
        clus = []
        for t in top:
            sel = np.round(off / 1e5).astype(np.int64) == u[t]
            clus.append(dict(offset_center=float(np.median(off[sel])), count=int(c[t]), frac_i1=float(fi1[sel].mean()), frac_i2=float(fi2[sel].mean()), offset_mod_20000=int(np.median(off[sel]) % 20000)))
        R['delay_clusters'] = clus
        # delay-lift histories vs integer baseline
        dl = {}
        for cl in clus[:3]:
            cval = int((2 * int(cl['offset_center']) + 312) // 625); row = dict(counter_delay=cval)
            base = [int(x) for x in rng.integers(max(2, cval // 2), 2 * cval, size=1500)]
            for pw in (2, 3):
                F = hist(cval, pw)[0]; bF = np.array([hist(b, pw)[0] for b in base]); bR = np.array([Rn(b, pw) for b in base])
                row['pw%d' % pw] = dict(R=Rn(cval, pw), F=F, depth=hist(cval, pw)[1], rank_R=float(np.mean(bR <= Rn(cval, pw))), rank_F=float(np.mean(bF <= F)))
            dl[str(int(cl['offset_center']))] = row
        R['delay_lift_histories'] = dl
        # joint gap structure on synchronized pairs
        kM = (2 * Mj + 312) // 625; kP = (2 * psj + 312) // 625; hM = np.diff(kM); hP = np.diff(kP); v = (hM > 0) & (hP > 0)
        med = float(np.median(hM[v])); v &= (hM <= 1000 * med) & (hP <= 1000 * med); hM, hP = hM[v], hP[v]
        n = len(hM); sub = np.sort(rng.choice(n, size=min(3000, n), replace=False)); hM, hP = hM[sub], hP[sub]
        jg = dict(n_pairs=int(len(hM)), frac_equal=float(np.mean(hM == hP)), median_abs_diff=float(np.median(np.abs(hM - hP))))
        for pw in (2, 3):
            a = np.array([Rn(int(x), pw) > 0 for x in hM]); b = np.array([Rn(int(x), pw) > 0 for x in hP])
            row = dict(observed=stat_pair(a, b)); lagc = []
            for L in (1, 2, 3, 5, 8):
                bl = np.roll(b, L); lagc.append(stat_pair(a, bl))
            pg = [x['P_b_given_a'] for x in lagc if x['P_b_given_a'] is not None]; ph = [x['phi'] for x in lagc if x['phi'] is not None]
            row['index_lag_controls'] = dict(P_b_given_a_mean=float(np.mean(pg)) if pg else None, phi_mean=float(np.mean(ph)) if ph else None, phi_max_abs=float(np.max(np.abs(ph))) if ph else None)
            jit = (hP * rng.uniform(0.9, 1.1, size=len(hP))).astype(np.int64).clip(1); bj = np.array([Rn(int(x), pw) > 0 for x in jit]); row['jitter_control'] = stat_pair(a, bj)
            jg['pw%d' % pw] = row
        R['joint_gap_structure'] = jg
    return R

for zn in ZIPS:
    z = zipfile.ZipFile(RAW / zn); G = defaultdict(dict)
    for info in z.infolist():
        if not info.filename.endswith('.pt'): continue
        folder, fn = info.filename.split('/'); ch, suf = fn[:-3].split('_', 1); G[(folder, suf)][ch] = info.filename
    for (folder, suf), mem in sorted(G.items()):
        # unify suffix: strip leading dataset tag differences (e.g. 110_156p45_tot vs 156p45_tot)
        pf = PARTS / ((zn.replace(' ', '_') + '__' + folder + '__' + suf) + '.json')
        if pf.exists(): continue
        if set(mem) != set(CH): print('SKIP incomplete', zn, folder, suf, sorted(mem)); continue
        if time.time() - T0 > BUDGET: print('BUDGET: rerun to continue', flush=True); sys.exit(2)
        r = analyse(zn, folder, suf, mem, z); pf.write_text(json.dumps(r, default=str)); print('done', zn, folder, suf, round(time.time() - T0), flush=True)
        _fc.clear(); hist.cache_clear()
print('ALL PARTS DONE')
