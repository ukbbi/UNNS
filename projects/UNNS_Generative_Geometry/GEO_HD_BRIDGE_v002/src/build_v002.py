"""Builder: computes every recorded result of GEO_HD_BRIDGE_v002 and writes results/*.json.  python build_v002.py [section ...]
Sections: geom, rewrite, forcing, field, events, family, high, beyond, all.  (The independent verifier is verify_bridge.py.)"""
import _paths  # noqa
import json, os, sys, time, random, hashlib
from fractions import Fraction as Fr
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, 'results')
from geo_snapshots import closed_form, state_record, qvec, persists
from geometric_history import (states, step, edge_transport, gain_loss, predicted_loss_steps, arrangements, benchmark_B3, avoids_square, feasible, both_active, ambient_profile)
from rewrite_geometry import content_G, content_H, multiplier, loss_vector_diff, check_rewrite_law, forced_square
import field_regimes as FR
import event_correspondence as EC
import higher_dimensional as HD
import carry_analysis as CA
from geo1lib import factor, divisors_from


def dump(name, obj):
    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, name), 'w') as f:
        json.dump(obj, f, indent=1, sort_keys=True, default=str)


def sec_geom():
    t0 = time.time(); rng = random.Random(20261101)
    ms = [2 ** a * 3 ** b * 5 ** c * 7 ** d for a in range(0, 9) for b in range(0, 7) for c in range(0, 4) for d in range(0, 3)]
    ms = [m for m in ms if m < 10 ** 9 and closed_form(m)]
    rng.shuffle(ms); bad = []; n = 0
    for m in ms[:260]:
        r = state_record(m); cf = r['closed']; fr = r['frozen']
        ok = (fr['d_aff'] == cf['d_aff'] and fr['q'] == cf['q'] and fr['R'] == cf['nF'] and sum(fr['axis_cells']) == cf['ncells']
              and fr['axis_cells'] == fr['move_cells'] and fr['components'] == 1 and fr['betti_gf2'][0] == 1 and not any(fr['betti_gf2'][1:]) and fr['d2_zero'])
        n += 1
        if not ok: bad.append(m)
    # edge transport law on all (m, N) for m <= 3000
    et_bad = []; cnt = 0
    for m in range(1, 3001):
        for N in sorted(divisors_from(factor(m))):
            mp = step(m, N); a, b = qvec(m), qvec(mp)
            dq = edge_transport(m, N)
            for p, d in dq.items():
                if b.get(p, 0) - a.get(p, 0) != d: et_bad.append((m, N, p))
            cnt += 1
    b3 = benchmark_B3()
    dump('GEOMETRY_STATES.json', {'closed_form_vs_frozen_checked': n, 'violations': bad, 'edge_transport_edges_checked': cnt, 'edge_transport_violations': et_bad[:10],
                                  'B3': {k: {'states': v['states'], 'q': [r['closed']['q'] for r in v['records']], 'primes': [r['closed']['primes'] for r in v['records']],
                                             'betti': [r['frozen']['betti_gf2'] for r in v['records']], 'f_cells': [r['frozen']['move_cells'] for r in v['records']],
                                             'G': v['gain_loss']['G'], 'Lambda': v['gain_loss']['Lambda'], 'net': v['gain_loss']['net']} for k, v in b3.items()}})
    return 'geom %.1fs' % (time.time() - t0)


def sec_rewrite():
    t0 = time.time(); rows = []
    pairs = [((2, 2, 2, 2), (1, 8, 8)), ((2, 2, 3, 3, 3, 3), (1,) * 7), ((2, 2, 2, 2, 3), (1, 8, 8, 3)), ((2, 2, 2, 2, 3, 3), (1, 8, 8, 3, 3))]
    for u, v in pairs:
        if multiplier(u) != multiplier(v):
            u2 = u
        res = []
        for e2 in range(0, 8):
            for e3 in range(0, 5):
                m = 2 ** e2 * 3 ** e3
                r = check_rewrite_law(m, u, v)
                if r is not None: res.append((e2, e3, r['ok']))
        rows.append({'u': list(u), 'v': list(v), 'multiplier_equal': multiplier(u) == multiplier(v), 'pred_Lambda_diff': loss_vector_diff(u, v) if multiplier(u) == multiplier(v) else None,
                     'sources_tested': len(res), 'all_ok': all(x[2] for x in res)})
    # parity law
    par = []
    for content in [(2, 2, 3, 3, 3, 3), (2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3), (2, 3, 5, 6), (2, 3, 3, 5, 6, 7)]:
        okc = True; nsrc = 0
        for m in [2, 4, 6, 8, 12, 18, 24, 36, 48, 72, 96, 144, 30, 60, 120, 210, 420]:
            for labs, path in arrangements(m, content):
                gl = gain_loss(m, labs); nsrc += 1
                for p in {q for N in content for q in factor(N)}:
                    pr = predicted_loss_steps(content, m, p)
                    if pr is not None and len(gl['loss_steps'].get(p, [])) != pr: okc = False
        par.append({'content': list(content), 'arrangements_checked': nsrc, 'ok': okc})
    dump('REWRITE_LAWS.json', {'block_rewrites': rows, 'parity_conservation': par})
    return 'rewrite %.1fs' % (time.time() - t0)


