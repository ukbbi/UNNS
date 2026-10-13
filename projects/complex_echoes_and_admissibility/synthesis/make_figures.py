#!/usr/bin/env python3
"""Generates the six manuscript figures from ESC-I code and recorded reports. No external imagery."""
import sys, os, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from fractions import Fraction as Fr
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import esc_i as E, admissibility as A
plt.rcParams.update({"pdf.fonttype": 42, "font.family": "serif", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.7, "figure.dpi": 150})
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
C1, C2, C3, C4, GR = "#1f5aa6", "#c4561b", "#2a8a5a", "#7a3b8f", "#777777"

def orbit(M, x0, n):
    z = tuple(Fr(c) for c in x0); pts = [z]
    for _ in range(n): z = E.apply(M, z); pts.append(z)
    return np.array([[float(a), float(b)] for a, b in pts])
def fr(*s): return tuple(E.q(x) for x in s)

# ---- Fig 1
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.3))
a = ax[0]; a.set_aspect("equal"); a.axhline(0, c="#ddd", lw=.6); a.axvline(0, c="#ddd", lw=.6)
J = fr("0", "-1", "1", "0"); o = orbit(J, ("1", "0"), 4); labs = [r"$x_0$", r"$Jx_0$", r"$J^2x_0=-x_0$", r"$J^3x_0$"]
for k in range(4):
    a.annotate("", xy=o[k+1]*0.93, xytext=o[k]*0.93, arrowprops=dict(arrowstyle="->", color=C1, lw=1.2, shrinkA=6, shrinkB=6, connectionstyle="arc3,rad=0.25"))
    a.plot(*o[k], "o", c=C1, ms=4); off = [(6, 4), (4, 6), (-62, 4), (4, -12)][k]; a.annotate(labs[k], o[k], xytext=off, textcoords="offset points", fontsize=8)
a.set_xlim(-1.6, 1.6); a.set_ylim(-1.5, 1.5); a.set_title(r"(a) $i\mapsto J$, $J^2=-I$: four quarter-turns", fontsize=9)
a.text(-1.55, -1.4, r"$a+bi\ \mapsto\ aI+bJ$", fontsize=9, color=GR)
b = ax[1]; b.set_aspect("equal"); t = np.linspace(0, 2*np.pi, 200); b.plot(np.cos(t), np.sin(t), c="#ddd", lw=.8)
P = fr("3/5", "-4/5", "4/5", "3/5"); o = orbit(P, ("1", "0"), 40); b.plot(o[:, 0], o[:, 1], ".", c=C2, ms=4)
Q = fr("1/2", "-3/4", "3/4", "1/2")  # placeholder, replaced below
b.plot(*o[0], "o", c="k", ms=4); b.annotate(r"$x_0$", o[0], xytext=(5, -10), textcoords="offset points", fontsize=8)
b.set_title(r"(b) $(3+4i)/5$: a rotation that never returns", fontsize=9); b.set_xlim(-1.4, 1.4); b.set_ylim(-1.4, 1.4)
b.text(-1.35, -1.3, "40 exact steps on the unit circle;\nangle is not a rational multiple of $\\pi$", fontsize=7.5, color=GR)
fig.tight_layout(); fig.savefig(f"{OUT}/fig1_complex_rotation.pdf"); plt.close(fig)

# ---- Fig 2: four regimes, classes computed by the exact classifier
cases = [("Periodic", fr("0", "-1", "1", "1"), ("1", "0"), C1), ("Bounded, not periodic", fr("1", "-1", "1/2", "1/2"), ("1", "0"), C3),
         ("Convergent", fr("0.54", "-0.72", "0.72", "0.54"), ("1", "0"), C4), ("Divergent", fr("0.66", "-0.88", "0.88", "0.66"), ("1", "0"), C2)]
