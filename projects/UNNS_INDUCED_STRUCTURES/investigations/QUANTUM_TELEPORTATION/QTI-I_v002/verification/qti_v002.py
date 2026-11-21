#!/usr/bin/env python3
"""QTI-I v002: QTI-I/A induced-structure analysis on ALL raw channels of both Zenodo zips (research, not manuscript).
Input : data/raw/'Short distance.zip' and '1 km.zip' (read in place; nothing extracted, nothing modified).
Output: results/qti_v002_results.json, results/qti_v002_streams.csv.  Deterministic (SEED).  Needs numpy, sympy.
Declared correspondence phi (unchanged from v001): event times t -> counter k=floor((2t+312)/625); gap h=k_{i+1}-k_i>0,
giant gaps (>1000*median) excluded; induced object = UNNS history structure of h (F, depth, mergers, R).
Usage: python3 qti_v002.py [raw_dir] [out_dir]
"""
import sys, io, csv, json, hashlib, math, zipfile, random
from functools import lru_cache
from pathlib import Path
import numpy as np
from sympy import factorint

RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / 'data' / 'raw'
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parents[1] / 'results'
ZIPS = ['Short distance.zip', '1 km.zip']
SEED = 20261121; NS = 4000; NC = 4000
rng = np.random.default_rng(SEED)

_fc = {}
def fac(n):
    r = _fc.get(n)
    if r is None: r = _fc[n] = factorint(n)
    return r
