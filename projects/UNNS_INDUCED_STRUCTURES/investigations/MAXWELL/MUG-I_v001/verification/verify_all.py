#!/usr/bin/env python3
"""MUG-I v001 verification suite. Maxwell Mode Geometry and Torsion-Class Carry Activation.
Usage: python3 verification/verify_all.py [--quick]   Requires sympy (symbolic Maxwell checks) + standard library.
Writes results/verification_results.json and tables/*.tex. Exit 0 iff every check passes."""
import argparse, json, random, sys, hashlib
from fractions import Fraction as F
from math import gcd, floor, isqrt
from functools import reduce
from itertools import product
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parent.parent
(ROOT/"results").mkdir(exist_ok=True); (ROOT/"tables").mkdir(exist_ok=True)
ap = argparse.ArgumentParser(); ap.add_argument("--quick", action="store_true"); args = ap.parse_args()
TR = 3000 if args.quick else 30000
random.seed(7)
checks = {}
def record(name, ok, detail):
    checks[name] = {"status": "PASS" if ok else "FAIL", "detail": detail}; print(("PASS " if ok else "FAIL ")+name+" :: "+str(detail)[:300])
def r(N): return F((N+1)**2, N)
def gc(v): return reduce(gcd, [abs(x) for x in v])
def sqfree(s):
    out, d, t = 1, 2, s
    while d*d <= t:
        e = 0
        while t % d == 0: t //= d; e += 1
        if e % 2: out *= d
        d += 1
    return out*t
