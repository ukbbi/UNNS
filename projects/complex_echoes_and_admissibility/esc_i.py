#!/usr/bin/env python3
"""
ESC-I v0.1 -- Echo Structures chamber (UNNS successor to the Complex-Numbers work).

Pure standard library. Exact rational arithmetic (fractions.Fraction) for the
classical side; IEEE floats for the recursion ("echo") side.

  Generate  : x_{n+1} = A x_n for a real 2x2 matrix A and state x_0
  Classify  : periodic | bounded | convergent | divergent
                - exact   : Jury/Jordan/eigenvector analysis in Q (no floating point)
                - echo    : read off the trajectory alone, finite horizon + tolerance
  Challenge : perturb A (generic, area-preserving) or x_0 and see whether the
              exact class survives, as a function of the perturbation size eps.

Usage:
  python esc_i.py                       # run the built-in suite -> output/
  python esc_i.py --matrix 0 -1 1 0 --x0 1 0 [--steps 2000 --tol 1e-9]
"""
from fractions import Fraction as Fr
import argparse, cmath, csv, datetime, json, math, os, sys

VERSION = "0.1"

# ----------------------------------------------------------------- utilities
def q(s):
    """Exact parse of '3/5', '0.54', '-1e-7' (decimals are taken literally)."""
    return s if isinstance(s, Fr) else Fr(str(s).strip())

def fq(x):
    """Human-readable rational."""
    if x.denominator == 1: return str(x.numerator)
    if x.denominator < 10**6: return f"{x.numerator}/{x.denominator}"
    return f"{float(x):.10g}"

def apply(A, x):
    a, b, c, d = A
    return (a * x[0] + b * x[1], c * x[0] + d * x[1])

# ---------------------------------------------------- exact classical analysis
def classical(A, x0):
    """Exact classification of the orbit of x0 under A (all comparisons in Q)."""
    a, b, c, d = A
    tau, dl = a + d, a * d - b * c
    D = tau * tau - 4 * dl
    p1, pm1 = 1 - tau + dl, 1 + tau + dl            # char. poly at +1 / -1
    stable = dl < 1 and abs(tau) < 1 + dl            # Jury: rho < 1
    marginal = (not stable) and (
        (D < 0 and dl == 1) or (p1 == 0 and abs(dl) <= 1) or (pm1 == 0 and abs(dl) <= 1))
    rc = "<" if stable else ("=" if marginal else ">")   # rho vs 1, exactly
    sq = cmath.sqrt(float(D))
    lam = [(float(tau) + sq) / 2, (float(tau) - sq) / 2]
    rho = max(abs(l) for l in lam)
    naive = {"<": "convergent", "=": "marginal (inconclusive)", ">": "divergent"}[rc]

    cls, sub, period, why = None, "", None, ""
    u, v = apply(A, x0)
    if x0[0] == 0 and x0[1] == 0:
        cls, sub, period, why = "periodic", "origin (fixed)", 1, "x0 = 0"
    elif x0[0] * v - x0[1] * u == 0:                 # x0 is an eigenvector, exactly
        r = u / x0[0] if x0[0] != 0 else v / x0[1]
        why = f"x0 is an eigenvector, eigenvalue {fq(r)}"
        if r == 0:        cls, sub = "convergent", "finite-time collapse (A x0 = 0)"
        elif abs(r) < 1:  cls, sub = "convergent", "to origin along eigenvector"
        elif r == 1:      cls, sub, period = "periodic", "fixed point", 1
        elif r == -1:     cls, sub, period = "periodic", "period-2 flip", 2
        else:             cls, sub = "divergent", "geometric along eigenvector"
    elif rc == "<":
        cls = "convergent"
        sub = "finite-time collapse (A nilpotent)" if (tau == 0 and dl == 0) else "to origin"
        why = "rho < 1"
    elif rc == ">":
        cls = "divergent"
        sub = "geometric (spiral)" if D < 0 else "geometric (dominant real eigenvalue)"
        why = "rho > 1 and x0 not an eigenvector"
    else:                                             # rho == 1, x0 not an eigenvector
        if D < 0:                                     # eigenvalues e^{+-i theta}
            if tau in (0, 1, -1):
                cls, period = "periodic", {0: 4, 1: 6, -1: 3}[int(tau)]
                sub = f"root of unity, order {period}"
                why = "tau in {0,+-1}: A^n = I (cyclotomic)"
            else:
                cls, sub = "bounded", "quasi-periodic (theta/2pi irrational, Niven)"
                why = "|lambda|=1, tau not in {0,+-1,+-2}: never returns exactly"
        elif p1 == 0:                                 # eigenvalues 1 and dl
            if dl == 1:   cls, sub, why = "divergent", "linear (Jordan block, lambda=1)", "defective at +1"
            elif dl == -1: cls, sub, period, why = "periodic", "period-2 (A^2 = I)", 2, "eigenvalues +1,-1"
            else:         cls, sub, why = "convergent", "to a nonzero fixed point", "eigenvalues 1 and |mu|<1"
        else:                                         # eigenvalues -1 and -dl
            if dl == 1:   cls, sub, why = "divergent", "linear (Jordan block, lambda=-1)", "defective at -1"
            else:         cls, sub, why = "convergent", "to a 2-cycle (asymptotically period 2)", "eigenvalues -1 and |mu|<1"
    return dict(tau=fq(tau), delta=fq(dl), disc=fq(D), eigenvalues=[_c(l) for l in lam],
                rho=rho, rho_vs_1=rc, naive_eigenvalue_class=naive,
                cls=cls, sub=sub, period=period, why=why)

