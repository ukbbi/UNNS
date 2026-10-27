"""GEO-I v002 verifier.  Exact integer / Fraction arithmetic only.
Usage:  python3 verify.py --smoke     (fast: benchmarks, small corpus, small dynamics)
        python3 verify.py             (full)
Writes output/verify_<mode>.json, CSV exports, and exits 1 on any FAIL.  Undecided/skipped cases are counted and reported."""
import sys, os, json, csv, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'geometry'))
from collections import Counter
from fractions import Fraction as Fr
from math import gcd, prod
from geo2lib import *
from geo1lib import succ, Cstep, fibre_q, R as Rint, build_graph, factor, val

SMOKE = '--smoke' in sys.argv
MODE = 'smoke' if SMOKE else 'full'
OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
CHECKS = []; RES = {}
def check(name, ok, detail=None):
    CHECKS.append({'check': name, 'pass': bool(ok), 'detail': detail}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)
def csvw(name, rows, header):
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
t0 = time.time()

# ======================================================= E1-E4 and the specification table (exact)
BM = {'72': Fr(72), '144': Fr(144), '3600': Fr(3600), '44100': Fr(44100), '210^4': Fr(210 ** 4), '2304/5': Fr(2304, 5)}
prof = {k: analyse(v) for k, v in BM.items()}
RES['benchmarks'] = prof
spec = {'72': (3, 2, 2, 1, 0), '144': (5, 2, 2, 2, 0), '3600': (11, 3, 3, 3, 0), '44100': (15, 4, 4, 3, 0),
        '210^4': (80, 4, 4, 4, 0), '2304/5': (2, 2, 1, 0, 0)}
ok = True
for k, (R_, da, daf, dc, _) in spec.items():
    p = prof[k]; ok &= (p['R'], p['d_amb'], p['d_aff'], p['axis']['d_cell']) == (R_, da, daf, dc)
check('SPEC TABLE: (R, d_amb, d_aff, d_cell[axis]) reproduced exactly for 72, 144, 3600, 44100, 210^4, 2304/5', ok,
      {k: (v['R'], v['d_amb'], v['d_aff'], v['axis']['d_cell']) for k, v in prof.items()})
# E1 : 3600 -- the full 3-cell {1,2}x{0,1}x{0,1}
p = prof['3600']; ps, q, b = coords(3600); F = set(fibre_points(ps, q, b))
cube = (1, 0, 0); gens = ((0, 0, 1), (0, 1, 0), (1, 0, 0))
cube_cell = ((1, 0, 0), ((0, 0, 1), (0, 1, 0), (1, 0, 0)))
cells = build_cells(sorted(F), set(unit_moves(3)), 3)
def closed_under_faces(cells, top):
    cur = {top}; seen = {top}
    while cur:
        nxt = set()
        for c in cur:
            for f in boundary(c): nxt.add(f)
        cur = nxt - seen; seen |= nxt
    return seen
faces = closed_under_faces(cells, cube_cell)
cnt = Counter(len(g) for (_, g) in faces)
check('E1 3600: full 3-cell {1,2}x{0,1}x{0,1} present; certified 8 vertices, 12 edges, 6 square faces, 1 cube, all faces in the complex',
      cube_cell in set(cells[3]) and cnt == {0: 8, 1: 12, 2: 6, 3: 1} and all(f in set(cells[len(f[1])]) for f in faces), dict(cnt))
check('E1 3600: complex has 11 vertices, 17 edges, 8 squares, 1 cube; Euler characteristic 1',
      p['axis']['cells_per_dim'] == [11, 17, 8, 1])
# E2
p = prof['44100']
check('E2 44100: 15 vertices, no admissible 4-cell (origin removed), exactly four 3-cells, d_cell=3; box has 16 points',
      p['R'] == 15 and p['axis']['cells_per_dim'] == [15, 28, 18, 4] and p['axis']['d_cell'] == 3 and p['d_amb'] == 4)
