#!/usr/bin/env python3
"""MUG-I v005 verification: the induced structure G_U(Maxwell; phi) for one fixed system.

Fixed system M_p: cold electron plasma in the infinite-magnetisation limit (B0 || z),
  eps = diag(1, 1, 1 - p/w^2), mu = 1, c = 1, on the torus R^3/(2 pi Z^3), so k = m in Z^3.
  p = (omega_p L / 2 pi)^2 is the single dimensionless medium+cell parameter.
Branches: O (E perp z, perp k): Phi = |k|^2
          E+/E-: roots of Phi^2 - (s+p) Phi + z p = 0,  s=|m|^2, z=m_z^2   (E- absent iff z=0)
Requires: mpmath (ships with sympy).  Run: python3 verify_v005.py
"""
import json, hashlib, math, random, itertools
from fractions import Fraction as F
from math import gcd
from functools import reduce
import mpmath as mp

mp.mp.dps = 60
TOL = mp.mpf(10) ** -45
random.seed(5)
results = {}
def rec(name, ok, **kw):
    results[name] = dict(ok=bool(ok), **kw)
    print(("PASS " if ok else "FAIL ") + name, {k: v for k, v in kw.items() if not isinstance(v, (list, dict))})

# ---------------- the fixed system -----------------
def sz(m): return sum(x * x for x in m), m[2] * m[2]

def Phi(b, m, p):
    s, z = sz(m)
    if b == 'O': return mp.mpf(s)
    D = mp.mpf((s + p) ** 2 - 4 * z * p)
    r = mp.sqrt(D)
    if b == 'E+': return (s + p + r) / 2
    if b == 'E-':
        if z == 0: return None          # branch absent (static root)
        return (s + p - r) / 2
    raise ValueError