def _c(z):
    z = complex(z)
    return f"{z.real:.10g}" if abs(z.imag) < 1e-15 else f"{z.real:.10g}{z.imag:+.10g}i"

# ------------------------------------------------- recursion ("echo") analysis
def trajectory(A, x0, N, blow=1e12):
    af = [float(t) for t in A]
    x = (float(x0[0]), float(x0[1]))
    lim = blow * max(1.0, math.hypot(*x))
    pts = [x]
    for _ in range(N):
        x = (af[0] * x[0] + af[1] * x[1], af[2] * x[0] + af[3] * x[1])
        pts.append(x)
        if math.hypot(*x) > lim: break
    return pts

def echo_classify(A, x0, N=2000, tol=1e-9, pmax=64, blow=1e6):
    """Classify from the trajectory alone (finite horizon N, resolution tol)."""
    pts = trajectory(A, x0, N)
    nr = [math.hypot(*p) for p in pts]
    scale = max(1.0, max(nr))
    n = len(pts)
    if nr[-1] > blow * max(1.0, nr[0]):
        return dict(cls="divergent", sub="norm blew up", period=None, steps=n - 1)
    def resid(p, start):
        return max(max(abs(pts[i + p][0] - pts[i][0]), abs(pts[i + p][1] - pts[i][1]))
                   for i in range(start, n - p))
    for p in range(1, min(pmax, n - 1) + 1):
        if resid(p, 0) <= tol * scale:
            return dict(cls="periodic", sub=f"returns every {p} step(s) within tol", period=p, steps=n - 1)
    w = max(2, min(200, n // 4))
    if max(nr[-w:]) <= tol * scale:
        return dict(cls="convergent", sub="to origin (within tol)", period=None, steps=n - 1)
    for p in (1, 2):
        if resid(p, n - w - p) <= tol * scale:
            return dict(cls="convergent", sub=f"tail is {p}-periodic (within tol)", period=None, steps=n - 1)
    q3, q2 = max(nr[3 * n // 4:]), max(nr[n // 2: 3 * n // 4])
    if q3 > 1.2 * q2 and q3 > 2 * nr[0]:
        return dict(cls="divergent", sub="sustained growth", period=None, steps=n - 1)
    return dict(cls="bounded", sub="no return, no decay, no growth within horizon", period=None, steps=n - 1)

def compare(ex, ec, rho, N, tol):
    """Agreement verdict between exact (classical) and echo classes, with a reason."""
    if ex["cls"] == ec["cls"]: return "agree", ""
    e, c = ec["cls"], ex["cls"]
    if c == "bounded" and e == "periodic":
        return "echo-overclaims", "resolution: orbit returns within tol although exact orbit never returns"
    if e == "bounded" and c in ("divergent", "convergent") and rho > 0 and rho != 1:
        need = math.ceil(math.log(1e6 if c == "divergent" else tol) / math.log(rho))
        return "echo-misses", f"horizon: drift is below resolution within N={N}; ~{need} steps needed"
    if c == "periodic" and e == "bounded":
        return "echo-misses", "tolerance too tight for float rounding of a periodic orbit"
    return "disagree", "unexplained -- investigate"

# ------------------------------------------------------------------ challenge
def mulberry32(seed):
    a = [seed & 0xFFFFFFFF]
    M = 0xFFFFFFFF
    def nxt():
        a[0] = (a[0] + 0x6D2B79F5) & M
        t = a[0]
        t = ((t ^ (t >> 15)) * (t | 1)) & M
        t = (t ^ ((t + (((t ^ (t >> 7)) * (t | 61)) & M)) & M)) & M
        return (t ^ (t >> 14)) & M
    return nxt

COARSE = {"periodic": "bounded", "bounded": "bounded", "convergent": "convergent", "divergent": "divergent"}
KS = list(range(1, 10))

def challenge(A, x0, M=100, seed=1):
    """Does the exact class survive perturbations of size eps = 10^-k?
    generic : A + eps*E, entries of E in [-1,1]
    area    : A * shear(eps s) * shear^T(eps t)   (det preserved exactly)
    state   : x0 + eps*g, A unchanged
    'fine' = same 4-way class; 'coarse' merges periodic into bounded."""
    base = classical(A, x0)["cls"]
    a, b, c, d = A
    rows = []
    for k in KS:
        eps = Fr(1, 10 ** k)
        rnd = mulberry32(seed * 1000 + k)
        draw = lambda: Fr(rnd() % 2001 - 1000, 1000)
        cnt = {f: [0, 0] for f in ("generic", "area", "state")}
        for _ in range(M):
            e1, e2, e3, e4, s, t, g1, g2 = (draw() for _ in range(8))
            Ag = (a + eps * e1, b + eps * e2, c + eps * e3, d + eps * e4)
            sp, tp = eps * s, eps * t
            b2, d2 = a * sp + b, c * sp + d
            Aa = (a + b2 * tp, b2, c + d2 * tp, d2)
            xs = (x0[0] + eps * g1, x0[1] + eps * g2)
            for fam, (AA, xx) in (("generic", (Ag, x0)), ("area", (Aa, x0)), ("state", (A, xs))):
                cl = classical(AA, xx)["cls"]
                cnt[fam][0] += cl == base
                cnt[fam][1] += COARSE[cl] == COARSE[base]
        rows.append(dict(k=k, eps=float(eps), **{f"{f}_fine": cnt[f][0] / M for f in cnt},
                         **{f"{f}_coarse": cnt[f][1] / M for f in cnt}))
    hold = {}
    for key in ("generic_fine", "generic_coarse", "area_fine", "area_coarse", "state_fine"):
        h = 0.0                                       # largest eps with survival 1 for it and all smaller eps
        for r in reversed(rows):                      # k=9 (smallest eps) first
            if r[key] == 1.0: h = r["eps"]
            else: break
        hold[key] = h
    ex = classical(A, x0)
    margin = abs(ex["rho"] - 1.0)
    return dict(base=base, M=M, seed=seed, rows=rows, eps_hold=hold, rho_margin=margin)

# ---------------------------------------------- phase inletting (audit item S5)
def phase_inlet(T, U):
    """Compare rho(T), rho(UT), rho(U T U^-1). The unrestricted claim rho(UT)=rho(T) is false."""
    def mul(P, Q): return (P[0]*Q[0]+P[1]*Q[2], P[0]*Q[1]+P[1]*Q[3], P[2]*Q[0]+P[3]*Q[2], P[2]*Q[1]+P[3]*Q[3])
    def rho(P):
        t, dl = P[0] + P[3], P[0]*P[3] - P[1]*P[2]
        s = cmath.sqrt(float(t * t - 4 * dl)); return max(abs((float(t) + s) / 2), abs((float(t) - s) / 2))
    dU = U[0] * U[3] - U[1] * U[2]
    out = dict(rho_T=rho(T), rho_UT=rho(mul(U, T)), commute=(mul(U, T) == mul(T, U)))
    if dU != 0:
        Ui = (U[3] / dU, -U[1] / dU, -U[2] / dU, U[0] / dU)
        out["rho_similar"] = rho(mul(mul(U, T), Ui))
    out["claim_rho(UT)=rho(T)_holds"] = abs(out["rho_UT"] - out["rho_T"]) < 1e-12
    return out

# ----------------------------------------------------------------------- suite
SUITE = [
 dict(id="rot90", name="Rotation by 90 deg", A=["0","-1","1","0"], x0=["1","0"], surprise=False,
      note="Baseline: J with J^2=-I. Exactly periodic (order 4)."),
 dict(id="rot60", name="Order-6 rotation (companion of x^2-x+1)", A=["0","-1","1","1"], x0=["1","0"], surprise=False,
      note="tau=1: A^6=I. Periodic, but orbit is an ellipse, not a circle."),
 dict(id="rot_pyth", name="Pythagorean rotation 3-4-5", A=["3/5","-4/5","4/5","3/5"], x0=["1","0"], surprise=False,
      note="A genuine rotation, yet never periodic: tau=6/5 not in {0,+-1,+-2}."),
 dict(id="spiral_in", name="Contracting spiral, rho=0.9", A=["0.54","-0.72","0.72","0.54"], x0=["1","0"], surprise=False,
      note="Complex pair, |lambda|=0.9."),
 dict(id="spiral_out", name="Expanding spiral, rho=1.1", A=["0.66","-0.88","0.88","0.66"], x0=["1","0"], surprise=False,
      note="Complex pair, |lambda|=1.1."),
 dict(id="shear_gen", name="Shear, generic state (rho=1)", A=["1","1","0","1"], x0=["0","1"], surprise=True,
      note="Expectation 'rho=1 => bounded' is false: Jordan block gives linear growth."),
 dict(id="shear_eig", name="Shear, eigenvector state", A=["1","1","0","1"], x0=["1","0"], surprise=True,
      note="Same matrix, different x0: fixed point. Class depends on the state, not only on A."),
 dict(id="saddle_stable", name="Saddle, state on stable axis", A=["2","0","0","1/2"], x0=["0","1"], surprise=True,
      note="rho=2 yet the orbit converges: the eigenvalue test alone says 'divergent'."),
 dict(id="saddle_gen", name="Saddle, generic state", A=["2","0","0","1/2"], x0=["1","1"], surprise=False,
      note="Same matrix as above; generic state diverges."),
 dict(id="T_ones", name="T = all-ones, generic state", A=["1","1","1","1"], x0=["1","0"], surprise=False,
      note="rho(T)=2, divergent."),
 dict(id="UT_ones", name="U T with U=diag(1,-1)", A=["1","1","-1","-1"], x0=["1","0"], surprise=True,
      note="Audit S5 counterexample: rho(UT)=0, so UT is nilpotent. Phase inletting does not preserve rho."),
 dict(id="proj_fixed", name="Projection-like, nonzero limit", A=["1","0","0","1/2"], x0=["1","1"], surprise=True,
      note="rho=1 (marginal) but convergent to (1,0): an attractor that is not the origin."),
 dict(id="jordan_m1", name="Jordan block at -1", A=["-1","1","0","-1"], x0=["0","1"], surprise=False,
      note="Linear growth with alternating sign."),
 dict(id="trap_horizon", name="Horizon trap: rho = 1 + 1e-7", A=["30000003/50000000","-40000004/50000000","40000004/50000000","30000003/50000000"],
      x0=["1","0"], surprise=True,
      note="Exactly divergent, but growth over 2000 steps is e^(2e-4): the echo reads 'bounded'."),
 dict(id="trap_resolution", name="Resolution trap: tau = 1 + 1e-12", A=["0","-1","1","1000000000001/1000000000000"], x0=["1","0"], surprise=True,
      note="Exactly quasi-periodic (bounded), but within tol=1e-9 it looks period-6."),
]

def run_one(entry, N=2000, tol=1e-9, M=100, seed=1):
    A = tuple(q(s) for s in entry["A"]); x0 = tuple(q(s) for s in entry["x0"])
    ex = classical(A, x0); ec = echo_classify(A, x0, N, tol)
    verdict, reason = compare(ex, ec, ex["rho"], N, tol)
    return dict(id=entry.get("id", "custom"), name=entry.get("name", "custom"), note=entry.get("note", ""),
                surprise=entry.get("surprise", False), A=[fq(t) for t in A], x0=[fq(t) for t in x0],
                exact=ex, echo=ec, verdict=verdict, reason=reason,
                challenge=challenge(A, x0, M, seed))

def fmt_hold(x):
    return "0 (knife-edge)" if x == 0 else (">=0.1 (whole grid)" if x >= 0.1 else f"{x:g}")

def write_reports(results, out, N, tol):
    os.makedirs(out, exist_ok=True)
    meta = dict(esc_i_version=VERSION, generated=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                echo_steps=N, echo_tol=tol)
    inlet = phase_inlet(tuple(map(Fr, (1, 1, 1, 1))), tuple(map(Fr, (1, 0, 0, -1))))
    with open(os.path.join(out, "report.json"), "w") as f:
        json.dump(dict(meta=meta, phase_inlet_counterexample=inlet, results=results), f, indent=1)
    L = [f"# ESC-I v{VERSION} report", "",
         f"Echo horizon N={N}, tolerance={tol:g}. Exact side: rational arithmetic, no floating point.", "",
         "| id | exact class | naive eigenvalue test | echo class | verdict | rho | hold eps (generic / area / state) |",
         "|---|---|---|---|---|---|---|"]
    for r in results:
        h = r["challenge"]["eps_hold"]
        L.append(f"| {r['id']} | {r['exact']['cls']} - {r['exact']['sub']} | {r['exact']['naive_eigenvalue_class']} | "
                 f"{r['echo']['cls']} | {r['verdict']} | {r['exact']['rho']:.6g} | "
                 f"{fmt_hold(h['generic_fine'])} / {fmt_hold(h['area_fine'])} / {fmt_hold(h['state_fine'])} |")
    L += ["", "## Notes per example", ""]
    for r in results:
        L.append(f"- **{r['id']}** ({'designed to contradict' if r['surprise'] else 'baseline'}): {r['note']} "
                 f"Why: {r['exact']['why']}." + (f" Echo vs exact: {r['reason']}." if r["reason"] else ""))
    L += ["", "## Tally", ""]
    L.append(f"- examples: {len(results)}; echo agrees with exact: {sum(r['verdict']=='agree' for r in results)}")
    L.append(f"- naive eigenvalue-only test differs from exact class: "
             f"{sum(r['exact']['naive_eigenvalue_class'] != r['exact']['cls'] for r in results)}")
    L.append(f"- every echo/exact disagreement explained by horizon or resolution: "
             f"{all(r['verdict'] in ('agree','echo-overclaims','echo-misses') for r in results)}")
    L += ["", "## Phase-inletting counterexample (audit S5)", "",
          f"T=[[1,1],[1,1]], U=diag(1,-1): rho(T)={inlet['rho_T']:.6g}, rho(UT)={inlet['rho_UT']:.6g}, "
          f"rho(UTU^-1)={inlet['rho_similar']:.6g}, commute={inlet['commute']}. "
          "rho(UT)=rho(T) is false in general; similarity preserves rho, multiplication does not."]
    with open(os.path.join(out, "report.md"), "w") as f: f.write("\n".join(L) + "\n")

def main(argv=None):
    ap = argparse.ArgumentParser(description="ESC-I v0.1 chamber")
    ap.add_argument("--matrix", nargs=4, metavar=("a", "b", "c", "d"))
    ap.add_argument("--x0", nargs=2, metavar=("x", "y"), default=["1", "0"])
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--tol", type=float, default=1e-9)
    ap.add_argument("--samples", type=int, default=100)
    ap.add_argument("--out", default="output")
    ap.add_argument("--suite", action="store_true", help="run the built-in suite (default when no --matrix)")
    a = ap.parse_args(argv)
    entries = [dict(id="custom", name="custom", A=a.matrix, x0=a.x0)] if a.matrix else SUITE
    results = [run_one(e, a.steps, a.tol, a.samples) for e in entries]
    write_reports(results, a.out, a.steps, a.tol)
    if a.matrix:
        A = tuple(q(s) for s in a.matrix); x0 = tuple(q(s) for s in a.x0)
        with open(os.path.join(a.out, "trajectory.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["n", "x", "y", "norm"])
            for i, p in enumerate(trajectory(A, x0, min(a.steps, 5000))): w.writerow([i, p[0], p[1], math.hypot(*p)])
    print(f"{'id':16}{'exact':12}{'naive':26}{'echo':12}{'verdict'}")
    for r in results:
        print(f"{r['id']:16}{r['exact']['cls']:12}{r['exact']['naive_eigenvalue_class']:26}{r['echo']['cls']:12}{r['verdict']}")
    print(f"\nreport: {os.path.join(a.out, 'report.md')}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