def sec_forcing():
    t0 = time.time(); table = {}; exc = []
    for al in range(1, 9):
        for be in range(1, 9):
            for e2 in range(0, 9):
                for e3 in range(0, 5):
                    if not feasible(e2, e3, al, be): continue
                    av = avoids_square(e2, e3, al, be)
                    pred_avoid = (al == 1 and e3 == 0 and e2 in (1, 2) and be in (1, 2))
                    if av != pred_avoid: exc.append((al, be, e2, e3))
                    if av: table[str((al, be, e2, e3))] = 'avoidable'
    # brute force confirmation by explicit enumeration of arrangements (small)
    brute_bad = []; nb = 0
    for al, be in [(1, 1), (1, 2), (2, 1), (2, 2), (2, 4), (4, 4), (3, 2), (1, 3)]:
        for e2 in range(0, 6):
            for e3 in range(0, 3):
                m = 2 ** e2 * 3 ** e3
                arr = arrangements(m, [2] * al + [3] * be)
                if not arr: continue
                av = any(not both_active(p) for _, p in arr); nb += 1
                if av != (al == 1 and e3 == 0 and e2 in (1, 2) and be in (1, 2)): brute_bad.append((al, be, e2, e3))
    # loss-step / n-family: 2^{2n}3^{4n}
    fam = []
    for n in range(1, 7):
        fam.append({'n': n, 'forced_everywhere': all(forced_square(n, e2, e3) in (True, None) for e2 in range(0, 12) for e3 in range(0, 6))})
    dump('MIXED_INDEX_FORCING.json', {'classification_exceptions': exc, 'avoidable_cases': table, 'brute_force_cases': nb, 'brute_force_violations': brute_bad, 'family_2^2n_3^4n': fam})
    return 'forcing %.1fs' % (time.time() - t0)


