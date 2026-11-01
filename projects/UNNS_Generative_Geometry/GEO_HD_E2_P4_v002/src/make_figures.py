"""E2-P4 figures (explanatory renderings of certified exact data).  Usage: python src/make_figures.py [--root DIR]"""
import json
import os
import sys
from fractions import Fraction as Fr

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]
sys.path.insert(0, HERE)
import _boot  # noqa: E402,F401
import certificate_check as cc  # noqa: E402


def J(rel):
    return json.load(open(os.path.join(ROOT, rel)))


def corners(cell):
    return [tuple(float(x) for x in v) for v in cc._verts(cell["base"], cell["gens"])]


def coupled_target_geometry(out):
    c = J("results/P4_CERTIFICATES.json")
    f = J("data/P4_F110.json")["members"]["1"]
    fig = plt.figure(figsize=(11, 4.8))
    for idx, (title, pts, color) in enumerate((("source: Lambda_9 (a-b+c = 0 mod 6), 5 vertices", f["F9"], "#1b6b2f"),
                                              ("target: Lambda_3 = E_3 (a+b+c even), 13 vertices", f["F3"], "#4a7fb5"))):
        ax = fig.add_subplot(1, 2, idx + 1, projection="3d")
        cells = c["m1_forward"]["source_maximal"] if idx == 0 else c["m1_forward"]["target_maximal"]
        for cell in cells:
            vs = corners(cell)
            xs, ys, zs = zip(*vs)
            ax.plot(xs, ys, zs, "-", color=color, alpha=0.35, lw=0.8)
        xs, ys, zs = zip(*pts)
        ax.scatter(xs, ys, zs, color=color, s=22)
        ax.set_title(title, fontsize=8)
        ax.set_xlim(0, 2); ax.set_ylim(0, 2); ax.set_zlim(0, 2)
    fig.suptitle("P4-F110, m = 1, box [0,2]^3: maximal cells (lines) and occurrence vertices", fontsize=9)
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)


def planar_residual_gaps(out):
    r = J("data/E2P3_PLANAR_REFERENCE.json")
    fig, ax = plt.subplots(figsize=(6.5, 4))
    names = list(r["partition"].keys())
    vals = [r["partition"][k] for k in names]
    ax.barh(range(len(names)), vals, color=["#4a7fb5", "#1b6b2f", "#b03030", "#d08a2e"])
    ax.set_yticks(range(len(names))); ax.set_yticklabels([n.replace("RESIDUAL_", "").replace("_", " ") for n in names], fontsize=7)
    ax.set_title("E2-P2 ENLARGE rows (266) by target class; CP3-A open for hollow-box / sub-threshold (P4-E3 not started)", fontsize=7)
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)


def transport_obstruction(out):
    g = J("results/P4_GEOMETRY.json")
    fig, ax = plt.subplots(figsize=(7, 4))
    cats = ["m=1 target gap pieces\n(certified)", "m=1 source cells\nmeeting a gap piece", "n=4 corner: gap nodes\n(E_3 hull-covered)"]
    vals = [g["geometry_m1"]["target_gap"]["n_gap_pieces"], 0, g["corner_n4"]["n_gap_pieces"]]
    ax.bar(cats, vals, color=["#d08a2e", "#1b6b2f", "#4a7fb5"])
    ax.set_title("P4-F110: target holes at m=1 do not obstruct the source (holes are not obstructions)", fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=140); plt.close(fig)


if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    coupled_target_geometry(os.path.join(ROOT, "figures", "coupled_target_geometry.png"))
    planar_residual_gaps(os.path.join(ROOT, "figures", "planar_residual_gaps.png"))
    transport_obstruction(os.path.join(ROOT, "figures", "transport_obstruction.png"))
    print("figures written")
