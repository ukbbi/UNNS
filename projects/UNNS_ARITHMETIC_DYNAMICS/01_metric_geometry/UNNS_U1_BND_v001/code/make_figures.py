#!/usr/bin/env python3
"""Figures for UNNS-U1-BND v001, built only from computed data (CSV, identities)."""
import csv, sys
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import u1_bnd_lib as L

OUT = sys.argv[1]; CSV = sys.argv[2]
C = {4: "#4C78A8", 5: "#F2B134", 6: "#C0392B"}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf", bbox_inches="tight"); fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight"); plt.close(fig)

# ---- Fig 1: residue-class cover modulo 24
fig, ax = plt.subplots(figsize=(7.2, 3.3))
for r in range(24):
    n = r + 24 * 3
    ident = L.identity_for(n)[0]; ln = len(ident["steps"])
    x, y = r % 12, 1 - r // 12
    ax.add_patch(FancyBboxPatch((x + .04, y + .04), .92, .92, boxstyle="round,pad=0.0,rounding_size=0.08",
                                fc=C[ln], ec="white", lw=1.5, alpha=.92))
    ax.text(x + .5, y + .64, f"{r}", ha="center", va="center", fontsize=11, color="white", weight="bold")
    ax.text(x + .5, y + .30, f"{ident['name']} · {ln}", ha="center", va="center", fontsize=8.5, color="white")
ax.set_xlim(0, 12); ax.set_ylim(0, 2); ax.axis("off")
ax.set_title("Residue of $n$ modulo 24 → identity class and number of steps", fontsize=10)
for i, (ln, c) in enumerate(C.items()):
    ax.add_patch(plt.Rectangle((3.2 + i * 2.1, -.42), .28, .22, color=c, clip_on=False))
    ax.text(3.6 + i * 2.1, -.31, f"{ln} steps", va="center", fontsize=9)
save(fig, "fig1_residue_cover")

# ---- Fig 2: exact distances
rows = [(int(a), int(b)) for a, b in list(csv.reader(open(CSV)))[1:]]
dist = Counter(d for _, d in rows); N = len(rows)
six = Counter(n % 24 for n, d in rows if d == 6)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9))
ds = sorted(dist)
a1.bar([str(d) for d in ds], [dist[d] for d in ds], color=[C.get(d, "#7f7f7f") if d >= 4 else "#9aa" for d in ds])
for i, d in enumerate(ds): a1.text(i, dist[d], f"{dist[d]}", ha="center", va="bottom", fontsize=8)
a1.set_xlabel("exact distance $d(n,n+1)$"); a1.set_ylabel(f"number of $n\\leq {N}$")
a1.set_title("Distribution", fontsize=10)
rs = list(range(24)); a2.bar(rs, [six.get(r, 0) for r in rs], color=C[6])
a2.set_xlabel("$n$ mod 24"); a2.set_ylabel("count with $d(n,n+1)=6$"); a2.set_xticks([0, 3, 7, 11, 15, 19, 23])
a2.set_title("Where the value 6 occurs", fontsize=10)
fig.tight_layout(); save(fig, "fig2_distance_distribution")

# ---- Fig 3: two concrete paths (identity A at n=41, identity I at n=163)
def chain(ax, n, y, title):
    st = L.replay(n); ident, t = L.identity_for(n); labs = L.labels_at(ident, t)
    k = len(st); xs = [i * (10.0 / (k - 1)) for i in range(k)]
    for i, (x, s) in enumerate(zip(xs, st)):
        ax.add_patch(FancyBboxPatch((x - .62, y - .17), 1.24, .34, boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc="#eef3f8" if 0 < i < k - 1 else "#d6e4f0", ec="#4C78A8", lw=1))
        ax.text(x, y, f"{s}", ha="center", va="center", fontsize=8)
    for i, (d, Nn) in enumerate(labs):
        ax.add_patch(FancyArrowPatch((xs[i] + .64, y), (xs[i + 1] - .64, y), arrowstyle="-|>", mutation_scale=9,
                                     color="#C0392B" if d == "-" else "#2E7D32", lw=1.2))
        ax.text((xs[i] + xs[i + 1]) / 2, y + .27, f"{'+' if d == '+' else '−'}{Nn}", ha="center", fontsize=8,
                color="#C0392B" if d == "-" else "#2E7D32")
    ax.text(-0.9, y + .5, title, fontsize=9.5, weight="bold")
fig, ax = plt.subplots(figsize=(7.6, 2.9))
chain(ax, 41, 1.45, "n = 41 (class A, 4 steps)")
chain(ax, 163, .35, "n = 163 (class I, 6 steps; d = 6 is attained here)")
ax.set_xlim(-1, 11); ax.set_ylim(-.1, 2.1); ax.axis("off")
ax.text(5, -.12, "green: forward step $+N$   ·   red: inverse step $-N$", ha="center", fontsize=8.5)
save(fig, "fig3_example_paths")
print("figures written")