def sec_field():
    t0 = time.time()
    mism = 0; chk = 0
    for x0 in list(range(4, 400, 4)) + [1140, 4556, 9000, 123456, 10 ** 7 + 4 * 11]:
        if x0 % 4: continue
        ps = FR.orbit_pairs(x0, 50); dx = FR.direct_orbit(x0, 50)
        chk += 1
        if [FR.value(p) for p in ps] != dx: mism += 1
    # rigid-set theorem: x_{n+3} = 4 x_n  iff  t_n in {1,2,3}
    viol = 0; tot = 0
    for sigma in (2, 4, 6, 8, 10, 12):
        for t0_ in [t for t in range(1, 160) if FR.split(t)[1] == t]:
            ps = FR.orbit_pairs(sigma * sigma * t0_, 120)
            xs = [FR.value(p) for p in ps]
            for n in range(100):
                tot += 1
                if (xs[n + 3] == 4 * xs[n]) != (ps[n][1] in FR.RIGID_T): viol += 1
    e = FR.entry_time_table(300000)
    mx = max(e.values()); worst = sorted(e, key=lambda t: -e[t])[:5]
    bound_viol = sum(1 for t in e if e[t] > 4 * FR.kappa3(t))
    hist = Counter(e.values())
    births = []
    for sigma in (2, 4, 6, 12, 30):
        for t_ in (1, 2, 3):
            x = sigma * sigma * t_; ps = FR.orbit_pairs(x, 3)
            for i in range(1, 4):
                if ps[i][2] > 1: births.append({'sigma': sigma, 't': t_, 'carry_step': i, 'u': ps[i][2], 'new_indices': FR.births_at_carry(ps[i - 1][0], ps[i][2]), 'tau_odd_part': FR.tau(sigma // (2 ** (len([1 for _ in range(60) if sigma % (2 ** (_ + 1)) == 0]))))})
    dump('REGIME_I.json', {'pair_model_vs_frozen_C': {'orbits': chk, 'mismatches': mism}, 'rigid_set_theorem': {'pairs_tested': tot, 'violations': viol},
                           'entry_time': {'T': 300000, 'squarefree_t': len(e), 'max': mx, 'argmax_examples': worst, 'bound_4kappa3_violations': bound_viol, 'histogram': dict(sorted(hist.items()))},
                           'births_at_rigid_carry': births})
    return 'field %.1fs' % (time.time() - t0)


def sec_events():
    t0 = time.time()
    # event saturation: sigma' = sigma (N+1)/c  and sigma' > sigma for every edge
    bad = 0; n = 0; ch = 0
    from geo_snapshots import s_of
    for m in range(1, 3001):
        for N in sorted(divisors_from(factor(m))):
            mp = step(m, N); n += 1
            if s_of(m) * EC.sigma_transport(m, N) != s_of(mp): bad += 1
            if s_of(mp) <= s_of(m): bad += 1
            if set(__import__('geo1lib').fibre(m)) == set(__import__('geo1lib').fibre(mp)): ch += 1
    # rigid phase table
    rig = [EC.rigid_phase_record(s, t) for s in (2, 4, 6, 8, 10, 12, 14, 30, 36, 60, 210) for t in (1, 2, 3)]
    # bounded pair classification
    starts = [s * s * t for s in (2, 4, 6, 8) for t in (1, 2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21)]
    cnt, viol, tot = EC.classify_pairs(starts, nmax=18, span=30, maxratio_pow=6)
    dump('EVENT_CORRESPONDENCE.json', {'saturation': {'edges_checked': n, 'violations': bad, 'edges_with_unchanged_D': ch},
                                       'rigid_phases': rig, 'pair_classification': {'starts': len(starts), 'pairs': tot, 'counts': {str(k): v for k, v in sorted(cnt.items())}, 'violations_of_ratio_4^j': viol}})
    return 'events %.1fs' % (time.time() - t0)


def sec_family():
    t0 = time.time()
    rows = []
    for a in range(2, 25):
        N = 2 ** a - 1
        sqf = all(e == 1 for e in factor(N).values())
        r = EC.family_trace(a, 2) if sqf else None
        if not sqf:
            # negative control: orbit of N s^2 never meets (2^a s)^2 within a long horizon
            x = N * 4; y = (2 ** a * 2) ** 2; ps = FR.orbit_pairs(x, 400); hit = any(FR.value(p) == y for p in ps)
            rows.append({'a': a, 'N': N, 'squarefree': False, 'hit_within_400': hit})
        else:
            pred_k = 1 + 3 * a // 2 if a % 2 == 0 else 3 * (a + 1) // 2
            rows.append({'a': a, 'N': N, 'squarefree': True, 'hit': r['hit'], 'k': r['k'], 'k_pred': pred_k, 'collective_events': r['collective_events'],
                         'events_pred': 1 + (a + 1) // 2, 'select_events': 1})
    hits = EC.coincidence_scan(4000, 60)
    scan = {str(k): v[:6] for k, v in sorted(hits.items())}
    forms = sorted({(N + 1) for (N, k) in hits})
    dump('SINGLE_EDGE_COINCIDENCES.json', {'family': rows, 'scan_x<4000': scan, 'N_plus_1_values': forms,
                                           'N_plus_1_form': {str(f): ('2^%d' % (f.bit_length() - 1) if f & (f - 1) == 0 else ('3*2^%d' % ((f // 3).bit_length() - 1) if f % 3 == 0 and (f // 3) & (f // 3 - 1) == 0 else 'other')) for f in forms}})
    return 'family %.1fs' % (time.time() - t0)


def sec_high():
    t0 = time.time()
    dump('HIGHER_DIMENSIONAL.json', {n: HD.example_table(n) for n in HD.EXAMPLES})
    return 'high %.1fs' % (time.time() - t0)


def sec_beyond():
    t0 = time.time()
    rows = CA.regime_census(600, 600)
    cnt = Counter((h[0] if h else None) for _, h in rows)
    dump('BEYOND_REGIME_I.json', {'eight_step_G11': CA.eight_step_check(5), 'square_multiplier_rho_le_12': {str(k): v for k, v in CA.square_multiplier_rho().items()},
                                  'single_edge_square_multiplier': CA.single_edge_square(1_000_000), 'census_non_regime_I_integers_x<600': {'n': len(rows), 'outcome_counts': dict(cnt), 'max_steps_to_G1': max(h[1] for _, h in rows if h and h[0] == 'G=1')}})
    return 'beyond %.1fs' % (time.time() - t0)


SECTIONS = {'geom': sec_geom, 'rewrite': sec_rewrite, 'forcing': sec_forcing, 'field': sec_field, 'events': sec_events, 'family': sec_family, 'high': sec_high, 'beyond': sec_beyond}

if __name__ == '__main__':
    todo = sys.argv[1:] or ['all']
    if 'all' in todo: todo = list(SECTIONS)
    for s in todo: print(SECTIONS[s](), flush=True)
