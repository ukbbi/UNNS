"""GEO-HD-1B / E2-P1 -- static 3-D figures from the stored JSON data (needs matplotlib + numpy).
Usage: python src/make_figures.py   -> figures/*.png  (figures are illustrations; the record is the JSON/certificates)"""
import json
import os
from itertools import product

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLUE, RED, GREEN, ORANGE, GREY = "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#7f7f7f"


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def add(u, g, b=1):
    return tuple(a + b * c for a, c in zip(u, g))


def corners(base, gens):
    out = []
    for bits in product((0, 1), repeat=len(gens)):
        v = base
        for b, g in zip(bits, gens):
            if b:
                v = add(v, g)
        out.append(v)
    return out


def faces_of_cell(base, gens):
    """Polygons (list of 4 corners in order) bounding / forming the cell."""
    gens = [tuple(g) for g in gens]
    base = tuple(base)
    polys = []
    if len(gens) == 2:
        g, h = gens
        polys.append([base, add(base, g), add(add(base, g), h), add(base, h)])
    elif len(gens) == 3:
        for i in range(3):
            g, h = [gens[j] for j in range(3) if j != i]
            for off in (base, add(base, gens[i])):
                polys.append([off, add(off, g), add(add(off, g), h), add(off, h)])
    return polys


def style(ax, title):
    ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.set_zlim(0, 2)
    ax.set_xlabel(r"$\alpha_2$"); ax.set_ylabel(r"$\alpha_5$"); ax.set_zlabel(r"$\alpha_{11}$")
    ax.set_xticks([0, 1, 2]); ax.set_yticks([0, 1, 2]); ax.set_zticks([0, 1, 2])
    ax.set_title(title, fontsize=9)
    ax.view_init(elev=22, azim=-58)
    ax.set_box_aspect((1, 1, 1))


def draw_points(ax, pts, color, s=34, marker="o", label=None):
    if pts:
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], [p[2] for p in pts], c=color, s=s, marker=marker, depthshade=False, label=label, edgecolors="k", linewidths=0.4)


def draw_edges(ax, edges, color, lw=0.8, alpha=0.7):
    for u, v in edges:
        ax.plot([u[0], v[0]], [u[1], v[1]], [u[2], v[2]], color=color, lw=lw, alpha=alpha)


def cell_edges(cells):
    return [(tuple(c["verts"][0]), tuple(c["verts"][-1])) for c in cells]


