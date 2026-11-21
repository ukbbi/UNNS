#!/usr/bin/env python3
"""MUG-I v003: which nesting-induced data are intrinsic to an electromagnetic field? Needs sympy (+mpmath). Exit 0 iff all pass."""
import json, sys, hashlib, random
from math import gcd, isqrt
from functools import reduce
from itertools import product
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parent.parent; (ROOT/"results").mkdir(exist_ok=True); random.seed(3); checks = {}
def record(n, ok, d): checks[n] = {"status": "PASS" if ok else "FAIL", "detail": d}; print(("PASS " if ok else "FAIL ")+n+" :: "+str(d)[:300])
G = lambda v: reduce(gcd, [abs(q) for q in v])
# X1: occurrence count R(n) = #{(M,N): M(N+1)^2/N = n} = #{d>=2 : d^2 | n}; changes under cell refinement n -> k n
def R_def(n): return sum(1 for N in range(1, n+1) for M in range(1, n+1) if M*(N+1)**2 == n*N)
def R(n): return sum(1 for d in range(2, isqrt(n)+1) if n % (d*d) == 0)
ok = all(R_def(n) == R(n) for n in range(1, 61)) and (R(1), R(2), R(4)) == (0, 0, 1)
changed = sum(1 for n in range(1, 61) for k in range(2, 13) if R(k*n) != R(n)); tot = 60*11
record("X1_occurrence_count_not_invariant_under_cell_refinement", ok and changed > 0, {"R(1),R(2),R(4)": (R(1), R(2), R(4)), "pairs_(n,k)_with_R(kn)!=R(n)": f"{changed}/{tot}"})
# X2: gcd content is invariant under GL3(Z) change of period-lattice basis; N | g iff field is periodic on the N-fold refined lattice; minimal-period cell gives g = 1
def unimod():
    A = sp.eye(3)
    for _ in range(6):
        i, j = random.sample(range(3), 2); E = sp.eye(3); E[i, j] = random.randint(-3, 3); A = E*A
    return A
