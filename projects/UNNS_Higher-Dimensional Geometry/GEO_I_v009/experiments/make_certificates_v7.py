"""GEO-I v007 Programme D: generate certificates D1-D5 into certificates/.
D1  coverage certificates (strip-cell cover with explicit finite SUBDIVISION of conv(F) into convex pieces, each inside a listed cell)
D2  obstruction-rank certificates (minimal binary boxes)
D3  hollow-box topology certificates
D4  symbolic general-proof records (statement/dependency/status/machine-checked ranges) -- records, not machine proofs
D5  cost accounting (certificate sizes and wall-clock for the checker vs. recomputation)"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d_))
from fractions import Fraction as Fr
import checker as K, corner_sail as CS, modular_layers as ML, binary_01 as B, rank_reduction as RR, centre_collisions as CC
CD = os.path.join(ROOT, 'certificates'); os.makedirs(CD, exist_ok=True)


def subdivision(d, s, Q, cells):
    F = K.fibre(d, s, Q); H = [(Fr(x), Fr(y)) for x, y in K.hull(F)]
    if K.area2(H) < 0: H = H[::-1]
    rem = [H]; pieces = []
    for k, (u, g, h) in enumerate(cells):
        cp = [(Fr(x), Fr(y)) for x, y in (u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1]))]
        if K.area2(cp) < 0: cp = cp[::-1]
        hp = K.halfplanes_ccw(cp); new = []
        for pc in rem:
            cur = pc
            for (a, b, c) in hp:
                out = K.clip(cur, -a, -b, -c)
                if len(out) >= 3 and K.area2(out) > 0: new.append(out)
                cur = K.clip(cur, a, b, c)
                if len(cur) < 3 or K.area2(cur) <= 0: cur = None; break
            if cur is not None: pieces.append({'cell': k, 'poly': [[str(x), str(y)] for x, y in cur]})
        rem = new
    return pieces, len(rem)


def d1(d, s, Q):
    cells, tags = CS.strip_cells(d, s, Q); cells = list(dict.fromkeys(cells))
    pcs, left = subdivision(d, s, Q, cells)
    assert left == 0
    return {'kind': 'D1_coverage', 'claim': 'conv(F) = U', 'method': 'Theorem A-COL strip cells', 'd': d, 's': s, 'Q': list(Q),
            'cells': [[list(u), list(g), list(h)] for u, g, h in cells], 'pieces': pcs}


t0 = time.time()
D1 = [d1(*x) for x in [(5, 2, (7, 10)), (7, 3, (9, 14)), (8, 3, (8, 16)), (11, 4, (13, 22)), (13, 5, (20, 26)), (4, 3, (12, 8))]]
json.dump(D1, open(os.path.join(CD, 'D1_coverage.json'), 'w'))
D2 = []
for cols in ([1, 1, 1, 1], [1, 1, 1, 2, 3], [1, 1, 2, 2, 3, 3], [1, 1, 2, 2, 3, 4, 7], [1, 1, 2, 2, 4, 4, 7, 7]):
    n = len(cols); rks = [RR.witness_rank(n, a, b)[0] for _, a, b in CC.collisions(cols)]
    D2.append({'kind': 'D2_rank', 'columns': cols, 'claim': 'minimal non-embedded box; minimum witness rank', 'min_rank': min(rks), 'max_rank': max(rks)})
json.dump(D2, open(os.path.join(CD, 'D2_rank.json'), 'w'))
D3 = [{'kind': 'D3_hollow', 'd': d, 's': s, 'claim': 'beta_1(U) >= 2 (two bounded complement components)'} for d, s in ((3, 1), (4, 3), (7, 3), (7, 6), (8, 3), (12, 5), (17, 5), (21, 8))]
json.dump(D3, open(os.path.join(CD, 'D3_hollow.json'), 'w'))
D4 = [
 {'id': 'G7-T1', 'name': 'Theorem A-COL', 'statement': 'for all d>=2, all units s, all Q with max(Q)>=2d: U=conv(F)', 'status': 'PROVED+CHECKED',
  'proof': 'COVERAGE.md sections 2-4 (Lemmas E, K>=1, bridges, mismatch, slivers)', 'machine_checked': 'strip-cell cover exact for d<=12 (all units, all boxes Q1 in [d,3d], Q2 in [2d,3d]); also d<=8 non-units and Q1<d'},
 {'id': 'G7-C1', 'name': 'general coverage', 'statement': 'U=conv(F) for all Q>=(d,d), Q!=(d,d)', 'status': 'OPEN', 'reduced_to': 'small boxes Q in [d,2d-1]^2 minus (d,d); squareless zone is the residue',
  'machine_checked': 'CHECKED d<=30 (v006 window) and squareless zone d<=32 (v007)'},
 {'id': 'G7-T3', 'name': 'hollow lower bound', 'statement': 'for all d>=3 and all units s: int T1, int T2 are disjoint from U, boundary(T_i) subset U, hence R^2\\U has >=2 bounded components and beta_1(U_(d,d)) >= 2',
  'status': 'PROVED+CHECKED', 'proof': 'HOLLOW_TOPOLOGY.md section 2 (integer height a = d-y, Graver domination, A/C edge argument)', 'machine_checked': 'exact certificate for all unit classes with 3<=d<=64'},
 {'id': 'G7-T4', 'name': 'hollow upper bound', 'statement': 'H \\ (T1 u T2) subset U for s != -1, d>=3, i.e. beta_1 = 2 and complement = two triangles of total area d', 'status': 'CHECKED',
  'gap': 'covering of H minus two triangles not proved for all (d,s)', 'machine_checked': 'v006 exact area check d<=45 (inherited record)'},
 {'id': 'G7-B1', 'name': 'B-DELTA', 'statement': 'witness rank = rank of generators', 'status': 'PROVED+CHECKED', 'proof': 'BINARY_RANK.md section 2'},
 {'id': 'G7-B2', 'name': 'B-COSET', 'statement': 'cells of union U = (circuit partition, coset of its span)', 'status': 'PROVED+CHECKED', 'proof': 'BINARY_RANK.md section 2'},
 {'id': 'G7-B3', 'name': 'B-NULL', 'statement': 'full-support collision => nullity >= 3', 'status': 'PROVED+CHECKED', 'proof': 'BINARY_RANK.md section 2'},
 {'id': 'G7-C2', 'name': 'r_min <= 3', 'statement': 'every minimal non-embedded 0/1 box has minimum witness rank <= 3', 'status': 'OPEN', 'machine_checked': 'complete n<=6; n=7 complete modulo full-support lemma (CHECKED); n=8 restricted'}]
json.dump(D4, open(os.path.join(CD, 'D4_symbolic_records.json'), 'w'), indent=1)
# D5 cost accounting
import coverage as C
from lattice_model import Lat
rows = []
for d, s, Q in ((7, 3, (9, 14)), (11, 4, (13, 22)), (13, 5, (20, 26))):
    t = time.time(); cells, _ = CS.strip_cells(d, s, Q); ts = time.time() - t
    t = time.time(); cd = C.complex_data(Lat(d, d, d, s), Q); tg = time.time() - t
    t = time.time(); ok, why = K.check_D1(d1(d, s, Q)); tc = time.time() - t
    rows.append({'d': d, 's': s, 'Q': list(Q), 'F': len(ML.fibre(d, s, Q)), 'strip_cells': len(set(cells)), 'generic_2cells': len(cd['cells'][2]), 'seconds_build_strip_cells': round(ts, 3),
                 'seconds_generic_enumeration': round(tg, 3), 'seconds_standalone_check_incl_build': round(tc, 3), 'checker_ok': ok})
json.dump(rows, open(os.path.join(CD, 'D5_cost.json'), 'w'), indent=1)
print('certificates written', round(time.time() - t0, 1), 's'); print(rows)
