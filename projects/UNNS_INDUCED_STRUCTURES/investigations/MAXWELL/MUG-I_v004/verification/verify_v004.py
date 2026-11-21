#!/usr/bin/env python3
"""MUG-I v004: dispersion-resolved nesting. Standard library only.
Operation A: index nesting n -> r_N n followed by assigning the on-shell eigenfrequency. Operation B: spacetime dilation (k,w)->(a k,a w).
Usage: python3 verification/verify_v004.py   Exit 0 iff all pass."""
import json, sys, hashlib, random, math
from fractions import Fraction as F
from math import gcd
from functools import reduce
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent; (ROOT/"results").mkdir(exist_ok=True)
random.seed(4); checks = {}
def record(n, ok, d): checks[n] = {"status": "PASS" if ok else "FAIL", "detail": d}; print(("PASS " if ok else "FAIL ")+n+" :: "+str(d)[:340])
r = lambda N: F((N+1)**2, N)
gc = lambda v: reduce(gcd, [abs(x) for x in v])
# Y1: scope of "content": whole-field vs component; anisotropic cell change alters index-space ratios
S = [(1, 0, 0), (0, 1, 0)]; S2 = [(2*a, b, c) for a, b, c in S]                      # cell doubled in x only
whole = gc([x for m in S for x in m]); comp = [gc(m) for m in [(1,)+(0, 0), (2, 0, 0)]]
fieldS = [(1, 0, 0), (2, 0, 0)]                                                    # harmonics 1 and 2 on one cell
ok1 = gc(S[0]) == 1 and gc(S2[0]) == 2 and gc(S[1]) == gc(S2[1]) == 1              # ratio of contents 1 -> 2
ok1 &= gc([x for m in fieldS for x in m]) == 1 and gc(fieldS[1]) == 2              # whole-field content 1, second harmonic 2
iso = True
for _ in range(500):
    T = [tuple(random.randint(-9, 9) for _ in range(3)) for _ in range(3)]
    g = gc([x for m in T for x in m]) or 1; m_ = random.randint(2, 5)
    iso &= [tuple(m_*x//(m_*g) for x in v) for v in T] == [tuple(x//g for x in v) for v in T]
record("Y1_content_scope", ok1 and iso, {"anisotropic doubling": "content ratio 1 -> 2", "harmonics {1,2}": "whole-field content 1, component 2 has content 2 (T_2 admissible on the component, not on the field)", "isotropic cell multiples preserve index-space shape": iso})
# Y2: Drude/plasma exact identity  w(a k)^2 - a^2 w(k)^2 = (1 - a^2) wp^2   (c = 1); vacuum = 0; example T_2(2) = 9
ok2 = True
for _ in range(2000):
    k = F(random.randint(1, 60), random.randint(1, 6)); wp = F(random.randint(0, 9), random.randint(1, 4)); N = random.randint(1, 30); a = r(N)
    w2 = lambda kk: kk*kk+wp*wp
    ok2 &= w2(a*k)-a*a*w2(k) == (1-a*a)*wp*wp
    if wp == 0: ok2 &= w2(a*k)-a*a*w2(k) == 0
ex_ok = (F(4)+1 == 5) and (F(81)+1 == 82) and (F(82)-r(2)**2*5 == (1-r(2)**2)) and F(82, 5) != r(2)**2
record("Y2_drude_identity_and_T2_example", ok2 and ex_ok, {"identity": "w(k')^2 - a^2 w(k)^2 = (1-a^2) wp^2 exact (2000 rational cases)", "T_2(2)=9": "w_2^2=5, w_9^2=82; w_9/w_2 = sqrt(82/5) != 9/2 (16.4 vs 20.25)", "defect": str(F(82)-r(2)**2*5)})
# Y3: the defect is a cocycle (coboundary of Phi = w^2): Delta(ba;k) = Delta(b;ak) + b^2 Delta(a;k); path independence of the total, path dependence of the stepwise defects
def lorentz_w(k, w0=5.0, Om=2.0):
    lo, hi = 1e-9, w0-1e-9; f = lambda w: w*math.sqrt(1+Om*Om/(w0*w0-w*w))-k
    for _ in range(200):
        mid = (lo+hi)/2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo+hi)/2
def Delta(Phi, k, a): return Phi(a*k)-a*a*Phi(k)
ok3 = True; Phi_p = lambda k: k*k+1
for _ in range(500):
    k = F(random.randint(1, 20)); a = r(random.randint(1, 6)); b = r(random.randint(1, 6))
    ok3 &= Delta(Phi_p, k, b*a) == Delta(Phi_p, a*k, b)+b*b*Delta(Phi_p, k, a)
Phi_l = lambda k: lorentz_w(float(k))**2
for _ in range(60):
    k = random.randint(1, 8); a = float(r(random.randint(1, 4))); b = float(r(random.randint(1, 4)))
    ok3 &= abs(Delta(Phi_l, k, b*a)-Delta(Phi_l, a*k, b)-b*b*Delta(Phi_l, k, a)) < 1e-8
# explicit orders: n=3, (N=1 then N=3) vs (N=3 then N=1), plasma wp=1
d1, d3 = Delta(Phi_p, F(3), r(1)), Delta(Phi_p, F(3), r(3))
stepA = (d1, Delta(Phi_p, 4*F(3), r(3))); stepB = (d3, Delta(Phi_p, r(3)*F(3), r(1)))
totA = stepA[1]+r(3)**2*stepA[0]; totB = stepB[1]+r(1)**2*stepB[0]
ok3 &= (totA == totB == 1-(r(1)*r(3))**2) and (stepA[0] != stepB[0])
record("Y3_defect_cocycle_path_independent_total", ok3, {"stepwise A (N=1,3)": [str(x) for x in stepA], "stepwise B (N=3,1)": [str(x) for x in stepB], "total": str(totA)})
# Y4: gyrotropic cold plasma, parallel propagation, c=1: R/L branches distinguish polarisation under nesting
def w_gyro(k, wp, Oc, s):    # s=+1 R (upper branch, w > Oc), s=-1 L ; k^2 = w^2 - wp^2 w/(w - s Oc)
    f = lambda w: w*w-wp*wp*w/(w-s*Oc)-k*k
    lo = (Oc+1e-9) if s == 1 else 1e-9; hi = 1e4
    for _ in range(300):
        mid = (lo+hi)/2
        if f(mid) > 0: hi = mid
        else: lo = mid
    return (lo+hi)/2
ok4 = True; rows = []
for N, n in [(1, 1), (1, 3), (2, 2), (2, 6), (3, 3), (3, 9)]:
    a = float(r(N)); k = float(n); row = []
    for s in (1, -1):
        d = w_gyro(a*k, 1.0, 1.0, s)**2-a*a*w_gyro(k, 1.0, 1.0, s)**2; row.append(round(d, 5))
    rows.append((N, n, row[0], row[1])); ok4 &= abs(row[0]-row[1]) > 1e-3
# limits: Oc -> 0 reproduces the plasma identity (same for both branches); wp -> 0 gives 0
a = float(r(2)); k = 6.0
for s in (1, -1):
    ok4 &= abs((w_gyro(a*k, 1.0, 1e-7, s)**2-a*a*w_gyro(k, 1.0, 1e-7, s)**2)-(1-a*a)) < 1e-4
    ok4 &= abs(w_gyro(a*k, 1e-8, 1.0, s)**2-a*a*w_gyro(k, 1e-8, 1.0, s)**2) < 1e-4
vary = {round(w_gyro(float(r(1))*n, 1.0, 1.0, 1)**2-16*w_gyro(float(n), 1.0, 1.0, 1)**2, 5) for n in (1, 2, 3, 4)}
ok4 &= len(vary) > 1
record("Y4_gyrotropic_defect_depends_on_polarisation_and_index", ok4, {"(N,n,defect_R,defect_L)": rows, "R-branch defect for N=1 varies with n": sorted(vary)})
res = {"suite": "MUG-I v004", "all_pass": all(v["status"] == "PASS" for v in checks.values()), "checks": checks}
out = ROOT/"results"/"verification_results.json"; out.write_text(json.dumps(res, indent=1, default=str)); print("\nALL PASS" if res["all_pass"] else "\nFAILURES"); print("sha256", hashlib.sha256(out.read_bytes()).hexdigest()); sys.exit(0 if res["all_pass"] else 1)
