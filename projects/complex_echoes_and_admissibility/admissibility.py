#!/usr/bin/env python3
"""
ESC-I admissibility module: theorem audit -> frozen rules -> exact comparison, in one run.

Stages (order is enforced and recorded in the report):
  1. FREEZE   write admissibility_rules.md, hash it (SHA-256).
  2. AUDIT    verify the corrected theorems of s4/s5 (independent of the rules) -> theorem_audit.md
  3. PREDICT  apply the frozen rules to a fixed, seeded test set; hash the predictions.
              Rule code may not call the exact classifier (checked by source inspection).
  4. COMPARE  only now run esc_i.classical / exact rational simulation; tally agreements,
              disagreements, abstentions -> admissibility_report.json

Usage:  python admissibility.py [--out output]
Pure standard library; exact rational arithmetic (fractions.Fraction) wherever a verdict is decided.
"""
from fractions import Fraction as Fr
import argparse, cmath, datetime, hashlib, inspect, json, math, os, sys
import esc_i as E

SEED = 20261013
P = dict(            # frozen parameters (part of the hash)
    ar1_conj_cases=400, ar1_phase_grid_t=[Fr(k, 4) for k in range(-12, 13)],
    ar1_negctl_cases=300,
    ar2_cert_cases=300, ar2_violation_samples=40, ar2_violation_scale=0.98,
    ar2_sharp_cases=120, ar2_sharp_K=10, ar2_sharp_dirs=14, ar2_sharp_step=1.12,
    ar3_N=60,
)

