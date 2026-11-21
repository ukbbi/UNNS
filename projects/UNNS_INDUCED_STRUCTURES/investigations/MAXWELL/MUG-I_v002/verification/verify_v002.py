#!/usr/bin/env python3
"""MUG-I v002 verification: restricted carry admissibility and boundary geometry. Needs sympy.
Usage: python3 verification/verify_v002.py   Writes results/verification_results.json. Exit 0 iff all pass."""
import json, sys, hashlib, random
from fractions import Fraction as F
from math import gcd, isqrt
from itertools import product
from pathlib import Path
import sympy as sp
ROOT = Path(__file__).resolve().parent.parent; (ROOT/"results").mkdir(exist_ok=True)
random.seed(5); checks = {}
def record(n, ok, d): checks[n] = {"status": "PASS" if ok else "FAIL", "detail": d}; print(("PASS " if ok else "FAIL ")+n+" :: "+str(d)[:320])
def three_sq(n):  # Legendre
    while n % 4 == 0 and n: n //= 4
    return n % 8 != 7
def two_sq(n): return any(isqrt(n-a*a)**2 == n-a*a for a in range(isqrt(n)+1))
def vecs(nrm, R=None):
    R = R or isqrt(nrm); return [v for v in product(range(-R, R+1), repeat=3) if sum(q*q for q in v) == nrm]
dot = lambda a, b: sum(x*y for x, y in zip(a, b))
# W1: scope correction -- rational similarity admits a finite-index sublattice, not the whole lattice
Mh = sp.Matrix([[1, 1], [-1, 1]])/2          # (1-i)/2 : rational similarity, ratio 1/sqrt2
adm = [(x, y) for x in range(-6, 7) for y in range(-6, 7) if all(v.q == 1 for v in Mh*sp.Matrix([x, y]))]
ok1 = len(adm) == sum(1 for x in range(-6, 7) for y in range(-6, 7) if (x+y) % 2 == 0) and not all(v.q == 1 for v in (sp.eye(2)/2)*sp.Matrix([1, 0]))
record("W1_rational_similarity_gives_finite_index_sublattice", ok1, "M=(1-i)/2 admits exactly {m_x+m_y even}, index 2; M=I/2 is a rational similarity and is not whole-lattice")
# W2: 3D ray carry: sqrt(rho) maps ray g*u into an integer ray iff rho*|u|^2 is a sum of three squares (Legendre; Davenport-Cassels makes rational targets integral)
ok2 = True; cnt = 0
for u in product(range(0, 5), repeat=3):
    if u == (0, 0, 0) or gcd(gcd(u[0], u[1]), u[2]) != 1: continue
    for rho in range(1, 41):
        tgt = rho*dot(u, u); exists = len(vecs(tgt)) > 0
        ok2 &= exists == three_sq(tgt); cnt += 1
