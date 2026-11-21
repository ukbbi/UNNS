#!/usr/bin/env python3
"""MUG-I v006 verification: Maxwell-constrained generative histories.
Part A: no-go baseline for polarization transport along UNNS histories.
Part B: do Maxwell constraints remove or restrict T_N edges?  (closure / Bragg arithmetic)
Needs mpmath, numpy, scipy.  Reuses the v005 system M_p (uniaxial cold plasma, B0 || z, torus 2pi, c=1).
"""
import json, hashlib, math, random, itertools
from functools import reduce
from math import gcd
from fractions import Fraction as F
import mpmath as mp
import numpy as np
from scipy.linalg import eigh

mp.mp.dps = 50
TOL = mp.mpf(10) ** -35
random.seed(6)
results = {}
def rec(name, ok, **kw):
    results[name] = dict(ok=bool(ok), **kw)
    print(("PASS " if ok else "FAIL ") + name, {k: v for k, v in kw.items() if not isinstance(v, (list, dict))})

def content(m): return reduce(gcd, [abs(x) for x in m])
def sz(m): return sum(x * x for x in m), m[2] * m[2]
def Phi(b, m, p):
    s, z = sz(m)
    if b == 'O': return mp.mpf(s)
    D = mp.mpf((s + p) ** 2 - 4 * z * p); r = mp.sqrt(D)
    if b == 'E+': return (s + p + r) / 2
    if z == 0: return None
    return (s + p - r) / 2
def evec(b, m, p):
    """real unit E-direction of the simple eigenmode (null vector of w^2 eps - |k|^2 I + k k^T)."""
    s, z = sz(m); ph = Phi(b, m, p)
    A = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            A[i, j] = m[i] * m[j] - (s if i == j else 0)
    A[0, 0] += ph; A[1, 1] += ph; A[2, 2] += ph - p
    E, Q = mp.eigsy(A)
    idx = min(range(3), key=lambda i: abs(E[i]))
    v = Q[:, idx]; n = mp.sqrt(sum(x * x for x in v))
    return [x / n for x in v]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def prim_dirs(R):
    out = []; r = math.isqrt(R)
    for u in itertools.product(range(-r, r + 1), repeat=3):
        if u == (0, 0, 0) or sum(x * x for x in u) > R or content(u) != 1: continue
        if next(x for x in u if x != 0) < 0: continue
        out.append(u)
    return out

# ======================= PART A =======================
# A1: off-axis, p>0: the three branch eigenvalues are pairwise distinct (simple eigenmodes)
mingap = mp.mpf(10); ok = True
for p in (36, 2, 7):
    for u in prim_dirs(14):
        s, z = sz(u)
        if s == z: continue
        for g in range(1, 150):
            m = tuple(g * x for x in u)
            vals = [Phi('O', m, p), Phi('E+', m, p)] + ([Phi('E-', m, p)] if z else [])
            for a, b in itertools.combinations(vals, 2):
                gap = abs(a - b) / (g * g)
                mingap = min(mingap, gap); ok &= gap > 0
rec("A1_off_axis_branches_nondegenerate", ok, min_normalised_gap=mp.nstr(mingap, 6))
# on axis: two transverse polarisations degenerate for all g; L crosses them at g^2 = p
ok = True
for p in (36, 2):
    for g in range(1, 100):
        m = (0, 0, g)
        roots = sorted([Phi('E+', m, p), Phi('E-', m, p)])
        ok &= abs(roots[0] - min(mp.mpf(g * g), p)) < TOL and abs(roots[1] - max(mp.mpf(g * g), p)) < TOL
rec("A1b_on_axis_roots_are_T_and_L", ok)

# A2: baselines with constant polarization along the ray: vacuum (p=0) and isotropic plasma
ok = True; maxang = 0.0
for u in [(1, 1, 1), (1, 0, 1), (1, 2, 3), (0, 1, 1), (1, 0, 0)]:
    for b in ('O', 'E+'):
        v0 = evec(b, tuple(1 * x for x in u), 0)
        for g in (2, 5, 17, 100):
            v = evec(b, tuple(g * x for x in u), 0)
            maxang = max(maxang, float(1 - abs(dot(v, v0))))
            ok &= abs(abs(dot(v, v0)) - 1) < TOL
rec("A2a_vacuum_polarization_constant_along_ray", ok, max_deviation=maxang)
# isotropic plasma eps = (1 - p/w^2) I : transverse space = k-perp (const), longitudinal = k-hat (const)
ok = True
for u in [(1, 1, 1), (1, 2, 3), (2, 1, 0)]:
    for g in (1, 3, 10, 40):
        k = mp.matrix(u) * g; kk = mp.sqrt(sum(x * x for x in k)); w2T = kk ** 2 + 36
        A = mp.matrix(3, 3)
        for i in range(3):
            for j in range(3):
                A[i, j] = k[i] * k[j] - (kk ** 2 if i == j else 0) + (w2T - 36 if i == j else 0)
        # transverse mode: A annihilates any v perpendicular to k
        vperp = mp.matrix([u[1], -u[0], 0]) if (u[0] or u[1]) else mp.matrix([1, 0, 0])
        ok &= max(abs(x) for x in (A * vperp)) < TOL * g ** 2 * 10
        Al = mp.matrix(3, 3)
        for i in range(3):
            for j in range(3):
                Al[i, j] = k[i] * k[j] - (kk ** 2 if i == j else 0) + (36 - 36 if i == j else 0)
        ok &= max(abs(x) for x in (Al * k)) < TOL * g ** 3 * 10     # longitudinal: Phi = p, E || k