def sqdivs(d):
    ps = [(p, e // 2) for p, e in fac(d).items() if e >= 2]
    ms = [1]
    for p, e in ps: ms = [m * p ** k for m in ms for k in range(e + 1)]
    return sorted(m for m in ms if m > 1)
def R_of(d):
    R = 1
    for p, e in fac(d).items(): R *= e // 2 + 1
    return R - 1
@lru_cache(maxsize=None)
def hist(d):
    F = 1; depth = 0; anc = set()
    for m in sqdivs(d):
        p = d * (m - 1) // (m * m); Fp, dp, ap = hist(p)
        F += Fp; depth = max(depth, dp + 1); anc.add(p); anc |= ap
    return F, depth, frozenset(anc)
def stat_vec(vals):
    R = np.array([R_of(v) for v in vals]); H = [hist(v) for v in vals]
    F = np.array([h[0] for h in H]); D = np.array([h[1] for h in H]); A = np.array([len(h[2]) for h in H])
    return dict(P_R_pos=float(np.mean(R > 0)), P_R_ge2=float(np.mean(R >= 2)), P_merger=float(np.mean((F - 1 - A) > 0)),
                mean_logF=float(np.mean(np.log(F))), mean_depth=float(np.mean(D)), n=len(vals))
def zprop(o, c, n):
    s = math.sqrt(max(c * (1 - c), 1e-12) / n); return (o - c) / s

import time, os
T0 = time.time(); BUDGET = 150
PARTS = OUT / 'parts'; PARTS.mkdir(parents=True, exist_ok=True)
streams = []
for zname in ZIPS:
    z = zipfile.ZipFile(RAW / zname)
    for info in sorted(z.infolist(), key=lambda i: i.filename):
        if not info.filename.endswith('.pt'): continue
        pf = PARTS / (zname.replace(' ', '_') + '__' + info.filename.replace('/', '__') + '.json')
        if pf.exists(): streams.append(json.loads(pf.read_text())); continue
        if time.time() - T0 > BUDGET: print('BUDGET: rerun to continue', flush=True); sys.exit(2)
        rng = np.random.default_rng(int(hashlib.sha256((zname + info.filename).encode()).hexdigest(), 16) % 2**32)
        b = z.read(info); t = np.frombuffer(b, dtype='<u8').astype(np.int64)
        folder, fn = info.filename.split('/'); stem = fn[:-3]; chan = stem.split('_')[0]
        rec = dict(zip=zname, member=info.filename, channel=chan, dataset=folder, bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), events=int(len(t)))
        g = np.diff(t); rec['neg_gaps'] = int((g < 0).sum()); rec['zero_gaps'] = int((g == 0).sum())
        pg = g[g > 0]; rec['gcd_pos_gaps'] = int(np.gcd.reduce(pg)) if len(pg) else None
        k = (2 * t + 312) // 625; err = np.abs(2 * t - 625 * k) / 2.0
        rec['grid_max_roundoff'] = float(err.max()); rec['grid_frac_within5'] = float(np.mean(err <= 5))
        h = np.diff(k); valid = (g > 0) & (h > 0)
        if valid.sum() < 50: rec['analysed'] = 0; pf.write_text(json.dumps(rec, default=str)); streams.append(rec); continue
        med = float(np.median(h[valid])); inc = valid & (h <= 1000 * med); hh = h[inc]
        rec.update(analysed=int(len(hh)), median_counter_gap=med, mean_counter_gap=float(hh.mean()), max_counter_gap=int(hh.max()))
        take = hh[rng.choice(len(hh), size=min(NS, len(hh)), replace=False)] if len(hh) > NS else hh
        o = stat_vec([int(x) for x in take]); rec['obs'] = o
        # magnitude-matched integer control (+-10%) and exponential same-mean control, pool size NC each
        pick = rng.choice(hh, size=NC); lo = (pick * 9) // 10; hi = (pick * 11) // 10
        sj = [int(rng.integers(l, u + 1)) for l, u in zip(lo, hi)]
        se = [max(1, int(x)) for x in rng.exponential(float(hh.mean()), size=NC)]
        cj = stat_vec(sj); ce = stat_vec(se); rec['ctrl_jitter'] = cj; rec['ctrl_exp'] = ce
        n = o['n']
        for tag, c in (('jitter', cj), ('exp', ce)):
            rec['z_' + tag] = {k2: zprop(o[k2], c[k2], n) for k2 in ('P_R_pos', 'P_R_ge2', 'P_merger')}
        # clock-lift check on this stream's sample (T1 in v001): F must be nondecreasing under d -> 4d
        sub = [int(x) for x in take[:300]]
        rec['lift4_monotone'] = bool(all(hist(4 * v)[0] >= hist(v)[0] for v in sub))
        rec['raw_div4_all'] = bool(np.all(pg % 4 == 0))
        pf.write_text(json.dumps(rec, default=str)); streams.append(rec)
        print(zname, info.filename, rec['events'], rec['analysed'], round(o['P_R_pos'], 3), flush=True)
        _fc.clear(); hist.cache_clear()

# channel-aware: nearest ps event for each iPsi event of the same data set (descriptive, uses the timestamps only)
chan_aware = {}
for zname in ZIPS:
    z = zipfile.ZipFile(RAW / zname)
    for info in z.infolist():
        folder, fn = info.filename.split('/'); stem = fn[:-3]
        if not stem.startswith('iPsi'): continue
        key = (zname, folder, stem.split('_', 1)[1])
        pn = folder + '/ps_' + stem.split('_', 1)[1] + '.pt'
        if pn not in z.namelist(): continue
        t = np.frombuffer(z.read(info), dtype='<u8').astype(np.int64); ps = np.frombuffer(z.read(pn), dtype='<u8').astype(np.int64)
        i = np.searchsorted(ps, t); i0 = np.clip(i - 1, 0, len(ps) - 1); i1 = np.clip(i, 0, len(ps) - 1)
        off = np.where(np.abs(ps[i0] - t) <= np.abs(ps[i1] - t), ps[i0] - t, ps[i1] - t)
        q = np.percentile(off, [1, 25, 50, 75, 99]).tolist()
        chan_aware[zname + '/' + info.filename] = dict(events=int(len(t)), ps_events=int(len(ps)), offset_quantiles_1_25_50_75_99=q,
                                                       frac_abs_offset_lt_2e7=float(np.mean(np.abs(off) < 2e7)))
an = [s for s in streams if s.get('analysed', 0) >= 50]
def pooled(tag, k2):
    num = sum(s['obs']['n'] * (s['obs'][k2] - s['ctrl_' + tag][k2]) for s in an)
    den = math.sqrt(sum(s['obs']['n'] * max(s['ctrl_' + tag][k2] * (1 - s['ctrl_' + tag][k2]), 1e-12) for s in an))
    return num / den
summary = dict(streams_total=len(streams), streams_analysed=len(an), events_total=int(sum(s['events'] for s in streams)),
               all_raw_gaps_div4=bool(all(s.get('raw_div4_all', True) for s in an)), all_lift4_monotone=bool(all(s['lift4_monotone'] for s in an)),
               grid_fit_streams=int(sum(1 for s in an if s['grid_max_roundoff'] <= 5)),
               pooled_z={tag + '_' + k2: pooled(tag, k2) for tag in ('jitter', 'exp') for k2 in ('P_R_pos', 'P_R_ge2', 'P_merger')},
               n_streams_abs_z_gt3={tag: int(sum(1 for s in an for v in s['z_' + tag].values() if abs(v) > 3)) for tag in ('jitter', 'exp')})
res = dict(seed=SEED, sample_per_stream=NS, control_pool=NC, summary=summary, streams=streams, channel_aware=chan_aware)
blob = json.dumps(res, sort_keys=True, indent=1, default=str)
OUT.mkdir(parents=True, exist_ok=True); (OUT / 'qti_v002_results.json').write_text(blob)
with open(OUT / 'qti_v002_streams.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['zip', 'dataset', 'channel', 'member', 'events', 'analysed', 'grid_max_roundoff', 'grid_frac_within5', 'mean_counter_gap', 'P_R_pos', 'P_R_ge2', 'P_merger', 'ctrlJ_P_R_pos', 'ctrlJ_P_R_ge2', 'ctrlJ_P_merger', 'ctrlE_P_R_pos', 'ctrlE_P_R_ge2', 'ctrlE_P_merger', 'sha256'])
    for s in streams:
        o = s.get('obs'); cj = s.get('ctrl_jitter'); ce = s.get('ctrl_exp')
        w.writerow([s['zip'], s['dataset'], s['channel'], s['member'], s['events'], s.get('analysed', 0), s['grid_max_roundoff'], round(s['grid_frac_within5'], 4), s.get('mean_counter_gap', ''),
                    *( [round(o[k2], 4) for k2 in ('P_R_pos', 'P_R_ge2', 'P_merger')] if o else ['', '', ''] ),
                    *( [round(cj[k2], 4) for k2 in ('P_R_pos', 'P_R_ge2', 'P_merger')] if cj else ['', '', ''] ),
                    *( [round(ce[k2], 4) for k2 in ('P_R_pos', 'P_R_ge2', 'P_merger')] if ce else ['', '', ''] ), s['sha256']])
print(json.dumps(summary, indent=1)); print('sha256', hashlib.sha256(blob.encode()).hexdigest())
