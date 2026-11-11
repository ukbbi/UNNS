import sys, json, csv
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
rep = json.load(open(sys.argv[1])); out = sys.argv[2]; data = sys.argv[3]
blue, amber, red, grey = "#4a78a8", "#f2b138", "#c0392b", "#8a8a8a"
tot = sum(v["cases"] for v in rep.values() if isinstance(v, dict) and "cases" in v)
f3 = rep["F3"]; f4 = rep["F4"]; f5 = rep["F5"]; f6 = rep["F6"]
nm = {"TotalCases": tot, "VerSha": rep["verifier_sha256"][:16], "NPrimePairs": sum(f4["histogram"].values()), "MeanPrime": f4["mean"],
      "MaxFib": f5["maximum"], "NFib": sum(f5["histogram"].values()), "BfourPrime": f3["d_661_673"]["B4_661"], "BthreePrime": f3["d_661_673"]["B3_673"],
      "BthreeA": f3["d_61_67"]["B3_61"], "BthreeB": f3["d_61_67"]["B3_67"], "MeanCtl": f6["ratio_matched_mean"], "MeanRnd": f6["random_pairs_mean"], "NCtl": sum(f6["ratio_matched_hist"].values()), "NRnd": sum(f6["random_pairs_hist"].values())}
with open(out + "/numbers.tex", "w") as f:
    for k, v in nm.items(): f.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
def hrow(h): return " & ".join(str(h.get(str(d), 0)) for d in range(2, 9))
with open(out + "/dist_table.tex", "w") as f:
    f.write("\\begin{tabular}{@{}lrrrrrrrr@{}}\\toprule family & pairs & $d{=}2$ & 3 & 4 & 5 & 6 & 7 & 8\\\\\\midrule\n")
    for lab, h in (("consecutive Fibonacci", f5["histogram"]), ("ratio-matched generic pairs", f6["ratio_matched_hist"]), ("consecutive primes $<1200$", f4["histogram"]), ("random pairs $<1200$", f6["random_pairs_hist"])):
        f.write(f"{lab} & {sum(h.values())} & {hrow(h)} \\\\\n")
    f.write("\\bottomrule\\end{tabular}\n")
with open(out + "/big_pairs.tex", "w") as f:
    f.write(", ".join(f"$({p},{q})$" for p, q in f4["pairs_ge7"]))
# figure 1: normalized distributions
fams = [("consecutive Fibonacci", f5["histogram"], blue), ("ratio-matched generic", f6["ratio_matched_hist"], "#9bb7d4"), ("consecutive primes", f4["histogram"], red), ("random pairs <1200", f6["random_pairs_hist"], "#e3a79f")]
fig, ax = plt.subplots(figsize=(7.2, 3.3)); w = 0.2
for i, (lab, h, c) in enumerate(fams):
    n = sum(h.values()); ax.bar([d + (i - 1.5) * w for d in range(2, 9)], [h.get(str(d), 0) / n for d in range(2, 9)], w, label=lab, color=c)
ax.set_xlabel("exact distance"); ax.set_ylabel("fraction of pairs"); ax.legend(frameon=False, fontsize=8)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_title("Consecutive Fibonacci numbers and primes against generic pairs of the same size", fontsize=9.5)
fig.savefig(out + "/figures/fig1_distributions.pdf", bbox_inches="tight"); fig.savefig(out + "/figures/fig1_distributions.png", dpi=150, bbox_inches="tight"); plt.close(fig)
# figure 2: prime distance vs gap
rows = list(csv.DictReader(open(data + "/prime_distance_table.csv")))
import collections
g = collections.defaultdict(list)
for r in rows: g[int(r["q"]) - int(r["p"])].append(int(r["d"]))
fig, ax = plt.subplots(figsize=(6.4, 3.1))
for gap, v in sorted(g.items()):
    ax.scatter([gap] * len(v), v, s=12, color=blue, alpha=.45)
    ax.plot([gap - .4, gap + .4], [sum(v) / len(v)] * 2, color=red, lw=2)
ax.set_xlabel("prime gap $q-p$"); ax.set_ylabel("exact distance $d(p,q)$"); ax.set_yticks(range(4, 9))
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_title("Distance between consecutive primes versus gap (red: mean per gap)", fontsize=9.5)
fig.savefig(out + "/figures/fig2_gap.pdf", bbox_inches="tight"); fig.savefig(out + "/figures/fig2_gap.png", dpi=150, bbox_inches="tight"); plt.close(fig)
# figure 3: the two certified prime paths
fig, axs = plt.subplots(2, 1, figsize=(9.2, 3.8))
for ax, key, ttl in ((axs[0], "d_61_67", "61 → 67 (7 moves)"), (axs[1], "d_661_673", "661 → 673 (8 moves)")):
    P = f3[key]["path"]; L = f3[key]["labels"]; ax.axis("off"); ax.set_xlim(0, len(P)); ax.set_ylim(0, 1.3); ax.set_title(ttl, fontsize=9, loc="left")
    for i, v in enumerate(P):
        ax.text(i + .5, .35, f"{v:,}", ha="center", va="center", fontsize=6.6, bbox=dict(boxstyle="round", fc="#eaf1f8", ec=blue))
        if i < len(L):
            c = "#2e7d32" if L[i][0] == "+" else red
            ax.annotate("", xy=(i + 1.04, .35), xytext=(i + .96, .35), arrowprops=dict(arrowstyle="->", color=c)); ax.text(i + 1, .8, L[i], ha="center", fontsize=6.8, color=c)
fig.savefig(out + "/figures/fig3_prime_paths.pdf", bbox_inches="tight"); fig.savefig(out + "/figures/fig3_prime_paths.png", dpi=150, bbox_inches="tight"); plt.close(fig)
print("built")
