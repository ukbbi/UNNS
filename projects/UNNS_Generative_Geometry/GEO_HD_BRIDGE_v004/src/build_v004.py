"""Builds results/*.json and data/*.json for GEO_HD_BRIDGE v004 (frozen GEO-I engine via the copied libraries).
usage: python build_v004.py [section ...]   sections: family reach exemplars towers history scan"""
import _paths, os, sys, json, time, itertools, shutil
from fractions import Fraction as Fr
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda n: os.path.join(ROOT, 'results', n); Dd = lambda n: os.path.join(ROOT, 'data', n)
def dump(p, o): json.dump(o, open(p, 'w'), indent=1, sort_keys=True, default=str)

def sec_family():
    import activation_family as A, move_complex as M
    from graver_relations import isprime, primitive_root_of_order, primes_in_class
    insts = [(2, 3, [5, 11], 17), (2, 3, [5, 11], 2)] + [A.default_instance(k) for k in (2, 3, 4, 5)]
    for k, l in [(2, 7), (2, 13), (3, 13), (4, 13), (3, 19)]:     # further primes l with k | l-1
        c = primitive_root_of_order(l, k); ps = primes_in_class(c, l, k, start=3); cinv = pow(c, -1, l)
        q = next(n for n in range(3, 10 ** 4) if isprime(n) and n % l == cinv and n not in ps); insts.append((k, l, ps, q))
    rows = []
    for inst in insts:
        a = A.analyse(*inst); x, y, P = A.make(*inst); mv = M.move_complex(y); mx = M.move_complex(x); k = inst[0]
        rows.append({**a, 'Kmove_y': {kk: mv[kk] for kk in ('vertices', 'edges', 'cells2', 'cells3', 'betti_gf2', 'betti_gf3', 'axis_edges')},
                     'Kmove_x_vertices': mx['vertices'], 'Kmove_x_edges': mx['edges'], 'beta1_predicted': k * (k - 1) // 2,
                     'Gr_x_predicted': k * (k - 1) + 2, 'Gr_y_predicted': (k + 1) * (k + 2)})
    dump(R('ACTIVATION_FAMILY.json'), rows); return rows

def sec_reach():
    import dynamic_activation as T
    from graver_relations import isprime, primitive_root_of_order
    t0 = time.time(); rows = []
    def go(k, l, qs, pmax, pcount, c=None):
        c = c or primitive_root_of_order(l, k); cinv = pow(c, -1, l)
        pr = [p for p in range(3, pmax) if isprime(p) and p % l == c][:pcount]
        qq = qs if qs else [q for q in range(2, 80) if isprime(q) and q % l == cinv]
        for ps in itertools.combinations(pr, k):
            for q in qq:
                if q in ps or (q * c) % l != 1: continue
                r = T.classify(k, l, list(ps), q, cap=30000)
                rows.append({'k': k, 'l': l, 'ps': list(ps), 'q': q, **r})
    go(2, 3, [2, 5, 11, 17, 23, 29], 400, 16)
    go(2, 5, None, 300, 12); go(2, 7, None, 300, 12); go(3, 7, [2], 260, 9, c=4)
    dump(R('REACHABILITY.json'), rows); return rows

def sec_exemplars():
    import dynamic_activation as T
    out = []
    for inst in [(2, 3, [5, 11], 2), (2, 3, [11, 23], 2), (3, 7, [11, 53, 67], 2), (2, 3, [41, 107], 5)]:
        t = T.trace_events(*inst)
        out.append({'inst': [inst[0], inst[1], inst[2], inst[3]], 'reached': t['reached'], 'steps': t['steps'], 'x': str(t['x']), 'y': str(t['y']),
                    'log': [{'n': n, 'b': s['b'], 'D': sorted(s['D']), 'nV': s['nV'], 'nE': s['nE'], 'n2': s['n2'], 'betti': s['betti'],
                             'dormant': len(s['dormant']), 'Gr': len(s['Gr']),
                             'g12': {'in_Gr': tuple(sorted(((inst[2][0], 1), (inst[2][1], -1)))) in s['Gr'],
                                     'dormant': tuple(sorted(((inst[2][0], 1), (inst[2][1], -1)))) in s['dormant'],
                                     'edge_realised': tuple(sorted(((inst[2][0], 1), (inst[2][1], -1)))) in s['edge_real']}} for n, s in t['log']]})
    dump(R('EXEMPLARS.json'), out); return out

def sec_towers():
    from tower_topology import row11, row5
    r11 = [row11(k) for k in range(0, 46)]; r5 = [row5(k) for k in range(0, 46)]
    for r in r11 + r5: r.pop('sec', None)
    dump(R('TOWERS.json'), {'tower11': r11, 'tower5': r5}); return r11, r5

def sec_history():
    import history_bridge as H
    ms = [4, 36, 900, 12100, 48400, 1296, 44100, 2 ** 4 * 3 ** 4 * 5 ** 2, 2 ** 2 * 3 ** 2 * 5 ** 2 * 7 ** 2 * 11 ** 2]
    out = {'integer_kmove': H.integer_kmove_rows(ms), 'bridge': H.bridge_rows(3)}
    dump(R('HISTORY_BRIDGE.json'), out); return out

def sec_l29():
    import dynamic_activation as T
    r = T.activation_events(Fr(1890 ** 2, 29), 24); out = []
    for n, (x, s) in enumerate(zip(r['X'], r['S'])):
        out.append({'n': n, 'x': str(x), 'b': s['b'], 'D': sorted(s['D']), 'dormant': len(s['dormant']), 'Gr': len(s['Gr']), 'nE': s['nE'], 'betti': s['betti']})
    dump(R('L29_TOWER.json'), {'rows': out, 'events': {k: len(v) if isinstance(v, list) else v for k, v in r['events'].items()}}); return out

def sec_scan():
    src = '/tmp/ACT_SCAN.json'
    if os.path.exists(src): shutil.copy(src, Dd('ACTIVATION_SCAN.json'))
    return json.load(open(Dd('ACTIVATION_SCAN.json')))

if __name__ == '__main__':
    secs = sys.argv[1:] or ['family', 'reach', 'exemplars', 'towers', 'history', 'l29', 'scan']
    for s in secs:
        t = time.time(); globals()['sec_' + s](); print(s, round(time.time() - t, 1), 's', flush=True)