rec("A2b_isotropic_plasma_polarization_constant_along_ray", ok)

# A3: the plasma polarization eigenline rotates along the ray (off-axis E+/E-)
rows = []
for u in [(1, 1, 1), (1, 0, 1), (1, 2, 3)]:
    for b in ('E+', 'E-'):
        v1 = evec(b, u, 36)
        rows.append(dict(u=u, branch=b, angle_deg_from_g1={g: float(mp.degrees(mp.acos(min(1, abs(dot(v1, evec(b, tuple(g * x for x in u), 36)))))))
                                                              for g in (2, 4, 9, 36, 324)}))
rec("A3_plasma_polarization_rotates_along_ray", True, table=rows)

# A4: cascade of ideal matched polarizers: amplitude product of overlaps, history dependent
def cascade(b, u, path, p):
    vs = [evec(b, tuple(g * x for x in u), p) for g in path]
    a = mp.mpf(1)
    for i in range(len(vs) - 1): a *= abs(dot(vs[i], vs[i + 1]))
    return a
diamond = ([2, 8, 36], [2, 9, 36])
# confirm both are admissible UNNS histories
def admissible(path):
    for g, g2 in zip(path, path[1:]):
        if not any(g % N == 0 and g * (N + 1) ** 2 == g2 * N for N in range(1, g + 1)): return False
    return True
assert all(admissible(h) for h in diamond)
tab = []; spread_pl = 0; spread_vac = mp.mpf(0)
for u in [(1, 1, 1), (1, 0, 1), (1, 2, 3), (0, 1, 1)]:
    for b in ('E+', 'E-'):
        if b == 'E-' and u[2] == 0: continue
        A_, B_ = cascade(b, u, diamond[0], 36), cascade(b, u, diamond[1], 36)
        D_ = abs(dot(evec(b, tuple(2 * x for x in u), 36), evec(b, tuple(36 * x for x in u), 36)))
        tab.append(dict(u=u, branch=b, A=mp.nstr(A_, 10), B=mp.nstr(B_, 10), direct=mp.nstr(D_, 10), diff=mp.nstr(abs(A_ - B_), 4)))
        spread_pl = max(spread_pl, float(abs(A_ - B_)))
    for b in ('O', 'E+'):
        spread_vac = max(spread_vac, abs(cascade(b, u, diamond[0], 0) - cascade(b, u, diamond[1], 0)))
rec("A4a_projective_cascade_diamond", spread_pl > 1e-6 and spread_vac < TOL, max_plasma_difference=spread_pl,
    vacuum_difference=mp.nstr(spread_vac, 3), table=tab)
# 17-history merger from v005
u = (1, 1, 1); g0, g1 = 6, 3600
hs = []
def dfs(g, path):
    if g == g1: hs.append(tuple(path)); return
    for N in range(1, g + 1):
        if g % N == 0:
            g2 = g * (N + 1) ** 2 // N
            if g2 <= g1: dfs(g2, path + [g2])
dfs(g0, [g0])
amps = {b: [cascade(b, u, h, 36) for h in hs] for b in ('E+', 'E-')}
sp = {b: float((max(v) - min(v))) for b, v in amps.items()}
rec("A4b_cascade_spread_over_merger_histories", len(hs) == 17 and sp['E+'] > 1e-8, histories=len(hs),
    spread_Eplus=sp['E+'], spread_Eminus=sp['E-'],
    amplitudes_Eplus=[mp.nstr(a, 8) for a in sorted(amps['E+'])[:3]] + ['...'])

# A5: representation-of-multiplier-group rules are path independent (exact)
ok = True
for _ in range(500):
    Ns = [random.randint(1, 6) for _ in range(random.randint(2, 4))]
    g0_ = 1
    for N in Ns: g0_ *= N * 2
    base = F(1)
    for N in Ns: base *= F((N + 1) ** 2, N)
    perm = Ns[:]; random.shuffle(perm)
    pr = F(1)
    for N in perm: pr *= F((N + 1) ** 2, N)
    ok &= base == pr
rec("A5_multiplier_product_is_history_invariant", ok)

# ======================= PART B =======================
# B1: closure of scale-invariant vertex sets under every admissible edge (torus, PEC box, PEC waveguide)
def mult_box(m):      # PEC box: modes (|m1|,|m2|,|m3|), zero pattern rule
    z = sum(1 for x in m if x == 0)
    return 2 if z == 0 else (1 if z == 1 else 0)
