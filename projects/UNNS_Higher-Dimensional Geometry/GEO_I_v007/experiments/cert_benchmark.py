"""Programme C / E3: effective certification cost.  For thick/thin boxes the PROOF-CELL certificate (theory/modular_layers.py: O(|F|/d... ) cells
named by a closed rule) is compared with the GENERIC certificate (all cells of K_abs, theory/coverage.py).  Both exact.  Reports #cells and seconds.
usage: cert_benchmark.py OUT.json"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import modular_layers as ML, coverage as C
from lattice_model import Lat
rows = []
for (d, s, Q) in [(7, 3, (14, 14)), (11, 4, (22, 25)), (11, 4, (30, 30)), (13, 5, (26, 40)), (16, 3, (32, 32)), (17, 5, (40, 40)), (21, 8, (42, 60)), (25, 7, (50, 60)), (29, 12, (58, 58))]:
    t = time.time(); r = ML.verify_box(d, s, Q); tp = time.time() - t
    row = {'d': d, 's': s, 'Q': Q, 'proof_ok': r['ok'], 'proof_cells': r['n_cells'], 'proof_seconds': round(tp, 3), 'fibre': len(ML.fibre(d, s, Q))}
    if d <= 21 and max(Q) <= 45:
        t = time.time(); L = Lat(d, d, d, s); cd = C.complex_data(L, Q); n2 = len(cd['cells'][2]); u = C.uncovered(L, Q)
        row.update({'generic_ok': (u is not None and len(u) == 0), 'generic_2cells': n2, 'generic_seconds': round(time.time() - t, 3)})
    rows.append(row); print(row, flush=True)
json.dump(rows, open(sys.argv[1], 'w'), indent=1)