fig, axs = plt.subplots(1, 4, figsize=(7.4, 2.4))
for ax_, (nm, M, x0, c) in zip(axs, cases):
    cl = E.classical(M, tuple(E.q(s) for s in x0))["cls"]; n = {"Periodic": 24, "Bounded, not periodic": 400, "Convergent": 90, "Divergent": 60}[nm]
    o = orbit(M, x0, n); ax_.plot(o[:, 0], o[:, 1], "-", c=c, lw=.5, alpha=.5); ax_.plot(o[:, 0], o[:, 1], ".", c=c, ms=2.5)
    ax_.plot(*o[0], "ko", ms=3); ax_.set_aspect("equal", "datalim"); ax_.set_xticks([]); ax_.set_yticks([]); ax_.set_title(f"{nm}\n(exact class: {cl})", fontsize=7.5)
    for s in ("left", "bottom"): ax_.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig2_regimes.pdf"); plt.close(fig)

# ---- Fig 3: state-dependent admissibility, T = diag(2, 1/2)
T = fr("2", "0", "0", "1/2"); fig, ax = plt.subplots(figsize=(4.6, 3.6))
ax.axvline(0, c=C3, lw=1.4, alpha=.5); ax.text(0.06, 3.35, "stable eigenline ($u=0$)", color=C3, fontsize=7.5)
ax.axhline(0, c=C2, lw=1.4, alpha=.35); ax.text(-4.1, -0.45, "unstable eigenline ($w=0$)", color=C2, fontsize=7.5)
for x0, c, lab in [(("0", "1"), C3, r"$x_0=(0,1)$: converges"), (("0.02", "1"), C2, r"$x_0=(0.02,1)$: diverges"), (("-0.05", "-1"), C2, None), (("1", "1"), C4, r"$x_0=(1,1)$: diverges")]:
    o = orbit(T, tuple(E.q(s) for s in x0), 9); m = (abs(o[:, 0]) < 4.2) & (abs(o[:, 1]) < 3.8)
    ax.plot(o[m, 0], o[m, 1], "o-", c=c, ms=3, lw=.8, label=lab)
ax.set_xlim(-4.2, 4.2); ax.set_ylim(-3.8, 3.8); ax.set_xlabel("$u$ (dominant coordinate, eigenvalue 2)"); ax.set_ylabel("$w$ (eigenvalue 1/2)"); ax.legend(fontsize=7, frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig(f"{OUT}/fig3_state_dependence.pdf"); plt.close(fig)

# ---- Fig 4: observational traps (exact vs. echo)
from decimal import Decimal as D, getcontext; getcontext().prec = 60
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.0))
a = ax[0]; n = np.logspace(0, 8, 300); a.loglog(n, (1 + 1e-7)**n, c=C2); a.axvline(2000, c=GR, ls="--", lw=.8); a.text(2600, 3e3, "echo horizon\n$N=2000$", fontsize=7.5, color=GR)
a.axhline(1.0002, c="#bbb", lw=.5); a.set_xlabel("step $n$"); a.set_ylabel("$|x_n|/|x_0|$"); a.set_title(r"(a) horizon trap, $\rho=1+10^{-7}$: exact class divergent", fontsize=8)
a.annotate(r"$e^{2\times10^{-4}}\approx1.0002$ at $N$:" "\nreads as bounded", xy=(2000, 1.0002), xytext=(1.5, 80), fontsize=7.5, arrowprops=dict(arrowstyle="->", lw=.6, color=GR))
b = ax[1]; tau = D(1) + D(10)**-12
def mulv(M, v): return (M[0]*v[0] + M[1]*v[1], M[2]*v[0] + M[3]*v[1])
x = (D(1), D(0)); x0 = x; ks, drift, step6 = [], [], []; hist = [x]
for n in range(1, 12001):
    x = mulv((D(0), D(-1), D(1), tau), x); hist.append(x)
for k in range(1, 2001):
    n = 6*k; ks.append(n); drift.append(float(((hist[n][0]-x0[0])**2 + (hist[n][1]-x0[1])**2).sqrt()))
    step6.append(float(max(abs(hist[n][0]-hist[n-6][0]), abs(hist[n][1]-hist[n-6][1]))))