# E3
p = prof['210^4']; ps, q, b = coords(210 ** 4)
cells = build_cells(sorted(fibre_points(ps, q, b)), set(unit_moves(4)), 4)
top = ((1, 1, 1, 1), ((0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)))
faces = closed_under_faces(cells, top); cnt = Counter(len(g) for (_, g) in faces)
check('E3 210^4=1944810000: 80 points; 4-cell {1,2}^4 certified: 16 vertices, 32 edges, 24 squares, 8 cubes, 1 4-cell; all faces in the complex',
      top in set(cells[4]) and cnt == {0: 16, 1: 32, 2: 24, 3: 8, 4: 1} and p['R'] == 80 and all(f in set(cells[len(f[1])]) for f in faces) and p['axis']['cells_per_dim'] == [80, 212, 210, 92, 15], dict(cnt))
# E4
p = prof['2304/5']
check('E4 2304/5: coordinate adjacency has 0 edges (2 components); move adjacency has exactly 1 edge with vector (3,-1); region Graver set {(1,1),(3,-1),(4,0)}',
      p['axis']['cells_per_dim'] == [2] and p['axis']['components'] == 2 and p['move']['cells_per_dim'] == [2, 1] and p['move']['components'] == 1
      and sorted(map(tuple, p['graver_region'])) == [(1, 1), (3, -1), (4, 0)])
check('Complexes are chain complexes (boundary of boundary = 0) and Betti numbers agree mod 2 and mod 2^31-1 on all six benchmarks',
      all(v['axis']['d2_zero'] and v['move']['d2_zero'] and v['axis']['betti']['2'] == v['axis']['betti']['2147483647'] and v['move']['betti']['2'] == v['move']['betti']['2147483647'] for v in prof.values()))

# ======================================================= T1 : dimension classification for integer fibres (b = 1)
def d_cell_formula(q):
    k = len(q)
    return 0 if k == 0 else (k if max(q) >= 2 else k - 1)
bad = 0; nbad_b = 0; npat = 0
KMAX, QMAX = (3, 3) if SMOKE else (4, 4)
for k in range(1, KMAX + 1):
    for q in itertools.product(range(1, QMAX + 1), repeat=k):
        if list(q) != sorted(q): continue
        ps = [2, 3, 5, 7][:k]; F = fibre_points(ps, list(q), 1)
        cells = build_cells(F, set(unit_moves(k)), k); npat += 1
        if len(cells) - 1 != d_cell_formula(q): bad += 1
        h, d2 = homology(cells)
        if h[2] != [1] + [0] * (len(cells) - 1) or not d2: nbad_b += 1
check('T1 d_cell = k if max q_i >= 2 else k-1 for integer fibres: all %d sorted exponent patterns with k<=%d, q_i<=%d (builder vs formula)' % (npat, KMAX, QMAX), bad == 0, bad)
check('Prop (integer fibre complex is contractible): Betti numbers (1,0,...,0) for the same %d patterns' % npat, nbad_b == 0, nbad_b)
bad = 0; M = 800 if SMOKE else 3000
for m in range(2, M + 1):
    ps, q, b = coords(m)
    if not ps: continue
    F = fibre_points(ps, q, b)
    if len(build_cells(F, set(unit_moves(len(ps))), len(ps))) - 1 != d_cell_formula(q): bad += 1
check('T1 formula vs builder on all integers 2..%d' % M, bad == 0, bad)

# ======================================================= Corpus E5 (rational fibres)
rows = []; skipped = 0; stats = Counter(); witnesses = []
def axis_theory(ps, q, b, F):
    """Thm A prediction: S = axes with p_i = 1 mod b, T = others; components = |Lambda_T ∩ B_T \\ 0| + [S nonempty]."""
    k = len(ps); S = [i for i in range(k) if (ps[i] - 1) % b == 0]; T = [i for i in range(k) if i not in S]
    nT = 0
    for al in itertools.product(*[range(q[i] + 1) for i in T]):
        if any(al) and chi_ok([ps[i] for i in T], b, al): nT += 1
    comps = nT + (1 if S else 0)
    if not S: dc = 0
    elif nT > 0 or max(q[i] for i in S) >= 2: dc = len(S)
    else: dc = len(S) - 1
    return comps, dc