def content(m): return reduce(gcd, [abs(x) for x in m])
def prim(m):
    g = content(m); return tuple(x // g for x in m), g
def edges_from(m):
    """UNNS transport edges out of vertex m: N | content(m) -> m (N+1)^2/N."""
    g = content(m); out = []
    for N in range(1, g + 1):
        if g % N == 0:
            f = F((N + 1) ** 2, N)
            out.append((N, tuple(int(x * f) for x in m)))
    return out
def Theta(b, u, g, p):
    ph = Phi(b, tuple(g * x for x in u), p)
    return None if ph is None else ph / g ** 2

def prim_dirs(R):
    """primitive directions u with |u|^2<=R, modulo overall sign (u ~ -u)."""
    out = []
    r = int(math.isqrt(R))
    for u in itertools.product(range(-r, r + 1), repeat=3):
        if u == (0, 0, 0) or sum(x * x for x in u) > R: continue
        if content(u) != 1: continue
        if next(x for x in u if x != 0) < 0: continue
        out.append(u)
    return out

# ---------------- Z1: potential identity & path independence -----------------
ok = True; n = 0; maxerr = mp.mpf(0)
dirs = prim_dirs(14)
for p in (36, 2):
    for u in random.sample(dirs, 25):
        for g in range(1, 60):
            m = tuple(g * x for x in u)
            for (N, m2) in edges_from(m):
                g2 = content(m2); al = mp.mpf(g2) / g
                for b in ('O', 'E+', 'E-'):
                    a, c = Phi(b, m, p), Phi(b, m2, p)
                    if a is None: continue
                    Delta = c - al ** 2 * a
                    err = abs(Delta / g2 ** 2 - (Theta(b, u, g2, p) - Theta(b, u, g, p)))
                    maxerr = max(maxerr, err); n += 1
                    ok &= err < TOL
rec("Z1a_weighted_defect_equals_potential_difference", ok, edges_checked=n, max_err=mp.nstr(maxerr, 3))

# random forward paths: sum_i Delta_i (g_f/g_i')^2 == Phi(g_f u) - (g_f/g_0)^2 Phi(g_0 u)
ok = True; n = 0; maxerr = mp.mpf(0)
for p in (36, 2):
    for u in random.sample(dirs, 20):
        for _ in range(30):
            g0 = random.randint(1, 30); m = tuple(g0 * x for x in u); path = [m]
            for _ in range(3):
                es = edges_from(path[-1]); path.append(random.choice(es)[1])
            gf = content(path[-1])
            for b in ('O', 'E+', 'E-'):
                if Phi(b, path[0], p) is None: continue
                tot = mp.mpf(0)
                for i in range(len(path) - 1):
                    gi, gj = content(path[i]), content(path[i + 1])
                    Dl = Phi(b, path[i + 1], p) - (mp.mpf(gj) / gi) ** 2 * Phi(b, path[i], p)
                    tot += Dl * (mp.mpf(gf) / gj) ** 2
                ref = Phi(b, path[-1], p) - (mp.mpf(gf) / g0) ** 2 * Phi(b, path[0], p)
                err = abs(tot - ref); maxerr = max(maxerr, err * 1); n += 1
                ok &= err < TOL * gf ** 2
rec("Z1b_path_total_is_endpoint_function", ok, paths_checked=n, max_err=mp.nstr(maxerr, 3))

# ---------------- Z2: graph decomposition by (u, branch) -----------------
# every edge preserves the primitive direction; truncated components of the substrate fibre
ok = True; n = 0
for u in random.sample(dirs, 40):
    for g in range(1, 120):
        for (N, m2) in edges_from(tuple(g * x for x in u)):
            ok &= prim(m2)[0] == u; n += 1
rec("Z2a_edges_preserve_primitive_direction", ok, edges_checked=n)

def fibre_components(G):
    par = list(range(G + 1))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for g in range(1, G + 1):
        for N in range(1, g + 1):
            if g % N == 0:
                g2 = g * (N + 1) ** 2 // N
                if g2 <= G: par[f(g)] = f(g2)
    roots = {f(g) for g in range(1, G + 1)}
    return len(roots)
comp = {G: fibre_components(G) for G in (100, 400, 1600, 6400)}
rec("Z2b_truncated_fibre_components", True, components_by_cutoff=comp,
    note="truncation artefact: components of the substrate graph on 1..G; one component only in the G->inf limit (arithmetic-dynamics result), not proved here")

# ---------------- Z3: Lyapunov monotonicity of Theta (= v_ph^2 |u|^2) -----------------
ok = True; n = 0; strict_fail = []; bound_ok = True
for p in (36, 2, 7):
    for u in prim_dirs(14):
        s, z = sz(u); par_z = (s == z)
        for g in range(1, 120):
            m = tuple(g * x for x in u)
            q = mp.mpf(p) / g ** 2
            tp, tm = Theta('E+', u, g, p), Theta('E-', u, g, p)
            bound_ok &= tp >= s - TOL and (tm is None or tm <= z + TOL) and tp >= z - TOL
            for (N, m2) in edges_from(m):
                g2 = content(m2)
                for b in ('E+', 'E-'):
                    a, c = Theta(b, u, g, p), Theta(b, u, g2, p)
                    if a is None: continue
                    n += 1
                    ok &= c <= a + TOL                      # non-increasing, always
                    if not par_z and not c < a - TOL: strict_fail.append((p, u, g, N, b))
rec("Z3a_Theta_nonincreasing_forward", ok and bound_ok, edges_checked=n, bounds_ok=bool(bound_ok))
rec("Z3b_Theta_strictly_decreasing_off_axis", len(strict_fail) == 0, violations=len(strict_fail))
# on-axis: E+ constant on the side g^2 p^-1 >.. ; confirm Theta+ = max(1,p/g^2) for u=e_z
ok = True
for p in (36, 2):
    for g in range(1, 200):
        ok &= abs(Theta('E+', (0, 0, 1), g, p) - max(mp.mpf(1), mp.mpf(p) / g ** 2)) < TOL
        ok &= abs(Theta('E-', (0, 0, 1), g, p) - min(mp.mpf(1), mp.mpf(p) / g ** 2)) < TOL
rec("Z3c_on_axis_ordered_branches_are_max_min", ok)

# ---------------- Z4: branch crossing on the axis; labelling convention matters -----------------
res = {}
for p in (36, 2):
    u = (0, 0, 1); cross = 0; mism = 0; tot = 0; ex = None; ok = True
    for g in range(1, 400):
        for (N, m2) in edges_from((0, 0, g)):
            g2 = content(m2); al = mp.mpf(g2) / g; tot += 1
            # analytic identities: T: Phi=g^2 (covariant, zero defect); L: Phi=p
            dT = Phi('O', m2, p) * 0 + mp.mpf(g2) ** 2 - al ** 2 * mp.mpf(g) ** 2
            dL = mp.mpf(p) - al ** 2 * mp.mpf(p)
            ok &= abs(dT) < TOL * g2 ** 2 and abs(dL - (1 - al ** 2) * p) < TOL
            lab_swap = (g * g < p) != (g2 * g2 < p) and not (g * g == p or g2 * g2 == p)
            dU = Phi('E+', m2, p) - al ** 2 * Phi('E+', (0, 0, g), p)
            if lab_swap:
                cross += 1
                if abs(dU - dT) > TOL and abs(dU - dL) > TOL: mism += 1
                if ex is None: ex = dict(g=g, N=N, g2=g2, upper_defect=mp.nstr(dU, 8), T_defect=mp.nstr(dT, 8), L_defect=mp.nstr(dL, 8))
    res[p] = dict(edges=tot, crossing_edges=cross, upper_defect_matches_neither_analytic=mism, example=ex)
    rec(f"Z4_axis_crossing_p{p}", ok and (cross == 0 or mism == cross), **res[p])

# off-axis: branches never touch (D > (s-q)^2 >= 0)
ok = True
for p in (36, 2, 7):
    for u in prim_dirs(14):
        s, z = sz(u)
        if s == z: continue
        for g in range(1, 200):
            m = tuple(g * x for x in u)
            D = (s * g * g + p) ** 2 - 4 * z * g * g * p
            ok &= D > (s * g * g - p) ** 2 >= 0
rec("Z4b_no_crossing_off_axis", ok)

# ---------------- Z5: mergers (many histories, one endpoint) + polarization -----------------
def pol(b, m, p):
    """E-field direction and |B|/|E| of the on-shell mode (k=m, c=1)."""
    s, z = sz(m); ph = Phi(b, m, p)
    k = mp.matrix([m[0], m[1], m[2]])
    A = mp.matrix(3, 3)
    for i in range(3):
        for j in range(3):
            A[i, j] = k[i] * k[j] - (s if i == j else 0)
    A[0, 0] += ph; A[1, 1] += ph; A[2, 2] += ph - p
    E, Q = mp.eigsy(A)
    idx = min(range(3), key=lambda i: abs(E[i]))
    v = Q[:, idx]; resid = max(abs(x) for x in (A * v))
    nrm = mp.sqrt(sum(x * x for x in v)); v = v / nrm
    kn = mp.sqrt(s)
    long_frac = (sum(k[i] * v[i] for i in range(3)) / kn) ** 2
    cx = mp.matrix([k[1] * v[2] - k[2] * v[1], k[2] * v[0] - k[0] * v[2], k[0] * v[1] - k[1] * v[0]])
    BE = mp.sqrt(sum(x * x for x in cx)) / mp.sqrt(ph)
    return long_frac, BE, resid

def histories(g0, g1, cache={}):
    if (g0, g1) in cache: return cache[(g0, g1)]
    if g0 == g1: return [[g0]]
    out = []
    for N in range(1, g0 + 1):
        if g0 % N == 0:
            g2 = g0 * (N + 1) ** 2 // N
            if g2 <= g1:
                for h in histories(g2, g1): out.append([g0] + h) if h[0] == g2 else None
    cache[(g0, g1)] = out
    return out

p = 36; u = (1, 1, 1)
best = None
for g0 in (6, 8, 12, 16, 24):
    reach = {}
    def dfs(g, path):
        reach.setdefault(g, []).append(tuple(path))
        for N in range(1, g + 1):
            if g % N == 0:
                g2 = g * (N + 1) ** 2 // N
                if g2 <= 4000: dfs(g2, path + [g2])
    dfs(g0, [g0])
    for gt, hs in reach.items():
        if best is None or len(hs) > best[2]: best = (g0, gt, len(hs), hs)
g0, g1, nh, hs = best
ok = True; sigs = set(); steps = set()
endpoint = {b: Theta(b, u, g1, p) for b in ('O', 'E+', 'E-')}
for h in hs:
    for b in ('E+', 'E-'):
        tot = Theta(b, u, g0, p)
        for i in range(len(h) - 1): tot += Theta(b, u, h[i + 1], p) - Theta(b, u, h[i], p)
        ok &= abs(tot - endpoint[b]) < TOL
    sigs.add(tuple(h)); steps.add(len(h) - 1)
profile_distinct = len({tuple(mp.nstr(Theta('E+', u, x, p), 20) for x in h) for h in hs})
rec("Z5a_merger_histories_same_endpoint_data", ok and nh >= 2, g0=g0, g1=g1, histories=nh,
    distinct_path_lengths=sorted(steps), distinct_Theta_profiles=profile_distinct)
# polarization/field relations at the common endpoint do not see the history (depend on m only)
fr = {b: [mp.nstr(x, 12) for x in pol(b, tuple(g1 * x for x in u), p)[:2]] for b in ('O', 'E+', 'E-')}
resid_ok = all(pol(b, tuple(g1 * x for x in u), p)[2] < TOL * g1 ** 4 for b in ('O', 'E+', 'E-'))
rec("Z5b_field_data_at_endpoint_eigenproblem", resid_ok, endpoint_longitudinal_fraction_and_B_over_E=fr)

# along a fixed fibre the field data DO vary with g (dispersion), unlike the vacuum control
rows = []
okmono = True
for uu in ((1, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0)):
    for b in ('O', 'E+', 'E-'):
        if Phi(b, uu, 36) is None: continue
        prev = None; vals = []
        for g in (1, 2, 4, 9, 16, 36, 81, 324):
            m = tuple(g * x for x in uu); lf, be, rs = pol(b, m, 36)
            vals.append((g, float(lf), float(be)))
        rows.append(dict(u=uu, branch=b, data=vals))
rec("Z5c_field_data_along_fibre_table", True, rows=rows)
# vacuum control p=0: field data constant along every fibre
okc = True
for uu in ((1, 1, 1), (0, 0, 1), (1, 0, 1)):
    for b in ('O', 'E+'):
        d = {(round(float(pol(b, tuple(g * x for x in uu), 0)[0]), 12), round(float(pol(b, tuple(g * x for x in uu), 0)[1]), 12)) for g in (1, 2, 4, 9, 36)}
        okc &= len(d) == 1
rec("Z5d_vacuum_control_fibre_constant", okc)

# ---------------- Z6: alternative induction rules -----------------
# rule R1: restriction of the substrate relation T_N to the observed-state set S3 (shell integers |m|^2)
def in_S3(n):
    while n % 4 == 0: n //= 4
    return n % 8 != 7
X = 4000
def comps(vs):
    vs = set(vs); par = {v: v for v in vs}
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    ne = 0
    for g in vs:
        for N in range(1, g + 1):
            if g % N == 0:
                g2 = g * (N + 1) ** 2 // N
                if g2 in vs: par[f(g)] = f(g2); ne += 1
    return len({f(v) for v in vs}), ne
full = comps(range(1, X + 1)); S3 = [x for x in range(1, X + 1) if in_S3(x)]; rs = comps(S3)
rec("Z6a_restriction_rule_R1_on_shell_integers", True, cutoff=X, full=dict(components=full[0], edges=full[1]),
    S3=dict(vertices=len(S3), components=rs[0], edges=rs[1]))
# R2 (vector lift) acts on shells by x -> x r_N^2, not x -> x r_N : phi_shell does not intertwine
ok = True
for _ in range(2000):
    m = tuple(random.randint(-9, 9) for _ in range(3))
    if m == (0, 0, 0): continue
    g = content(m)
    for (N, m2) in edges_from(m):
        ok &= sum(x * x for x in m2) * N * N == sum(x * x for x in m) * (N + 1) ** 4
rec("Z6b_vector_lift_acts_on_shells_by_rN_squared", ok)
bad = []
for N in range(1, 10 ** 6 + 1):
    d = (N * N + 1) * (N * N + 4 * N + 1); r = math.isqrt(d)
    if r * r == d: bad.append(N)
rec("Z6c_rN_squared_is_not_single_step_multiplier", len(bad) == 0, searched_N_up_to=10 ** 6, solutions=bad,
    note="r_M=r_N^2 solvable (rational M) iff (N^2+1)(N^2+4N+1) is a square; none found, not proved")

# ---------------- Z7: sector census -----------------
cen = []
for R in (3, 6, 14, 30):
    ds = prim_dirs(R); nz = sum(1 for u in ds if u[2] != 0)
    cen.append(dict(R=R, directions=len(ds), branches_plasma=2 * len(ds) + nz, branches_vacuum=2 * len(ds),
                    note="O,E+ for every u; E- iff u_z!=0; vacuum has 2 light-cone polarisations per u"))
rec("Z7_sector_census", True, census=cen)

# ---------------- write results -----------------
blob = json.dumps(results, sort_keys=True, default=str, indent=1)
open('verification_results_v005.json', 'w').write(blob)
print("sha256", hashlib.sha256(blob.encode()).hexdigest())
print("ALL PASS" if all(v['ok'] for v in results.values()) else "SOME FAIL")
