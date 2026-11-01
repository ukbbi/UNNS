"""Figures for E2-P2, drawn from the certified records (data/P2_A.json, data/P2_B.json, data/P2_F21.json,
results/P2_GEOMETRY.json).  Needs matplotlib.  No geometric statement depends on the pictures."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)


def L(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def corners(c):
    b, g = c["base"], c["gens"]
    if len(g) == 0:
        return [tuple(b)]
    if len(g) == 1:
        return [tuple(b), (b[0] + g[0][0], b[1] + g[0][1])]
    p = [tuple(b), (b[0] + g[0][0], b[1] + g[0][1]), (b[0] + g[0][0] + g[1][0], b[1] + g[0][1] + g[1][1]),
         (b[0] + g[1][0], b[1] + g[1][1])]
    return p


def draw_union(ax, cells, face, edge, alpha=0.5, lw=1.0, z=1):
    for c in cells:
        p = corners(c)
        if len(p) == 4:
            ax.add_patch(Polygon(p, closed=True, facecolor=face, edgecolor=edge, alpha=alpha, lw=lw, zorder=z))
        elif len(p) == 2:
            ax.plot([p[0][0], p[1][0]], [p[0][1], p[1][1]], color=edge, lw=lw * 1.6, zorder=z + 1)
        else:
            ax.plot([p[0][0]], [p[0][1]], "o", color=edge, ms=4, zorder=z + 1)


def setup(ax, h, title):
    ax.set_xlim(-0.5, h + 0.5)
    ax.set_ylim(-0.5, h + 0.5)
    ax.set_aspect("equal")
    ax.set_xticks(range(h + 1))
    ax.set_yticks(range(h + 1))
    ax.grid(True, lw=0.3, color="#bbbbbb")
    ax.set_title(title, fontsize=9)
    ax.set_xlabel("exponent of p1")
    ax.set_ylabel("exponent of p2")


def fig_lattice():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    for ax, name, tr, h in ((axes[0], "P2_A", "P2-A: 21^8/5 -> 21^8/4", 4), (axes[1], "P2_B", "P2-B: 55^12/27 -> 55^12/18", 6)):
        d = L("data/%s.json" % name)
        setup(ax, h, tr + "\n(source lattice a-b=0 mod %d, target a-b=0 mod %d)" % ((4, 2)[name == "P2_A"] if False else (4 if name == "P2_A" else 18), (2 if name == "P2_A" else 6)))
        src = {tuple(v) for v in d["fibre"]["source"]}
        tgt = {tuple(v) for v in d["fibre"]["target"]}
        for v in tgt - src:
            ax.plot(*v, "s", color="#2a9d8f", ms=9, zorder=3)
        for v in src:
            ax.plot(*v, "o", color="#e76f51", ms=8, zorder=4)
        ax.plot([], [], "o", color="#e76f51", label="source fibre (preserved vertex)")
        ax.plot([], [], "s", color="#2a9d8f", label="new vertex")
        ax.legend(loc="upper left", fontsize=7)
    fig.suptitle("Occurrence vertices: all source vertices persist; the lattice (not the vertex set) decides the geometry", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "lattice_transport.png"), dpi=140)


def fig_edges():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    d = L("data/P2_A.json")
    ax = axes[0]
    setup(ax, 4, "P2-A: source Graver edges, kept (green) vs lost (red)")
    for e in d["edges"]["kept"]:
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color="#2a9d8f", lw=3, zorder=3)
    for e in d["edges"]["lost"]:
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color="#e63946", lw=1.6, zorder=2)
    for v in d["fibre"]["source"]:
        ax.plot(*v, "ko", ms=6, zorder=5)
    ax = axes[1]
    d = L("data/P2_B.json")
    setup(ax, 6, "P2-B: strict enlargement, every old edge kept")
    for e in d["edges"]["kept"]:
        ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color="#2a9d8f", lw=3, zorder=3)
    for v in d["fibre"]["source"]:
        ax.plot(*v, "ko", ms=6, zorder=5)
    ax = axes[2]
    rows = L("results/P2_CELL_SURVIVAL.json")["family_P2_F21"]["rows"]
    hs = [r["h"] for r in rows]
    ax.plot(hs, [r["formula"]["E_src"] for r in rows], "o-", label="source edges", color="#264653")
    ax.plot(hs, [r["formula"]["E_kept"] for r in rows], "o-", label="kept = (1,1)-edges", color="#2a9d8f")
    ax.plot(hs, [r["formula"]["E_lost"] for r in rows], "o-", label="lost", color="#e63946")
    ax.set_xlabel("h  (x_h = 21^(2h)/5)")
    ax.set_ylabel("number of Graver edges")
    ax.set_title("P2-F21 (theorem P2-TF1): kept ~ h^2/4, source ~ 3h^2/2", fontsize=9)
    ax.legend(fontsize=8)
    ax.grid(True, lw=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "edge_survival.png"), dpi=140)


def fig_geom():
    G = L("results/P2_GEOMETRY.json")["specimens"]
    fig, axes = plt.subplots(2, 3, figsize=(15, 9.5))
    for r, (name, h) in enumerate((("P2-A", 4), ("P2-B", 6))):
        s = G[name]
        d = L("data/P2_%s.json" % name[-1])
        ax = axes[r][0]
        setup(ax, h, "%s: source union U  (Betti %s, embedded=%s)" % (name, s["union_topology"]["source"]["betti"], s["union_topology"]["source"]["embedded"]))
        draw_union(ax, s["maximal_cells_source"], "#e76f51", "#9d2f1d", alpha=0.35)
        ax = axes[r][1]
        setup(ax, h, "%s: target union U'  (Betti %s, embedded=%s)" % (name, s["union_topology"]["target"]["betti"], s["union_topology"]["target"]["embedded"]))
        draw_union(ax, s["maximal_cells_target"], "#2a9d8f", "#14564f", alpha=0.35)
        ax = axes[r][2]
        setup(ax, h, "%s: U inside U' (%s); lost abstract edges in red" % (name, s["union_relation"] if "union_relation" in s else L("data/P2_%s.json" % name[-1])["geometry"]["union_relation"]))
        draw_union(ax, s["maximal_cells_target"], "#cfd8dc", "#78909c", alpha=0.6, lw=0.6)
        for e in d["edges"]["lost"]:
            ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color="#e63946", lw=2, zorder=5)
        for e in d["edges"]["kept"]:
            ax.plot([e[0][0], e[1][0]], [e[0][1], e[1][1]], color="#2a9d8f", lw=2.5, zorder=6)
        w = d["geometry"]["witness_target_not_in_source"]
        ax.plot(float(eval(w[0])), float(eval(w[1])), "k*", ms=12, zorder=9)
    fig.suptitle("Geometric transport (planar, exact): every source cell lies in the target union although abstract edges are lost; "
                 "black star = point of U' not in U", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "geometric_containment.png"), dpi=140)


if __name__ == "__main__":
    fig_lattice()
    fig_edges()
    fig_geom()
    print("figures written")