b.loglog(ks, step6, c=C1, label="one-period residual $|x_{n}-x_{n-6}|$ (what the echo test checks)"); b.loglog(ks, drift, c=C4, label="accumulated drift $|x_n-x_0|$")
b.axhline(1e-9, c=C2, ls="--", lw=.8); b.text(2.2e3, 1.5e-9, "tolerance $10^{-9}$", fontsize=7.5, color=C2)
b.axvline(2000, c=GR, ls="--", lw=.8); b.text(2200, 3e-12, "horizon", fontsize=7.5, color=GR)
b.set_xlabel("step $n=6k$"); b.set_ylabel("residual"); b.set_title(r"(b) resolution trap, $\tau=1+10^{-12}$: exact class bounded", fontsize=8); b.legend(fontsize=6.5, frameon=False, loc="upper left", bbox_to_anchor=(0, 0.86))
fig.tight_layout(); fig.savefig(f"{OUT}/fig4_observational_traps.pdf"); plt.close(fig)

# ---- Fig 5: projection routing, common recurrence T=diag(2,1/2), x0=(0.2,1)
fams = [("Unprojected", None, GR), ("Dead-zone ($\\theta=1$)", dict(kind="DZ", theta=Fr(1)), C1), ("Clipping ($c=1$)", dict(kind="CLIP", c=Fr(1)), C3),
        ("Lattice ($h=1$)", dict(kind="LAT", h=Fr(1)), C4), ("Lattice ($h=1/2$)", dict(kind="LAT", h=Fr(1, 2)), "#b8860b"), ("State gate", dict(kind="GATE"), C2)]
fig, ax = plt.subplots(figsize=(5.4, 3.4)); z0 = (Fr(1, 5), Fr(1)); N = 14; res = {}
for nm, fam, c in fams:
    z = z0; ys = [max(abs(z[0]), abs(z[1]))]
    for _ in range(N):
        y = E.apply(T, z); z = y if fam is None else A.pi_apply(fam, y); ys.append(float(max(abs(z[0]), abs(z[1]))))
    res[nm] = ys[-1]; ax.plot(range(N+1), ys, "o-", c=c, ms=3, lw=1, label=nm)
ax.set_yscale("symlog", linthresh=1e-2); ax.set_xlabel("step $n$"); ax.set_ylabel(r"$\max(|u_n|,|w_n|)$ (symlog)"); ax.legend(fontsize=7, frameon=False, ncol=2, loc="upper left")
ax.set_title(r"$T=\mathrm{diag}(2,\frac{1}{2})$, $x_0=(0.2,1)$: one operator, several regimes", fontsize=8.5)
fig.tight_layout(); fig.savefig(f"{OUT}/fig5_projection_routing.pdf"); plt.close(fig); json.dump(res, open(f"{OUT}/fig5_final_values.json", "w"), indent=1)

# ---- Fig 6: PRD-1 coverage from the recorded report
rep = json.load(open(os.path.join(os.path.dirname(OUT), "..", "output", "prd1_report.json"))); pf = rep["per_family"]
fig, ax = plt.subplots(figsize=(6.4, 3.2)); names = [("DZ", "Dead-zone"), ("CLIP", "Clipping"), ("LAT", "Lattice"), ("GATE", "State gate")]; y = 0; yt = []; yl = []
for k, nm in names:
    for who in ("R", "C"):
        d = pf[k][who]; seg = [(d["CONFIRMED_ASYMPTOTIC"], C1, "analytical certificate"), (d["CONSISTENT_FINITE_HORIZON"], "#8fb3de", "finite-horizon only"), (d["ABSTAIN"], "#d9d9d9", "abstain")]
        left = 0
        for v, c, lb in seg:
            if v: ax.barh(y, v, left=left, color=c, height=.8, edgecolor="white", lw=.5, label=lb if (k, who) == ("DZ", "R") or (lb == "abstain" and (k, who) == ("DZ", "C")) else None)
            if v > 120: ax.text(left + v/2, y, str(v), ha="center", va="center", fontsize=7, color="white" if c == C1 else "k")
            left += v
        yt.append(y); yl.append(f"{nm}  {who}"); y += 1
    y += .5
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=7.5); ax.invert_yaxis(); ax.set_xlabel("cases (each bar sums to its family total: 1560, 1080, 1170, 387; 4197 overall)"); ax.legend(fontsize=7, frameon=False, loc="lower right")
ax.set_title("PRD-1 coverage: rule R vs classical comparator C (0 contradicted in both)", fontsize=8.5)
fig.tight_layout(); fig.savefig(f"{OUT}/fig6_prd1_coverage.pdf"); plt.close(fig)
print("figures written", os.listdir(OUT)); print(res)
