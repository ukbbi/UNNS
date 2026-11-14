"""Independent verification for UNNS_GRAPH_GEOMETRY_v001.  Usage: python3 verify_graph_geometry.py [--quick]"""
import json, sys, csv, time, random, hashlib, re
from fractions import Fraction
from math import isqrt
import sympy as sp
from paths import *
from ugraph import *

QUICK = '--quick' in sys.argv
R = {}   # report
T0 = time.time()
def rec(key, ok, detail=''):
    R[key] = {'pass': bool(ok), 'detail': detail}
    print(('PASS ' if ok else 'FAIL ') + key + ' ' + str(detail)[:150], flush=True)

# ---------- helpers for polynomial path identities
t = sp.symbols('t')
def P(s): return sp.sympify(s, locals={'t': t})
def shifted_nonneg(poly, t0):
    u = sp.symbols('u'); q = sp.Poly(sp.expand(poly.subs(t, t0 + u)), u)
    return all(c >= 0 for c in q.all_coeffs()) and q.eval(0) >= 1
def intcoeffs(poly):
    return all(c.is_integer for c in sp.Poly(sp.expand(poly), t).all_coeffs())

def certify(n_expr, steps, t0, target):
    """steps: list of (sign, N_expr).  Returns (ok, states) ; states symbolic."""
    s = P(n_expr); states = [sp.expand(s)]
    for sign, Ne in steps:
        N = P(Ne)
        if not (intcoeffs(N) and shifted_nonneg(sp.Poly(sp.expand(N), t).as_expr(), t0)): return False, 'label'
        den = N if sign == '+' else (N + 1) ** 2
        c = sp.cancel(s / den)
        num, dd = sp.fraction(sp.together(c))
        if dd.free_symbols or dd != 1 and not dd.is_number: return False, 'cof-not-poly'
        c = sp.expand(c)
        if not (intcoeffs(c) and shifted_nonneg(c, t0)): return False, 'cof'
        s = sp.expand(c * ((N + 1) ** 2 if sign == '+' else N))
        states.append(s)
    return sp.expand(s - P(target)) == 0, states

def replay(n_expr, steps, tv, expect):
    x = int(P(n_expr).subs(t, tv))
    for sign, Ne in steps:
        N = int(P(Ne).subs(t, tv)); x = move(x, sign, N)
    return x == expect

