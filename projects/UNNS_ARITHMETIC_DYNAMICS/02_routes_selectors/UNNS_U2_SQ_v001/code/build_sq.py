import sys, json, csv, sympy as sp
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from u1_bnd_lib import fwd, inv
import u2sq_selector as SS
rep = json.load(open(sys.argv[1])); outdir = sys.argv[2]; csvf = sys.argv[3]
blue, amber, red = "#4a78a8", "#f2b138", "#c0392b"
h = rep["Q4"]["histogram"]; q8 = rep["Q8"]
tot = sum(v["cases"] for v in rep.values() if isinstance(v, dict) and "cases" in v)
nm = {"TabN": rep["Q4"]["cases"], "MeanSq": rep["Q4"]["mean"], "KSq": q8["cases"], "QDirect": q8["control_states"], "MeanDirect": q8["mean"],
      "QWrap": rep["Q10"]["control_states"], "MeanWrap": rep["Q10"]["mean"], "TotalCases": tot, "VerSha": rep["verifier_sha256"][:16],
      "Bnum": rep["Q3"]["ball_529"], "Bden": rep["Q3"]["ball_576"], "FirstFive": ",\\,".join(str(x) for x in rep["Q4"]["first_five"][:6]),
      "CountFive": h.get("5", 0)}
with open(outdir + "/numbers.tex", "w") as f:
    for k, v in nm.items(): f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
with open(outdir + "/hist_table.tex", "w") as f:
    f.write("\\begin{tabular}{rr}\\toprule distance $d(n^2,(n+1)^2)$ & number of $n\\le\\TabN$\\\\\\midrule\n")
    for k, v in sorted(h.items(), key=lambda kv: int(kv[0])): f.write(f"{k} & {v} \\\\\n")
    f.write("\\bottomrule\\end{tabular}\n")
pw = rep["Q11"]["by_exponent"]
with open(outdir + "/power_table.tex", "w") as f:
    f.write("\\begin{tabular}{rrrr}\\toprule exponent $k$ & bound $6k$ & max moves observed & control states\\\\\\midrule\n")
    for k, v in pw.items(): f.write(f"{k} & {6*int(k)} & {v['max_moves']} & {v['control_states']} \\\\\n")
    f.write("\\bottomrule\\end{tabular}\n")
# identity table
t = SS._t
def Ls(N):
    e = sp.factor(sp.sympify(N, locals={"t": t})); l = sp.latex(e)
    return ("\\left(" + l + "\\right)") if isinstance(e, sp.Add) else l
with open(outdir + "/identity_table.tex", "w") as f:
    f.write("{\\footnotesize\\begin{longtable}{@{}rcp{0.78\\textwidth}@{}}\\toprule $r$ & $t\\ge$ & moves (labels $N_i(t)$ for $n=24t+r$)\\\\\\midrule\\endhead\n")
    for rs in sorted(SS.DATA["classes"], key=int):
        v = SS.DATA["classes"][rs]
        mv = ",\\ ".join(f"{s}{Ls(N)}" for s, N in v["steps"])
        f.write(f"{rs} & {v['t0']} & ${mv}$ \\\\\n")
    f.write("\\bottomrule\\end{longtable}}\n")
# figures
lens = {int(r): len(v["steps"]) for r, v in SS.DATA["classes"].items()}
fig, axs = plt.subplots(2, 12, figsize=(9, 2.9))
for r in range(24):
    ax = axs[r // 12][r % 12]; ax.axis("off"); col = {4: blue, 5: amber}[lens[r]]
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=col)); ax.text(.5, .62, str(r), ha="center", va="center", color="white", fontsize=11, weight="bold")
    ax.text(.5, .28, f"{lens[r]} moves", ha="center", va="center", color="white", fontsize=6.5); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
fig.suptitle("Residue of $n$ modulo 24 → number of moves from $n^2$ to $(n+1)^2$", fontsize=10)
fig.savefig(outdir + "/figures/fig1_residue_cover.pdf", bbox_inches="tight"); fig.savefig(outdir + "/figures/fig1_residue_cover.png", dpi=150, bbox_inches="tight"); plt.close(fig)
rows = list(csv.DictReader(open(csvf)))
fig, ax = plt.subplots(figsize=(6.2, 3.2)); ks = sorted(h, key=int)
ax.bar([int(k) for k in ks], [h[k] for k in ks], color=[blue if int(k) < 5 else red for k in ks])
for k in ks: ax.text(int(k), h[k], str(h[k]), ha="center", va="bottom", fontsize=8)
for x, lab in ((5, "sharp bound 5"), (8, "bound via successor + 2")):
    pass
ax.set_xlabel("exact distance $d(n^2,(n+1)^2)$"); ax.set_ylabel(f"number of $n\\leq{rep['Q4']['cases']}$")
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
ax.set_title("Exact distances between consecutive squares", fontsize=10)
fig.savefig(outdir + "/figures/fig2_distribution.pdf", bbox_inches="tight"); fig.savefig(outdir + "/figures/fig2_distribution.png", dpi=150, bbox_inches="tight"); plt.close(fig)
# example paths
def trace(n):
    c = SS.CLS[n % 24]; r = n % 24; tt = (n - r) // 24; x = n * n; st = [x]; lab = []
    for i, s in enumerate(c["signs"]):
        N = SS._label(r, i, tt); x = fwd(x, N) if s == "+" else inv(x, N); st.append(x); lab.append((s, N))
    return st, lab
fig, axs = plt.subplots(2, 1, figsize=(9, 3.6))
for ax, n, ttl in ((axs[0], 25, "n = 25 (class 1, 4 moves)"), (axs[1], 23, "n = 23 (class 23, 5 moves; d = 5 is attained here)")):
    st, lab = trace(n); ax.axis("off"); ax.set_xlim(0, len(st)); ax.set_ylim(0, 1.3); ax.set_title(ttl, fontsize=9, loc="left")
    for i, v in enumerate(st):
        ax.text(i + .5, .35, f"{v:,}", ha="center", va="center", fontsize=7.5, bbox=dict(boxstyle="round", fc="#eaf1f8", ec=blue))
        if i < len(lab):
            s, N = lab[i]; ax.annotate("", xy=(i + 1.08, .35), xytext=(i + .92 - 0.0, .35), arrowprops=dict(arrowstyle="->", color="#2e7d32" if s == "+" else red))
            ax.text(i + 1, .78, f"{s}{N}", ha="center", fontsize=7.5, color="#2e7d32" if s == "+" else red)
fig.savefig(outdir + "/figures/fig3_example_paths.pdf", bbox_inches="tight"); fig.savefig(outdir + "/figures/fig3_example_paths.png", dpi=150, bbox_inches="tight"); plt.close(fig)
print("built")