record("W2_ray_carry_exists_iff_target_norm_sum_of_three_squares", ok2, {"cases": cnt})
# W3: explicit field-level carry e1 -> (1,1,1) with alpha = sqrt3 on the 3-torus (symbolic, exact)
x, y, z, t = sp.symbols("x y z t", real=True); c, L = sp.symbols("c L", positive=True)
def curl(E): return sp.Matrix([sp.diff(E[2], y)-sp.diff(E[1], z), sp.diff(E[0], z)-sp.diff(E[2], x), sp.diff(E[1], x)-sp.diff(E[0], y)])
def div(E): return sp.diff(E[0], x)+sp.diff(E[1], y)+sp.diff(E[2], z)
def resid(E, B): return [sp.simplify(e) for e in list(curl(E)+sp.diff(B, t))+list(curl(B)-sp.diff(E, t)/c**2)]+[sp.simplify(div(E)), sp.simplify(div(B))]
n = 2; Ey = sp.cos(2*sp.pi*n*(x-c*t)/L); E0 = sp.Matrix([0, Ey, 0]); B0 = sp.Matrix([0, 0, Ey/c])   # wave along +x, E along y, B along z
w = sp.Matrix([1, 1, 1])/sp.sqrt(3); e1 = sp.Matrix([1, 0, 0]); v = e1.cross(w); cc = e1.dot(w); K = sp.Matrix([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
R = sp.simplify(sp.eye(3)+K+K*K*(1-cc)/sp.simplify(v.dot(v)))
okR = sp.simplify(R*e1-w) == sp.zeros(3, 1) and sp.simplify(R*R.T-sp.eye(3)) == sp.zeros(3, 3) and sp.simplify(R.det()) == 1
al = sp.sqrt(3); rr = al*R.T*sp.Matrix([x, y, z])
def carry(F_): return sp.simplify(R*F_.subs({x: rr[0], y: rr[1], z: rr[2], t: al*t}, simultaneous=True))
E1, B1 = carry(E0), carry(B0)
phase = 2*sp.pi*n*(x+y+z-sp.sqrt(3)*c*t)/L
okW = okR and all(e == 0 for e in resid(E0, B0)) and all(sp.simplify(e) == 0 for e in resid(E1, B1))
okW &= all(sp.simplify(E1.subs(s, s+L)-E1) == sp.zeros(3, 1) for s in (x, y, z))
okW &= sp.simplify(sp.Matrix(E1).dot(sp.Matrix([1, 1, 1]))) == 0 and sp.simplify(E1.dot(E1)-sp.cos(phase)**2) == 0
record("W3_sqrt3_ray_carry_e1_to_111_exact_maxwell_and_periodic", okW, "R e1=(1,1,1)/sqrt3; E' transverse to (1,1,1), periodic on L in x,y,z, residuals zero; R unique only up to rotation about the target axis")
# W4: support-rank profile of the sqrt(rho) carry into Z^3: rank1 {e1}; rank2 {e1,e2}; rank3 {e1,e2,e3}
rows = []; ok4 = True
for rho in range(1, 41):
    V = vecs(rho); r1 = len(V) > 0
    r2 = any(dot(a, b) == 0 for a in V for b in V)
    r3 = any(dot(a, b) == 0 and dot(a, d) == 0 and dot(b, d) == 0 for a in V for b in V for d in V) if r2 else False
    ok4 &= r1 == three_sq(rho) and r2 == two_sq(rho) and r3 == (isqrt(rho)**2 == rho)
    rows.append((rho, r1, r2, r3))
record("W4_profile_rank1_3sq_rank2_2sq_rank3_square", ok4, {"rho<=40": "rank1 iff sum of 3 squares; rank2 iff sum of 2 squares; rank3 iff perfect square", "failures_of_rank2_3sq_not_2sq": [r[0] for r in rows if r[1] and not r[2]][:8]})
# W5: general rank-2 support: rational embedding test via Hilbert symbols (Witt cancellation) vs brute force
def hil(a, b, p):
    a, b = int(a), int(b); al_ = be_ = 0
    while a % p == 0: a //= p; al_ += 1
    while b % p == 0: b //= p; be_ += 1
    if p != 2:
        leg = lambda q: 1 if pow(q % p, (p-1)//2, p) == 1 else -1
        s = (-1)**(al_*be_*((p-1)//2)) * leg(a)**be_ * leg(b)**al_; return s
    eps = lambda u: ((u-1)//2) % 2; om = lambda u: ((u*u-1)//8) % 2
    return (-1)**((eps(a)*eps(b)+al_*om(b)+be_*om(a)) % 2)
def primes_of(n):
    n = abs(n); ps = {2}; d = 2
    while d*d <= n:
        if n % d == 0: ps.add(d)
        while n % d == 0: n //= d
        d += 1
    if n > 1: ps.add(n)
    return ps
def embeds(m1, m2, rho):   # does rho*Gram(m1,m2) embed in (Q^3, I3)?  Witt: need Hasse invariants of <d1,d2,d1d2> to be 1 at all p
    a, b, cq = rho*dot(m1, m1), rho*dot(m1, m2), rho*dot(m2, m2); det = a*cq-b*b
    if det == 0: return None
    d1, d2 = a, det*a      # <a, det/a> ~ <a, det*a> modulo squares
    dl = d1*d2
    return all(hil(d1, d2, p)*hil(d1, dl, p)*hil(d2, dl, p) == 1 for p in primes_of(d1*d2*dl*2))
sound = True; agree = 0; tot = 0; gap = []
for _ in range(250):
    m1 = tuple(random.randint(-3, 3) for _ in range(3)); m2 = tuple(random.randint(-3, 3) for _ in range(3)); rho = random.choice([2, 3, 5, 6, 7, 10, 11, 13])
    e = embeds(m1, m2, rho)
    if e is None: continue
    n1, n2, d12 = rho*dot(m1, m1), rho*dot(m2, m2), rho*dot(m1, m2)
    A = vecs(n1); B = vecs(n2); found = any(dot(a_, b_) == d12 for a_ in A for b_ in B)
    tot += 1
    if found and not e: sound = False
    if e == found: agree += 1
    elif e and not found: gap.append((m1, m2, rho))
record("W5_rank2_embedding_test_sound_vs_bruteforce", sound, {"cases": tot, "agree": agree, "rational_yes_integral_not_found": len(gap), "note": "integral success implies rational test passes (soundness); gap cases need denominators or larger search"})
# W6: conducting walls: the 45-degree similarity carry does not keep wall conditions (square TM_z example), symbolic
a_ = sp.symbols("a", positive=True); m_ = 3
Ez = sp.sin(m_*sp.pi*x/a_)*sp.sin(m_*sp.pi*y/a_)
rr2 = sp.sqrt(2)*sp.Matrix([(x+y)/sp.sqrt(2), (y-x)/sp.sqrt(2)])
Ezc = sp.simplify(Ez.subs({x: rr2[0], y: rr2[1]}, simultaneous=True))
bad = sp.simplify(Ezc.subs(x, 0))
record("W6_45deg_carry_violates_conducting_square_wall", sp.simplify(Ez.subs(x, 0)) == 0 and bad != 0, {"E_z_wall_before": 0, "E_z_wall_after": str(bad)})
# W6b: polytope-edge necessity: carrying a box mode needs a signed-permutation rotation => alpha*m_i integral (checked on small cases by Gram of sign orbits)
def orbit(m): return sorted({(e1*m[0], e2*m[1], e3*m[2]) for e1 in (1, -1) for e2 in (1, -1) for e3 in (1, -1)})
ok6b = True
for m in product(range(0, 5), repeat=3):
    if m == (0, 0, 0): continue
    S = orbit(m)
    for rho in (2, 3, 5):
        # target must be a sign orbit of an integer vector w with the same Gram scaled by rho: compare Gram multisets
        G = sorted(rho*dot(a, b) for a in S for b in S)
        hit = False
        for wv in vecs(rho*dot(m, m)):
            T = orbit(wv)
            if len(T) == len(S) and sorted(dot(a, b) for a in T for b in T) == G: hit = True; break
        if hit: ok6b &= False      # any hit would mean an irrational carry maps a box mode to a box mode
record("W6b_no_irrational_carry_maps_box_mode_orbit_to_box_mode_orbit", ok6b, "all m in {0..4}^3, rho in {2,3,5}")
# W7: helicity: label preserved, integrated helicity scales 1/alpha (circular wave, Coulomb gauge)
E0s, om, s = sp.symbols("E0 omega s", positive=True); k = om/c; ph = k*z-om*t
for sg in (1, -1):
    a = E0s/om; A = a*sp.Matrix([sp.cos(ph), sg*sp.sin(ph), 0]); Bv = curl(A); Ev = -sp.diff(A, t)
    H = sp.simplify(A.dot(Bv)); u = sp.simplify((Ev.dot(Ev)+c**2*Bv.dot(Bv))/2)   # eps0=1 units
    ratio = sp.simplify(H*om/u)
    alpha = sp.symbols("alpha", positive=True)
    Hs = sp.simplify(H.subs({om: alpha*om}, simultaneous=True)); us = sp.simplify(u.subs({om: alpha*om}, simultaneous=True))
    okH = sp.simplify(ratio + sg/c) == 0 and sp.simplify(H.subs(om, alpha*om)*alpha - H) == 0
    checks.setdefault("W7_helicity", {"status": "PASS", "detail": {}}); checks["W7_helicity"]["detail"][str(sg)] = bool(okH)
    if not okH: checks["W7_helicity"]["status"] = "FAIL"
print(("PASS " if checks["W7_helicity"]["status"] == "PASS" else "FAIL ")+"W7_helicity_label_preserved_integrated_scales_1_over_alpha :: "+str(checks["W7_helicity"]["detail"]))
res = {"suite": "MUG-I v002", "all_pass": all(v["status"] == "PASS" for v in checks.values()), "checks": checks}
out = ROOT/"results"/"verification_results.json"; out.write_text(json.dumps(res, indent=1, default=str)); print("\nALL PASS" if res["all_pass"] else "\nFAILURES"); print("sha256", hashlib.sha256(out.read_bytes()).hexdigest()); sys.exit(0 if res["all_pass"] else 1)
