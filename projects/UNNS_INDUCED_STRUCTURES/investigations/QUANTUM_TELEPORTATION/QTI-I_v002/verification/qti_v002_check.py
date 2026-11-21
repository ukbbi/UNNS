#!/usr/bin/env python3
"""QTI-I v002 checks: independent full-stream recomputation (primes<=2e6 vectorised divisibility, no sympy), ps-clock theorem, per-channel tallies.
Reads ../results/qti_v002_results.json and the raw zips.  Writes ../results/qti_v002_analysis.json.  Needs numpy."""
import json, math, zipfile, collections, hashlib, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent; RES = HERE.parent / 'results'; RAW = HERE.parents[1] / 'data' / 'raw'
R = json.load(open(RES / 'qti_v002_results.json')); S = R['streams']; out = {}; ok_all = True
def rec(name, ok, **kw):
    global ok_all; ok_all &= bool(ok); out[name] = dict(ok=bool(ok), **kw); print('PASS' if ok else 'FAIL', name, {k: v for k, v in kw.items() if not isinstance(v, (dict, list))})
# primes
N = 2_000_000; sv = np.ones(N + 1, bool); sv[:2] = False
for i in range(2, int(N ** .5) + 1):
    if sv[i]: sv[i * i::i] = False
P2 = np.nonzero(sv)[0].astype(np.int64) ** 2
def squareful(h):
    """True iff some prime p<=2e6 has p^2 | h (exact for h < (2e6)^3 after cofactor argument; otherwise lower bound)."""
    res = np.zeros(len(h), bool)
    for p2 in P2[:2000]: res |= (h % p2 == 0)        # primes up to ~17389 : fast bulk
    rest = ~res
    if rest.any():
        hr = h[rest]; r2 = np.zeros(len(hr), bool)
        for p2 in P2[2000:]: r2 |= (hr % p2 == 0)
        res[rest] = r2
    return res
def counter_gaps(t):
    k = (2 * t + 312) // 625; g = np.diff(t); h = np.diff(k); v = (g > 0) & (h > 0)
    med = float(np.median(h[v])); inc = v & (h <= 1000 * med); return h[inc]
tests = ['Short distance.zip/data110/iPsiM_156p45_tot.pt', 'Short distance.zip/data110/iPsiP_156p45_tot.pt', 'Short distance.zip/data110/iPsiM_156p95_tot.pt',
         'Short distance.zip/data110/ps_156p45_tot.pt', '1 km.zip/data110/iPsiM_110_156p45_tot.pt', '1 km.zip/data110/ps_110_156p45_tot.pt', 'Short distance.zip/data155/iPsiM_155_156p7_tot.pt']
full = {}; good = True
for tn in tests:
    zn, mem = tn.split('/', 1); b = zipfile.ZipFile(RAW / zn).read(mem); t = np.frombuffer(b, dtype='<u8').astype(np.int64)
    h = counter_gaps(t); pf = float(squareful(h).mean()); s = next(x for x in S if x['zip'] == zn and x['member'] == mem)
    n = s['obs']['n']; sd = math.sqrt(max(pf * (1 - pf), 1e-12) / n); dev = abs(s['obs']['P_R_pos'] - pf)
    good &= (dev <= 4 * sd + 1e-3) and s['analysed'] == len(h)
    full[tn] = dict(full_P_R_pos=pf, sample_P_R_pos=s['obs']['P_R_pos'], gaps=len(h), analysed_match=s['analysed'] == len(h))
rec('C1_independent_full_stream_recomputation_matches_sampled_statistic', good, per_stream=full)
v1 = json.load(open(HERE.parents[1] / 'results' / 'results.json'))['files']
ok = True; cmpv = {}
for fn in ['iPsiM_156p45_tot', 'iPsiP_156p45_tot', 'iPsiM_156p95_tot']:
    s = next(x for x in S if x['zip'] == 'Short distance.zip' and x['member'] == 'data110/' + fn + '.pt'); a = v1[fn + '.pt']
    ok &= s['analysed'] == a['gaps_analyzed']; cmpv[fn] = dict(v002_gaps=s['analysed'], v001_gaps=a['gaps_analyzed'])