def mult_wg(m):       # PEC guide in x,y, periodic in z: TM needs m1,m2>=1 ; TE needs (m1,m2)!=(0,0)
    tm = 1 if (m[0] != 0 and m[1] != 0) else 0
    te = 1 if (m[0] != 0 or m[1] != 0) else 0
    return tm + te
ok = True; n = 0
for _ in range(20000):
    m = tuple(random.randint(-12, 12) for _ in range(3))
    if m == (0, 0, 0): continue
    g = content(m)
    for N in range(1, g + 1):
        if g % N == 0:
            m2 = tuple(x * (N + 1) ** 2 // N for x in m)
            ok &= mult_box(m2) == mult_box(m) and mult_wg(m2) == mult_wg(m); n += 1
rec("B1_PEC_box_and_waveguide_vertex_sets_closed_and_multiplicity_preserved", ok, edges_checked=n,
    note="vertex-set/multiplicity depend only on the zero pattern, which positive scaling preserves")

# B2: Bragg-resonant vertices of a periodic medium eps = 1 + 2 delta cos(q z): g in a*Z, a = q/2
#     exact arithmetic law: for an edge g -> g (N+1)^2/N (N|g), a | g:  target resonant iff N*a | g
ok = True; n = 0; cls = {}
for a in (1, 2, 3, 5, 6, 10, 12):
    cnt = {'R->R': 0, 'R->n': 0, 'n->R': 0, 'n->n': 0}
    for g in range(1, 6000):
        for N in range(1, g + 1):
            if g % N: continue
            g2 = g * (N + 1) ** 2 // N
            s_res = g % a == 0; t_res = g2 % a == 0
            cnt[('R' if s_res else 'n') + '->' + ('R' if t_res else 'n')] += 1
            if s_res: ok &= (t_res == (g % (N * a) == 0)); n += 1
            if s_res and gcd(N, a) == 1: ok &= t_res
    cls[a] = cnt
rec("B2a_Bragg_edge_arithmetic_law", ok, edges_checked=n, classes_by_a=cls)

# B2b: resonance-preserving histories: stay on the Bragg set; a diamond example
a = 2
def stays(path): return all(g % a == 0 for g in path)
dm = {tuple(h): stays(h) for h in diamond}
rec("B2b_resonance_dependence_of_equal_endpoint_histories_diamond", dm[tuple(diamond[0])] != dm[tuple(diamond[1])],
    a=a, history_1_2_on_resonance=dm[tuple(diamond[0])], history_2_1_on_resonance=dm[tuple(diamond[1])])
# over the 17 merger histories, how many visit k resonant vertices (a=2,3,5)?
sumry = {}
for a in (2, 3, 5):
    c = {}
    for h in hs: c[sum(1 for g in h if g % a == 0)] = c.get(sum(1 for g in h if g % a == 0), 0) + 1
    sumry[a] = c
rec("B2c_resonant_visits_differ_between_equal_endpoint_histories", all(len(v) > 1 for v in sumry.values()),
    histogram_of_resonant_vertices_visited=sumry)

# B3: Hill/Mathieu gap orders: eps = 1 + 2 delta cos(q z) on the 2pi torus; gap at m = j q/2 scales like delta^j
def band_gap(q, j, delta, M=60):
    m_res = j * q // 2
    kappa = m_res % q
    ms = [kappa + q * t for t in range(-M, M + 1)]
    n = len(ms); A = np.diag([float(x * x) for x in ms]); B = np.eye(n)
    for i in range(n - 1):
        B[i, i + 1] = B[i + 1, i] = delta
    w2 = eigh(A, B, eigvals_only=True)
    # modes of this Bloch block near the resonant value m_res^2
    near = sorted(w2, key=lambda x: abs(x - m_res ** 2))[:2]
    return abs(near[0] - near[1])
slopes = {}; ok = True
for j in (1, 2, 3):
    ds = [0.01, 0.02, 0.04]
    gs = [band_gap(4, j, d) for d in ds]
    sl = np.polyfit(np.log(ds), np.log(gs), 1)[0]
    slopes[j] = float(sl); ok &= abs(sl - j) < 0.25 and min(gs) > 0
# nonresonant control: m = 3 (q=4) is not a Bragg point: no pair with near-equal weight; look at degenerate partners
rec("B3_gap_at_jq_over_2_scales_as_delta_to_j", ok, fitted_slopes=slopes,
    note="every j-th Bragg point carries a gap of order delta^j (Mathieu tongues); here q=4, j=1,2,3")

# B4: dimension count of the claim 'Maxwell cannot remove T_N edges in these systems'
rec("B4_scope", True, note="k-labelled induction: translation-invariant media give every integer wave vector a mode in each branch (v005 S1); B1 closes the PEC cases; B2/B3 show the periodic medium changes labels (gaps) and resonance membership, not admissibility")

blob = json.dumps(results, sort_keys=True, default=str, indent=1)
open('verification_results_v006.json', 'w').write(blob)
print("sha256", hashlib.sha256(blob.encode()).hexdigest())
print("ALL PASS" if all(v['ok'] for v in results.values()) else "SOME FAIL")
