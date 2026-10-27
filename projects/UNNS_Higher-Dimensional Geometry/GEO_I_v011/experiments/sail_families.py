#!/usr/bin/env python3
"""GEO-I v010 Programme A: exact verification of the zonogon cover (THEOREM G10-Z, theory/modular_sail.py) for EVERY unit pair 5 <= d <= DMAX, 2 <= s <= d-2, and agreement with the v005/v009 engine.
python3 experiments/sail_families.py DMAX ENGINE_MAX     -> output/data/v10_sail_families.json
 * every (d,s): the cells of general_cover are valid cells (Graver generators by exact box scan, corners in F) and conv(F) minus (T1 u T2 u cells) has exact area 0;
 * the explicit parametric families S1 (d = s m + 1) and S2 (d = s M - 1), direct or transposed, are verified as well (their cell lists are the zonogon covers in closed form);
 * for d <= ENGINE_MAX: the engine confirms conv(F)\\U = int T1 u int T2 (hollow_check.check) and every cell of the cover is an engine cell."""
import os, sys, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory', 'experiments'): sys.path.insert(0, os.path.join(ROOT, d_))
from math import gcd
import modular_sail as MS

def main(dmax, emax):
    rec = {'dmax': dmax, 'engine_max': emax, 'pairs': 0, 'failures': [], 'max_cells': 0, 'max_steps': 0, 'explicit_S1_S2_pairs': 0, 'explicit_failures': [], 'engine_checked': 0, 'engine_failures': []}
    for d in range(5, dmax + 1):
        for s in range(2, d - 1):
            if gcd(d, s) != 1: continue
            v = MS.verify_general(d, s); rec['pairs'] += 1; rec['max_cells'] = max(rec['max_cells'], v['cells'])
            rec['max_steps'] = max(rec['max_steps'], len(MS.sail_steps(d, s)))
            if not (v['cells_valid'] and v['remainder_area2'] == 0): rec['failures'].append(v)
            e = MS.verify_cover(d, s)
            if e is not None:
                rec['explicit_S1_S2_pairs'] += 1
                if not (e['cells_valid'] and e['remainder_area2'] == 0): rec['explicit_failures'].append(e)
    if emax:
        import hollow_check as HC, coverage as C
        from lattice_model import Lat
        for d in range(5, emax + 1):
            for s in range(2, d - 1):
                if gcd(d, s) != 1: continue
                ok, tot, inT = HC.check(d, s); eng = {(u, g, h) for (u, (g, h)) in C.complex_data(Lat(d, d, d, s), (d, d))['cells'][2]}
                rec['engine_checked'] += 1
                if not (ok and all(c in eng for c in MS.general_cover(d, s))): rec['engine_failures'].append((d, s, ok))
    json.dump(rec, open(os.path.join(ROOT, 'output', 'data', 'v10_sail_families.json'), 'w'), indent=1)
    print({k: v for k, v in rec.items() if k not in ('failures', 'engine_failures', 'explicit_failures')}, 'failures', len(rec['failures']), 'explicit failures', len(rec['explicit_failures']), 'engine failures', len(rec['engine_failures']))

if __name__ == '__main__': main(int(sys.argv[1]), int(sys.argv[2]))