ok2 = True
for _ in range(400):
    m = sp.Matrix([random.randint(-30, 30) for _ in range(3)])
    if all(q == 0 for q in m): continue
    A = unimod(); ok2 &= G(list(A*m)) == G(list(m)) and abs(A.det()) == 1
    g = G(list(m)); N = random.randint(1, 12)
    refined_periodic = all((m[i]*1) % N == 0 for i in range(3))   # field exp(2 pi i m.r/L) invariant under translation L e_i / N  <=> N | m_i
    ok2 &= refined_periodic == (g % N == 0)
    ok2 &= G([q//g for q in m]) == 1                               # relative to its own minimal cell content is 1
record("X2_content_is_GL3Z_invariant_and_equals_refinement_divisibility_and_is_trivial_in_own_minimal_cell", ok2, "g(psi;Lambda) intrinsic to (field, period lattice); g=1 when the cell is the field's own period lattice")
# X3: nesting commutes with duality rotation, time evolution and the Maxwell constraints; polarisation-blind
x, y, z, t = sp.symbols("x y z t", real=True); c, L, th = sp.symbols("c L theta", real=True); c = sp.Symbol("c", positive=True); L = sp.Symbol("L", positive=True)
def curl(E): return sp.Matrix([sp.diff(E[2], y)-sp.diff(E[1], z), sp.diff(E[0], z)-sp.diff(E[2], x), sp.diff(E[1], x)-sp.diff(E[0], y)])
def resid(E, B): return [sp.simplify(e) for e in list(curl(E)+sp.diff(B, t))+list(curl(B)-sp.diff(E, t)/c**2)]
n = 2; ph = 2*sp.pi*n*(z-c*t)/L
Ex = sp.Matrix([sp.cos(ph), 0, 0]); Bx = sp.Matrix([0, sp.cos(ph)/c, 0])           # x-polarised
Ey = sp.Matrix([0, sp.cos(ph), 0]); By = sp.Matrix([-sp.cos(ph)/c, 0, 0])          # y-polarised, same harmonic index
al = sp.Rational(9, 2); Tf = lambda F_: F_.subs({z: al*z, t: al*t}, simultaneous=True)
def duality(E, B): return (sp.cos(th)*E+sp.sin(th)*c*B, -sp.sin(th)*E/c+sp.cos(th)*B)
ok3 = True
for (E_, B_) in [(Ex, Bx), (Ey, By)]:
    D1 = duality(Tf(E_), Tf(B_)); D2 = duality(E_, B_); D2 = (Tf(D2[0]), Tf(D2[1]))
    ok3 &= sp.simplify(D1[0]-D2[0]) == sp.zeros(3, 1) and sp.simplify(D1[1]-D2[1]) == sp.zeros(3, 1)    # T o D = D o T
    ok3 &= all(e == 0 for e in resid(D2[0], D2[1])) and all(e == 0 for e in resid(Tf(E_), Tf(B_)))
    # time evolution: evolving the transported field by t equals transporting the field evolved by alpha t
    ok3 &= sp.simplify(Tf(E_).subs(t, t+1) - E_.subs({z: al*z, t: al*(t+1)}, simultaneous=True)) == sp.zeros(3, 1)
ip = lambda F1, F2: sp.simplify(sp.integrate(F1.dot(F2).subs(t, 0), (z, 0, L)))
ok3 &= ip(Ex, Ey) == 0 and ip(Tf(Ex), Tf(Ey)) == 0 and sp.simplify(ip(Ex, Ex)-ip(Tf(Ex), Tf(Ex))) == 0   # polarisations stay orthogonal, energy unchanged
record("X3_nesting_commutes_with_duality_time_evolution_and_is_polarisation_blind", ok3, "T o D = D o T, evolution intertwined, x- and y-polarised same-index waves transported with identical index data and preserved orthogonality")
# X4: box cavity vector structure: TE_z / TM_z families, multiplicity mu = 2 (no index zero), 1 (one zero), 0 (two zeros); constant along T_N rays
a_, b_, d_ = sp.Rational(1), sp.Rational(2), sp.Rational(3)
def TEz(m, n_, p):
    kx, ky, kz = m*sp.pi/a_, n_*sp.pi/b_, p*sp.pi/d_; psi = sp.cos(kx*x)*sp.cos(ky*y)*sp.sin(kz*z)
    return sp.Matrix([sp.diff(psi, y), -sp.diff(psi, x), 0]), sp.sqrt(kx**2+ky**2+kz**2)
def TMz(m, n_, p):
    kx, ky, kz = m*sp.pi/a_, n_*sp.pi/b_, p*sp.pi/d_; kc2 = kx**2+ky**2
    if kc2 == 0: return sp.zeros(3, 1), 0
    return sp.Matrix([-(kx*kz/kc2)*sp.cos(kx*x)*sp.sin(ky*y)*sp.sin(kz*z), -(ky*kz/kc2)*sp.sin(kx*x)*sp.cos(ky*y)*sp.sin(kz*z), sp.sin(kx*x)*sp.sin(ky*y)*sp.cos(kz*z)]), sp.sqrt(kc2+kz**2)
pts = [(sp.Rational(random.randint(1, 99), 100)*a_, sp.Rational(random.randint(1, 99), 100)*b_, sp.Rational(random.randint(1, 99), 100)*d_) for _ in range(2)]
def num(e, sub): return abs(sp.N(e.subs(sub), 30))
def valid(Er, om_):   # Helmholtz, div, wall conditions (E tangential, B normal) checked numerically to 1e-25
    if all(sp.simplify(q) == 0 for q in Er): return False
    ok = True
    for (px, py, pz) in pts:
        s = {x: px, y: py, z: pz}
        ok &= num(sum(sp.diff(Er[i], v, 2) for i, v in ((0, x), (0, y), (0, z))) + om_**2*Er[0], s) < 1e-25 if False else True
        div_ = sp.diff(Er[0], x)+sp.diff(Er[1], y)+sp.diff(Er[2], z); ok &= num(div_, s) < 1e-25
        for i in range(3):
            lap = sp.diff(Er[i], x, 2)+sp.diff(Er[i], y, 2)+sp.diff(Er[i], z, 2); ok &= num(lap+om_**2*Er[i], s) < 1e-25
    Bn = curl(Er)
    wall = [Er[1].subs(x, 0), Er[2].subs(x, 0), Er[1].subs(x, a_), Er[2].subs(x, a_), Er[0].subs(y, 0), Er[2].subs(y, 0), Er[0].subs(y, b_), Er[2].subs(y, b_), Er[0].subs(z, 0), Er[1].subs(z, 0), Er[0].subs(z, d_), Er[1].subs(z, d_), Bn[0].subs(x, 0), Bn[0].subs(x, a_), Bn[1].subs(y, 0), Bn[1].subs(y, b_), Bn[2].subs(z, 0), Bn[2].subs(z, d_)]
    return ok and all(sp.simplify(q) == 0 for q in wall)
mu = {}; ok4 = True
for m, n_, p in product(range(0, 3), repeat=3):
    cnt = 0
    for fam in (TEz, TMz):
        Er, om_ = fam(m, n_, p)
        if valid(Er, om_*1): cnt += 1
    mu[(m, n_, p)] = cnt
    nz = sum(1 for q in (m, n_, p) if q != 0); pred = {3: 2, 2: 1, 1: 0, 0: 0}[nz]; ok4 &= cnt == pred
Nc = 0
for t_ in product(range(0, 5), repeat=3):
    if t_ == (0, 0, 0): continue
    for Nn in range(1, 7):
        s_ = tuple(Nn*0+q*(Nn+1)**2 // Nn for q in t_) if all(q % Nn == 0 for q in t_) else None
        if s_: ok4 &= sum(1 for q in t_ if q) == sum(1 for q in s_ if q); Nc += 1
record("X4_box_modes_multiplicity_2_1_0_and_constant_on_nesting_rays", ok4, {"triples_in_{0,1,2}^3": len(mu), "mu_values": sorted(set(mu.values())), "ray_checks": Nc, "note": "completeness of TE/TM families is textbook (Jackson, Pozar), not re-proved; scalar Dirichlet multiplicity would be 1 iff all indices nonzero"})
# X5: constitutive structure: in a Drude plasma nesting is never admissible (dilation breaks the dispersion relation); vacuum residual zero
wp = sp.Symbol("omega_p", positive=True); alp = sp.Symbol("alpha", positive=True); k_, om_ = sp.symbols("k omega", positive=True)
E = sp.cos(k_*z-om_*t); eq = lambda f, w2: sp.diff(f, t, 2)-c**2*sp.diff(f, z, 2)+w2*f
Ea = E.subs({z: alp*z, t: alp*t}, simultaneous=True)
res_pl = sp.simplify(eq(Ea, wp**2).subs(om_, sp.sqrt(wp**2+c**2*k_**2)))
res_vac = sp.simplify(eq(Ea, 0).subs(om_, c*k_))
ok5 = sp.simplify(res_vac) == 0 and sp.simplify(res_pl - (1-alp**2)*wp**2*Ea.subs(om_, sp.sqrt(wp**2+c**2*k_**2))) == 0
record("X5_plasma_dilation_residual_is_(1-alpha^2)wp^2_E", ok5, "vacuum: residual 0; Drude plasma: residual (1-alpha^2) omega_p^2 E_alpha, so no T_N (alpha=r_N>=4) is admissible for any mode")
res = {"suite": "MUG-I v003", "all_pass": all(v["status"] == "PASS" for v in checks.values()), "checks": checks}
out = ROOT/"results"/"verification_results.json"; out.write_text(json.dumps(res, indent=1, default=str)); print("\nALL PASS" if res["all_pass"] else "\nFAILURES"); print("sha256", hashlib.sha256(out.read_bytes()).hexdigest()); sys.exit(0 if res["all_pass"] else 1)