# ------------------------------------------------------------------ small algebra
def mm(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def det(A): return A[0]*A[3]-A[1]*A[2]
def inv(A):
    d = det(A); return (A[3]/d, -A[1]/d, -A[2]/d, A[0]/d)
def rot_t(t):
    d = 1 + t*t; return ((1-t*t)/d, -2*t/d, 2*t/d, (1-t*t)/d)
def in_C(T): return T[0] == T[3] and T[1] == -T[2]          # aI + bJ  (conformal)
def in_Cbar(T): return T[0] == -T[3] and T[1] == T[2]       # [[a,b],[b,-a]] (anti-conformal)
def sgn(x): return 1 if x >= 0 else -1
def rng_ints(seed, lo, hi):
    r = E.mulberry32(seed); return lambda: lo + r() % (hi - lo + 1)

# ================================================================ FROZEN RULES (no exact classifier inside)
def regime_tau2(tau2, dl):
    """Exact regime of rho vs 1 for a real 2x2 with tau^2 = tau2, det = dl.  '<' '=' '>'  (Jury form)."""
    D = tau2 - 4*dl; s1 = 1 + dl
    if dl < 1 and s1 > 0 and tau2 < s1*s1: return "<"
    if (D < 0 and dl == 1) or (s1 >= 0 and tau2 == s1*s1 and abs(dl) <= 1): return "="
    return ">"

def ar1_conjugation(T, U, x0):
    """AR-1(a): T -> U T U^-1 with x0 -> U x0 is route-preserving: full exact class and period preserved."""
    return dict(verdict="ADMIT", claim="class, period and sub-type of the orbit are preserved")

def ar1_phase_family(T):
    """AR-1(b): left-multiplication by rotations R_theta.  tr(R T) = A cos + B sin, det(RT) = det T,
    A=a+d, B=b-c.  Verdict about the *regime* (rho vs 1) over the whole rotation family."""
    a, b, c, d = T; A, B, dl = a+d, b-c, a*d-b*c; m2 = A*A + B*B
    if in_C(T) or in_Cbar(T):
        return dict(verdict="RHO-INVARIANT", regime=regime_tau2((a+d)**2, dl))
    lo, hi = regime_tau2(Fr(0), dl), regime_tau2(m2, dl)         # rho is nondecreasing in |tau|, |tau| in [0,m]
    if lo == hi: return dict(verdict="REGIME-PRESERVED", regime=lo)
    if {lo, hi} == {"<", ">"}: return dict(verdict="REGIME-CAN-CHANGE", regimes=[lo, hi])
    return dict(verdict="ABSTAIN", reason="range touches rho=1 only at isolated phases")

def ar1_general_left_multiplication(T, U):
    """AR-1(c): T -> U T for arbitrary invertible U.  No sufficient condition is asserted."""
    return dict(verdict="ABSTAIN", reason="no route-preservation certificate for non-commuting, non-similarity U")

def _eigs(T):
    a, b, c, d = (float(t) for t in T); tr, dt = a+d, a*d-b*c; s = cmath.sqrt(tr*tr - 4*dt)
    return (tr+s)/2, (tr-s)/2
def _kappa(T):
    a, b, c, d = (float(t) for t in T); l1, l2 = _eigs(T)
    if b == 0 and c == 0: return 1.0
    if abs(l1-l2) < 1e-12: return None                           # defective
    def vec(l): return (l-d, c) if c != 0 else (b, l-a)
    v1, v2 = vec(l1), vec(l2)
    n1, n2 = math.hypot(abs(v1[0]), abs(v1[1])), math.hypot(abs(v2[0]), abs(v2[1]))
    g = abs(v1[0].conjugate()*v2[0] + v1[1].conjugate()*v2[1]) / (n1*n2) if isinstance(v1[0], complex) else \
        abs(v1[0]*v2[0] + v1[1]*v2[1]) / (n1*n2)
    g = min(g, 1 - 1e-15)
    return math.sqrt((1+g)/(1-g))

def ar2_certificate(T):
    """AR-2: certified margin.  Regime (rho vs 1) of T+E is preserved for every real E with ||E||_2 < eps_cert
    (Bauer-Fike).  rho=1 or non-diagonalizable: no certificate (knife-edge / uncertified)."""
    l1, l2 = _eigs(T); rho = max(abs(l1), abs(l2)); margin = abs(rho - 1)
    if margin < 1e-12: return dict(verdict="KNIFE-EDGE", eps_cert=0.0, rho=rho)
    scalar = T[1] == 0 and T[2] == 0 and T[0] == T[3]
    k = 1.0 if scalar else _kappa(T)
    if k is None: return dict(verdict="UNCERTIFIED", reason="non-diagonalizable", rho=rho)
    gap = float("inf") if scalar else abs(l1 - l2)
    eps = (margin if rho < 1 else min(margin, gap/2)) / k
    return dict(verdict="CERTIFIED", eps_cert=eps, rho=rho, kappa=k, margin=margin)

def ar3_predict(sysd, pi, z0):
    """AR-3: projection persistence for x_{n+1} = Pi(T x_n), T = V diag(lam,mu) V^-1, eigen-coordinates z=(u,w).
    Error models: absolute h, relative eta (sup-norm in eigen-coordinates).  Dominant eigenvalue must satisfy |lam|>1, |lam|>|mu|."""
    lam, mu, Vi_norm, V_norm = abs(sysd["lam"]), abs(sysd["mu"]), sysd["Vinv_inf"], sysd["V_inf"]
    u0, w0 = z0
    if not (lam > 1 and lam > mu) or u0 == 0: return dict(verdict="ABSTAIN", reason="out of scope")
    k = pi["kind"]
    if k == "ADV_ABS":
        thr = pi["h"] / (lam - 1)
        return dict(verdict="ESCAPE" if abs(u0) > thr else "NO-ESCAPE", basis="escape radius h/(|lam|-1)", sharp=True)
    if k == "DEADZONE":
        thr = pi["theta"] / (lam - 1)
        if abs(u0) > thr: return dict(verdict="ESCAPE", basis="escape radius")
        if lam*abs(u0) < pi["theta"]: return dict(verdict="NO-ESCAPE", basis="first step erased by projection")
        return dict(verdict="ABSTAIN", reason="inside escape radius, not erased at step 1")
    if k in ("ADV_REL", "REL_QUANT"):
        eta = pi["eta"] if k == "ADV_REL" else V_norm*Vi_norm*Fr(1, 2**pi["bits"])
        if eta <= (lam - mu)/2 and abs(w0) <= abs(u0):
            return dict(verdict="CONE", rate=[lam - eta, lam + eta], eta_eig=eta, basis="cone invariance")
        if k == "ADV_REL" and eta >= lam: return dict(verdict="NO-ESCAPE", basis="error can erase u")
        return dict(verdict="ABSTAIN", reason="hypotheses of cone theorem not met")
    if k == "ROUND_ABS":
        h_eig = Vi_norm*pi["h"]/2; thr = h_eig/(lam - 1)
        if abs(u0) > thr: return dict(verdict="ESCAPE", basis="escape radius with kappa conversion")
        if pi.get("erased_first_step"): return dict(verdict="NO-ESCAPE", basis="T x0 rounds to 0")
        return dict(verdict="ABSTAIN", reason="inside converted escape radius")
    return dict(verdict="ABSTAIN", reason="unknown projection")

def ar3_predict_amended_relquant(sysd, pi, z0):
    """POST-HOC amendment (written after the frozen comparison, labelled exploratory). The k-bit quantizer rounds T y, so its error is
    relative to |T y|, not |y|: eta_eig = kappa_inf(V) |lam| 2^-k  (the frozen rule omitted the factor |lam|)."""
    lam, mu = abs(sysd["lam"]), abs(sysd["mu"]); u0, w0 = z0
    if not (lam > 1 and lam > mu) or u0 == 0: return dict(verdict="ABSTAIN", reason="out of scope")
    eta = sysd["V_inf"]*sysd["Vinv_inf"]*lam*Fr(1, 2**pi["bits"])
    if eta <= (lam - mu)/2 and abs(w0) <= abs(u0): return dict(verdict="CONE", rate=[lam-eta, lam+eta], eta_eig=eta)
    return dict(verdict="ABSTAIN", reason="hypotheses of cone theorem not met")

RULE_FUNCS = [ar3_predict_amended_relquant, regime_tau2, ar1_conjugation, ar1_phase_family, ar1_general_left_multiplication,
              _eigs, _kappa, ar2_certificate, ar3_predict]

RULES_MD = """# ESC-I admissibility rules AR-1, AR-2, AR-3 (frozen)

Status: **hypotheses derived from the audited mathematics in `theorem_audit.md`; not established UNNS laws.**
These definitions, thresholds and test-set parameters were written, hashed and saved *before* any exact
comparison was run. The hash is recorded in `admissibility_report.json`.

Verdict vocabulary: ADMIT / ESCAPE / CONE / RHO-INVARIANT / REGIME-PRESERVED (a transition or projection is
predicted to keep the regime), REGIME-CAN-CHANGE / NO-ESCAPE (predicted to leave it), CERTIFIED / KNIFE-EDGE /
UNCERTIFIED (robustness), ABSTAIN (the rule makes no claim). Rule code never calls the exact classifier.

## AR-1  Route preservation (phase and similarity transformations of a recursion T)
(a) Conjugation T -> U T U^-1 with x0 -> U x0, U invertible: **ADMIT**. Exact class, period and sub-type of the orbit are preserved.
(b) Left rotation family T -> R_theta T. With A = a+d, B = b-c, det(R T) = det T and tr(R T) = A cos(theta) + B sin(theta),
    so the family spans |tau| in [0, m], m^2 = A^2 + B^2.
    - T in C u C-bar (T = aI+bJ or [[a,b],[b,-a]], i.e. T a scaled isometry): **RHO-INVARIANT** for every theta.
    - otherwise compare the regime of rho at |tau|=0 and |tau|=m (exact, Jury form):
      equal -> **REGIME-PRESERVED**; one '<' and the other '>' -> **REGIME-CAN-CHANGE**; else **ABSTAIN** (touching rho=1 only at isolated phases).
(c) General left multiplication T -> U T: **ABSTAIN** (negative control: no certificate is asserted).
Falsification: (a) any case where the exact class/period/sub-type of (U T U^-1, U x0) differs from that of (T, x0);
(b) any rational rotation in the grid whose regime or rho contradicts the verdict (CAN-CHANGE must be witnessed by the grid or is recorded as unconfirmable).

## AR-2  Boundary sensitivity (certified margin)
For diagonalizable T with rho != 1: eps_cert = min(|rho-1|, gap/2 if rho>1) / kappa_2(V) (gap = |lambda1 - lambda2|; scalar T: kappa=1, gap=inf).
**CERTIFIED**: the regime (rho vs 1) of T+E is preserved for every real E with ||E||_2 < eps_cert.
rho = 1: **KNIFE-EDGE**: for every eps>0 some perturbation of norm <= eps*||T|| changes the regime.
Non-diagonalizable: **UNCERTIFIED**.
Falsification: (i) a regime change under ||E||_2 <= 0.98 eps_cert; (ii) a KNIFE-EDGE T whose scalings (1+-eps)T fail to change the regime.
Sharpness hypothesis (this one can fail): the smallest regime-changing perturbation is at most K = 10 times eps_cert.
It is confirmed per matrix by an explicit witness found by a fixed direction search; absence of a witness is recorded as 'unconfirmed', not as refutation.

## AR-3  Projection persistence (x_{n+1} = Pi(T x_n), T = V diag(lam, mu) V^-1, |lam| > 1, |lam| > |mu|, u0 != 0)
Eigen-coordinates z = (u, w); error measured in the eigen sup-norm.
- Absolute error <= h: **ESCAPE** iff |u0| > h/(|lam|-1); otherwise **NO-ESCAPE** (two-sided, sharp for the adversarial projection).
- Relative error <= eta: if eta <= (|lam|-|mu|)/2 and |w0| <= |u0|: **CONE**: every step satisfies |u_{n+1}|/|u_n| in [|lam|-eta, |lam|+eta] and |w_n| <= |u_n|. If eta >= |lam|: **NO-ESCAPE**. Else ABSTAIN.
- Dead-zone projection (u zeroed if |u|<theta): ESCAPE if |u0|>theta/(|lam|-1); NO-ESCAPE if |lam||u0|<theta; else ABSTAIN.
- Nearest rounding to the lattice h Z^2 (original coordinates): ESCAPE if |u0| > ||V^-1||_inf (h/2)/(|lam|-1); NO-ESCAPE if T x0 rounds to 0; else ABSTAIN.
- k-bit relative quantizer: eta_eig = ||V||_inf ||V^-1||_inf 2^-k, then the relative-error rule.
Falsification: simulate the projected orbit in exact rational arithmetic for N = 60 steps. ESCAPE fails if |u_n| is not strictly increasing; CONE fails if a ratio leaves its interval or |w|>|u|; NO-ESCAPE fails if the orbit escapes.

## Outcome vocabulary for the comparison
AGREE, DISAGREE (rule falsified or implementation error), ABSTAIN (the exact computation resolves the case; the rule does not),
UNCONFIRMABLE (prediction needs a witness outside the finite grid). Every DISAGREE is listed individually in the report.
"""

# ================================================================== STAGE helpers
def sha(obj): return hashlib.sha256(obj if isinstance(obj, bytes) else json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

def check_rule_independence(prd=False):
    funcs = list(RULE_FUNCS) + ([prd_rule] if prd else [])
    banned = ["classical(", "echo_classify(", "pi_apply(", "_prd_orbit(", "sim_ar3(", "_sim_confirm("]
    bad = [f.__name__ for f in funcs if any(b in inspect.getsource(f) for b in banned)]
    assert not bad, f"rule functions call the exact classifier: {bad}"

def rho_float(T):
    l1, l2 = _eigs(T); return max(abs(l1), abs(l2))
def op_norm2(M):
    a, b, c, d = (float(x) for x in M); F = a*a+b*b+c*c+d*d; dt = a*d-b*c
    return math.sqrt((F + math.sqrt(max(F*F - 4*dt*dt, 0.0)))/2)
def rat(x, q=10**9): return Fr(round(x*q), q)
def regime(T): return E.classical(T, (Fr(1), Fr(0)))["rho_vs_1"]

# ================================================================== AUDIT (theorem verification)
def audit():
    R = {}
    # S5.1 counterexample
    T, U = (Fr(1),)*4, (Fr(1), Fr(0), Fr(0), Fr(-1))
    ph = E.phase_inlet(T, U); R["s5_counterexample"] = ph
    # S5.2 similarity: class conjugacy
    rnd = rng_ints(SEED+1, -3, 3); n = bad = 0
    while n < 2000:
        T = tuple(Fr(rnd()) for _ in range(4)); Um = tuple(Fr(rnd()) for _ in range(4)); x0 = (Fr(rnd()), Fr(rnd()))
        if det(Um) == 0: continue
        n += 1; c1 = E.classical(T, x0); c2 = E.classical(mm(mm(Um, T), inv(Um)), apply(Um, x0))
        bad += (c1["cls"], c1["sub"], c1["period"]) != (c2["cls"], c2["sub"], c2["period"]) or abs(c1["rho"]-c2["rho"]) > 1e-9
    R["s5_similarity"] = dict(cases=n, violations=bad)
    # S5.4 trace law and S5.5 iff theorem on integer matrices x rational rotations
    grid = P["ar1_phase_grid_t"]; trace_bad = inv_bad = var_missing = inv_cases = var_cases = 0
    for a, b, c, d in __import__("itertools").product(range(-2, 3), repeat=4):
        T = tuple(Fr(x) for x in (a, b, c, d)); A, B = a+d, b-c; rhos = []
        for t in grid:
            Rt = rot_t(t); M = mm(Rt, T); cs, sn = Rt[0], Rt[2]
            trace_bad += (M[0]+M[3]) != A*cs + B*sn or det(M) != det(T)
            rhos.append(rho_float(M))
        const = max(rhos) - min(rhos) < 1e-9
        if in_C(T) or in_Cbar(T):
            inv_cases += 1; inv_bad += not const
        else:
            var_cases += 1; var_missing += const
    R["s5_trace_law"] = dict(violations=trace_bad)
    R["s5_iff_theorem"] = dict(invariant_family_cases=inv_cases, invariance_violations=inv_bad,
                              non_invariant_cases=var_cases, grid_failed_to_witness_variation=var_missing)
    # S5 corollary: sup over orthogonal U of rho(UT) = sigma_max(T)
    import random
    worst = 0.0; viol = 0; rr = E.mulberry32(SEED+2)
    for _ in range(300):
        T = tuple(Fr(rr() % 9 - 4, 2) for _ in range(4)); s1 = op_norm2(T); best = 0.0
        for k in range(720):
            th = 2*math.pi*k/720; c, s = math.cos(th), math.sin(th)
            for refl in (1, -1):
                M = (rat(c), rat(-s), rat(refl*s), rat(refl*c)); best = max(best, rho_float(mm(M, T)))
        viol += best > s1 + 1e-7; worst = max(worst, s1 - best)
    R["s5_sup_orthogonal"] = dict(cases=300, exceed_sigma_max=viol, max_gap_sigma_minus_sup=worst)
    # S4: counterexamples (exact) and theorem checks (exact adversarial simulation)
    T2 = (Fr(2), Fr(0), Fr(0), Fr(2)); y = (Fr(1, 5), Fr(0)); orb = []
    for _ in range(10):
        y = tuple(round(2*c) for c in y) ; y = tuple(Fr(c) for c in y); orb.append(y)   # lattice Z^2 rounding of T y
    R["s4_ce_absolute_rounding"] = dict(T="2I", x0="(1/5,0)", orbit_all_zero=all(o == (0, 0) for o in orb), exact_rho=2)
    R["s4_ce_stable_eigenline"] = dict(T="diag(2,1/2)", x0="(0,1)", exact_class=E.classical((Fr(2), 0, 0, Fr(1, 2)), (Fr(0), Fr(1)))["cls"])
    R["s4_ce_deadzone"] = dict(T="diag(2,1/2)", x0="(2/5,1)", unprojected=E.classical((Fr(2), 0, 0, Fr(1, 2)), (Fr(2, 5), Fr(1)))["cls"],
                               projected_orbit=_deadzone_demo())
    R["s4_ce_rotation_direction_drift"] = _rotation_drift()
    R["s4_thm_relative_cone"] = _verify_cone(); R["s4_thm_absolute_escape"] = _verify_escape()
    return R

def _deadzone_demo():
    z = (Fr(2, 5), Fr(1)); out = []
    for _ in range(8):
        zt = (2*z[0], z[1]/2); z = (Fr(0), zt[1]) if abs(zt[0]) < 1 else zt; out.append((str(z[0]), str(z[1])))
    return out

def _rotation_drift():
    r, eta, n = 1.5, 0.3, 200; th = math.asin(eta/r); ang_exact = n*th; return dict(
        T="1.5 * rotation by 30deg", relative_error=eta, max_norm_ratio_per_step=[r-eta, r+eta],
        adversarial_angle_drift_after_200_steps_rad=ang_exact, note="rate stays in [r-eta,r+eta]; direction is not preserved")

def _verify_cone(cases=1500):
    rr = E.mulberry32(SEED+3); viol = tested = 0
    for _ in range(cases):
        lam = Fr(rr() % 40 + 11, 10); mu = Fr(int(rr() % 21) - 10, 10)
        if abs(mu) >= lam: continue
        f = Fr(rr() % 101, 100); eta = f*(lam - abs(mu))/2
        u = Fr(rr() % 90 + 10, 10)*sgn(int(rr() % 2) - 1+0); w = Fr(int(rr() % 21) - 10, 10)*abs(u)/10
        tested += 1; ok = True
        for _ in range(40):
            nx = max(abs(u), abs(w)); ut = lam*u; wt = mu*w
            u2 = ut - sgn(ut)*min(eta*nx, abs(ut)) if rr() % 2 else ut + sgn(ut)*eta*nx
            w2 = wt + (sgn(wt) if rr() % 2 else -sgn(wt))*eta*nx
            ratio = abs(u2)/abs(u)
            if not (lam - eta <= ratio <= lam + eta) or abs(w2) > abs(u2): ok = False; break
            u, w = u2, w2
        viol += not ok
    return dict(cases=tested, violations=viol)

def _verify_escape(cases=1500):
    rr = E.mulberry32(SEED+4); viol = n_in = n_out = 0
    for _ in range(cases):
        lam = Fr(rr() % 40 + 11, 10); h = Fr(rr() % 20 + 1, 10); thr = h/(lam - 1)
        u0 = thr*Fr(int(rr() % 150) + 1, 100)
        if u0 == thr: continue
        u = u0; esc = True
        for _ in range(50):
            ut = lam*u; u2 = ut - sgn(ut)*min(h, abs(ut))
            if abs(u2) <= abs(u): esc = False; break
            u = u2
        if u0 > thr: n_out += 1; viol += not esc
        else: n_in += 1; viol += esc
    return dict(cases_above_radius=n_out, cases_below_radius=n_in, violations=viol)

# ================================================================== PREDICT stage
def build_cases():
    cases = {"AR-1a": [], "AR-1b": [], "AR-1c": [], "AR-2c": [], "AR-2k": [], "AR-3": []}
    r = rng_ints(SEED+10, -3, 3); k = 0
    while k < P["ar1_conj_cases"]:
        T = tuple(Fr(r()) for _ in range(4)); Um = tuple(Fr(r()) for _ in range(4)); x0 = (Fr(r()), Fr(r()))
        if det(Um) != 0: cases["AR-1a"].append((T, Um, x0)); k += 1
    cases["AR-1b"] = [tuple(Fr(x) for x in t) for t in __import__("itertools").product(range(-2, 3), repeat=4)]
    r = rng_ints(SEED+11, -3, 3); k = 0
    while k < P["ar1_negctl_cases"]:
        T = tuple(Fr(r()) for _ in range(4)); Um = tuple(Fr(r()) for _ in range(4)); x0 = (Fr(r()), Fr(r()))
        if det(Um) != 0: cases["AR-1c"].append((T, Um, x0)); k += 1
    rr = E.mulberry32(SEED+12); k = 0
    while k < P["ar2_cert_cases"]:
        T = tuple(Fr(int(rr() % 25) - 12, 4) for _ in range(4))
        c = ar2_certificate(T)
        if c["verdict"] == "CERTIFIED": cases["AR-2c"].append(T); k += 1
    for t in __import__("itertools").product(range(-2, 3), repeat=4):
        T = tuple(Fr(x) for x in t)
        if ar2_certificate(T)["verdict"] == "KNIFE-EDGE": cases["AR-2k"].append(T)
    Vs = [(Fr(1), Fr(0), Fr(0), Fr(1)), (Fr(1), Fr(1), Fr(0), Fr(1)), (Fr(1), Fr(2), Fr(1), Fr(3))]
    LM = [(Fr(2), Fr(1, 2)), (Fr(3), Fr(-1)), (Fr(3, 2), Fr(-1, 2)), (Fr(2), Fr(3, 2)), (Fr(5), Fr(2))]
    U0 = [Fr(1, 10), Fr(1, 2), Fr(1), Fr(3, 2), Fr(3), Fr(10)]; W0 = [Fr(0), Fr(1, 2), Fr(2)]
    for V in Vs:
        Vi = inv(V); infn = lambda M: max(abs(M[0])+abs(M[1]), abs(M[2])+abs(M[3]))
        for lam, mu in LM:
            sysd = dict(V=V, lam=lam, mu=mu, Vinv_inf=infn(Vi), V_inf=infn(V))
            pis = [dict(kind="ADV_ABS", h=h) for h in (Fr(1, 2), Fr(1))] + [dict(kind="DEADZONE", theta=t) for t in (Fr(1, 2), Fr(1))] \
                + [dict(kind="ADV_REL", eta=f*(lam-abs(mu)), f=str(f)) for f in (Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(1))] \
                + [dict(kind="ROUND_ABS", h=h) for h in (Fr(1, 4), Fr(1, 2))] + [dict(kind="REL_QUANT", bits=b) for b in (3, 6)]
            for u0 in U0:
                for w0 in W0:
                    for pi in pis: cases["AR-3"].append((sysd, dict(pi), (u0, w0)))
    return cases

def ar3_x0(sysd, z0): V = sysd["V"]; return (V[0]*z0[0]+V[1]*z0[1], V[2]*z0[0]+V[3]*z0[1])

def predict_all(cases):
    pred = {k: [] for k in cases}
    for T, Um, x0 in cases["AR-1a"]: pred["AR-1a"].append(ar1_conjugation(T, Um, x0))
    for T in cases["AR-1b"]: pred["AR-1b"].append(ar1_phase_family(T))
    for T, Um, x0 in cases["AR-1c"]: pred["AR-1c"].append(ar1_general_left_multiplication(T, Um))
    for T in cases["AR-2c"]: pred["AR-2c"].append(ar2_certificate(T))
    for T in cases["AR-2k"]: pred["AR-2k"].append(ar2_certificate(T))
    for sysd, pi, z0 in cases["AR-3"]:
        pi = dict(pi)
        if pi["kind"] == "ROUND_ABS":                       # the rule may use the first-step arithmetic of its own input
            x0 = ar3_x0(sysd, z0); V = sysd["V"]; Vi = inv(V)
            Tm = mm(mm(V, (sysd["lam"], Fr(0), Fr(0), sysd["mu"])), Vi); y1 = apply(Tm, x0)
            pi["erased_first_step"] = all(abs(c) < pi["h"]/2 for c in y1)
        pred["AR-3"].append(ar3_predict(sysd, pi, z0))
    return pred

# ================================================================== COMPARE stage (exact)
def apply(M, x): return (M[0]*x[0]+M[1]*x[1], M[2]*x[0]+M[3]*x[1])

def compare_ar1(cases, pred):
    out = {}
    rows = []
    for (T, Um, x0), p in zip(cases["AR-1a"], pred["AR-1a"]):
        c1 = E.classical(T, x0); c2 = E.classical(mm(mm(Um, T), inv(Um)), apply(Um, x0))
        ok = (c1["cls"], c1["sub"], c1["period"]) == (c2["cls"], c2["sub"], c2["period"])
        rows.append("AGREE" if ok else "DISAGREE")
    out["AR-1a"] = _tally(rows)
    rows, details = [], []
    for T, p in zip(cases["AR-1b"], pred["AR-1b"]):
        regs = {regime(mm(rot_t(t), T)) for t in P["ar1_phase_grid_t"]}
        rhos = [rho_float(mm(rot_t(t), T)) for t in P["ar1_phase_grid_t"]]; v = p["verdict"]
        if v == "RHO-INVARIANT": ok = (max(rhos)-min(rhos) < 1e-9) and regs == {p["regime"]}; rows.append("AGREE" if ok else "DISAGREE")
        elif v == "REGIME-PRESERVED": rows.append("AGREE" if regs == {p["regime"]} else "DISAGREE")
        elif v == "REGIME-CAN-CHANGE": rows.append("AGREE" if len(regs) > 1 else "UNCONFIRMABLE")
        else: rows.append("ABSTAIN")
        if rows[-1] == "DISAGREE": details.append(dict(T=[str(x) for x in T], verdict=v, grid_regimes=sorted(regs)))
    out["AR-1b"] = _tally(rows); out["AR-1b"]["details"] = details
    ch = 0
    for (T, Um, x0) in cases["AR-1c"]:
        c1 = E.classical(T, x0); c2 = E.classical(mm(Um, T), apply(Um, x0)); ch += c1["cls"] != c2["cls"]
    out["AR-1c"] = dict(total=len(cases["AR-1c"]), ABSTAIN=len(cases["AR-1c"]), class_changed_by_UT=ch,
                        note="negative control: how often an uncertified transformation changes the class")
    return out

def _tally(rows):
    t = {k: rows.count(k) for k in ("AGREE", "DISAGREE", "ABSTAIN", "UNCONFIRMABLE")}; t["total"] = len(rows); return t

def compare_ar2(cases, pred):
    rr = E.mulberry32(SEED+20); viol = tested = 0; viol_list = []
    for T, p in zip(cases["AR-2c"], pred["AR-2c"]):
        base = regime(T)
        for _ in range(P["ar2_violation_samples"]):
            Em = [(rr() % 2001 - 1000)/1000 for _ in range(4)]; nm = op_norm2(Em)
            sc = P["ar2_violation_scale"]*p["eps_cert"]/nm; Ep = tuple(rat(x*sc) for x in Em)
            tested += 1
            if regime(tuple(T[i]+Ep[i] for i in range(4))) != base:
                viol += 1; viol_list.append(dict(T=[str(x) for x in T], eps_cert=p["eps_cert"]))
    # sharpness: explicit witnesses within K*eps_cert
    K, nd, step = P["ar2_sharp_K"], P["ar2_sharp_dirs"], P["ar2_sharp_step"]; rows = []; ratios = []; unconf = []
    for T, p in list(zip(cases["AR-2c"], pred["AR-2c"]))[:P["ar2_sharp_cases"]]:
        base = regime(T); best = None
        dirs = [(math.cos(2*math.pi*i/nd), math.sin(2*math.pi*i/nd), math.cos(2*math.pi*j/nd), math.sin(2*math.pi*j/nd))
                for i in range(nd) for j in range(nd)]
        s = p["eps_cert"]
        while s <= K*p["eps_cert"] and best is None:
            for (c1, s1, c2, s2) in dirs:
                Ep = (rat(s*c1*c2), rat(s*c1*s2), rat(s*s1*c2), rat(s*s1*s2))
                if regime(tuple(T[i]+Ep[i] for i in range(4))) != base: best = s; break
            s *= step
        rows.append("AGREE" if best is not None else "UNCONFIRMABLE")
        if best is not None: ratios.append(best/p["eps_cert"])
        else: unconf.append((T, p))
    ratios.sort()
    ks = 0; kn = 0                                           # knife-edge check
    for T, p in zip(cases["AR-2k"], pred["AR-2k"]):
        e = Fr(1, 10**6); a = regime(tuple((1+e)*x for x in T)); b = regime(tuple((1-e)*x for x in T)); kn += 1
        ks += (a != "=" and b != "=")
    return dict(safety=dict(samples=tested, violations=viol, violating_cases=viol_list[:10]),
                sharpness=dict(_tally(rows), K=K, ratio_median=ratios[len(ratios)//2] if ratios else None,
                               ratio_max=ratios[-1] if ratios else None,
                               posthoc_wide_search_ratios=_wide_search(unconf),
                               posthoc_note="exploratory: unconfirmed cases re-searched with 24x24 directions up to 200 x eps_cert (not part of the frozen test)"),
                knife_edge=dict(cases=kn, regime_changed_by_scaling=ks, violations=kn-ks))

def _wide_search(unconf, nd=24, top=200, step=1.15):
    out = []
    for T, p in unconf:
        base = regime(T); found = None; s = p["eps_cert"]
        dirs = [(math.cos(2*math.pi*i/nd), math.sin(2*math.pi*i/nd), math.cos(2*math.pi*j/nd), math.sin(2*math.pi*j/nd)) for i in range(nd) for j in range(nd)]
        while s <= top*p["eps_cert"] and found is None:
            for (c1, s1, c2, s2) in dirs:
                Ep = (rat(s*c1*c2), rat(s*c1*s2), rat(s*s1*c2), rat(s*s1*s2))
                if regime(tuple(T[i]+Ep[i] for i in range(4))) != base: found = s; break
            s *= step
        out.append(dict(T=[str(x) for x in T], rho=p["rho"], kappa=p["kappa"], witness_ratio=None if found is None else round(found/p["eps_cert"], 1)))
    return out

def sim_ar3(sysd, pi, z0, N, eta_override=None):
    V, lam, mu = sysd["V"], sysd["lam"], sysd["mu"]; Vi = inv(V); Tm = mm(mm(V, (lam, Fr(0), Fr(0), mu)), Vi)
    z = z0; us = [z[0]]; ok_rate = ok_cone = True; eta = None
    y = ar3_x0(sysd, z0)
    if pi["kind"] == "ADV_REL": eta = pi["eta"]
    if pi["kind"] == "REL_QUANT": eta = sysd["V_inf"]*sysd["Vinv_inf"]*Fr(1, 2**pi["bits"])
    if eta_override is not None: eta = eta_override
    for _ in range(N):
        if pi["kind"] in ("ADV_ABS", "ADV_REL", "DEADZONE"):
            zt = (lam*z[0], mu*z[1])
            if pi["kind"] == "DEADZONE": z2 = (Fr(0), zt[1]) if abs(zt[0]) < pi["theta"] else zt
            else:
                bound = pi["h"] if pi["kind"] == "ADV_ABS" else pi["eta"]*max(abs(z[0]), abs(z[1]))
                z2 = (zt[0] - sgn(zt[0])*min(bound, abs(zt[0])), zt[1] + sgn(zt[1])*bound)
            y = ar3_x0(sysd, z2)
        else:
            yt = apply(Tm, y)
            if pi["kind"] == "ROUND_ABS": y = tuple(round(c/pi["h"])*pi["h"] for c in yt)
            else: y = tuple(_relq(c, pi["bits"]) for c in yt)
            z2 = (Vi[0]*y[0]+Vi[1]*y[1], Vi[2]*y[0]+Vi[3]*y[1])
        if z[0] != 0:
            r = abs(z2[0])/abs(z[0])
            if eta is not None and not (lam - eta <= r <= lam + eta): ok_rate = False
        if abs(z2[1]) > abs(z2[0]): ok_cone = False
        z = z2; us.append(z[0])
    inc = all(abs(us[i+1]) > abs(us[i]) for i in range(len(us)-1))
    return dict(escape=inc and abs(us[-1]) > abs(us[0]), cone=ok_cone and ok_rate, collapsed=us[-1] == 0)

def _relq(x, bits):
    if x == 0: return Fr(0)
    a = abs(x); e = a.numerator.bit_length() - a.denominator.bit_length()
    if Fr(2)**e > a: e -= 1
    q = Fr(2)**(e - bits + 1); return round(x/q)*q

def compare_ar3(cases, pred):
    N = P["ar3_N"]; res = []; by = {}
    for (sysd, pi, z0), p in zip(cases["AR-3"], pred["AR-3"]):
        o = sim_ar3(sysd, pi, z0, N); v = p["verdict"]
        if v in ("ESCAPE",): r = "AGREE" if o["escape"] else "DISAGREE"
        elif v == "CONE": r = "AGREE" if (o["cone"] and o["escape"] == o["escape"]) else "DISAGREE"
        elif v == "NO-ESCAPE": r = "AGREE" if not o["escape"] else "DISAGREE"
        else: r = "ABSTAIN"
        key = pi["kind"]; by.setdefault(key, []).append((r, v, o, p))
        res.append(r)
    out = dict(overall=_tally(res), by_projection={}, disagreements=[])
    for k, rows in by.items():
        t = _tally([r for r, *_ in rows]); ab = [x for x in rows if x[0] == "ABSTAIN"]
        t["abstain_but_orbit_escapes"] = sum(1 for x in ab if x[2]["escape"]); t["abstain_and_orbit_does_not_escape"] = len(ab) - t["abstain_but_orbit_escapes"]
        out["by_projection"][k] = t
    for (sysd, pi, z0), p, r in zip(cases["AR-3"], pred["AR-3"], res):
        if r == "DISAGREE" and len(out["disagreements"]) < 15:
            out["disagreements"].append(dict(pi={k: str(v) for k, v in pi.items()}, z0=[str(c) for c in z0], lam=str(sysd["lam"]), mu=str(sysd["mu"]), verdict=p["verdict"]))
    return out

# ================================================================== reports
POSTHOC_MD = """
---
## Post-hoc amendment (written AFTER the frozen comparison; exploratory; not covered by the hash above)
The frozen comparison falsified the k-bit quantizer clause of AR-3 (REL_QUANT): {n_dis} of {n_tot} cases disagreed, all of that one clause.
Cause (a derivation error in the frozen rule, found by the comparison): the quantizer rounds the image T y, so its error is relative to |T y|,
not to |y|. The frozen conversion eta_eig = kappa_inf(V) 2^-k omitted the factor |lam|. Amended clause: eta_eig = kappa_inf(V) |lam| 2^-k.
Re-run of the amended clause on the same {n_tot} cases (exploratory, same exact simulation): AGREE {a}, DISAGREE {d}, ABSTAIN {ab}.
This amendment must be confirmed on a fresh seeded test set before it is treated as part of AR-3.
"""

def posthoc_relquant(cases):
    idx = [i for i, (sysd, pi, z0) in enumerate(cases["AR-3"]) if pi["kind"] == "REL_QUANT"]; rows = []
    for i in idx:
        sysd, pi, z0 = cases["AR-3"][i]; p = ar3_predict_amended_relquant(sysd, pi, z0)
        if p["verdict"] == "CONE":
            o = sim_ar3(sysd, pi, z0, P["ar3_N"], eta_override=p["eta_eig"]); rows.append("AGREE" if o["cone"] else "DISAGREE")
        else: rows.append("ABSTAIN")
    t = _tally(rows); t["rule_sha256"] = sha(inspect.getsource(ar3_predict_amended_relquant).encode()); return t

# ================================================================== AR-3.1 CONFIRMATION (fresh, frozen beforehand)
CONFIRM = dict(seed=SEED + 100, random_systems=60, bits=[4, 8, 12], boundary_bases=20, boundary_bits=[7, 8, 9, 10],
               boundary_delta=[Fr(-1, 100), Fr(0), Fr(1, 100)], N=60,
               states_u0=[Fr(1, 2), Fr(-1), Fr(3)], states_w_over_u=[Fr(0), Fr(1, 2), Fr(-1, 2), Fr(1), Fr(3, 2)])
PREVIOUS_AMENDED_SOURCE_SHA256 = "2cf5d68ae0b293fb2f06a37579e0dd216870ae3046efb0ec11cf6b9c713ff3f1"   # recorded in the earlier run

AR31_MD = """
---
## AR-3.1  Corrected k-bit quantizer clause (frozen before the confirmation set is generated)
Clause: for the k-bit relative quantizer (each coordinate of T y rounded to k significant bits), eta_eig = kappa_inf(V) |lam| 2^-k,
and the CONE verdict of AR-3 applies with this eta_eig (conditions: |lam| > 1, |lam| > |mu|, u0 != 0, eta_eig <= (|lam|-|mu|)/2, |w0| <= |u0|), else ABSTAIN.
Origin: the frozen AR-3 clause used eta_eig = kappa_inf(V) 2^-k and was falsified in 92 of 540 REL_QUANT cases (retained in the report).
The amended clause was then explored post hoc on the same 540 cases (234 agree, 306 abstain, 0 disagree). The source hash of the amended rule function in
this run must equal the hash recorded in that earlier run: `{prev}`.
Confirmation set (all fresh; the original test set is not reused): seed {seed}; {rs} random systems (V with entries n/2, n in -6..6, det != 0; lam = +-m/4 in [1.25, 6]; |mu| < |lam|)
x bits {bits} x 15 states (u0 in {{1/2,-1,3}}, w0/u0 in {{0,1/2,-1/2,1,3/2}}); plus {bb} near-boundary base systems with lam = 3 and
|mu| = |lam| - 2 eta (1+delta) for delta in {{-1/100, 0, +1/100}}, bits {bbits}, same 15 states. The boundary families put eta_eig 1% above the cone-theorem limit (just outside: the rule must abstain), exactly at the limit (the rule must apply), and 1% below it (just inside), with |w0| = |u0| included.
Independent check of the conversion itself: at every step, the observed eigen-coordinate quantization error |V^-1 (Q(Ty) - Ty)|_inf / |z|_inf must not exceed eta_eig.
Simulation: exact rational arithmetic, N = {N} steps.
Success criteria: zero DISAGREE among CONE predictions (rate in [|lam|-eta, |lam|+eta] at every step, |w| <= |u|), zero violations of the per-step error bound, and
the frozen-original conversion (without |lam|) is violated by the observed error in at least one case (shows the factor is needed, not decorative).
The 92 original disagreements remain part of the record.
"""

def _ar31_cases():
    rr = E.mulberry32(CONFIRM["seed"]); r = lambda lo, hi: lo + int(rr() % (hi - lo + 1)); cases = []
    infn = lambda M: max(abs(M[0])+abs(M[1]), abs(M[2])+abs(M[3]))
    def rand_V():
        while True:
            V = tuple(Fr(r(-6, 6), 2) for _ in range(4))
            if det(V) != 0: return V
    states = [(u, u*f) for u in CONFIRM["states_u0"] for f in CONFIRM["states_w_over_u"]]
    for _ in range(CONFIRM["random_systems"]):
        V = rand_V(); lam = Fr(r(5, 24), 4)*(1 if r(0, 1) else -1); mu = Fr(r(0, int(abs(lam)*4) - 1), 4)*(1 if r(0, 1) else -1)
        sysd = dict(V=V, lam=lam, mu=mu, Vinv_inf=infn(inv(V)), V_inf=infn(V))
        for b in CONFIRM["bits"]:
            for z0 in states: cases.append(("random", sysd, b, z0))
    for _ in range(CONFIRM["boundary_bases"]):
        V = rand_V(); b = CONFIRM["boundary_bits"][r(0, len(CONFIRM["boundary_bits"]) - 1)]; lam = Fr(3)
        eta = infn(V)*infn(inv(V))*lam*Fr(1, 2**b)
        for dlt in CONFIRM["boundary_delta"]:
            mu_abs = lam - 2*eta*(1 + dlt)
            if mu_abs < 0 or mu_abs >= lam: continue
            sysd = dict(V=V, lam=lam, mu=mu_abs, Vinv_inf=infn(inv(V)), V_inf=infn(V))
            for z0 in states: cases.append(("boundary-just-outside(-1%)" if dlt < 0 else "boundary-at-limit" if dlt == 0 else "boundary-just-inside(+1%)", sysd, b, z0))
    return cases

def _sim_confirm(sysd, bits, z0, N, eta_am, eta_old):
    V, lam, mu = sysd["V"], sysd["lam"], sysd["mu"]; Vi = inv(V); Tm = mm(mm(V, (lam, Fr(0), Fr(0), mu)), Vi)
    y = ar3_x0(sysd, z0); z = z0; ok_rate = ok_cone = True; worst = Fr(0)
    for _ in range(N):
        yt = apply(Tm, y); y2 = tuple(_relq(c, bits) for c in yt); err = (y2[0]-yt[0], y2[1]-yt[1])
        ee = (Vi[0]*err[0]+Vi[1]*err[1], Vi[2]*err[0]+Vi[3]*err[1]); nz = max(abs(z[0]), abs(z[1]))
        if nz: worst = max(worst, max(abs(ee[0]), abs(ee[1]))/nz)
        z2 = (Vi[0]*y2[0]+Vi[1]*y2[1], Vi[2]*y2[0]+Vi[3]*y2[1])
        if z[0] != 0:
            ratio = abs(z2[0])/abs(z[0])
            if not (abs(lam) - eta_am <= ratio <= abs(lam) + eta_am): ok_rate = False
        if abs(z2[1]) > abs(z2[0]): ok_cone = False
        y, z = y2, z2
    return dict(cone=ok_rate and ok_cone, worst_err_ratio=worst, bound_ok=worst <= eta_am, old_bound_violated=worst > eta_old)

def confirm_ar31():
    cases = _ar31_cases(); rows = []; fam = {}
    for fam_name, sysd, bits, z0 in cases:
        pi = dict(kind="REL_QUANT", bits=bits); p = ar3_predict_amended_relquant(sysd, pi, z0)
        eta_am = sysd["V_inf"]*sysd["Vinv_inf"]*abs(sysd["lam"])*Fr(1, 2**bits); eta_old = eta_am/abs(sysd["lam"])
        o = _sim_confirm(sysd, bits, z0, CONFIRM["N"], eta_am, eta_old)
        if p["verdict"] == "CONE": r = "AGREE" if (o["cone"] and o["bound_ok"]) else "DISAGREE"
        else: r = "ABSTAIN"
        rows.append((fam_name, r, o, eta_am, p))
    out = dict(total=_tally([r for _, r, *_ in rows]), by_family={}, disagreements=[])
    for f in sorted({x[0] for x in rows}):
        sub = [x for x in rows if x[0] == f]; t = _tally([x[1] for x in sub])
        t["abstain_but_cone_holds"] = sum(1 for x in sub if x[1] == "ABSTAIN" and x[2]["cone"]); out["by_family"][f] = t
    cone = [x for x in rows if x[1] != "ABSTAIN"]
    out["per_step_error_bound"] = dict(cases_checked=len(rows), amended_bound_violations=sum(not x[2]["bound_ok"] for x in rows),
                                       frozen_original_bound_violated_in=sum(x[2]["old_bound_violated"] for x in rows),
                                       max_observed_over_amended_bound=max(float(x[2]["worst_err_ratio"]/x[3]) for x in rows))
    out["necessity_of_lambda_factor_demonstrated"] = out["per_step_error_bound"]["frozen_original_bound_violated_in"] > 0
    out["success_criteria_met"] = bool(out["total"]["DISAGREE"] == 0 and out["per_step_error_bound"]["amended_bound_violations"] == 0
                                       and out["necessity_of_lambda_factor_demonstrated"] and len(cone) > 0)
    for fam_name, r, o, eta_am, p in rows:
        if r == "DISAGREE" and len(out["disagreements"]) < 10: out["disagreements"].append(dict(family=fam_name, eta=float(eta_am)))
    out["amended_rule_source_sha256"] = sha(inspect.getsource(ar3_predict_amended_relquant).encode())
    out["matches_hash_recorded_in_earlier_run"] = out["amended_rule_source_sha256"] == PREVIOUS_AMENDED_SOURCE_SHA256
    return out

# ================================================================== PRD-1  Projection route dependence (separate experiment)
PRD = dict(seed=SEED + 200, systems=30, N=200, states_random=12,
           dz_theta=[Fr(1, 4), Fr(1, 2), Fr(1), Fr(2)], clip_c=[Fr(1), Fr(2), Fr(4)], lat_h=[Fr(1, 4), Fr(1, 2), Fr(1)],
           lin_a=[Fr(1, 2), Fr(2)], lin_b=[Fr(1, 2), Fr(2)],
           u_grid=[Fr(1, 8), Fr(1, 4), Fr(1, 2), Fr(1), Fr(2), Fr(4)],
           w_grid=[Fr(0), Fr(1, 8), Fr(1, 4), Fr(1, 2), Fr(1), Fr(2), Fr(4)],
           mu_abs=[Fr(0), Fr(1, 4), Fr(1, 2), Fr(3, 4), Fr(7, 8), Fr(1), Fr(5, 4), Fr(3, 2), Fr(2)],
           lin_recognition_triples=40, divergence_factor=10**6, decay_factor=10**6)

PRD1_MD = """# PRD-1  Projection route dependence (frozen before any case is generated)

Status of AR-3.1 when this was frozen: **closed as confirmed within its tested domain.** The corrected conversion eta_eig = kappa_inf(V) |lam| 2^-k holds
under the rule's stated conditions, and the cone condition is sufficient but conservative. The standalone checker (`independent_check_ar31.py`) is the evidence for the
bound itself; the stored records are evidence of internal consistency only. The condition is not to be adjusted using the observation that the cone often holds outside it.
Existing AR-1..3 and AR-3.1 files and results are not modified by this experiment.

## Question
Two systems with identical unprojected spectral data (T, x0) can have different projected asymptotic behaviour. Does a rule that examines the *structure of the projection*
predict the projected regime, on unseen systems and projections, where a classical method that knows only the projection's error bound cannot?

## Domain (a stated restriction)
x_(n+1) = Pi(T x_n) in the **spectral frame**: T = diag(lam, mu), lam, mu rational, |lam| > 1, |lam| > |mu|, state z = (u, w), u0 != 0, Pi(0) = 0.
Projections written in another frame need a frame conversion and are out of scope here.

## Projection families (all five are retained)
- **DZ(theta)** dead-zone: u -> 0 if |u| < theta, else identity; w untouched.
- **CLIP(c)** saturation: each coordinate clamped to [-c, c].
- **LAT(h)** lattice rounding: each coordinate rounded to the nearest multiple of h (ties to even).
- **GATE** state-gated zeroing: u -> 0 if |u| <= |w|, else identity.
- **LINP(a), LINQ(b)** linear kernel projections (control): LINP(y) = (0, a y1 + y2), LINQ(y) = (y1 + b y2, 0). The orbit is the linear recursion with matrix Pi T.
Pi is applied to y = T z.

## Verdicts
DIVERGENT (|z_n| -> infinity), COLLAPSE (z_n = 0 exactly from some step), CONVERGENT (z_n -> 0), BOUNDED(B) (|z_n|_inf <= B for all n >= 1), ABSTAIN,
and, for linear Pi only, LINEAR-REDUCTION (the rule recognises the case as reducible to the classical analysis of Pi T and claims no regime).

## Rule R (structure-aware; may not simulate and may not call the exact classifier)
Notation: al = |lam|, am = |mu|.
- DZ: if al |u0| >= theta: DIVERGENT. Else u is erased at step 1 and stays 0; w1 = mu w0. If w1 = 0: COLLAPSE; am < 1: CONVERGENT; am = 1: BOUNDED(|w0|); am > 1: DIVERGENT.
- CLIP: BOUNDED(c).
- LAT: (i) DIVERGENT if |u0| > (h/2)/(al-1); (ii) DIVERGENT if am > 1 and |w0| > (h/2)/(am-1); (iii) COLLAPSE if al |u0| < h/2 and am |w0| < h/2;
  (iv) BOUNDED(am |w0| + h/2) if al |u0| < h/2 and am <= 1; (v) otherwise ABSTAIN.
- GATE: if al |u0| > am |w0|: DIVERGENT (the ratio |w|/|u| shrinks by am/al, so u is never gated). Else u is erased at step 1 and stays 0: am < 1: CONVERGENT; am = 1: BOUNDED(|w0|); am > 1: DIVERGENT.
- LINP, LINQ: LINEAR-REDUCTION.

## Classical comparator C (knows T and the projection's *error bound* only; plus the exact classifier on Pi T for linear Pi)
Error bounds: DZ: absolute theta; LAT: absolute h/2; CLIP and GATE: no finite absolute bound, and the relative bound of GATE (eta = al) violates eta <= (al-am)/2, so C abstains.
For DZ and LAT: DIVERGENT if |u0| > e/(al-1), or am > 1 and |w0| > e/(am-1) (escape-radius theorem, e the absolute bound); otherwise ABSTAIN.
For LINP/LINQ: the exact classifier applied to the matrix Pi T (divergent -> DIVERGENT, convergent -> CONVERGENT, periodic or bounded -> BOUNDED).

## Ground truth and evidence levels
Exact rational simulation, N = {N} steps, no floating point. Finite-horizon evidence alone never certifies an asymptotic claim. Asymptotic certificates used:
- exact return to 0 (Pi(0) = 0, so 0 is absorbing) -> COLLAPSE;
- exact repetition of a state (deterministic autonomous recursion) -> periodic forever, hence BOUNDED;
- an a posteriori escape-radius certificate from the orbit (DZ and LAT only, the families with a finite absolute error bound).
Each certified prediction is scored: CONFIRMED_ASYMPTOTIC (a certificate above agrees), CONSISTENT_FINITE_HORIZON (no contradiction within N, no certificate), or CONTRADICTED.
Contradiction rules: DIVERGENT is contradicted by a zero hit, a repeated state, decay below |z0|/{decay}, or growth below {div} x max(1,|z0|); COLLAPSE by no zero hit;
CONVERGENT by neither a zero hit nor decay below |z0|/{decay}; BOUNDED(B) by growth or by any |z_n|_inf > B for n >= 1.
Growth and decay thresholds are fixed constants, chosen so that every divergent or convergent system in the test set clears them by orders of magnitude at N = {N}.

## Test set (fresh seed {seed}; nothing from earlier experiments is reused)
{systems} systems: lam = +-m/4 with m in 5..20, |mu| drawn from {mu_abs} with |mu| < |lam|, random signs. For each system, every family and parameter
(DZ theta in {dz}, CLIP c in {clip}, LAT h in {lat}, GATE, LINP a in {lina}, LINQ b in {linb}): {sr} random states (u0 in +-{ug}, w0 in +-{wg}, u0 != 0) plus exact tie states
(DZ: |lam u0| = theta; GATE: |lam u0| = |mu w0|; LAT: |lam u0| = h/2).
Recognition check: for every family, additivity and homogeneity of Pi are tested exactly on {lt} seeded random triples; the declared linear/nonlinear status must match.
Route dependence is measured against the unprojected exact classifier, which for every system and u0 != 0 returns divergent.

## Success criteria (stated in advance)
1. Zero CONTRADICTED among the certified predictions of R, and among those of C.
2. Coverage reported per family: certified / abstained, for R and for C, with the cases certified by R only, by C only, and by both.
3. Of the cases where the unprojected classifier is wrong about the projected regime (projection-induced flips), the number certified correctly by R and by C.
4. The recognition check passes for all five families, and for the linear control the orbit equals the matrix recursion Pi T exactly for all N steps.
5. Computational cost is reported separately from correctness: R evaluates a closed-form condition (no orbit); simulation costs N steps per case.
The strongest claim these criteria can support: for the stated domain, a structure-aware rule certifies the projected regime without trajectory simulation, with broader coverage than error-bound classical analysis.
They do not support a claim of superiority over classical mathematics: a classical analyst who reads the same projection definition can derive the same conditions.
"""

def pi_apply(fam, y):
    k = fam["kind"]
    if k == "DZ": return (Fr(0) if abs(y[0]) < fam["theta"] else y[0], y[1])
    if k == "CLIP": c = fam["c"]; return (max(-c, min(c, y[0])), max(-c, min(c, y[1])))
    if k == "LAT": h = fam["h"]; return (round(y[0]/h)*h, round(y[1]/h)*h)
    if k == "GATE": return (Fr(0) if abs(y[0]) <= abs(y[1]) else y[0], y[1])
    if k == "LINP": return (Fr(0), fam["a"]*y[0] + y[1])
    if k == "LINQ": return (y[0] + fam["b"]*y[1], Fr(0))
    raise ValueError(k)

def prd_rule(sysd, fam, z0):
    """Structure-aware rule R. Closed-form conditions only: no orbit, no exact classifier."""
    lam, mu = sysd["lam"], sysd["mu"]; al, am = abs(lam), abs(mu); u0, w0 = z0; k = fam["kind"]
    if not (al > 1 and al > am) or u0 == 0: return dict(verdict="ABSTAIN", reason="out of scope")
    if k in ("LINP", "LINQ"): return dict(verdict="LINEAR-REDUCTION", reason="Pi linear: governed by the matrix Pi T")
    if k == "DZ":
        if al*abs(u0) >= fam["theta"]: return dict(verdict="DIVERGENT", basis="u never erased")
        w1 = mu*w0
        if w1 == 0: return dict(verdict="COLLAPSE", basis="u erased at step 1, w1 = 0")
        if am < 1: return dict(verdict="CONVERGENT", basis="u erased, |mu| < 1")
        if am == 1: return dict(verdict="BOUNDED", bound=abs(w0), basis="u erased, |mu| = 1")
        return dict(verdict="DIVERGENT", basis="u erased, |mu| > 1")
    if k == "CLIP": return dict(verdict="BOUNDED", bound=fam["c"], basis="range of Pi inside the box")
    if k == "LAT":
        h = fam["h"]
        if abs(u0) > (h/2)/(al - 1): return dict(verdict="DIVERGENT", basis="u beyond escape radius")
        if am > 1 and abs(w0) > (h/2)/(am - 1): return dict(verdict="DIVERGENT", basis="w beyond escape radius")
        if al*abs(u0) < h/2 and am*abs(w0) < h/2: return dict(verdict="COLLAPSE", basis="both rounded to 0 at step 1")
        if al*abs(u0) < h/2 and am <= 1: return dict(verdict="BOUNDED", bound=am*abs(w0) + h/2, basis="u erased, |w| nonincreasing on the lattice")
        return dict(verdict="ABSTAIN", reason="no certificate")
    if k == "GATE":
        if al*abs(u0) > am*abs(w0): return dict(verdict="DIVERGENT", basis="ratio |w|/|u| shrinks; u never gated")
        if am < 1: return dict(verdict="CONVERGENT", basis="u gated at step 1, |mu| < 1")
        if am == 1: return dict(verdict="BOUNDED", bound=abs(w0), basis="u gated, |mu| = 1")
        return dict(verdict="DIVERGENT", basis="u gated, |mu| > 1")
    return dict(verdict="ABSTAIN", reason="unknown family")

def prd_comparator_errorbound(sysd, fam, z0):
    """Classical comparator C for nonlinear Pi: knows T and the absolute error bound e of Pi only (escape-radius theorem)."""
    lam, mu = sysd["lam"], sysd["mu"]; al, am = abs(lam), abs(mu); u0, w0 = z0
    e = {"DZ": fam.get("theta"), "LAT": (fam["h"]/2 if fam["kind"] == "LAT" else None)}.get(fam["kind"])
    if e is None or not (al > 1 and al > am) or u0 == 0: return dict(verdict="ABSTAIN", reason="no finite absolute error bound or out of scope")
    if abs(u0) > e/(al - 1) or (am > 1 and abs(w0) > e/(am - 1)): return dict(verdict="DIVERGENT", basis="escape radius")
    return dict(verdict="ABSTAIN", reason="inside escape radius")

PRD_RULE_FUNCS = [prd_rule, prd_comparator_errorbound]

def _prd_cases():
    rr = E.mulberry32(PRD["seed"]); r = lambda lo, hi: lo + int(rr() % (hi - lo + 1)); systems = []
    while len(systems) < PRD["systems"]:
        lam = Fr(r(5, 20), 4)*(1 if r(0, 1) else -1); mu = PRD["mu_abs"][r(0, len(PRD["mu_abs"]) - 1)]*(1 if r(0, 1) else -1)
        if abs(mu) < abs(lam): systems.append(dict(lam=lam, mu=mu))
    fams = [dict(kind="DZ", theta=t) for t in PRD["dz_theta"]] + [dict(kind="CLIP", c=c) for c in PRD["clip_c"]] + \
           [dict(kind="LAT", h=h) for h in PRD["lat_h"]] + [dict(kind="GATE")] + [dict(kind="LINP", a=a) for a in PRD["lin_a"]] + [dict(kind="LINQ", b=b) for b in PRD["lin_b"]]
    cases = []
    for sy in systems:
        for fam in fams:
            states = []
            for _ in range(PRD["states_random"]):
                u = PRD["u_grid"][r(0, len(PRD["u_grid"]) - 1)]*(1 if r(0, 1) else -1); w = PRD["w_grid"][r(0, len(PRD["w_grid"]) - 1)]*(1 if r(0, 1) else -1); states.append((u, w, "random"))
            al, am = abs(sy["lam"]), abs(sy["mu"])
            if fam["kind"] == "DZ": states.append((fam["theta"]/sy["lam"], Fr(1, 2), "tie"))
            if fam["kind"] == "GATE" and sy["mu"] != 0: states.append((Fr(1, 2), sy["lam"]*Fr(1, 2)/sy["mu"], "tie"))
            if fam["kind"] == "LAT": states.append((fam["h"]/(2*sy["lam"]), Fr(1, 4), "tie"))
            for u, w, tag in states: cases.append((sy, fam, (u, w), tag))
    return cases

def _prd_orbit(sy, fam, z0, N):
    z = z0; orb = [z]
    for _ in range(N): z = pi_apply(fam, (sy["lam"]*z[0], sy["mu"]*z[1])); orb.append(z)
    return orb

def _prd_evidence(sy, fam, orb):
    nrm = lambda z: max(abs(z[0]), abs(z[1])); al, am = abs(sy["lam"]), abs(sy["mu"]); ev = {}
    ev["hit_zero"] = next((n for n, z in enumerate(orb) if z == (0, 0)), None)
    seen = {}; ev["cycle"] = None
    for n, z in enumerate(orb):
        if z in seen: ev["cycle"] = (seen[z], n - seen[z]); break
        seen[z] = n
    n0, nN = nrm(orb[0]), nrm(orb[-1])
    ev["growing"] = nN > PRD["divergence_factor"]*max(1, n0); ev["decaying"] = nN < Fr(n0)/PRD["decay_factor"]
    ev["max_after0"] = max(nrm(z) for z in orb[1:])
    e = {"DZ": fam.get("theta"), "LAT": (fam["h"]/2 if fam["kind"] == "LAT" else None)}.get(fam["kind"]); ev["div_cert"] = False
    if e is not None:
        for z in orb:
            if abs(z[0]) > e/(al - 1) or (am > 1 and abs(z[1]) > e/(am - 1)): ev["div_cert"] = True; break
    ev["truth"] = "collapse" if ev["hit_zero"] is not None else "periodic/bounded" if ev["cycle"] else "divergent" if ev["growing"] else "convergent" if ev["decaying"] else "bounded"
    return ev

def _prd_score(v, ev, classical_exact=False):
    t = v["verdict"]
    if t in ("ABSTAIN", "LINEAR-REDUCTION"): return t
    if t == "DIVERGENT":
        if ev["hit_zero"] is not None or ev["cycle"] or ev["decaying"] or not ev["growing"]: return "CONTRADICTED"
        o = "CONFIRMED_ASYMPTOTIC" if ev["div_cert"] else "CONSISTENT_FINITE_HORIZON"
    elif t == "COLLAPSE": o = "CONFIRMED_ASYMPTOTIC" if ev["hit_zero"] is not None else "CONTRADICTED"
    elif t == "CONVERGENT":
        if ev["hit_zero"] is not None: o = "CONFIRMED_ASYMPTOTIC"
        elif ev["decaying"]: o = "CONSISTENT_FINITE_HORIZON"
        else: o = "CONTRADICTED"
    elif t == "BOUNDED":
        B = v.get("bound")
        if ev["growing"] or (B is not None and ev["max_after0"] > B): return "CONTRADICTED"
        o = "CONFIRMED_ASYMPTOTIC" if (ev["cycle"] or ev["hit_zero"] is not None) else "CONSISTENT_FINITE_HORIZON"
    else: o = "CONTRADICTED"
    if classical_exact and o == "CONSISTENT_FINITE_HORIZON": o = "CONFIRMED_ASYMPTOTIC"      # exact theorem on a linear recursion
    return o

def _tally_prd(rows):
    keys = ("CONFIRMED_ASYMPTOTIC", "CONSISTENT_FINITE_HORIZON", "CONTRADICTED", "ABSTAIN", "LINEAR-REDUCTION")
    t = {k: rows.count(k) for k in keys}; t["total"] = len(rows); t["certified"] = sum(t[k] for k in keys[:3]); return t

def _lin_cmap(sy, fam, z0, amended=False):
    """Classical verdict on the linear control Pi T. amended=False is the mapping frozen before the first PRD-1 run;
    amended=True is the post-hoc correction (exact-classifier 'convergent to a nonzero fixed point / 2-cycle' is BOUNDED, not CONVERGENT-to-origin)."""
    M = ((Fr(0), Fr(0), fam["a"]*sy["lam"], sy["mu"]) if fam["kind"] == "LINP" else (sy["lam"], fam["b"]*sy["mu"], Fr(0), Fr(0)))
    cl = E.classical(M, z0); cmap = {"divergent": "DIVERGENT", "convergent": "CONVERGENT", "periodic": "BOUNDED", "bounded": "BOUNDED"}
    pc = dict(verdict=cmap[cl["cls"]], basis="exact classifier on Pi T")
    if cl["cls"] == "convergent" and "collapse" in cl["sub"]: pc["verdict"] = "COLLAPSE"
    elif amended and cl["cls"] == "convergent" and ("nonzero" in cl["sub"] or "cycle" in cl["sub"]): pc["verdict"] = "BOUNDED"
    return pc

def run_prd1(outdir):
    check_rule_independence(prd=True)
    t0 = datetime.datetime.now(datetime.timezone.utc)
    text = PRD1_MD.format(N=PRD["N"], seed=PRD["seed"], systems=PRD["systems"], mu_abs=[str(x) for x in PRD["mu_abs"]], dz=[str(x) for x in PRD["dz_theta"]],
                          clip=[str(x) for x in PRD["clip_c"]], lat=[str(x) for x in PRD["lat_h"]], lina=[str(x) for x in PRD["lin_a"]], linb=[str(x) for x in PRD["lin_b"]],
                          sr=PRD["states_random"], ug=[str(x) for x in PRD["u_grid"]], wg=[str(x) for x in PRD["w_grid"]], lt=PRD["lin_recognition_triples"],
                          div=PRD["divergence_factor"], decay=PRD["decay_factor"])
    h_rules = sha((text + json.dumps(PRD, sort_keys=True, default=str)).encode())
    with open(os.path.join(outdir, "prd1_rules.md"), "w") as f: f.write(text + f"\n---\nSHA-256 of this text + frozen parameters: `{h_rules}`\n")
    # predict (rule R and comparator C), before any simulation
    cases = _prd_cases(); pred = []
    for sy, fam, z0, tag in cases:
        pr = prd_rule(sy, fam, z0)
        if fam["kind"] in ("LINP", "LINQ"):
            pc = _lin_cmap(sy, fam, z0, False)
        else: pc = prd_comparator_errorbound(sy, fam, z0)
        pred.append((pr, pc))
    h_pred = sha([[{k: str(v) for k, v in p.items()} for p in pair] for pair in pred])
    t1 = datetime.datetime.now(datetime.timezone.utc)
    # recognition check
    rr = E.mulberry32(PRD["seed"] + 1); rec = {}
    for fam in [dict(kind="DZ", theta=Fr(1)), dict(kind="CLIP", c=Fr(1)), dict(kind="LAT", h=Fr(1, 2)), dict(kind="GATE"), dict(kind="LINP", a=Fr(2)), dict(kind="LINQ", b=Fr(1, 2))]:
        ok = True
        for _ in range(PRD["lin_recognition_triples"]):
            q = lambda: Fr(int(rr() % 41) - 20, 4); a_, b_, s_ = (q(), q()), (q(), q()), q()
            sm = pi_apply(fam, (a_[0]+b_[0], a_[1]+b_[1])); pa, pb = pi_apply(fam, a_), pi_apply(fam, b_)
            if sm != (pa[0]+pb[0], pa[1]+pb[1]) or pi_apply(fam, (s_*a_[0], s_*a_[1])) != (s_*pa[0], s_*pa[1]): ok = False; break
        rec[fam["kind"]] = dict(declared_linear=fam["kind"] in ("LINP", "LINQ"), found_linear=ok, correct=(ok == (fam["kind"] in ("LINP", "LINQ"))))
    # simulate and score
    fams = {}; contrad = []; flips = dict(total=0, R=0, C=0); both = dict(R_only=0, C_only=0, both=0, neither=0); ties = dict(cases=0, contradicted=0)
    recur = dict(cases=0, exact=0); linAm = []; unproj_wrong = 0; sim_steps = 0
    for (sy, fam, z0, tag), (pr, pc) in zip(cases, pred):
        orb = _prd_orbit(sy, fam, z0, PRD["N"]); ev = _prd_evidence(sy, fam, orb); sim_steps += PRD["N"]
        key = fam["kind"]; d = fams.setdefault(key, dict(R=[], C=[]))
        lin = key in ("LINP", "LINQ")
        if lin:
            M = ((Fr(0), Fr(0), fam["a"]*sy["lam"], sy["mu"]) if key == "LINP" else (sy["lam"], fam["b"]*sy["mu"], Fr(0), Fr(0)))
            z = z0; exact = True
            for n in range(1, PRD["N"] + 1):
                z = apply(M, z)
                if z != orb[n]: exact = False; break
            recur["cases"] += 1; recur["exact"] += exact
            sr = "LINEAR-REDUCTION"; sc = _prd_score(pc, ev, classical_exact=True)
            linAm.append(_prd_score(_lin_cmap(sy, fam, z0, True), ev, classical_exact=True))
        else: sr = _prd_score(pr, ev); sc = _prd_score(pc, ev)
        d["R"].append(sr); d["C"].append(sc)
        if "CONTRADICTED" in (sr, sc) and len(contrad) < 20: contrad.append(dict(family=key, params={k: str(v) for k, v in fam.items() if k != "kind"}, lam=str(sy["lam"]), mu=str(sy["mu"]), z0=[str(c) for c in z0], R=sr, C=sc, rule=pr["verdict"], comparator=pc["verdict"]))
        if tag == "tie": ties["cases"] += 1; ties["contradicted"] += (sr == "CONTRADICTED")
        cert = lambda o: o in ("CONFIRMED_ASYMPTOTIC", "CONSISTENT_FINITE_HORIZON")
        if not lin:
            r_c, c_c = cert(sr), cert(sc); both["both" if r_c and c_c else "R_only" if r_c else "C_only" if c_c else "neither"] += 1
        flip = ev["truth"] != "divergent"; unproj = E.classical((sy["lam"], Fr(0), Fr(0), sy["mu"]), z0)["cls"]
        unproj_wrong += (unproj == "divergent" and flip)
        if flip and not lin:
            flips["total"] += 1; flips["R"] += (cert(sr) and pr["verdict"] != "DIVERGENT"); flips["C"] += (cert(sc) and pc["verdict"] != "DIVERGENT")
    out_f = {}
    for k, d in fams.items(): out_f[k] = dict(R=_tally_prd(d["R"]), C=_tally_prd(d["C"]))
    nl = [k for k in fams if k not in ("LINP", "LINQ")]
    allR = sum((fams[k]["R"] for k in nl), []); allC = sum((fams[k]["C"] for k in nl), []); linC = sum((fams[k]["C"] for k in ("LINP", "LINQ") if k in fams), [])
    sumR, sumC, sumL = _tally_prd(allR), _tally_prd(allC), _tally_prd(linC)
    crit = dict(zero_contradicted_R=sumR["CONTRADICTED"] == 0, zero_contradicted_C=sumC["CONTRADICTED"] == 0 and sumL["CONTRADICTED"] == 0,
                recognition_passed=all(v["correct"] for v in rec.values()), linear_control_orbit_equals_matrix_recursion=recur["cases"] == recur["exact"])
    crit["all_criteria_met"] = all(crit.values())
    sumLA = _tally_prd(linAm)
    amend = dict(status="POST-HOC, exploratory; first-run result above is retained unchanged",
                 finding="first-run linear-control mapping sent exact-classifier 'convergent' (which includes convergence to a nonzero fixed point or 2-cycle) to CONVERGENT (-> 0): a mapping error in the comparator, not in rule R",
                 control_contradicted_first_run=sumL["CONTRADICTED"], control_contradicted_amended=sumLA["CONTRADICTED"], control_amended=sumLA,
                 all_criteria_met_after_amendment=(crit["zero_contradicted_R"] and sumC["CONTRADICTED"] == 0 and sumLA["CONTRADICTED"] == 0 and crit["recognition_passed"] and crit["linear_control_orbit_equals_matrix_recursion"]))
    report = dict(prd1_version="1.0", seed=PRD["seed"], frozen_parameters=json.loads(json.dumps(PRD, default=str)),
                  order=dict(rules_frozen_and_hashed=t0.isoformat(timespec="seconds"), predictions_hashed_before_simulation=t1.isoformat(timespec="seconds"),
                             rules_sha256=h_rules, predictions_sha256=h_pred),
                  cases=len(cases), nonlinear_totals=dict(R=sumR, C=sumC), linear_control=dict(C_exact_classifier_on_PiT=sumL, recurrence_check=recur,
                  note="LINEAR-REDUCTION is a recognition, not a regime claim; its verdicts come from the classical classifier on Pi T and earn no credit for R"),
                  per_family=out_f, coverage_overlap_nonlinear=both, tie_states=ties, recognition_check=rec,
                  route_dependence=dict(unprojected_classifier_wrong_on=unproj_wrong, nonlinear_flip_cases=flips["total"], flips_certified_correct_by_R=flips["R"],
                                        flips_certified_correct_by_C=flips["C"], note="flip = finite-horizon projected regime is not divergent although the unprojected classifier says divergent"),
                  cost=dict(simulation_steps_used_for_ground_truth=sim_steps, note="R evaluates a closed-form condition per case (no orbit); the simulation steps are used only for scoring"),
                  contradictions=contrad, success_criteria=crit, posthoc_comparator_amendment=amend)
    with open(os.path.join(outdir, "prd1_report.json"), "w") as f: json.dump(report, f, indent=1, default=str)
    with open(os.path.join(outdir, "prd1_rules.md"), "a") as f:
        f.write(f"""
---
## PRD-1 outcome (appended after the run)
Cases: {len(cases)} ({sumR['total']} nonlinear scored for R and C, {sumL['total']} linear control).
Rule R: certified {sumR['certified']} (confirmed-asymptotic {sumR['CONFIRMED_ASYMPTOTIC']}, consistent-finite-horizon {sumR['CONSISTENT_FINITE_HORIZON']}), abstained {sumR['ABSTAIN']}, **contradicted {sumR['CONTRADICTED']}**.
Comparator C: certified {sumC['certified']}, abstained {sumC['ABSTAIN']}, contradicted {sumC['CONTRADICTED']}. Coverage overlap: {both}.
Projection-induced flips: {flips['total']}; certified correctly by R: {flips['R']}; by C: {flips['C']}.
Linear control: orbit equals the matrix recursion in {recur['exact']}/{recur['cases']} cases; classical Pi T verdicts contradicted: {sumL['CONTRADICTED']}.
Success criteria met (first run, as frozen): **{crit['all_criteria_met']}** ({crit}).

### Post-hoc comparator amendment (exploratory; first-run numbers above are retained)
The {sumL['CONTRADICTED']} first-run contradictions were all in the comparator on the linear control. Cause: the exact classifier's "convergent" includes
convergence to a nonzero fixed point or 2-cycle, which the frozen mapping read as CONVERGENT (to the origin). This is a mapping error in the control comparator; rule R is untouched.
With the corrected mapping the control has {sumLA['CONTRADICTED']} contradictions; criteria met after amendment: **{amend['all_criteria_met_after_amendment']}**.
Because the amendment was made after seeing the data, it is exploratory until confirmed on a fresh seed.
""")
    return report

def audit_md(R, rules_hash):
    ce, it, sim_, sup = R["s5_counterexample"], R["s5_iff_theorem"], R["s5_similarity"], R["s5_sup_orthogonal"]
    c4, e4 = R["s4_thm_relative_cone"], R["s4_thm_absolute_escape"]
    return f"""# Theorem audit: s4 and s5 of "Complex Numbers in the UNNS Substrate"

**Source caveat.** The manuscript text was not available to this module (it is not in the project documents or in the ESC_I
folder). Claims are audited **as stated in the review summary**. The s4 model `x_(n+1) = Pi C_eps (T x_n)` is formalised here as
`x_(n+1) = F(x_n)` with `|F(x) - T x| <= err(x)`, under two error models: absolute (`err = h`) and relative (`err = eta |x|`). That formalisation is an
assumption of this audit and should be checked against the paper's definitions of Pi and C_eps.

Status vocabulary: **ESTABLISHED** (proved here, verified computationally) / **CONDITIONAL** (true under stated hypotheses) /
**FALSE AS STATED** (counterexample) / **CONJECTURAL** (not decided here).

## Summary

| Claim | Original (as summarised) | Status | Corrected statement |
|---|---|---|---|
| s5 | rho(U_theta T) = rho(T) | **FALSE AS STATED** | T5.1 counterexample; true under T5.2-T5.5 |
| s4 | projected recursion preserves dominant growth rate and eigendirection | **FALSE AS STATED**, **CONDITIONAL** | T4.1 (relative error), T4.2 (absolute error) |
| s5 generalisation to n > 2 / cyclotomic lattices | not decided | **CONJECTURAL** | see C1 |

## s5  Phase inletting

**T5.1 (counterexample, exact).** T = [[1,1],[1,1]], U = diag(1,-1): rho(T) = {ce['rho_T']:g}, rho(UT) = {ce['rho_UT']:g}, rho(U T U^-1) = {ce['rho_similar']:g}, UT != TU.
U is even orthogonal, so orthogonality of the phase operator does not rescue the claim.

**T5.2 (similarity, ESTABLISHED).** For invertible U: (U T U^-1)^n (U x0) = U (T^n x0), and U is a bijective bi-Lipschitz map, so rho, the orbit class, its period and its
sub-type are all preserved. Verified exactly on {sim_['cases']} random integer cases: {sim_['violations']} violations.

**T5.3 (commuting, unimodular, ESTABLISHED).** If UT = TU and every eigenvalue of U has modulus 1, then rho(UT) = rho(T)
(simultaneous triangularisation: the eigenvalues of UT are u_i t_i). In 2x2 with U = R_theta, theta not in {{0, pi}}, commuting is equivalent to T in C = span(I, J), i.e. complex multiplication.

**T5.4 (phase law, ESTABLISHED).** For U = R_theta and T = [[a,b],[c,d]]: det(R_theta T) = det T and tr(R_theta T) = (a+d) cos(theta) + (b-c) sin(theta).
So the whole family R_theta T is governed by one number, tau_theta in [-m, m], m^2 = (a+d)^2 + (b-c)^2. Verified exactly with rational rotations: {R['s5_trace_law']['violations']} violations.

**T5.5 (characterisation, ESTABLISHED).** rho(R_theta T) is independent of theta **iff** T is a scaled isometry, T in C u C-bar = {{aI+bJ}} u {{[[a,b],[b,-a]]}}.
*Proof.* rho depends only on (|tau|, det) and is nondecreasing in |tau|; it is constant on |tau| <= 2 sqrt(det) when det > 0 and strictly increasing beyond;
strictly increasing in |tau| when det <= 0. As theta varies, |tau_theta| sweeps [0, m]. For det > 0, constancy needs m^2 <= 4 det, and
4 det - m^2 = -(a-d)^2 - (b+c)^2, so a = d and b = -c. For det <= 0 constancy needs m = 0, i.e. a = -d and b = c. The converse is direct. QED
*Corollary.* rho(UT) = rho(T) for all orthogonal U iff T = r Q with Q orthogonal; and sup over orthogonal U of rho(UT) equals the largest singular value sigma_max(T).
Computational check on integer matrices x 25 rational rotations: {it['invariant_family_cases']} scaled-isometry cases, {it['invariance_violations']} invariance violations;
{it['non_invariant_cases']} other cases, of which {it['grid_failed_to_witness_variation']} show no variation on the finite grid (grid-limited, not counterexamples: T5.5 asserts variation at some theta, possibly off-grid).
Sup check on 300 matrices: {sup['exceed_sigma_max']} exceed sigma_max; largest shortfall of the sampled sup below sigma_max = {sup['max_gap_sigma_minus_sup']:.2e}.

**Implication for admissibility.** Left phase multiplication preserves the spectral regime for scaled isometries and for conjugations; for every other T it
sweeps a range of rho and can cross rho = 1. This is the content frozen as AR-1.

## s4  Projection and spectral persistence

Setting: T = V diag(lam, mu) V^-1 with real eigenvalues, |lam| > 1, |lam| > |mu|; eigen-coordinates z = (u, w); eigen sup-norm.

**C4.0 (counterexamples to the unrestricted claim, exact).**
1. *Absolute error, attracting zero.* T = 2I and Pi = rounding to Z^2: x0 = (1/5, 0) maps to 0 at the first step; the projected orbit is identically 0 (all zero: {R['s4_ce_absolute_rounding']['orbit_all_zero']}) although rho(T) = 2.
2. *Relative error >= |lam|.* F = 0 satisfies |F(x) - T x| <= |lam| |x|; the orbit collapses.
3. *Degenerate state.* T = diag(2, 1/2), x0 = (0,1) lies on the stable eigenline: exact class **{R['s4_ce_stable_eigenline']['exact_class']}** although rho = 2. A growth theorem needs u0 != 0.
4. *Projection onto an invariant subspace.* T = diag(2, 1/2), Pi zeroes u when |u| < 1, x0 = (2/5, 1): the unprojected orbit is {R['s4_ce_deadzone']['unprojected']}; the projected orbit is
   {R['s4_ce_deadzone']['projected_orbit'][-1]} after 8 steps (u erased at step 1, then w decays): a **structural transition divergent -> convergent caused by the projection**.
5. *Complex dominant pair.* No real eigendirection exists. With T = 1.5 R_30deg and relative error eta = 0.3 the per-step norm ratio stays in [1.2, 1.8], but an adversary
   rotates the state by up to arcsin(eta/r) = {math.asin(0.3/1.5):.3f} rad each step: direction drift after 200 steps up to {R['s4_ce_rotation_direction_drift']['adversarial_angle_drift_after_200_steps_rad']:.1f} rad. Rate is robust, direction is not.

**T4.1 (relative error, CONDITIONAL).** Suppose |F(x) - T x|_inf <= eta |x|_inf in eigen-coordinates, eta <= (|lam| - |mu|)/2, and |w0| <= |u0|, u0 != 0.
Then for all n: |w_n| <= |u_n| and |u_(n+1)|/|u_n| in [|lam| - eta, |lam| + eta]. The growth rate is preserved **only up to eta**, not exactly; and divergence is guaranteed when |lam| - eta > 1.
In the limit the direction lies in the cone |w|/|u| <= eta/(|lam| - |mu| - eta). In original coordinates eta is multiplied by kappa_inf(V) = |V|_inf |V^-1|_inf.
*Proof.* |u_(n+1)| >= (|lam| - eta)|u_n| and |w_(n+1)| <= (|mu| + eta)|u_n| <= (|lam| - eta)|u_n| <= |u_(n+1)|, using the cone hypothesis; induct. QED
Adversarial exact simulation ({c4['cases']} cases x 40 steps): {c4['violations']} violations.

**T4.2 (absolute error, CONDITIONAL, sharp).** Suppose |F(x) - T x|_inf <= h. If |u0| > h/(|lam| - 1) then |u_n| increases strictly, |u_(n+1)|/|u_n| -> |lam|, and the direction converges to the dominant eigenline:
growth rate and eigendirection are preserved **exactly in the limit** (the ratio r_n = |w_n|/|u_n| obeys r_(n+1) <= (|mu| r_n + h/|u_n|)/(|lam| - h/|u_n|) -> 0 because |u_n| -> infinity; only the u-part is checked computationally). If |u0| <= h/(|lam| - 1) an admissible projection can stall or erase u (the adversary u -> |lam||u| - h is not escaping), so the threshold is sharp.
*Proof.* |u_(n+1)| >= |lam||u_n| - h > |u_n| iff |u_n| > h/(|lam| - 1); the threshold is then never re-crossed. QED
Adversarial exact simulation ({e4['cases_above_radius']} cases above and {e4['cases_below_radius']} below the radius x 50 steps): {e4['violations']} violations.

**Implication for admissibility.** Projection preserves a divergent regime when it is *small relative to the state* (T4.1) or when the state starts *outside an escape radius* (T4.2); otherwise it can
move the orbit into the stable invariant subspace (C4.0.4). Frozen as AR-3. Original claim as stated: **FALSE**; with these hypotheses: **CONDITIONAL**.

## Conjectures not decided here
**C1.** T5.5 for n x n real matrices: rho(UT) = rho(T) for all orthogonal U iff T is a scaled orthogonal matrix. Only the 2x2 case is proved here.
**C2.** T4.1 and T4.2 for non-diagonalizable T (Jordan blocks), complex dominant pairs (rate only), and cyclotomic lattice projections with non-nearest-point Pi.

Rules module hash (frozen before this audit was written): `{rules_hash}`
"""

def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="output"); a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True); t0 = datetime.datetime.now(datetime.timezone.utc)
    check_rule_independence()
    # 1. FREEZE
    rules_hash = sha((RULES_MD + json.dumps(P, sort_keys=True, default=str)).encode())
    with open(os.path.join(a.out, "admissibility_rules.md"), "w") as f:
        f.write(RULES_MD + f"\n---\nSHA-256 of rules text + frozen parameters: `{rules_hash}`\nSeed: {SEED}. Frozen parameters: `{json.dumps(P, default=str)}`\n")
    ar31_text = AR31_MD.format(prev=PREVIOUS_AMENDED_SOURCE_SHA256, seed=CONFIRM["seed"], rs=CONFIRM["random_systems"], bits=CONFIRM["bits"],
                               bb=CONFIRM["boundary_bases"], bbits=CONFIRM["boundary_bits"], N=CONFIRM["N"])
    ar31_hash = sha((ar31_text + json.dumps(CONFIRM, sort_keys=True, default=str)).encode())
    with open(os.path.join(a.out, "admissibility_rules.md"), "a") as f:
        f.write(ar31_text + f"\nSHA-256 of AR-3.1 text + confirmation parameters: `{ar31_hash}` (computed at the start of the run, before any test case was generated)\n")
    # 2. AUDIT
    R = audit()
    with open(os.path.join(a.out, "theorem_audit.md"), "w") as f: f.write(audit_md(R, rules_hash))
    # 3. PREDICT
    cases = build_cases(); pred = predict_all(cases)
    pred_hash = sha({k: v for k, v in pred.items()})
    t1 = datetime.datetime.now(datetime.timezone.utc)
    # 4. COMPARE
    c1 = compare_ar1(cases, pred); c2 = compare_ar2(cases, pred); c3 = compare_ar3(cases, pred)
    ph = posthoc_relquant(cases)
    disagreements = c1["AR-1a"]["DISAGREE"] + c1["AR-1b"]["DISAGREE"] + c2["safety"]["violations"] + c2["knife_edge"]["violations"] + c3["overall"]["DISAGREE"]
    verdict_counts = {r: {} for r in ("AR-1", "AR-2", "AR-3")}
    with open(os.path.join(a.out, "admissibility_rules.md"), "a") as f:
        f.write(POSTHOC_MD.format(n_dis=c3["by_projection"]["REL_QUANT"]["DISAGREE"], n_tot=c3["by_projection"]["REL_QUANT"]["total"], a=ph["AGREE"], d=ph["DISAGREE"], ab=ph["ABSTAIN"]))
    cf = confirm_ar31()
    with open(os.path.join(a.out, "admissibility_rules.md"), "a") as f:
        f.write(f"""
---
## AR-3.1 confirmation outcome (fresh set; appended after the run)
Cases: {cf['total']['total']}; AGREE {cf['total']['AGREE']}, DISAGREE {cf['total']['DISAGREE']}, ABSTAIN {cf['total']['ABSTAIN']}.
Per-step error-bound violations of the amended conversion: {cf['per_step_error_bound']['amended_bound_violations']} of {cf['per_step_error_bound']['cases_checked']};
frozen-original conversion violated in {cf['per_step_error_bound']['frozen_original_bound_violated_in']} cases; largest observed/amended bound = {cf['per_step_error_bound']['max_observed_over_amended_bound']:.3f}.
Success criteria met: **{cf['success_criteria_met']}**. Amended-rule source hash equals the earlier recorded hash: {cf['matches_hash_recorded_in_earlier_run']}.
The 92 original AR-3 disagreements are unchanged in `admissibility_report.json`.
""")
    report = dict(esc_i_admissibility_version="1.1", confirmation_ar31=dict(cf, ar31_sha256=ar31_hash, original_disagreements_retained=c3["by_projection"]["REL_QUANT"]["DISAGREE"]), seed=SEED, frozen_parameters=json.loads(json.dumps(P, default=str)),
                  order=dict(rules_frozen_and_hashed=t0.isoformat(timespec="seconds"), predictions_hashed_before_exact_comparison=t1.isoformat(timespec="seconds"),
                             rules_sha256=rules_hash, predictions_sha256=pred_hash),
                  rule_independence="rule functions contain no call to the exact classifier (source-checked)",
                  audit_summary={k: v for k, v in R.items()},
                  comparison={"AR-1": c1, "AR-2": c2, "AR-3": c3},
                  total_disagreements=disagreements, posthoc_amendment_relquant=ph,
                  interpretation=("Rules AR-1 and AR-3 are restatements of theorems proved in theorem_audit.md plus certificates; agreement is expected "
                                  "and a disagreement would indicate an implementation error or a wrong theorem. The informative quantities are coverage "
                                  "(abstentions that the exact computation resolves), the AR-2 sharpness ratio, and the negative control. "
                                  "No predictive advantage over the exact classical baseline is claimed."))
    with open(os.path.join(a.out, "admissibility_report.json"), "w") as f: json.dump(report, f, indent=1, default=str)
    prd_report = run_prd1(a.out)
    print("rules sha256      ", rules_hash[:16], "\npredictions sha256", pred_hash[:16])
    print("AR-1a", c1["AR-1a"]); print("AR-1b", {k: v for k, v in c1["AR-1b"].items() if k != "details"}); print("AR-1c", c1["AR-1c"])
    print("AR-2 safety", c2["safety"]["samples"], c2["safety"]["violations"], "| knife-edge", c2["knife_edge"], "| sharpness", c2["sharpness"])
    print("AR-3", c3["overall"]); [print("   ", k, v) for k, v in c3["by_projection"].items()]
    print("TOTAL DISAGREEMENTS (frozen comparison)", disagreements)
    print("AR-3.1 confirmation", cf["total"], "| bound", cf["per_step_error_bound"], "| criteria met:", cf["success_criteria_met"], "| hash match:", cf["matches_hash_recorded_in_earlier_run"])
    for k, v in cf["by_family"].items(): print("   ", k, v)
    print("PRD-1", prd_report["nonlinear_totals"], "\n   criteria:", prd_report["success_criteria"], "\n   flips:", prd_report["route_dependence"], "\n   overlap:", prd_report["coverage_overlap_nonlinear"])
    for k, v in prd_report["per_family"].items(): print("   ", k, "R", {x: y for x, y in v["R"].items() if y}, "| C", {x: y for x, y in v["C"].items() if y})
    print("(disagreements are recorded as data in admissibility_report.json, not as a failure of the run)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
