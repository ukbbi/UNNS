#!/usr/bin/env python3
"""Regenerates figures/*.pdf (matplotlib required)."""
from pathlib import Path
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
OUT = Path(__file__).resolve().parent.parent/"figures"; OUT.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 9}); C = ["#1f4e79", "#c0504d", "#4f8f4f", "#888888"]
# Fig 1: square torus, mode lattice with the similarity carry (1+i)
fig, ax = plt.subplots(figsize=(4.6, 4.4)); R = 7
for i in range(-R, R+1):
    for j in range(-R, R+1):
        ax.plot(i, j, ".", color="#cccccc", ms=3)
for n in range(1, R+1):
    ax.plot(n, 0, "o", color=C[0], ms=5); ax.plot(n, n, "s", color=C[1], ms=5)
ax.plot(0, 6, "o", color=C[0], ms=5)
def arr(a, b, col, rad): ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=11, color=col, lw=1.3, connectionstyle=f"arc3,rad={rad}", shrinkA=4, shrinkB=4))
arr((3, 0), (3, 3), C[1], -0.35); arr((3, 3), (0, 6), C[0], -0.35)
ax.text(4.1, 1.4, r"$\times\sqrt{2}\,R_{45^\circ}$", color=C[1], fontsize=8); ax.text(0.2, 4.9, r"$\times\sqrt{2}\,R_{45^\circ}$", color=C[0], fontsize=8, rotation=-35)
ax.set_xlim(-0.8, R+0.6); ax.set_ylim(-0.8, R+0.6); ax.set_aspect("equal"); ax.set_xlabel("$m_x$"); ax.set_ylabel("$m_y$")
ax.plot([], [], "o", color=C[0], label=r"layer 0: $|m|=n$ (direction $(1,0)$, $(0,1)$)"); ax.plot([], [], "s", color=C[1], label=r"layer 1: $|m|=n\sqrt{2}$ (direction $(1,1)$)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), fontsize=7, framealpha=1); ax.spines[["top", "right"]].set_visible(False)
fig.savefig(OUT/"fig_similarity_carry.pdf", bbox_inches="tight"); plt.close(fig)
# Fig 2: two periodic cavities, alpha = 3^(-1/3)
fig, ax = plt.subplots(figsize=(7.0, 2.7)); a1 = 3**(2/3)
for n in range(1, 15): ax.plot([n, n], [0, .35], color=C[0], lw=1.3); 
for n in range(1, 7): ax.plot([a1*n, a1*n], [0, -.35], color=C[2], lw=1.3)
for n in (2, 9): ax.text(n, .5, str(n), ha="center", fontsize=8, color=C[0])
ax.text(a1*3, -.75, "3", ha="center", fontsize=8, color=C[2])
ax.annotate("", xy=(9, .38), xytext=(2, .38), arrowprops=dict(arrowstyle="-|>", color=C[0], lw=1.2, connectionstyle="arc3,rad=-0.4")); ax.text(5.1, 2.0, r"$T_2$", color=C[0])
ax.annotate("", xy=(a1*3, -.38), xytext=(9, -.38), arrowprops=dict(arrowstyle="-|>", color=C[1], lw=1.2, connectionstyle="arc3,rad=0.35")); ax.text(7.2, -2.0, r"$\alpha=3^{-1/3}$", color=C[1])
ax.plot([2*3**(-1/3)], [0], "x", color=C[1], ms=7); ax.text(2*3**(-1/3), -.7, "not a mode", color=C[1], fontsize=7.5, ha="center")
ax.axhline(0, color="k", lw=.8); ax.set_xlim(0, 15); ax.set_ylim(-2.6, 2.6); ax.set_yticks([])
ax.set_xlabel(r"frequency $\omega/\omega_0$  (blue: cavity 0, modes $n\omega_0$; green: cavity 1, modes $3^{2/3}n\,\omega_0$)")
ax.spines[["top", "right", "left"]].set_visible(False)
fig.savefig(OUT/"fig_two_cavity_carry.pdf", bbox_inches="tight"); plt.close(fig)
print("ok")
