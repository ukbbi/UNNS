"""Exports exact data for the benchmark fibres, certified cells, Graver moves, and copies key outputs into the release folders."""
import sys, os, json, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'geometry'))
from geo2lib import *
BM = {'72': Fr(72), '144': Fr(144), '3600': Fr(3600), '44100': Fr(44100), '210^4': Fr(210 ** 4), '2304/5': Fr(2304, 5)}
fib = {}; mov = {}
for name, x in BM.items():
    ps, q, b = coords(x); F = fibre_points(ps, q, b)
    fib[name] = {'x': str(x), 'primes': ps, 'q': q, 'b': b, 'points': [{'alpha': list(u), 'd': d_value(ps, u), 'N': d_value(ps, u) - 1, 'M': str(x * (d_value(ps, u) - 1) / d_value(ps, u) ** 2)} for u in F]}
    G = [g for g in graver_region(ps, q, b) if lexpos(g)]
    cells = build_cells(F, set(graver_region(ps, q, b)), len(ps)); Fs = set(F)
    edges = [{'from': list(u), 'to': list(add(u, g[0])), 'move': list(g[0]), 'chi_of_move_mod_b': (None if b == 1 else int(__import__('math').prod(pow(p, e, b) for p, e in zip(ps, g[0])) % b))} for (u, g) in (cells[1] if len(cells) > 1 else [])]
    mov[name] = {'graver_positive_in_region': [list(g) for g in G], 'move_edges': edges}
os.makedirs(os.path.join(ROOT, 'geometry', 'fibres'), exist_ok=True)
json.dump(fib, open(os.path.join(ROOT, 'geometry', 'fibres', 'benchmark_fibres.json'), 'w'), indent=1)
json.dump(mov, open(os.path.join(ROOT, 'geometry', 'modular_moves', 'benchmark_graver_moves.json'), 'w'), indent=1)
cert = {}
for name, x, top in (('3600', 3600, ((1, 0, 0), ((0, 0, 1), (0, 1, 0), (1, 0, 0)))), ('210^4', 210 ** 4, ((1, 1, 1, 1), ((0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0))))):
    seen = {top}; cur = {top}
    while cur:
        nxt = set()
        for c in cur: nxt |= set(boundary(c))
        cur = nxt - seen; seen |= nxt
    ps, q, b = coords(x); cells = build_cells(sorted(fibre_points(ps, q, b)), set(unit_moves(len(ps))), len(ps))
    cert[name] = {'top_cell': {'base': list(top[0]), 'generators': [list(g) for g in top[1]]},
                  'faces_by_dim': {str(j): sorted([{'base': list(u), 'gens': [list(g) for g in gg]} for (u, gg) in seen if len(gg) == j], key=str) for j in range(len(top[1]) + 1)},
                  'all_faces_in_complex': all(f in set(cells[len(f[1])]) for f in seen)}
json.dump(cert, open(os.path.join(ROOT, 'geometry', 'cells', 'certified_cells.json'), 'w'), indent=1)
O = os.path.join(ROOT, 'output')
shutil.copy(os.path.join(O, 'corpus_rational.csv'), os.path.join(ROOT, 'geometry', 'topology', 'corpus_rational.csv'))
shutil.copy(os.path.join(O, 'move_homology_witnesses.json'), os.path.join(ROOT, 'geometry', 'topology', 'move_homology_witnesses.json'))
R = json.load(open(os.path.join(O, 'verify_full.json')))
shutil.copy(os.path.join(O, 'dynamics_c_orbits.csv'), os.path.join(ROOT, 'dynamics', 'c_orbit_geometry.csv'))
json.dump({'select2_geometry_change': R['select2_geometry_change'], 'select2_from_72': R['select2_from_72'], 'M1_orbits': R['M1_orbits']}, open(os.path.join(ROOT, 'dynamics', 'select2_and_summary.json'), 'w'), indent=1)
print('export ok')