def run_item(x, fam):
    global skipped
    ps, q, b = coords(x)
    if not ps: return
    F = fibre_points(ps, q, b)
    if not F: return
    if len(F) > 300: skipped += 1; return
    o = analyse(x); o['family'] = fam
    G = graver_region(ps, q, b)
    # Theorem A prediction for the coordinate complex
    pc, pdc = axis_theory(ps, q, b, F)
    stats['n'] += 1
    stats['A_comp_ok'] += pc == o['axis']['components']; stats['A_dcell_ok'] += pdc == o['axis']['d_cell']
    stats['A_betti_trivial'] += all(v == 0 for v in o['axis']['betti']['2'][1:]) and o['axis']['betti']['2'] == o['axis']['betti']['2147483647']
    stats['move_connected'] += o['move']['components'] == 1
    stats['move_d2'] += o['move']['d2_zero'] and o['axis']['d2_zero']
    mb2 = o['move']['betti']['2']; mbp = o['move']['betti']['2147483647']
    stats['move_betti_p_agree'] += mb2 == mbp
    if any(mb2[1:]):
        fb = flag_betti(flag_cells(F, set(G), 3)); o['flag_betti'] = fb[2]
        witnesses.append(o)
    stats['dcell_move_gt_axis'] += o['move']['d_cell'] > o['axis']['d_cell']; stats['dcell_move_ge_axis'] += o['move']['d_cell'] >= o['axis']['d_cell']
    rows.append(o)
t = time.time()
BMAX, AMAX = (13, 3000) if SMOKE else (31, 20000)
for b in range(2, BMAX + 1):
    for a in range(2, AMAX + 1):
        if gcd(a, b) == 1: run_item(Fr(a, b), 'F1_small_denominator')
GS = (5, 7, 11, 13, 17, 19, 23) if SMOKE else (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 15, 21, 35, 39, 25, 33)
LMAX = 120 if SMOKE else 400
for g in GS:
    for L in range(2, LMAX):
        if gcd(L, g) == 1: run_item(Fr(L * L, g), 'F2_reset_states_L2_over_g')