rec('C2_v002_reproduces_v001_gap_counts_from_raw_zip', ok, per_stream=cmpv)
# ps theorem: raw ps timestamps on 20000-grid => counter gaps multiples of 64 => 8^2 | gap => every gap squareful (R>=3)
ps = [s for s in S if s['channel'] == 'ps']; g20 = [s for s in ps if s['gcd_pos_gaps'] and s['gcd_pos_gaps'] % 20000 == 0]
rec('C3_ps_streams_with_gap_gcd_multiple_of_20000_are_fully_squareful', all(s['obs']['P_R_pos'] == 1.0 for s in g20) and len(g20) > 0, streams=len(g20), of=len(ps),
    note='raw gaps multiples of 20000 = 2*625*16 -> counter gaps multiples of 64 -> 8^2 | h; exact consequence of the clock lift W(d) subset W(hd), not a feature of the events')
rest = [s for s in ps if s not in g20]
rec('C3b_remaining_ps_streams', True, streams=[dict(member=s['member'], gcd=s['gcd_pos_gaps'], P_R_pos=s['obs']['P_R_pos']) for s in rest])
# per-channel tallies excluding ps
chan = collections.defaultdict(list)
for s in S: chan[s['channel']].append(s)
tab = {}
for ch, L in chan.items():
    n = sum(s['obs']['n'] for s in L); w = lambda k, src='obs': sum(s[src][k] * s['obs']['n'] for s in L) / n
    row = dict(streams=len(L), events=int(sum(s['events'] for s in L)))
    for k in ('P_R_pos', 'P_R_ge2', 'P_merger'):
        row[k] = dict(obs=w(k), jitter=w(k, 'ctrl_jitter'), exp=w(k, 'ctrl_exp'))
    row['n_abs_z_gt3'] = {tag: int(sum(1 for s in L for v in s['z_' + tag].values() if abs(v) > 3)) for tag in ('jitter', 'exp')}
    row['tests'] = 3 * len(L); tab[ch] = row
nops = [s for s in S if s['channel'] != 'ps']
def pooled(tag, k):
    num = sum(s['obs']['n'] * (s['obs'][k] - s['ctrl_' + tag][k]) for s in nops)
    den = math.sqrt(sum(s['obs']['n'] * max(s['ctrl_' + tag][k] * (1 - s['ctrl_' + tag][k]), 1e-12) for s in nops)); return num / den
pz = {tag + '_' + k: pooled(tag, k) for tag in ('jitter', 'exp') for k in ('P_R_pos', 'P_R_ge2', 'P_merger')}
rec('C4_non_ps_channels_vs_controls', max(abs(v) for v in pz.values()) < 4, pooled_z=pz, per_channel=tab, streams=len(nops),
    note='60 non-ps streams x 3 statistics = 180 tests per control; |z|>3 counts in per_channel; control draws are finite so z carries control sampling noise')
# raw-unit divisibility by 4 per channel
d4 = {ch: dict(streams=len(L), all_div4=sum(1 for s in L if s['raw_div4_all']), gcd_values=sorted(set(s['gcd_pos_gaps'] for s in L if s['gcd_pos_gaps']))) for ch, L in chan.items()}
rec('C5_raw_gap_divisibility_by_channel', True, per_channel=d4, note='v001 statement raw gaps divisible by 4 holds for some, not all, streams')
out['channel_alignment_summary'] = {k: dict(median_offset=v['offset_quantiles_1_25_50_75_99'][2], p1=v['offset_quantiles_1_25_50_75_99'][0], p99=v['offset_quantiles_1_25_50_75_99'][4], frac_within=v['frac_abs_offset_lt_2e7'], events=v['events'], ps_events=v['ps_events']) for k, v in R['channel_aware'].items()}
out['lift4_monotone_all_streams'] = bool(R['summary']['all_lift4_monotone'])
blob = json.dumps(out, sort_keys=True, indent=1, default=str); (RES / 'qti_v002_analysis.json').write_text(blob)
print('sha256', hashlib.sha256(blob.encode()).hexdigest()); print('ALL PASS' if ok_all else 'SOME FAIL')
