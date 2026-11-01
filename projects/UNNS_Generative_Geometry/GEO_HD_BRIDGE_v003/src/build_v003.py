"""GEO_HD_BRIDGE v003 builder.  python build_v003.py [section ...]  (default: all).  Writes ../results/*.json"""
import _paths, sys, os, json, time, random, itertools
from fractions import Fraction as Fr
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(os.path.dirname(HERE), 'results')
def dump(name, obj): json.dump(obj, open(os.path.join(RES, name + '.json'), 'w'), indent=1, default=str)

def sec_rational():
    import rational_geometry as R, graver_relations as GR, arithmetic_classes as AC
    from geo1lib import factor
    out = {}
    # R3-T1a: F-only reconstruction of positive-primitive + edge-realized moves, on constructed states with nonempty F
    rng = random.Random(5); P = [2, 3, 5, 7, 11, 13]; n = big = withd = bad = 0; seen = set()
    def divs(m):
        f = factor(m); ds = [1]
        for p, e in f.items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
        return ds
    for _ in range(900):
        k = rng.randint(2, 4); ps = rng.sample(P, k); q = [rng.randint(1, 3) for _ in ps]
        a = 1
        for p, e in zip(ps, q): a *= p ** (2 * e + rng.randint(0, 1))
        al = [rng.randint(0, e) for e in q]; m = 1
        for p, e in zip(ps, al): m *= p ** e
        if m == 1: continue
        ds = [d for d in divs(m - 1) if d > 1]
        if not ds: continue
        b = rng.choice(ds)
        if gcd(a, b) != 1 or (a, b) in seen: continue
        seen.add((a, b)); rec = R.record(Fr(a, b)); s = R.split_graver(rec); n += 1
        big += len(rec['F']) >= 2; withd += bool(s['dormant'])
        pos, edge = R.classes_from_F(rec['F'], len(rec['ps'])); G = set(rec['G'])
        joined = {tuple(c - a_ for a_, c in zip(u, v)) for u in rec['F'] for v in rec['F'] if u != v}
        if not ((pos | edge) <= G and (G & joined) <= edge): bad += 1
    out['T1a_census'] = {'states': n, 'with_|F|>=2': big, 'with_dormant_moves': withd, 'violations': bad}
    out['family2'] = GR.family2(12); out['familyk'] = GR.familyk((2, 3, 4, 5))
    out['classification_k2'] = AC.scan(pmax=40, bmax=260)
    dump('RATIONAL_GEOMETRY', out)

def sec_history():
    import history_invariants as H
    out = {}
    pool = [3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15]; rows = []
    for r in range(1, 5):
        for A in itertools.combinations(pool, r):
            rows.append(H.analyse_content(A))
    rows = [x for x in rows if x['n_words']]
    out['scan'] = {'contents': len(rows), 'bit_constant_everywhere': all(x['bit_constant_on_components'] for x in rows),
                   'first_label_always_2_or_4': all(set(x['first_labels']) <= {2, 4} for x in rows),
                   'adjacent_2_4_ever': any(x['adjacent_2_4_in_some_word'] for x in rows),
                   'disconnected_via_bit': sum(x['both_orders_present'] for x in rows),
                   'component_counts': {str(c): sum(1 for x in rows if x['components'] == c) for c in sorted({x['components'] for x in rows})}}
    chain = []
    for A, E in H.extension_chain((5, 9), 4):
        a = H.analyse_content(A); a['endpoint'] = E; chain.append(a)
    out['extension_chain'] = chain
    out['named'] = {'disconnected_3_primes': H.analyse_content((3, 5, 6)), 'disconnected_4_primes': H.analyse_content((3, 5, 6, 7))}
    rng = random.Random(1); bad = 0
    for _ in range(3000):
        s = rng.randint(1, 400); N, M = rng.randint(1, 30), rng.randint(1, 30)
        if N == M: continue
        def v(n, p):
            c = 0
            while n % p == 0: n //= p; c += 1
            return c
        both = H.junction_both_orders(s, N, M)
        from geo1lib import factor
        ps = set(factor(N)) | set(factor(M)) | set(factor(N + 1)) | set(factor(M + 1))
        ok1 = all(v(s, p) >= v(N, p) and v(s, p) + 2 * v(N + 1, p) - v(N, p) >= v(M, p) for p in ps)
        ok2 = all(v(s, p) >= v(M, p) and v(s, p) + 2 * v(M + 1, p) - v(M, p) >= v(N, p) for p in ps)
        if both != (ok1 and ok2): bad += 1
    out['junction_lemma_violations'] = bad
    dump('HISTORY_INVARIANTS', out)

def sec_collective():
    import collective_regimes as C
    out = {}
    out['tower11'] = {'bad': C.tower_formula_ok(C.S11, 11, 8, 9, 12), 'K': 12}
    out['tower5'] = {'bad': C.tower_formula_ok(C.S5, 5, 3, 4, 16), 'K': 16}
    xs, infos, ev = C.stage_decomposition(C.S11(0), 11, 40); out['tower11_events'] = ev
    xs, infos, ev = C.stage_decomposition(C.S5(0), 5, 20); out['tower5_events'] = ev
    xs, infos, ev = C.stage_decomposition(1890, 29, 110); out['l29_S1890_events'] = ev
    # stage law on the search results
    sr = json.load(open('/tmp/search_g.json')) if os.path.exists('/tmp/search_g.json') else None
    rows = []
    for (b, S) in [(5, 126), (7, 450), (11, 300), (11, 900), (13, 280), (13, 2700), (17, 3 * 5 * 7 * 5 * 3), (29, 1890), (29, 5400), (29, 12600)]:
        if not C.in_class(S, b): rows.append({'l': b, 'S': S, 'in_class': False}); continue
        xs, infos, ev = C.stage_decomposition(S, b, 140)
        rows.append({'l': b, 'S': S, 'in_class': True, 'tau': C.tau(S, b), 'events': [(e['step'], e['t_event']) for e in ev[:8]]})
    out['local_stage_rows'] = rows
    dump('COLLECTIVE_REGIMES', out)