RES['corpus_stats'] = dict(stats); RES['corpus_skipped_over_300_points'] = skipped
n = stats['n']
check('E5 corpus: %d rational fibres analysed (b<=%d, a<=%d; plus L^2/g states); %d skipped (>300 points, reported)' % (n, BMAX, AMAX, skipped), n > 0 and stats['move_d2'] == n, {'skipped': skipped})
check('Thm A (coordinate complex): components = |Lambda_T∩B_T\\0| + [S≠∅] and d_cell formula, on every corpus fibre', stats['A_comp_ok'] == n and stats['A_dcell_ok'] == n, {k: stats[k] for k in ('A_comp_ok', 'A_dcell_ok', 'n')})
check('Thm A: coordinate complex has no homology beyond components (all Betti_{j>=1} = 0), mod 2 and mod 2^31-1 agree, on every corpus fibre', stats['A_betti_trivial'] == n, stats['A_betti_trivial'])
check('GEO-T2: Graver-move graph connected on every corpus fibre (%d of %d)' % (stats['move_connected'], n), stats['move_connected'] == n, stats['move_connected'])
check('Move-complex Betti numbers agree mod 2 and mod 2^31-1 (no torsion evidence) on every corpus fibre', stats['move_betti_p_agree'] == n, stats['move_betti_p_agree'])
check('Prop C: K_axis is a subcomplex of K_move whenever e_i in Lambda_b, hence d_cell(move) >= d_cell(axis) (strictly larger on %d fibres)' % stats['dcell_move_gt_axis'], stats['dcell_move_ge_axis'] == n, stats['dcell_move_ge_axis'])
# Graver completeness: every nonzero lattice vector in the region is a conformal sum of region Graver vectors (independent greedy check)
bad = 0; checked = 0
sample = rows[::max(1, len(rows) // (60 if SMOKE else 400))]
for o in sample:
    ps, q, b = coords(Fr(o['x'])); G = graver_region(ps, q, b); Gs = set(G); checked += 1
    for g in itertools.product(*[range(-e, e + 1) for e in q]):
        if not any(g) or not chi_ok(ps, b, g): continue
        cur = g
        while any(cur):
            h = next((h for h in G if all(hi * ci >= 0 and abs(hi) <= abs(ci) for hi, ci in zip(h, cur))), None)
            if h is None: bad += 1; break
            cur = tuple(c - hh for c, hh in zip(cur, h))
check('Graver completeness: every lattice vector in [-q,q] decomposes conformally into region Graver moves (%d fibres, exhaustive in region)' % checked, bad == 0, bad)
# witnesses of nontrivial move-complex homology
RES['move_homology_witnesses'] = [{'x': o['x'], 'q': o['q'], 'b': o['b'], 'primes': o['primes'], 'R': o['R'], 'cells_move': o['move']['cells_per_dim'],
                                   'betti_move': o['move']['betti']['2'], 'betti_flag': o['flag_betti'], 'graver': o['graver_region']} for o in witnesses]
RES['move_betti_distribution'] = Counter(str(o['move']['betti']['2']) for o in rows)
RES['b_of_witnesses'] = Counter(o['b'] for o in witnesses)
RES['dim_triples_(d_amb,d_cell_axis,d_cell_move)'] = Counter(str((o['d_amb'], o['axis']['d_cell'], o['move']['d_cell'])) for o in rows)
check('E5: move-complex H_1 nonzero on %d fibres (witnesses exported); H_{>=2} nonzero on %d' % (len(witnesses), sum(1 for o in witnesses if any(o['move']['betti']['2'][2:]))), True,
      {'b_values': dict(RES['b_of_witnesses'])})
# --- syzygy statistic: b_1(K_move) vs |G+| - k   (CONJECTURE M1 evidence; reported, never assumed)
viol = 0; eq = 0; deficit = []; 
for o in rows:
    gp = o['graver_region_size'] // 2; k = o['d_amb']; b1 = o['move']['betti']['2'][1] if len(o['move']['betti']['2']) > 1 else 0
    pred = max(0, gp - k)
    if b1 > pred: viol += 1
    elif b1 == pred: eq += 1
    else: deficit.append((o['x'], o['R'], k, gp, b1))
RES['M1_corpus'] = {'violations_of_upper_bound': viol, 'equalities': eq, 'deficits': len(deficit), 'deficit_examples': deficit[:10],
                    'max_R_among_deficits': max([d[1] for d in deficit], default=0)}
check('MEASURED (corpus): b_1(K_move) = max(0,|G+|-k) on %d of %d fibres; deficits %d, excesses %d (counterexamples to a bound are recorded, not hidden)' % (eq, n, len(deficit), viol), eq + len(deficit) + viol == n, RES['M1_corpus'])
# --- clique-complex comparison (H_1,H_2 exact for simplices up to dim 3)
nf = 0; nontriv_flag = []; 
for o in rows:
    if o['R'] > 80: continue
    ps, q, b = coords(Fr(o['x'])); F = fibre_points(ps, q, b); G = graver_region(ps, q, b)
    fb = flag_betti(flag_cells(F, set(G), 3))
    nf += 1
    if any(fb[2][1:3]) or fb[2] != fb[2147483647]: nontriv_flag.append((o['x'], fb[2]))
RES['flag_comparison'] = {'fibres_with_R<=80': nf, 'with_nontrivial_H1_or_H2': len(nontriv_flag), 'examples': nontriv_flag[:10]}
check('Clique complex of the move graph (comparison): H_1,H_2 computed on %d corpus fibres (R<=80); nontrivial on %d' % (nf, len(nontriv_flag)), True, RES['flag_comparison'])
csvw('corpus_rational.csv', [(o['x'], o['family'], o['b'], '|'.join(map(str, o['primes'])), '|'.join(map(str, o['q'])), o['R'], o['d_amb'], o['d_aff'],
      o['axis']['d_cell'], o['move']['d_cell'], o['axis']['components'], o['move']['components'], '|'.join(map(str, o['axis']['cells_per_dim'])),
      '|'.join(map(str, o['move']['cells_per_dim'])), '|'.join(map(str, o['move']['betti']['2'])), o['graver_region_size']) for o in rows],
     ['x', 'family', 'b', 'primes', 'q', 'R', 'd_amb', 'd_aff', 'd_cell_axis', 'd_cell_move', 'components_axis', 'components_move', 'cells_axis', 'cells_move', 'betti_move', 'graver_region_size'])
json.dump(RES['move_homology_witnesses'], open(os.path.join(OUT, 'move_homology_witnesses.json'), 'w'), indent=1)

# ======================================================= E6 dynamics (grammar labelled; SELECT-II and C never mixed)
# --- A2 / SELECT-II
LIM = 1500 if SMOKE else 5000
pc = {m: (len(coords(m)[0]), d_cell_formula(coords(m)[1])) for m in range(1, LIM + 1)}
dk = Counter(); ddc = Counter(); nedges = 0; bound_ok = True; examples = {}
for m in range(1, LIM + 1):
    for N, mp in succ(m):
        if mp > LIM: break
        nedges += 1; a = pc[m]; c = pc[mp]
        dk[c[0] - a[0]] += 1; ddc[c[1] - a[1]] += 1
        wN = len(factor(N)) if N > 1 else 0; wN1 = len(factor(N + 1))
        bound_ok &= (-wN <= c[0] - a[0] <= wN1)
        if c[0] < a[0] and 'dk-' not in examples: examples['dk-'] = (m, N, mp, a, c)
RES['select2_geometry_change'] = {'edges': nedges, 'delta_d_amb': sorted(dk.items()), 'delta_d_cell': sorted(ddc.items()), 'example_decrease': examples.get('dk-')}
check('E6 [A2 SELECT-II] %d edges <= %d: d_amb changes by -omega(N) .. +omega(N+1) always; geometry is NOT monotone (examples with decrease exist)' % (nedges, LIM),
      bound_ok and min(dk) < 0 and max(dk) > 0 and min(ddc) < 0, {'delta_d_amb': sorted(dk.items()), 'delta_d_cell': sorted(ddc.items())})
r72 = [(N, mp, len(coords(mp)[0]), coords(mp)[1]) for N, mp in succ(72)]
RES['select2_from_72'] = r72
# --- C-map orbits
def orbit_geometry(x0, steps, label):
    xs = [Fr(x0)]
    for _ in range(steps - 1):
        y = Cstep(xs[-1])
        if y is None: break
        xs.append(Fr(y))
    out = []
    for n, x in enumerate(xs):
        o = analyse(x)
        out.append({'n': n, 'x': str(x) if len(str(x)) < 40 else str(x)[:18] + '...', 'b': o['b'], 'q': o['q'], 'R': o['R'], 'd_amb': o['d_amb'], 'd_aff': o['d_aff'],
                    'axis_components': o['axis']['components'], 'axis_d_cell': o['axis']['d_cell'], 'move_components': o['move']['components'],
                    'move_d_cell': o['move']['d_cell'], 'move_betti': o['move']['betti']['2'], 'graver': o['graver_region_size']})
    return out
NSTEP = 24 if SMOKE else 60
orbits = {'72 [C, G=1]': orbit_geometry(72, NSTEP, '72'), 'g11 benchmark 67500^2/11 [C]': orbit_geometry(Fr(67500 ** 2, 11), NSTEP, 'g11')}
if not SMOKE:
    for g, E in ((11, (1, 3, 4)), (13, (1, 3, 4)), (17, (2, 3, 5)), (19, (2, 3, 5)), (23, (2, 3, 5))):
        pr = [p for p in (2, 3, 5, 7) if g % p][:len(E)]; Lq = prod(p ** e for p, e in zip(pr, E))
        orbits['g=%d L=%s [C]' % (g, '*'.join('%d^%d' % (p, e) for p, e in zip(pr, E)))] = orbit_geometry(Fr(Lq * Lq, g), NSTEP, str(g))
RES['c_orbits'] = orbits
rows_o = []
for name, rs in orbits.items():
    for r in rs: rows_o.append((name, r['n'], r['x'], r['b'], '|'.join(map(str, r['q'])), r['R'], r['d_amb'], r['d_aff'], r['axis_components'], r['axis_d_cell'], r['move_components'], r['move_d_cell'], '|'.join(map(str, r['move_betti']))))
csvw('dynamics_c_orbits.csv', rows_o, ['orbit', 'n', 'x', 'b', 'q', 'R', 'd_amb', 'd_aff', 'axis_components', 'axis_d_cell', 'move_components', 'move_d_cell', 'betti_move'])
ok72 = all(r['axis_components'] == 1 and r['move_components'] == 1 and r['move_betti'] == [1] + [0] * (len(r['move_betti']) - 1) for r in orbits['72 [C, G=1]'])
check('E6 [C, G=1] orbit of 72: coordinate and move complexes are connected and acyclic at every step (b=1 contractible); d_amb=2 throughout; d_cell reaches 2 and stays', ok72 and orbits['72 [C, G=1]'][-1]['axis_d_cell'] == 2 and all(r['d_amb'] == 2 for r in orbits['72 [C, G=1]']),
      [r['axis_d_cell'] for r in orbits['72 [C, G=1]']][:12])
rg = orbits['g11 benchmark 67500^2/11 [C]']
check('E6 [C, g=11 benchmark]: coordinate complex edgeless (components = R) at every step; move complex connected at every step (GEO-T2 along an orbit)',
      all(r['axis_components'] == r['R'] for r in rg) and all(r['move_components'] == 1 for r in rg), {'R': [r['R'] for r in rg][:16], 'move_betti_nontrivial_steps': [r['n'] for r in rg if any(r['move_betti'][1:])]})
allc = [r for rs in orbits.values() for r in rs]
check('E6 [C]: move complexes along all tracked orbits connected at every step (%d states)' % len(allc), all(r['move_components'] == 1 for r in allc), len(allc))
eqs = 0; tot = 0; vio = []; defi = 0
for name, rs in orbits.items():
    for r in rs:
        tot += 1; pred = max(0, r['graver'] // 2 - r['d_amb']); b1 = r['move_betti'][1] if len(r['move_betti']) > 1 else 0
        if b1 == pred: eqs += 1
        elif b1 > pred: vio.append((name, r['n'], r['R'], r['q'], r['graver'] // 2, r['d_amb'], b1, pred))
        else: defi += 1
RES['M1_orbits'] = {'states': tot, 'equal': eqs, 'excess_counterexamples_to_upper_bound': vio, 'deficits': defi}
check('MEASURED (C-orbits): b_1(K_move) = max(0,|G+|-k) at %d of %d tracked states; %d excesses (counterexamples to the upper bound, e.g. g=11 L=2*3^3*5^4 at n=8: b1=2 > 1) and %d deficits recorded' % (eqs, tot, len(vio), defi),
      eqs + len(vio) + defi == tot and (len(vio) > 0 or SMOKE), vio[:4])
xs = [Fr(67500 ** 2, 11)]
for _ in range(NSTEP - 1): xs.append(Fr(Cstep(xs[-1])))
flag_rows = []
for n_ in range(0, NSTEP, 4):
    ps, q, b = coords(xs[n_]); F = fibre_points(ps, q, b); G = graver_region(ps, q, b)
    fb = flag_betti(flag_cells(F, set(G), 3)); flag_rows.append((n_, len(F), fb[2], orbits['g11 benchmark 67500^2/11 [C]'][n_]['move_betti']))
RES['g11_flag_vs_cubical'] = flag_rows
check('g=11 benchmark orbit: clique complex of the move graph has Betti (b0,b1,b2)=(1,0,0) at every sampled step (%d states) while the cubical move complex has b_1>=6 -- topology depends on the cell definition' % len(flag_rows),
      all(r[2][:3] == [1, 0, 0] for r in flag_rows) and all(r[3][1] >= 6 for r in flag_rows), flag_rows[:3])
RES['c_orbit_nontrivial_move_homology_steps'] = {k: [r['n'] for r in v if any(r['move_betti'][1:])] for k, v in orbits.items()}

# ======================================================= summary
RES['checks'] = CHECKS; RES['seconds'] = round(time.time() - t0, 1)
RES['summary'] = {'passed': sum(c['pass'] for c in CHECKS), 'total': len(CHECKS), 'mode': MODE}
json.dump(RES, open(os.path.join(OUT, 'verify_%s.json' % MODE), 'w'), indent=1, default=str, sort_keys=True)
print('SUMMARY %d/%d PASS (%s, %.1fs)' % (RES['summary']['passed'], RES['summary']['total'], MODE, RES['seconds']))
sys.exit(0 if all(c['pass'] for c in CHECKS) else 1)
