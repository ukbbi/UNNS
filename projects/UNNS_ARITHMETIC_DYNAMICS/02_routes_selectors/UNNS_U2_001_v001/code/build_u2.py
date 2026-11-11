"""Builds manuscript numbers, selector chains, and figures from the verification report."""
import sys, json, sympy as sp
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
rep = json.load(open(sys.argv[1])); outdir = sys.argv[2]
import u2_selector as S
from u1_bnd_lib import IDENTITIES, SPECIAL
t = S._t
# ---- numbers
w5 = rep["W5"]; h = w5["step_histogram"]
tot = sum(v["cases"] for k, v in rep.items() if isinstance(v, dict) and "cases" in v)
nm = {"KWay": w5["cases"], "TotSteps": w5["total_steps"], "MeanSteps": w5["mean_steps"], "MaxSteps": w5["max_steps_per_waypoint"],
      "Qsize": rep["W4"]["control_states"], "TotalCases": tot, "VerSha": rep["verifier_sha256"][:16]}
with open(outdir + "/numbers.tex", "w") as f:
    for k, v in nm.items(): f.write(f"\\newcommand{{\\{k}}}{{{v:,}}}\n".replace(",", "\\,") if isinstance(v, int) else f"\\newcommand{{\\{k}}}{{{v}}}\n")
with open(outdir + "/hist_table.tex", "w") as f:
    f.write("\\begin{tabular}{rr}\\toprule steps to next waypoint & count\\\\\\midrule\n")
    for k, v in sorted(h.items(), key=lambda kv: int(kv[0])): f.write(f"{k} & {v:,} \\\\\n".replace(",", "\\,"))
    f.write("\\bottomrule\\end{tabular}\n")
# ---- chains
def L(e): return sp.latex(sp.factor(e))
with open(outdir + "/chains.tex", "w") as f:
    for ident in IDENTITIES:
        nm_ = ident["name"]; xs = S.POLY[nm_][2]; steps = ident["steps"]
        segs = []
        for i, (d, e) in enumerate(steps):
            N = sp.factor(e.subs(S.T, t))
            Ls = sp.latex(N); Ls = ("\\left(" + Ls + "\\right)") if isinstance(N, sp.Add) else Ls
            segs.append("%s \\xrightarrow{%s%s}" % (L(xs[i]), "+" if d == "+" else "-", Ls))
        lines = []
        for j in range(0, len(segs), 2):
            chunk = " ".join(segs[j:j + 2]) + " " + L(xs[min(j + 2, len(steps))])
            lines.append(chunk)
        n = f"{ident['M']}t+{ident['r']}" if ident['r'] else f"{ident['M']}t"
        f.write(f"\\paragraph{{Class {nm_}.}} $n={n}$, $t\\ge {S.T0[nm_]}$:\n\\begin{{gather*}}\n" + " \\\\\n".join(lines) + "\n\\end{gather*}\n")
# ---- figures
blue, green, red, amber = "#4a78a8", "#2e7d32", "#c0392b", "#f2b138"
fig, ax = plt.subplots(figsize=(8.4, 3.9)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 5)
cls = [i["name"] for i in IDENTITIES]; ell = {i["name"]: len(i["steps"]) for i in IDENTITIES}
ax.add_patch(FancyBboxPatch((3.8, 0.9), 2.4, 1.0, boxstyle="round,pad=0.05", fc="#d6e4f0", ec=blue, lw=1.8))
ax.text(5, 1.4, "READY  (state = n)", ha="center", va="center", fontsize=11, weight="bold")
for k, c in enumerate(cls):
    cx = 0.75 + k * 1.06; cy = 3.5; col = {4: blue, 5: amber, 6: red}[ell[c]]
    ax.add_patch(FancyBboxPatch((cx - 0.46, cy - 0.45), 0.92, 0.9, boxstyle="round,pad=0.03", fc="white", ec=col, lw=2))
    ax.text(cx, cy + 0.14, f"class {c}", ha="center", va="center", fontsize=8.5, weight="bold")
    ax.text(cx, cy - 0.17, f"{ell[c]} moves", ha="center", va="center", fontsize=8)
    ax.add_patch(FancyArrowPatch((cx, cy - 0.47), (5 + (cx - 5) * 0.3, 1.92), arrowstyle="<->", mutation_scale=10, color="#666", lw=1.1))
ax.text(5, 0.25, "special starts: x = 1 (5 moves), x = 3 (2 moves)  |  9 residue templates, 43 control states", ha="center", fontsize=9)
ax.text(5, 4.75, "Finite-control successor selector: READY \u2192 one template \u2192 READY at n+1", ha="center", fontsize=10.5)
fig.savefig(outdir + "/figures/fig1_control_automaton.pdf", bbox_inches="tight"); fig.savefig(outdir + "/figures/fig1_control_automaton.png", dpi=150, bbox_inches="tight"); plt.close(fig)
# trajectory
x, q, traj, way = 1, S.READY, [1], []
nxt = 2
while nxt <= 40:
    s, N, q2 = S.sigma(x, q); x = S.fwd(x, N) if s == "+" else S.inv(x, N); q = q2; traj.append(x)
    if q == S.READY: way.append(len(traj) - 1); nxt += 1
import math as m
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(range(len(traj)), [m.log10(v) for v in traj], "-", color="#999", lw=1, zorder=1)
ax.scatter(range(len(traj)), [m.log10(v) for v in traj], s=10, color=blue, zorder=2, label="intermediate state")
ax.scatter([0] + way, [m.log10(traj[i]) for i in [0] + way], s=34, color=red, zorder=3, label="waypoint n (READY)")
ax.set_xlabel("step number along the trajectory"); ax.set_ylabel(r"$\log_{10}$ (state)"); ax.legend(frameon=False, fontsize=9)
ax.set_title("Trajectory of $\\Sigma$ from $x=1$ through the waypoints $1,2,\\ldots,40$", fontsize=11)
for sp_ in ("top", "right"): ax.spines[sp_].set_visible(False)
fig.savefig(outdir + "/figures/fig2_trajectory.pdf", bbox_inches="tight"); fig.savefig(outdir + "/figures/fig2_trajectory.png", dpi=150, bbox_inches="tight"); plt.close(fig)
print("built")