# ================= C1 definitions: neighbours = brute force, two engines
ok = True
for x in range(1, 1500):
    a = nbrs(x); b = nbrs_trial(x)
    # literal definition: y adjacent iff exists k,N with {kN,k(N+1)^2} = {x,y}
    c = set()
    for N in range(1, x + 1):
        if x % N == 0: c.add(x // N * (N + 1) ** 2)
    q = 2
    while q * q <= x:
        if x % (q * q) == 0: c.add(x // (q * q) * (q - 1))
        q += 1
    ok &= (a == b == c)
# second check: definition scan of all pairs among small vertices
V = 400
E_def = {(x, y) for x in range(1, V) for y in range(x + 1, V) if is_edge_def(x, y)}
E_nb = {(x, y) for x in range(1, V) for y in nbrs(x) if x < y < V}
ok &= (E_def == E_nb)
rec('C1_neighbours_three_ways', ok, f'x<1500 two engines+definition; all pairs <{V}: {len(E_def)} edges')

# ================= C2 degree formula, structure
ok = True; Dmax = 20000 if not QUICK else 3000
dist3 = False; selfloop = False; fi = fo = 0
for x in range(1, Dmax):
    nb = nbrs(x)
    if len(nb) != degree_formula(x): ok = False
    if len(nb) == 3: dist3 = True
    if x in nb: selfloop = True
    f = {x // N * (N + 1) ** 2 for N in divisors(x)}
    if len(f) != len(divisors(x)): ok = False
    if any(y <= x for y in f): ok = False
    i = {x // (q * q) * (q - 1) for q in square_roots(x)}
    if len(i) != len(square_roots(x)) or any(y >= x for y in i): ok = False
ok &= (not dist3) and (not selfloop)
# primes degree 2, deg(1)=1
ok &= len(nbrs(1)) == 1 and nbrs(1) == {4}
ok &= all(nbrs(p) == {4 * p, (p + 1) ** 2} for p in sp.primerange(2, Dmax))
rec('C2_degree_formula_and_prime_rigidity', ok, f'x<{Dmax}')

# ================= C3 triangle-free, edge ratio, cycles, odd girth
ok = True
for x in range(1, Dmax // 2 if not QUICK else 1500):
    nb = nbrs(x)
    for y in nb:
        for z in nbrs(y):
            if z != x and z in nb: ok = False
rec('C3a_no_triangle_search', ok, 'no triangle with a vertex <' + str(Dmax // 2 if not QUICK else 1500))
# symbolic triangle argument: r_a r_b = r_c  ==> a+b = (t-1)(1-ct) <= 0 ; verify the algebra
a_, b_, c_, tt = sp.symbols('a b c t', positive=True)
# with h = c t, ab = c t^2 and (a+1)(b+1) = t (c+1):  a+b = t(c+1) - 1 - ab = t c + t - 1 - c t^2
expr = sp.expand(t_ := (tt * (c_ + 1) - 1 - c_ * tt ** 2) - (tt - 1) * (1 - c_ * tt))
rec('C3b_triangle_identity', expr == 0, 'a+b = t(c+1)-1-ct^2 = (t-1)(1-ct)')
# the quadratic constraint (t-1)(1-ct) >0 impossible for t>=1,c>=1 integers, a+b>=2:
ok = all((tv - 1) * (1 - cv * tv) <= 0 for tv in range(1, 300) for cv in range(1, 300))
rec('C3c_sign_check', ok, 't,c<300 (also analytic: t>=1,c>=1 => (t-1)(1-ct)<=0)')
def is_cycle(vs):
    L = len(vs); return len(set(vs)) == L and all(vs[(i + 1) % L] in nbrs(vs[i]) for i in range(L))
rec('C3d_4cycle_5cycle', is_cycle([2, 8, 36, 9]) and is_cycle([6, 24, 96, 784, 27]), '2-8-36-9 ; 6-24-96-784-27')
# girth / odd girth lower bounds by exhaustive local search: no 3-cycle (above) ; no 5-cycle needed; check no even... compute shortest odd cycle through small vertices
def shortest_cycle_through(v, maxlen):
    # BFS layers from v; odd cycle exists of length 2d+1 if an edge joins two vertices at same layer d
    dist = {v: 0}; front = [v]; best = None
    for d in range(1, maxlen):
        nxt = []
        for m in front:
            for w in nbrs(m):
                if w not in dist: dist[w] = d; nxt.append(w)
        # same-layer edge among 'front' nodes at level d-1 ... check after building layer
        front = nxt
        lay = [m for m in front]
        S = set(lay)
        for m in lay:
            for w in nbrs(m):
                if w in S and best is None: best = 2 * d + 1
        if best: break
    return best
og = [shortest_cycle_through(v, 4) for v in (6, 27, 96, 784, 24)]
rec('C3e_odd_girth_witness', all(o == 5 for o in og), 'BFS odd-cycle detection through each vertex of the 5-cycle: ' + str(og))

# ================= C4 successor identities: symbolic + replay + coverage + distances
U1 = json.load(open(f'{INH}/u1_identities.json'))
ok = True; info = []
for idn in U1:
    steps = [(('+' if s['direction'] == 'forward' else '-'), s['N']) for s in idn['steps']]
    n_expr = idn['n']; t0 = idn['t_min']
    good, _ = certify(n_expr, steps, t0, f'({n_expr})+1')
    rep = all(replay(n_expr, steps, tv, int(P(n_expr).subs(t, tv)) + 1) for tv in range(t0, t0 + (60 if not QUICK else 10)))
    ok &= good and rep and len(steps) <= 6
    info.append((idn['name'], len(steps), good, rep))
rec('C4a_successor_identities_symbolic_and_replay', ok, str(info))
# coverage of n>=1 by the 9 classes plus exceptional n=1,3
cov = {}
for idn in U1:
    m = idn['modulus']; r = idn['residue']
    for n in range(1, 4000):
        if n % m == r and (n - r) // m >= idn['t_min']: cov.setdefault(n, []).append(idn['name'])
miss = [n for n in range(1, 4000) if n not in cov]
rec('C4b_residue_cover', miss == [1, 3] or sorted(miss) == [1, 3], f'uncovered n<4000: {miss}')
exc1 = [1, 4, 18, 81, 8, 2]; exc3 = [3, 16, 4]
rec('C4c_exceptional_walks', all(b in nbrs(a) for a, b in zip(exc1, exc1[1:])) and all(b in nbrs(a) for a, b in zip(exc3, exc3[1:])), '1,4,18,81,8,2 ; 3,16,4')
# exact successor distances
Nsucc = 2500 if not QUICK else 300
inh = {int(r['n']): int(r['d_n_n_plus_1']) for r in csv.DictReader(open(f'{INH}/u1_successor_distance_table.csv'))}
dsucc = {}; bad = []
for n in range(1, Nsucc + 1):
    dsucc[n] = distance(n, n + 1, 6)
    if dsucc[n] is None or dsucc[n] < 2 or dsucc[n] > 6: bad.append(n)
    if n in inh and inh[n] != dsucc[n]: bad.append(('mismatch', n))
rec('C4d_exact_successor_distances', not bad and max(dsucc.values()) == 6, f'n<={Nsucc}; max {max(dsucc.values())}; bad {bad[:5]}; first 6 at {min(n for n in dsucc if dsucc[n]==6)}')
cnt = {}; [cnt.__setitem__(v, cnt.get(v, 0) + 1) for v in dsucc.values()]
R['succ_distribution'] = {'N': Nsucc, 'counts': cnt, 'mean': sum(dsucc.values()) / Nsucc}
json.dump(dsucc, open(f'{DATA}/successor_distances_independent.json', 'w'))
# lower-bound certificate d(163,164)=6
B3 = ball(163, 3); B2 = ball(164, 2)
rec('C4e_lower_bound_163_164', not (set(B3) & set(B2)), f'|B3(163)|={len(B3)} |B2(164)|={len(B2)} disjoint; path length 6 exists: {distance(163,164,6)==6}')
R['ball_sizes_163_164'] = [len(B3), len(B2)]
# consecutive integers never adjacent
rec('C4f_consecutive_nonadjacent', all(n + 1 not in nbrs(n) for n in range(1, 20000)), 'n<20000 ; analytic: ratio >=4')

# ================= C5 squares
SQ = json.load(open(f'{INH}/u2sq_square_identities.json'))
ok = True; info = []
for r in range(24):
    c = SQ['classes'][str(r)]; steps = [(sg, e) for sg, e in c['steps']]
    n_expr = f'24*t+{r}'
    s0 = f'(24*t+{r})**2'; target = f'(24*t+{r}+1)**2'
    good, _ = certify(s0, steps, c['t0'], target)
    rep = all(replay(s0, steps, tv, (24 * tv + r + 1) ** 2) for tv in range(c['t0'], c['t0'] + (40 if not QUICK else 8)))
    ok &= good and rep and len(steps) <= 5
    info.append((r, len(steps), good, rep))
rec('C5a_24_square_identities', ok, f'all 24: symbolic+replay; lengths {sorted(set(i[1] for i in info))}')
sp_ = SQ['special']
okp = all(b in nbrs(a) for v in sp_.values() for a, b in zip(v['path'], v['path'][1:]))
rec('C5b_square_exceptions', okp, str({k: v['path'] for k, v in sp_.items()}))
covered = set()
for r in range(24):
    t0 = SQ['classes'][str(r)]['t0']
    for n in range(1, 3000):
        if n % 24 == r and (n - r) // 24 >= t0: covered.add(n)
miss = [n for n in range(1, 3000) if n not in covered]
rec('C5c_square_cover', miss == [1, 2, 3], f'uncovered {miss}')
dsq = {}
Nsq = 150 if not QUICK else 40
inhsq = {int(r['n']): int(r['d_sq']) for r in csv.DictReader(open(f'{INH}/u2sq_square_distance_table.csv'))}
for n in range(1, Nsq + 1):
    dsq[n] = distance(n * n, (n + 1) ** 2, 5)
bad = [n for n in dsq if dsq[n] is None or (n in inhsq and inhsq[n] != dsq[n])]
rec('C5d_exact_square_distances', not bad and max(dsq.values()) == 5, f'n<={Nsq}; max 5 at n={min(n for n in dsq if dsq[n]==5)}')
B2a = ball(529, 2); B2b = ball(576, 2)
rec('C5e_lower_bound_23sq_24sq', not (set(B2a) & set(B2b)) and distance(529, 576, 5) == 5, f'|B2(529)|={len(B2a)} |B2(576)|={len(B2b)}')
R['ball_sizes_529_576'] = [len(B2a), len(B2b)]
json.dump(dsq, open(f'{DATA}/square_distances_independent.json', 'w'))
path_sq = geodesic(529, 576, 5); R['path_529_576'] = path_sq
rec('C5f_sq_path_529_576', [label_of(a, b) for a, b in zip(path_sq, path_sq[1:])] and len(path_sq) == 6, str(path_sq))

# ================= C6 scaling & power lifting & doubling
ok = True; random.seed(7)
for _ in range(400):
    x = random.randint(1, 400); y = random.choice(list(nbrs(x)))
    m = random.randint(1, 50)
    ok &= (m * y in nbrs(m * x))
rec('C6a_scaling_preserves_edges', ok, '400 random edges x 50 multipliers')
ok = True
for _ in range(300):
    x = random.randint(1, 300); y = random.choice(list(nbrs(x))); k = random.randint(1, 6)
    ch = [x ** (k - j) * y ** j for j in range(k + 1)]
    ok &= all(b in nbrs(a) for a, b in zip(ch, ch[1:])) and len(set(ch)) == k + 1
rec('C6b_power_chain', ok, '300 random edges, k<=6')
ok = True; Nd = 1500 if not QUICK else 200
for n in range(1, 31):
    ok &= distance(n, 2 * n, 5) is not None and distance(n, 2 * n, 5) <= 5
ok &= distance(1, 2, 5) == 5 and set(ball(1, 2)).isdisjoint(ball(2, 2)) and set(ball(1,2)) == {1,4,16,18,25}
rec('C6c_doubling', ok, 'd(n,2n)<=5 for n<=30 ; d(1,2)=5; B2(1)={1,4,16,18,25} disjoint from B2(2) (|B2(2)|=%d)' % len(ball(2, 2)))
ok = True
for _ in range(60):
    a = random.randint(1, 60); b = random.randint(a + 1, a + 8); m = random.randint(2, 6)
    da = distance(a, b, 8); db = distance(m * a, m * b, 8)
    if da is not None and db is not None: ok &= db <= da
    elif da is not None and db is None: ok = False
rec('C6d_scaling_nonexpanding_distance', ok, '60 random (a,b,m): d(ma,mb)<=d(a,b)')
ok = True
for _ in range(25):
    x = random.randint(1, 40); y = random.randint(x + 1, x + 4); k = random.randint(2, 3)
    d1 = distance(x, y, 7)
    if d1 is None: continue
    d2 = distance(x ** k, y ** k, k * d1)
    ok &= d2 is not None and d2 <= k * d1
rec('C6e_power_lifting_distance', ok, '25 samples, exact distances')

ok = True; d1j = {}
for j in range(2, 13): d1j[j] = distance(1, j, 9)
for j in range(2, 9):
    for n in (2, 3, 5, 7):
        dd = distance(n, j * n, 9); ok &= dd is not None and dd <= d1j[j]
R['d_1_j'] = d1j
json.dump(d1j, open(f'{DATA}/d_1_j.json', 'w'))
rec('C6f_multiples_bound', ok and d1j[11] == 6, 'd(n,jn)<=d(1,j) for j<=8, n in {2,3,5,7}; d(1,j) table stored')

# ================= C7 primes
ok = True
for p in sp.primerange(2, 100000): ok &= nbrs(p) == {4 * p, (p + 1) ** 2}
rec('C7a_prime_neighbours', ok, 'p<100000')
ok = True
ps = list(sp.primerange(2, 400))
for p, q in zip(ps, ps[1:]):
    d = distance(p, q, 9); nb_p, nb_q = nbrs(p), nbrs(q)
    best = min(distance(u, v, 9) for u in nb_p for v in nb_q if distance(u, v, 9) is not None) + 2
    ok &= (d == best)
rec('C7b_prime_distance_reduction', ok, 'consecutive primes <400: d(p,q)=2+min d(u,v)')
d61 = distance(61, 67, 8); rec('C7c_d_61_67', d61 == 7 and set(ball(61, 3)).isdisjoint(ball(67, 3)), f'd={d61}; |B3(61)|={len(ball(61,3))}, |B3(67)|={len(ball(67,3))} disjoint')
R['d_61_67'] = d61
t1 = time.time(); d661 = distance(661, 673, 8)
rec('C7d_d_661_673', d661 == 8, f'd={d661}; |B4(661)|={len(ball(661,4))} |B3(673)|={len(ball(673,3))}; {time.time()-t1:.0f}s')
R['d_661_673'] = d661
R['ball_sizes_661_673'] = [len(ball(661, 4)), len(ball(673, 3))]
pdist = {}
for p, q in zip(ps, ps[1:]): pdist[p] = distance(p, q, 9)
R['prime_distance_range_p_lt_400'] = [min(pdist.values()), max(pdist.values())]
json.dump({str(k): v for k, v in pdist.items()}, open(f'{DATA}/prime_distances_lt400.json', 'w'))

# ================= C8 Fibonacci
CC = json.load(open(f'{INH}/u2fpsym_class_certificates.json'))
a, b = sp.symbols('a b')
def elem(pair, eps):
    return sp.expand(sp.sympify(pair[0], locals={'b': b}) + sp.sympify(pair[1], locals={'b': b}) * a)
def red(expr, eps):
    return sp.rem(sp.expand(expr), a ** 2 + a * b - b ** 2 - eps, a)
ok = True; info = []
for r in range(12):
    c = CC[str(r)]; eps = c['eps']
    S = [elem(p, eps) for p in c['states_ring']]; Nn = [elem(p, eps) for p in c['labels_ring']]
    sg = [x[0] for x in c['labels']]
    cc = a + b
    if r % 2 == 0: x0, y0 = b * (2 * a + b), b ** 2 + cc ** 2
    else: x0, y0 = b ** 2 + cc ** 2, cc * (a + 3 * b)
    good = red(S[0] - x0, eps) == 0 and red(S[-1] - y0, eps) == 0 and len(S) == len(Nn) + 1
    for i, (s_prev, s_new, N_, sgn) in enumerate(zip(S, S[1:], Nn, sg)):
        if sgn == '+': e = s_new * N_ - s_prev * (N_ + 1) ** 2
        else: e = s_new * (N_ + 1) ** 2 - s_prev * N_
        good &= red(e, eps) == 0
    ok &= good; info.append((r, len(Nn), good))
rec('C8a_fibonacci_ring_certificates', ok, f'12 classes, identities in Q[b][a]/(a^2+ab-b^2-eps); lengths {[i[1] for i in info]}')
R['fib_lengths'] = {i[0]: i[1] for i in info}
# numeric replay from F_k alone using ring labels
F = [0, 1]
Kmax = 1500 if not QUICK else 200
for _ in range(Kmax + 3): F.append(F[-1] + F[-2])
ok = True; maxlen = 0; steps_checked = 0
for k in range(20, Kmax):
    r = k % 12; c = CC[str(r)]; h = k // 2
    A, B = F[h - 1], F[h]; x = F[k]
    for sg_, pair in zip([l[0] for l in c['labels']], c['labels_ring']):
        p0 = Fraction(str(sp.Rational(sp.sympify(pair[0], locals={'b': b}).subs(b, B)))) if False else None
        N_ = sp.sympify(pair[0], locals={'b': b}).subs(b, B) + sp.sympify(pair[1], locals={'b': b}).subs(b, B) * A
        if not (N_.is_integer and N_ >= 1): ok = False; break
        N_ = int(N_)
        try: x = move(x, sg_, N_)
        except AssertionError: ok = False; break
        steps_checked += 1
    ok &= (x == F[k + 1]); maxlen = max(maxlen, len(c['labels']))
rec('C8b_fibonacci_replay', ok and maxlen == 12, f'20<=k<{Kmax}: every step legal, ends at F_(k+1); {steps_checked} steps; max length {maxlen}')
SM = json.load(open(f'{INH}/u2fpsym_small_fib_paths.json'))
ok = True; ds = {}
for k in range(2, 30):
    pth = SM[str(k)]['path']
    ok &= pth[0] == F[k] and pth[-1] == F[k + 1] and all(y in nbrs(x) for x, y in zip(pth, pth[1:])) and len(pth) - 1 == SM[str(k)]['d']
    ds[k] = SM[str(k)]['d']
rec('C8c_small_fibonacci_paths', ok, f'k=2..29 stored paths are paths; max stored length {max(ds.values())}')
# independent exact distances for small k
t1 = time.time(); exact = {}
kk = range(2, 26 if not QUICK else 14)
for k in kk:
    exact[k] = distance(F[k], F[k + 1], 6)
okx = all(exact[k] == ds[k] for k in kk)
rec('C8d_small_fibonacci_exact', okx, f'k<{max(kk)+1}: independent exact distances equal stored; {time.time()-t1:.0f}s')
R['fib_exact_small'] = exact

# ================= C9 hand proof of the k = 4 (mod 12) family
a, b = sp.symbols('a b'); eps = 1
cas = a**2 + a*b - b**2 - eps
x = b*(2*a + b); y = b**2 + (a + b)**2; c_ = a + b; H = a + 3*b; Lh = 2*a + b
ids = [x + 1 - a*H + cas, c_*Lh - (y + 1) - cas, H**2 - (x + 3*y - 2) + 2*cas, Lh**2 - (2*y - x + 2) - 2*cas, a*(H**2 + 4) - c_*(Lh**2 + 1) + (3*a - b)*cas]
ok = all(sp.expand(e) == 0 for e in ids)
cert4 = CC['4']; Nn = [elem(p, 1) for p in cert4['labels_ring']]
ok &= red(Nn[2] - (x + 3*y - 2)/4, 1) == 0 and red(Nn[3] - (2*y - x + 2), 1) == 0 and red(Nn[4] - y, 1) == 0 and red(Nn[1] - x, 1) == 0
rec('C9_hand_proof_family_k4', ok, 'five expansions of Thm famA are polynomial identities modulo Cassini; labels agree with certified class 4')

R['elapsed_sec'] = time.time() - T0
R['all_pass'] = all(v['pass'] for k, v in R.items() if isinstance(v, dict) and 'pass' in v)
json.dump(R, open(f'{REP}/verification_report.json', 'w'), indent=1, default=str)
print('ALL PASS' if R['all_pass'] else 'FAILURES', f'{time.time()-T0:.0f}s')