# V1: content-direction decomposition and integrality of scale transport on vector indices
ok = True; adm = 0
for _ in range(TR):
    m = tuple(random.randint(-30, 30) for _ in range(3))
    if m == (0, 0, 0): continue
    N = random.randint(1, 40); g = gc(m); u = tuple(x//g for x in m)
    sc = tuple(r(N)*x for x in m); integral = all(x.denominator == 1 for x in sc)
    ok &= integral == (g % N == 0)
    if integral:
        adm += 1; m2 = tuple(int(x) for x in sc); ok &= gc(m2) == int(r(N))*g if r(N).denominator == 1 else gc(m2) == g*(N+1)**2//N
        ok &= tuple(x//gc(m2) for x in m2) == u
record("V1_content_direction_transport", ok, {"trials": TR, "admissible": adm})
# V2: spectral torsion classes of the cubic torus: realised squarefree parts are exactly sigma not 7 mod 8
B = 14; real = {}
for u in sorted(product(range(0, B+1), repeat=3), key=lambda v: (sum(q*q for q in v), v)):   # nonnegative representatives, smallest norm first
    if u == (0, 0, 0) or gc(u) != 1: continue
    s = sum(x*x for x in u); real.setdefault(sqfree(s), u)
SMAX = 70
sf = [s for s in range(1, SMAX+1) if sqfree(s) == s]
ok2 = all((s in real) == (s % 8 != 7) for s in sf) and all(sg % 8 != 7 for sg in real)
record("V2_realised_classes_legendre", ok2, {"squarefree_up_to": SMAX, "excluded_7mod8": [s for s in sf if s % 8 == 7][:8], "coordinate_bound": B})
# V3: multimode admissibility reduces to the gcd of the support
def hist_adm(S, hist):
    S = list(S)
    for N in hist:
        if any(x % N for x in S): return False
        S = [x*(N+1)**2//N for x in S]
    return True
ok = True; cnt = 0
for _ in range(TR//3):
    S = [random.randint(1, 400) for _ in range(random.randint(1, 5))]; g = reduce(gcd, S)
    h = [random.choice([1, 2, 3, 4, 5, 6, 8, 9]) for _ in range(random.randint(1, 4))]
    a, b = hist_adm(S, h), hist_adm([g], h); ok &= a == b; cnt += a
record("V3_multimode_admissibility_is_gcd", ok, {"trials": TR//3, "admissible": cnt})
# V4: exact Maxwell transport (symbolic)
x, y, z, t = sp.symbols("x y z t", real=True); c, L, A1, A2 = sp.symbols("c L A1 A2", positive=True)
def curl(E): return sp.Matrix([sp.diff(E[2], y)-sp.diff(E[1], z), sp.diff(E[0], z)-sp.diff(E[2], x), sp.diff(E[1], x)-sp.diff(E[0], y)])
def div(E): return sp.diff(E[0], x)+sp.diff(E[1], y)+sp.diff(E[2], z)
def residuals(E, Bf):
    return [sp.simplify(e) for e in list(curl(E)+sp.diff(Bf, t))+list(curl(Bf)-sp.diff(E, t)/c**2)]+[sp.simplify(div(E)), sp.simplify(div(Bf))]
def plane(ns, Lx):
    Ex = sum(A1*sp.cos(2*sp.pi*n*(z-c*t)/Lx) for n in ns[0]); Ey = sum(A2*sp.sin(2*sp.pi*n*(z-c*t)/Lx+sp.Rational(1, 3)) for n in ns[1])
    E = sp.Matrix([Ex, Ey, 0]); Bf = sp.Matrix([-Ey/c, Ex/c, 0]); return E, Bf
E0, B0 = plane(([2, 4, 6], [4, 8]), L)
okM = all(e == 0 for e in residuals(E0, B0))
al = sp.Rational(9, 2)
Ea, Ba = E0.subs({z: al*z, t: al*t}, simultaneous=True), B0.subs({z: al*z, t: al*t}, simultaneous=True)
okT = all(e == 0 for e in residuals(Ea, Ba)); okP = sp.simplify(Ea.subs(z, z+L)-Ea) == sp.zeros(3, 1) and sp.simplify(Ba.subs(z, z+L)-Ba) == sp.zeros(3, 1)
record("V4_scale_transport_maxwell_exact_and_periodic", okM and okT and okP, {"base": okM, "alpha=9/2_transport": okT, "periodic_on_L_for_N=2_sector": okP})
# V4b: blocked transport leaves the periodic sector
Eb = E0.subs({z: sp.Rational(25, 4)*z, t: sp.Rational(25, 4)*t}, simultaneous=True)  # alpha_4 on indices {2,4,6}: not all divisible by 4
okB = sp.simplify(Eb.subs(z, z+L)-Eb) != sp.zeros(3, 1) and all(e == 0 for e in residuals(Eb, B0.subs({z: sp.Rational(25, 4)*z, t: sp.Rational(25, 4)*t}, simultaneous=True)))
record("V4b_blocked_transport_still_maxwell_but_not_L_periodic", okB, "N=4 on indices 2,4,6: solves Maxwell on R^3 but is not L-periodic")
# V5: carry example alpha = 3^(-1/3), two periodic domains L1 = L0 * 3^(-2/3)
L0 = sp.symbols("L0", positive=True); L1 = L0*sp.Integer(3)**sp.Rational(-2, 3); alpha = sp.Integer(3)**sp.Rational(-1, 3)
def shift_multiple(n):  # alpha*(2 pi n/L0)*L1/(2 pi) : integer iff the scaled mode is L1-periodic
    return sp.nsimplify(sp.simplify(alpha*n*L1/L0))
vals = {n: shift_multiple(n) for n in (2, 9, 3, 18)}
ok5 = vals[2] == sp.Rational(2, 3) and vals[9] == 3 and vals[3] == 1 and vals[18] == 6
Ec = sp.cos(2*sp.pi*9*(z-c*t)/L0); sc = {z: alpha*z, t: alpha*t}
Ecs = Ec.subs(sc, simultaneous=True); per1 = sp.simplify(Ecs.subs(z, z+L1)-Ecs)
Ep2 = sp.cos(2*sp.pi*2*(z-c*t)/L0).subs(sc, simultaneous=True); per2 = sp.simplify(Ep2.subs(z, z+L1)-Ep2)
target = sp.cos(2*sp.pi*3*(z-c*t)/L1)
ok5 &= sp.simplify(Ecs-target) == 0 and per1 == 0 and per2 != 0
record("V5_carry_example_alpha_3^(-1/3)_two_domains", ok5, {"index_multiples": {k: str(v) for k, v in vals.items()}, "9->3 mode of domain1": True, "2 blocked": per2 != 0})
# V6: layered spectra: frequency sets of d domains with L_i = L_0/a_i; carries are the rational index maps c_i
def factor(n):
    f, d = {}, 2
    while d*d <= n:
        while n % d == 0: f[d] = f.get(d, 0)+1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0)+1
    return f
def vec(n):
    n = F(n); v = {}
    for p, e in factor(n.numerator).items(): v[p] = F(e)
    for p, e in factor(n.denominator).items(): v[p] = v.get(p, F(0))-e
    return v
def add(a, b):
    o = dict(a)
    for p, e in b.items(): o[p] = o.get(p, F(0))+e
    return {p: e for p, e in o.items() if e != 0}
def sc_(a, k): return {p: e*k for p, e in a.items() if e*k != 0}
def den(w): return reduce(lambda a, b: a*b//gcd(a, b), [e.denominator for e in w.values()], 1)
ok6 = True; rows = []
for name, w in {"sqrt2": {2: F(1, 2)}, "cbrt2": {2: F(1, 3)}, "3^(-1/3)": {3: F(-1, 3)}, "sqrt(2/3)": {2: F(1, 2), 3: F(-1, 2)}}.items():
    d = den(w); a = [{p: (i*e-floor(i*e)) for p, e in w.items() if i*e-floor(i*e) != 0} for i in range(d+1)]
    cs = []
    for i in range(d):
        ci = add(add(w, a[i]), sc_(a[(i+1) % d if i+1 < d else d], -1)); ok6 &= all(e.denominator == 1 for e in ci.values()); cs.append(ci)
    freq = lambda i, n: add(a[i], vec(n))
    seen = {}
    for i in range(d):
        for n in range(1, 61):
            key = tuple(sorted(freq(i, n).items())); ok6 &= key not in seen; seen[key] = (i, n)
    rows.append((name, d))
record("V6_layer_spectra_disjoint_and_carries_rational_index_maps", ok6, {"cases": rows, "bound_n": 60})
# V7: conducting rectangular cavity: TM_z mode, scale transport preserves BCs iff alpha*(m,n,p) integer
a_, b_, d_ = sp.symbols("a b d", positive=True)
def TM(m, n, p, aa, bb, dd):
    kx, ky, kz = m*sp.pi/aa, n*sp.pi/bb, p*sp.pi/dd; kc2 = kx**2+ky**2
    Ex = -(kx*kz/kc2)*sp.cos(kx*x)*sp.sin(ky*y)*sp.sin(kz*z); Ey = -(ky*kz/kc2)*sp.sin(kx*x)*sp.cos(ky*y)*sp.sin(kz*z); Ez = sp.sin(kx*x)*sp.sin(ky*y)*sp.cos(kz*z)
    return sp.Matrix([Ex, Ey, Ez]), sp.sqrt(kc2+kz**2)*c
def cavity_fields(m, n, p, aa, bb, dd):
    Er, om = TM(m, n, p, aa, bb, dd); E = Er*sp.cos(om*t); Bf = -curl(Er)*sp.sin(om*t)/om; return E, Bf
def bc_ok(E, Bf, aa, bb, dd):
    tang = [E[1].subs(x, 0), E[2].subs(x, 0), E[1].subs(x, aa), E[2].subs(x, aa), E[0].subs(y, 0), E[2].subs(y, 0), E[0].subs(y, bb), E[2].subs(y, bb), E[0].subs(z, 0), E[1].subs(z, 0), E[0].subs(z, dd), E[1].subs(z, dd)]
    norm = [Bf[0].subs(x, 0), Bf[0].subs(x, aa), Bf[1].subs(y, 0), Bf[1].subs(y, bb), Bf[2].subs(z, 0), Bf[2].subs(z, dd)]
    return all(sp.simplify(q) == 0 for q in tang+norm)
Ec_, Bc_ = cavity_fields(2, 4, 6, a_, b_, d_)
ok7 = all(e == 0 for e in residuals(Ec_, Bc_)) and bc_ok(Ec_, Bc_, a_, b_, d_)
al = sp.Rational(9, 2); Es, Bs = Ec_.subs({x: al*x, y: al*y, z: al*z, t: al*t}, simultaneous=True), Bc_.subs({x: al*x, y: al*y, z: al*z, t: al*t}, simultaneous=True)
ok7 &= all(e == 0 for e in residuals(Es, Bs)) and bc_ok(Es, Bs, a_, b_, d_)
Et, Bt = cavity_fields(9, 18, 27, a_, b_, d_); ok7 &= sp.simplify(Es-Et) == sp.zeros(3, 1) and sp.simplify(Bs-Bt) == sp.zeros(3, 1)   # transported mode = TM_(9,18,27) with the same amplitude
alb = sp.Rational(25, 4); Ef, Bf_ = Ec_.subs({x: alb*x, y: alb*y, z: alb*z, t: alb*t}, simultaneous=True), Bc_.subs({x: alb*x, y: alb*y, z: alb*z, t: alb*t}, simultaneous=True)
ok7 &= (not bc_ok(Ef, Bf_, a_, b_, d_)) and all(e == 0 for e in residuals(Ef, Bf_))
record("V7_conducting_cavity_BC_preserved_iff_integral", ok7, "TM_(2,4,6): N=2 -> TM_(9,18,27) exact eigenmode, same amplitude; N=4 gives a Maxwell solution violating the wall conditions")
# V8: energy density and action: mean energy density preserved, frequency x alpha, so action E/omega divided by alpha
ok8 = True
for _ in range(300):
    ns = random.sample(range(1, 40), 3); amps = [F(random.randint(1, 9), random.randint(1, 5)) for _ in ns]
    N = random.choice([1, 2, 3, 4, 6]); ns = [n*N for n in ns]
    En = sum(a*a for a in amps); w = sum(a*a*n for a, n in zip(amps, ns))      # energy ~ sum a^2, omega-weighted sum a^2 n
    ns2 = [n*(N+1)**2//N for n in ns]; En2 = En; w2 = sum(a*a*n for a, n in zip(amps, ns2))
    ok8 &= En2 == En and w2/w == r(N) and (En2/w2)/(En/w) == 1/r(N)
record("V8_energy_preserved_action_scales_inverse", ok8, "per-cell energy sum|a|^2 invariant; mean frequency x r_N; action E/omega divided by r_N")

# V9: rational lattice similarities Z^D -> Z^D with M^T M = sigma I (brute force over norm-sigma rows)
def sims(D, sig):
    R = isqrt(sig); vs = [v for v in product(range(-R, R+1), repeat=D) if sum(q*q for q in v) == sig]
    def ext(rows):
        if len(rows) == D: return True
        return any(all(sum(a*b for a, b in zip(v, w)) == 0 for w in rows) and ext(rows+[v]) for v in vs)
    return ext([])
def two_sq(n): return any(isqrt(n-a*a)**2 == n-a*a for a in range(isqrt(n)+1))
ok9 = True; found = {}
for sg in range(1, 41):
    s2 = sims(2, sg); ok9 &= s2 == two_sq(sg)
for sg in range(1, 41):
    s3 = sims(3, sg); ok9 &= s3 == (isqrt(sg)**2 == sg)
for sg in range(1, 16):
    ok9 &= sims(4, sg)      # D=4: every sigma (Lagrange) -- Hurwitz/quaternion similarities
record("V9_lattice_similarity_classification", ok9, "D=2: exists iff sigma is a sum of two squares; D=3: iff sigma is a perfect square; D=4: all sigma<=15 (checked)")
# V10: field-level similarity (rotation by 45 deg + dilation sqrt2) on the square torus, exact
th = sp.pi/4; al2 = sp.sqrt(2); n_ = sp.Integer(3)
Rm = sp.Matrix([[sp.cos(th), -sp.sin(th), 0], [sp.sin(th), sp.cos(th), 0], [0, 0, 1]]); Rin = Rm.T
Ez = sp.cos(2*sp.pi*n_*(x-c*t)/L); Ev = sp.Matrix([0, 0, Ez]); Bv = sp.Matrix([0, -Ez/c, 0])
def sim(F_, ):
    rr = al2*Rin*sp.Matrix([x, y, z])
    return sp.simplify(Rm*F_.subs({x: rr[0], y: rr[1], z: rr[2], t: al2*t}, simultaneous=True))
E1, B1 = sim(Ev), sim(Bv)
ok10 = all(e == 0 for e in residuals(Ev, Bv)) and all(sp.simplify(e) == 0 for e in residuals(E1, B1))
ok10 &= sp.simplify(E1[2]-sp.cos(2*sp.pi*n_*(x+y-sp.sqrt(2)*c*t)/L)) == 0
ok10 &= sp.simplify(E1.subs(x, x+L)-E1) == sp.zeros(3, 1) and sp.simplify(E1.subs(y, y+L)-E1) == sp.zeros(3, 1)
Ez2 = E1[2].subs({x: x, y: y})  # second application: (n,n) -> (0,2n)
E2 = sp.simplify(Rm*E1.subs({x: (al2*Rin*sp.Matrix([x, y, z]))[0], y: (al2*Rin*sp.Matrix([x, y, z]))[1], t: al2*t}, simultaneous=True))
ok10 &= sp.simplify(E2[2]-sp.cos(2*sp.pi*2*n_*(y-c*t)/L)) == 0
record("V10_similarity_carry_sqrt2_on_square_torus", ok10, "rotation 45deg + dilation sqrt2 maps TM mode m=(3,0) to (3,3), again to (0,6); exact Maxwell solution, L-periodic in x and y")

# V11: on the square torus, Gaussian multiplication by (1+i) reproduces the abstract sqrt2 carry layers exactly (c0=1, c1=2; inverse: c0=1/2, c1=1)
ok11 = True; n_checked = 0
for mx in range(-60, 61):
    for my in range(-60, 61):
        if (mx, my) == (0, 0): continue
        s2 = mx*mx+my*my; g = gcd(abs(mx), abs(my)); u2 = s2//(g*g)
        sg = sqfree(u2)
        if sg not in (1, 2): continue
        t = isqrt(u2//sg); n = g*t                       # |m| = n sqrt(sg)
        gm = (mx-my, mx+my); s2b = gm[0]**2+gm[1]**2          # (1+i)(mx+i my) = (mx-my) + i(mx+my)
        g2 = gcd(abs(gm[0]), abs(gm[1])); u2b = s2b//(g2*g2); sgb = sqfree(u2b); nb = g2*isqrt(u2b//sgb)
        ok11 &= (sg == 1 and sgb == 2 and nb == n) or (sg == 2 and sgb == 1 and nb == 2*n)      # forward carries c0=1, c1=2
        inv_adm = (mx+my) % 2 == 0                                                      # (1+i) | m
        ok11 &= inv_adm == ((n % 2 == 0) if sg == 1 else True)                          # inverse carries c0=1/2, c1=1
        n_checked += 1
record("V11_gaussian_carry_equals_abstract_layers_sqrt2", ok11, {"modes_checked": n_checked})
res = {"suite": "MUG-I v001", "mode": "quick" if args.quick else "full", "all_pass": all(v["status"] == "PASS" for v in checks.values()), "checks": checks}
out = ROOT/"results"/"verification_results.json"; out.write_text(json.dumps(res, indent=1, default=str))
rows = ["%d & %s \\\\" % (s, ("yes" if s in real else "no")) for s in sf[:0]]
cl = [s for s in sf if s <= 30]
tab = "\\begin{tabular}{@{}rcl@{}}\n\\toprule\n$\\sigma$ & realised & example $u$ \\\\ \\midrule\n"
for s in cl: tab += "%d & %s & %s \\\\\n" % (s, "yes" if s in real else "no", ("$%s$" % str(real[s]).replace(" ", "")) if s in real else "---")
tab += "\\bottomrule\n\\end{tabular}\n"; (ROOT/"tables"/"classes.tex").write_text(tab)
print("\nALL PASS" if res["all_pass"] else "\nFAILURES"); print("sha256", hashlib.sha256(out.read_bytes()).hexdigest()); sys.exit(0 if res["all_pass"] else 1)
