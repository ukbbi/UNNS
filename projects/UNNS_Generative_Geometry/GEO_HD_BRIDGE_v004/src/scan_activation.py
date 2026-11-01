"""B4-4: scan actual FIELD-I orbits from x=S^2/l (S in the modular class) for dormant->active events and their topological effect."""
import _paths, json, sys, time
from fractions import Fraction as Fr
from collective_regimes import in_class
from dynamic_activation import activation_events
from geometric_transitions import geo_row

def run(ls=(5, 7, 11, 13), Smax=1500, nsteps=24, budget=600):
    t0 = time.time(); rows = []
    for l in ls:
        for S in range(2, Smax):
            if time.time() - t0 > budget: break
            if not in_class(S, l): continue
            try: r = activation_events(Fr(S * S, l), nsteps)
            except Exception as e: rows.append({'l': l, 'S': S, 'error': repr(e)}); continue
            ev = r['events']; steps = sorted({n for n, g in ev['step_activation']})
            row = {'l': l, 'S': S, 'n': len(r['S']) - 1, 'persist_viol': ev['persistence_violations'],
                   'n_step_act': len(ev['step_activation']), 'n_creat': len(ev['creation_realisation']), 'n_traj': len(ev['trajectory_activation']),
                   'act_steps': []}
            for n in steps:
                a, b = geo_row(r['X'][n]), geo_row(r['X'][n + 1])
                row['act_steps'].append({'n': n, 'n_rel': sum(1 for m, g in ev['step_activation'] if m == n),
                                         'betti_before': a['betti'], 'betti_after': b['betti'], 'dorm_before': a['dormant'], 'dorm_after': b['dormant'],
                                         'cells_before': a['cells_move'], 'cells_after': b['cells_move'], 'D_before': a['D'], 'D_after': b['D']})
            rows.append(row)
    return rows

if __name__ == '__main__':
    out = sys.argv[1]; rows = run(budget=int(sys.argv[2]) if len(sys.argv) > 2 else 600)
    json.dump(rows, open(out, 'w'))
    print(len(rows))