def sec_geometry():
    import geometric_transitions as GT, collective_regimes as C
    out = {}
    out['tower11_period_starts'] = GT.tower_period_starts(C.S11, 11, 12)
    out['tower11_within_k0'] = GT.within_period(C.S11(0), 11, 8)
    out['tower11_within_k1'] = GT.within_period(C.S11(1), 11, 8)
    out['tower5_within_k0'] = GT.within_period(C.S5(0), 5, 3)
    dump('GEOMETRIC_TRANSITIONS', out)

def sec_corr():
    import correspondence as CO, collective_regimes as C
    out = {}
    for name, S, l, P, rho2 in (('tower11_k0', C.S11(0), 11, 8, 9), ('tower5_k0', C.S5(0), 5, 3, 4)):
        nmax = P * 5
        rows = CO.coincidences(S, l, nmax)
        xs, _ = C.orbit(Fr(S * S, l), nmax)
        pred = CO.predicted(lambda n: xs[n], P, rho2, nmax)
        out[name] = {'coincidences': rows, 'predicted_equal': sorted((r['n'], r['m'], r['N']) for r in rows) == sorted(pred), 'nmax': nmax}
        out[name]['summary'] = {str(N): [(r['n'] % P + 1, r['m'] // P - r['n'] // P, r['m'] % P + 1, r['collective_events'], r['level3']) for r in rows if r['N'] == N and r['n'] < P] for N in sorted({r['N'] for r in rows})}
    dump('CORRESPONDENCE', out)

SECTIONS = {'rational': sec_rational, 'history': sec_history, 'collective': sec_collective, 'geometry': sec_geometry, 'corr': sec_corr}

def sec_gcensus():
    """finite-exact census of persistent G>1 orbits x0 = S^2/l: period P and multiplier rho^2 (exact ratios)"""
    import collective_regimes as C
    from collections import Counter
    rows = []; unresolved = []; n = 0
    grids = {5: None, 7: None, 11: None, 13: None}
    for l in (5, 7, 11, 13):
        for a2, a3, a5, a7 in itertools.product(range(0, 4), range(0, 4), range(0, 3), range(0, 2)):
            S = 2 ** a2 * 3 ** a3 * 5 ** a5 * 7 ** a7
            if S < 4 or gcd(S, l) != 1: continue
            xs, infos = C.orbit(Fr(S * S, l), 70) if C.info(Fr(S * S, l)) else (None, None)
            if xs is None or any(i is None for i in infos): continue
            n += 1
            if infos[0]['G'] <= 1: continue
            found = None
            for P in range(1, 41):
                r = xs[-2] / xs[-2 - P]
                if all(xs[-2 - i] / xs[-2 - i - P] == r for i in range(0, min(P + 8, 30))): found = (P, r); break
            (rows if found else unresolved).append({'l': l, 'S': S, 'G0': infos[0]['G'], 'G_end': infos[-2]['G'], 'P': found[0] if found else None, 'rho2': str(found[1]) if found else None})
    extra = json.load(open('/tmp/search_g.json')) if os.path.exists('/tmp/search_g.json') else {'periodic': [], 'unresolved': [], 'n': 0}
    for b, S, G0, G1, P, r in extra['periodic']: rows.append({'l': b, 'S': S, 'G0': G0, 'G_end': G1, 'P': P, 'rho2': r})
    for b, S, G0, G1 in extra['unresolved']: unresolved.append({'l': b, 'S': S, 'G0': G0, 'G_end': G1, 'P': None, 'rho2': None})
    pers = [r for r in rows if r['G_end'] > 1]; exits = [r for r in rows if r['G_end'] == 1]
    cnt = Counter((r['l'], r['P'], r['rho2']) for r in pers)
    json.dump(rows + unresolved, open(os.path.join(os.path.dirname(HERE), 'data', 'G_CENSUS_ROWS.json'), 'w'))
    dump('G_CENSUS', {'orbits_simulated': n + extra['n'], 'periodic_detected': len(rows), 'persistent_G_gt_1': len(pers), 'exit_to_G1': len(exits),
                      'unresolved_in_window': len(unresolved), 'by_l_P_rho2_persistent': {str(k): v for k, v in sorted(cnt.items())},
                      'pairs_P_rho2_persistent': sorted({(r['P'], r['rho2']) for r in pers}), 'pairs_P_rho2_exits': sorted({(r['P'], r['rho2']) for r in exits}),
                      'persistent_G_end_equals_l': sum(1 for r in pers if r['G_end'] == r['l']), 'persistent_G_end_other': sum(1 for r in pers if r['G_end'] != r['l']),
                      'unresolved_G_end_equals_G0': sum(1 for r in unresolved if r['G_end'] == r['G0'])})
SECTIONS['gcensus'] = sec_gcensus

if __name__ == '__main__':
    todo = sys.argv[1:] or list(SECTIONS)
    for k in todo:
        t = time.time(); SECTIONS[k](); print(k, 'done %.1fs' % (time.time() - t), flush=True)
