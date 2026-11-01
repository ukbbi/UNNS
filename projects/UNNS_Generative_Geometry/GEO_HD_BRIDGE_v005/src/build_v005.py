"""Builds results/*.json for GEO_HD_BRIDGE_v005 from the data/ files and exact recomputation.  usage: python build_v005.py [exemplars census towers]"""
import _paths, os, sys, json, collections, hashlib
from fractions import Fraction as Fr
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = lambda n: os.path.join(ROOT, 'results', n); Dd = lambda n: os.path.join(ROOT, 'data', n)
def dump(p, o): json.dump(o, open(p, 'w'), indent=1, sort_keys=True, default=str)
pad = lambda b, n=8: list(b) + [0] * (n - len(b))

def sec_exemplars():
    from reachability import decide
    from activation_family import make
    from transition_calculus import analyse_transition
    from geo1lib import fibre_q, Lof, Gof
    from stage_sieve import stage_data, first_event
    out = {}
    def orbitD(x0, n):
        cur = Fr(x0); Ds = []
        for _ in range(n + 1):
            D = fibre_q(cur); Ds.append(D); cur = cur + Fr(Lof(D) ** 2, Gof(D))
        return Ds
    # B5-1
    x, y, P = make(2, 3, [5, 11], 2); r = decide(x, y, want_log=True); S = stage_data(x)
    Ds = orbitD(x, 8)
    ev = [(n, Ds[n], Ds[n + 1]) for n in range(8) if Ds[n] != Ds[n + 1]]
    tr = [analyse_transition(a, b) for n, a, b in ev]
    out['B5-1'] = {'x': str(x), 'y': str(y), 'decide': {k: r[k] for k in ('class', 'steps', 'stages', 'log')}, 'sieve_stage0': {'L': S['L'], 'G': S['G'], 'a': S['a'], 'b': S['b'], 'h': S['h']},
                   'events': [{'state_index': n, 'D_before': a, 'D_after': b, 'betti_before': t['betti'], 'betti_after': t['betti2'], 'dead': t['dead'], 'new': t['new'], 'delta': t['delta']} for (n, a, b), t in zip(ev, tr)]}
    # B5-2
    x, y, P = make(3, 7, [11, 53, 67], 2); r = decide(x, y, want_log=True)
    out['B5-2'] = {'x': str(x), 'y': str(y), 'decide': {k: r[k] for k in ('class', 'steps', 'stages', 'log')}}
    # B5-3 blocked members
    bl = [t for t in json.load(open(Dd('REACHABILITY_V004.json'))) if t['class'] == 'BLOCKED'][:2000:400]
    out['B5-3'] = []
    for t in bl:
        x, y, P = make(t['k'], t['l'], t['ps'], t['q']); r = decide(x, y, want_log=True)
        out['B5-3'].append({'inst': [t['k'], t['l'], t['ps'], t['q']], 'class': r['class'], 'bad': r.get('bad'), 'sieve_log': r['log'], 'D_y': fibre_q(y)})
    # B5-9
    x = Fr(1890 ** 2, 29); S = stage_data(x); ev = first_event(S, 60); Ds = orbitD(x, 26)
    tr = analyse_transition(Ds[23], Ds[24])
    out['B5-9'] = {'x': str(x), 'G': S['G'], 'L': S['L'], 'predicted_first_event': ev, 'observed_D_change_at_state': 24 if Ds[23] != Ds[24] else None,
                   'betti_before': tr['betti'], 'betti_after': tr['betti2'], 'dead': tr['dead'], 'new': tr['new']}
    # G=5 event 5->6 (tower index k=1->2)
    from tower_laws import tower_D, S5, S11
    t = analyse_transition(tower_D(S5(1), 5), tower_D(S5(2), 5))
    out['G5_event'] = {'orbit_step': '5->6', 'tower_index': 'k=1->2', 'betti_before': t['betti'], 'betti_after': t['betti2'], 'f': t['f'], 'f2': t['f2'], 'dead': t['dead'], 'new': t['new'], 'newv': t['newv'], 'r': t['r'], 'rp': t['rp'], 'h': t['h'], 'hp': t['hp']}
    t = analyse_transition(tower_D(S11(8), 11), tower_D(S11(9), 11))
    out['G11_event_k8_to_k9'] = {'betti_before': t['betti'], 'betti_after': t['betti2'], 'dead': t['dead'], 'new': t['new'], 'newv': t['newv']}
    # B5-5 / B5-6 representatives from the census
    rows = json.load(open(Dd('EVENT_CENSUS.json')))
    unch = [r for r in rows if pad(r['betti']) == pad(r['betti2'])]
    drop = [r for r in rows if pad(r['betti2'])[1] < pad(r['betti'])[1]]
    def detail(r):
        cur = Fr(r['S'] * r['S'], r['l']); Ds = []
        for i in range(r['n'] + 2):
            D = fibre_q(cur); Ds.append(D); cur = cur + Fr(Lof(D) ** 2, Gof(D))
        t = analyse_transition(Ds[r['n']], Ds[r['n'] + 1])
        return {'l': r['l'], 'S': r['S'], 'n': r['n'], 'D_before': Ds[r['n']], 'D_after': Ds[r['n'] + 1], 'newv': t['newv'], 'betti': t['betti'], 'betti2': t['betti2'],
                'f': t['f'], 'f2': t['f2'], 'dead': t['dead'], 'new': t['new'], 'r': t['r'], 'rp': t['rp'], 'h': t['h'], 'hp': t['hp'], 'beta_surv': t['beta_surv']}
    nodead_unch = [r for r in unch if not any(r['dead'])]; dead_unch = [r for r in unch if any(r['dead'])]
    out['B5-5'] = {'unchanged_nested_example': detail(nodead_unch[len(nodead_unch) // 3]), 'unchanged_with_dead_example': detail(dead_unch[len(dead_unch) // 2])}
    dnest = [r for r in drop if not any(r['dead'])]; ddead = [r for r in drop if any(r['dead'])]
    out['B5-6'] = {'drop_nested_new2cell_example': detail(dnest[len(dnest) // 2]), 'drop_with_dead_edges_example': detail(ddead[len(ddead) // 2])}
    dump(R('EXEMPLARS_V005.json'), out); return out

def sec_census():
    rows = json.load(open(Dd('EVENT_CENSUS.json'))); g = lambda v, i: v[i] if len(v) > i else 0
    T = collections.Counter(); M = collections.Counter(); bytype = collections.Counter(r['type'] for r in rows)
    for r in rows:
        de = r['dead'][1] > 0; n2 = g(r['new'], 2) > 0; d = g(r['betti2'], 1) - g(r['betti'], 1)
        M['dead_edge=%s,new_2cell=%s,dbeta1=%s' % (de, n2, 'up' if d > 0 else 'down' if d < 0 else 'same')] += 1
    graph = [r for r in rows if len(r['f']) <= 2 and len(r['f2']) <= 2]
    s = {'events': len(rows), 'orbits': len({(r['l'], r['S']) for r in rows}), 'types': dict(bytype), 'mechanism_table_beta1': dict(M),
         'events_with_dead_edges': sum(1 for r in rows if r['dead'][1] > 0), 'max_dead_edges': max(r['dead'][1] for r in rows),
         'events_nested_no_dead': sum(1 for r in rows if not any(r['dead'])),
         'beta1_drops': sum(1 for r in rows if g(r['betti2'], 1) < g(r['betti'], 1)),
         'graph_level_events': len(graph), 'max_new_vertices_in_event': max(r['nnew'] for r in rows),
         'beta2_changes': sum(1 for r in rows if g(r['betti2'], 2) != g(r['betti'], 2)), 'beta3_changes': sum(1 for r in rows if g(r['betti2'], 3) != g(r['betti'], 3))}
    dump(R('CENSUS_SUMMARY.json'), s); return s


def sec_unresolved():
    """B5-4: the 24 step-capped rows of the v004 table, decided exactly (line scan for stage 1 + exact simulation afterwards)"""
    from reachability import resolve_family
    from stage_sieve import proper_divisor_block
    rows = [t for t in json.load(open(Dd('REACHABILITY_V004.json'))) if t['class'] == 'UNRESOLVED']; out = []
    for t in rows:
        r = resolve_family(t['k'], t['l'], t['ps'], t['q'])
        b, uf, ua = proper_divisor_block(t['ps'], t['l'], t['q'])
        out.append({'inst': [t['k'], t['l'], t['ps'], t['q']], **r, 'proper_divisor_criterion': b, 'u_forbidden_first': uf, 'u_allowed_first': ua})
    dump(R('UNRESOLVED24.json'), out); return out

def sec_obstruction():
    """proper-divisor obstruction against the whole v004 table"""
    from stage_sieve import proper_divisor_block
    rows = json.load(open(Dd('REACHABILITY_V004.json'))); C = collections.Counter()
    for t in rows:
        b, uf, ua = proper_divisor_block(t['ps'], t['l'], t['q']); C['%s/%s' % (t['class'], 'flagged' if b else 'not flagged')] += 1
    dump(R('OBSTRUCTION_TABLE.json'), dict(C)); return dict(C)

def sec_pins():
    pins = {'inherited_verification': 'NOT_RERUN', 'sha256': {}}
    for rel in ['src/frozen/geo1lib.py', 'src/frozen/geo2lib.py', 'src/rational_geometry.py', 'src/geometric_transitions.py', 'src/collective_regimes.py', 'src/dynamic_activation.py',
                'src/activation_family.py', 'src/graver_relations.py', 'src/move_complex.py', 'src/_paths.py', 'data/REACHABILITY_V004.json', 'data/ACTIVATION_SCAN_V004.json', 'data/TOWERS_V004.json']:
        pins['sha256'][rel] = hashlib.sha256(open(os.path.join(ROOT, rel), 'rb').read()).hexdigest()
    pins['note'] = 'v004 sources/data copied verbatim (frozen); hashes recorded at v005 build. Inherited verification of GEO_HD_1D v001-v004, BRIDGE v001-v004, E2_P4 v005 is NOT re-run.'
    dump(R('PINS.json'), pins); return pins

if __name__ == '__main__':
    secs = sys.argv[1:] or ['exemplars', 'census', 'pins']
    for s in secs: globals()['sec_' + s](); print('done', s, flush=True)