def fig_fibre_transition():
    fib = load("data/E2_FIBRES.json")
    cells = load("data/E2_CELLS.json")
    F = [set(map(tuple, s["fibre"])) for s in fib["stages"]]
    fig = plt.figure(figsize=(15, 5.2))
    titles = [r"Stage 0: $x_0=110^4/3$, $b=3$" + "\n13 occurrence vertices, lattice = even-sum,\n45 Graver edges",
              r"Stage 1: $x_1=2\cdot110^4/3$, $b=3$" + "\nidentical fibre, lattice and complex (0 changes)",
              r"Stage 2: $x_2=110^4$, $b=1$" + "\n26 vertices (13 preserved + 13 new), lattice = $\\mathbb{Z}^3$,\n51 unit edges (none = a source edge)"]
    for n in range(3):
        ax = fig.add_subplot(1, 3, n + 1, projection="3d")
        style(ax, titles[n])
        src = cells["stage0"]["cells"]["1"] if n < 2 else cells["stage2"]["cells"]["1"]
        edges = [(tuple(c["verts"][0]), tuple(c["verts"][1])) for c in src]
        draw_edges(ax, edges, GREY if n < 2 else GREEN, lw=0.7, alpha=0.55)
        draw_points(ax, sorted(F[0]), BLUE, label="preserved vertex (13)")
        if n == 2:
            draw_points(ax, sorted(F[2] - F[0]), GREEN, marker="^", label="new vertex (13)")
        ax.scatter([0], [0], [0], facecolors="none", edgecolors="k", s=50, marker="s", label="origin (removed)")
        if n == 0:
            ax.legend(loc="upper left", fontsize=7)
        if n == 2:
            ax.legend(loc="upper left", fontsize=7)
    fig.suptitle("E2-P1: occurrence vertices persist (D(x0)=D(x1) subset D(x2)); Graver edges do not (0 of 45 are target edges)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(ROOT, "figures", "fibre_transition.png"), dpi=130)
    plt.close(fig)


def fig_cell_survival():
    tr = load("results/E2_TRANSPORT.json")
    ab = tr["abstract_survival"]["0->2"]
    gs = tr["geometry"]["source_cells_vs_U2"]
    fig = plt.figure(figsize=(15, 5.2))
    ax = fig.add_subplot(1, 3, 1)
    dims = ["0 (vertex)", "1 (edge)", "2 (square-type)", "3 (solid)"]
    pres = [ab[str(j)]["preserved"] for j in range(4)]
    lost = [ab[str(j)]["lost"] for j in range(4)]
    new = [ab[str(j)]["new"] for j in range(4)]
    x = list(range(4))
    ax.bar([i - 0.27 for i in x], pres, 0.27, color=BLUE, label="preserved")
    ax.bar(x, lost, 0.27, color=RED, label="lost (source cell not a target cell)")
    ax.bar([i + 0.27 for i in x], new, 0.27, color=GREEN, label="new (target cell)")
    for i in x:
        for off, v in ((-0.27, pres[i]), (0, lost[i]), (0.27, new[i])):
            ax.text(i + off, v + 0.8, str(v), ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(dims, fontsize=8); ax.set_ylabel("number of cells")
    ax.set_title("Abstract K_abs: stage 0 -> stage 2", fontsize=10); ax.legend(fontsize=7)
    ax = fig.add_subplot(1, 3, 2)
    cont = [gs[str(j)]["CONTAINED"] for j in range(4)]
    part = [gs[str(j)]["PARTIAL"] for j in range(4)]
    ax.bar(x, cont, 0.5, color=BLUE, label="source cell lies inside U(x2)")
    ax.bar(x, part, 0.5, bottom=cont, color=ORANGE, label="source cell leaves U(x2)")
    for i in x:
        ax.text(i, cont[i] + part[i] + 0.8, "%d / %d" % (cont[i], cont[i] + part[i]), ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels(dims, fontsize=8); ax.set_ylabel("number of source cells")
    ax.set_ylim(0, 56)
    ax.set_title("Geometric: source cells vs the target union U(x2)", fontsize=10); ax.legend(fontsize=7, loc="upper right")
    ax = fig.add_subplot(1, 3, 3, projection="3d")
    style(ax, "The 6 cells that leave U(x2): all contain (0,1,1),(1,0,1),(1,1,0)")
    # corner region R = [0,1]^3 wireframe
    for a, b in ((0, 1),):
        pass
    cube = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]:
        ax.plot(*zip(cube[i], cube[j]), color="k", lw=0.8, ls="--")
    for c in tr["geometry"]["partial_cells"]:
        col = ORANGE
        polys = faces_of_cell(c["base"], c["gens"])
        pc = Poly3DCollection(polys, facecolor=col, edgecolor="k", linewidths=0.4, alpha=0.18 if c["dim"] == 3 else 0.45)
        ax.add_collection3d(pc)
    ax.scatter([2 / 3], [2 / 3], [2 / 3], c="red", s=90, marker="*", label="witness (2/3,2/3,2/3)", depthshade=False, zorder=10)
    fib = load("data/E2_FIBRES.json")
    draw_points(ax, [tuple(p) for p in fib["stages"][0]["fibre"]], BLUE, s=18)
    ax.legend(loc="upper left", fontsize=7)
    fig.suptitle("E2-P1: cell survival. All 45 edges are abstractly lost but geometrically kept; 6 of 39 higher cells leave the target union", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(ROOT, "figures", "cell_survival.png"), dpi=130)
    plt.close(fig)


def fig_geometry_comparison():
    tr = load("results/E2_TRANSPORT.json")
    g0, g2 = tr["geometry"]["stage0"], tr["geometry"]["stage2"]
    partial = {(tuple(c["base"]), tuple(map(tuple, c["gens"]))) for c in tr["geometry"]["partial_cells"]}
    fig = plt.figure(figsize=(15, 5.4))
    ax = fig.add_subplot(1, 3, 1, projection="3d")
    style(ax, "U(x0)=U(x1): 15 sheets + 3 solids\nbeta(U)=(1,0,18);  K_abs beta=(1,6,6);  NOT embedded")
    for c in g0["geometric_maximal"]:
        key = (tuple(c["base"]), tuple(map(tuple, c["gens"])))
        col = ORANGE if key in partial else BLUE
        polys = faces_of_cell(c["base"], c["gens"])
        ax.add_collection3d(Poly3DCollection(polys, facecolor=col, edgecolor="k", linewidths=0.3, alpha=0.10 if c["dim"] == 3 else 0.35))
    fib = load("data/E2_FIBRES.json")
    draw_points(ax, [tuple(p) for p in fib["stages"][0]["fibre"]], BLUE, s=22)
    ax = fig.add_subplot(1, 3, 2, projection="3d")
    style(ax, "U(x2)=Y: 7 unit cubes (origin cube removed)\nbeta(U)=beta(K_abs)=(1,0,0);  embedded")
    for c in g2["geometric_maximal"]:
        polys = faces_of_cell(c["base"], c["gens"])
        ax.add_collection3d(Poly3DCollection(polys, facecolor=GREEN, edgecolor="k", linewidths=0.3, alpha=0.18))
    draw_points(ax, [tuple(p) for p in fib["stages"][2]["fibre"]], GREEN, s=16)
    ax = fig.add_subplot(1, 3, 3, projection="3d")
    style(ax, "Overlay: source sheets inside U(x2) (blue),\nleaving it through the corner region R (orange)")
    for c in g0["geometric_maximal"]:
        key = (tuple(c["base"]), tuple(map(tuple, c["gens"])))
        col = ORANGE if key in partial else BLUE
        polys = faces_of_cell(c["base"], c["gens"])
        ax.add_collection3d(Poly3DCollection(polys, facecolor=col, edgecolor="none", alpha=0.06 if c["dim"] == 3 else 0.28))
    cube = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    ax.add_collection3d(Poly3DCollection(faces_of_cell((0, 0, 0), [(1, 0, 0), (0, 1, 0), (0, 0, 1)]), facecolor=RED, edgecolor=RED, alpha=0.06))
    draw_points(ax, [tuple(p) for p in fib["stages"][2]["fibre"] if tuple(p) not in set(map(tuple, fib["stages"][0]["fibre"]))], GREEN, marker="^", s=22, label="new vertex")
    draw_points(ax, [tuple(p) for p in fib["stages"][0]["fibre"]], BLUE, s=22, label="preserved vertex")
    ax.scatter([2 / 3], [2 / 3], [2 / 3], c="red", s=60, marker="*", label="witness in R")
    ax.legend(loc="upper left", fontsize=7)
    fig.suptitle("E2-P1: realized geometry before and after the lattice change (red cube = deleted corner region [0,1)^3)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(os.path.join(ROOT, "figures", "geometry_comparison.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig_fibre_transition()
    fig_cell_survival()
    fig_geometry_comparison()
    print("figures written")
