"""E2-P3 figures.  Explanatory renderings of CERTIFIED exact data (data/P3_CONTROLS.json); not substitutes for proof.
Usage: python make_figures.py [--root DIR]"""
import json
import os
import sys
from fractions import Fraction as Fr
from itertools import product

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]
sys.path.insert(0, HERE)
import audit_p3 as au  # noqa: E402
import certificate_check as cc  # noqa: E402


def verts(cell):
    return [tuple(float(x) for x in v) for v in cc._verts(cell["base"], cell["gens"])]


def hull2(pts):
    import math
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return sorted(pts, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))


def planar_gap_geometry(ctl, out):
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    for ax, name, title in ((axes[0], "A", "Control A: 21^8/5 -> 21^8/4  (target hull-covered, inherited)"),
                            (axes[1], "B", "Control B: 55^12/27 -> 55^12/18  (target hollow box)")):
        c = ctl[name]
        for t in c["target_maximal"]:
            vs = verts(t)
            if len(vs) >= 3:
                ax.add_patch(Polygon(hull2(vs), closed=True, facecolor="#cfe3f7", edgecolor="#4a7fb5", lw=0.8, alpha=0.8))
        for g in c["coverage_gap"].get("gap_pieces", []):
            pts = [(float(Fr(a)), float(Fr(b))) for a, b in g["vertices"]]
            if len(pts) >= 3:
                ax.add_patch(Polygon(hull2(pts), closed=True, facecolor="#f4b6b6", edgecolor="#b03030", lw=0.8, hatch="//"))
        src = c.get("source_maximal") or []
        for s in src:
            vs = verts(s)
            if len(vs) >= 3:
                ax.add_patch(Polygon(hull2(vs), closed=True, facecolor="none", edgecolor="#1b6b2f", lw=1.6))
            elif len(vs) == 2:
                ax.plot([vs[0][0], vs[1][0]], [vs[0][1], vs[1][1]], color="#1b6b2f", lw=1.6)
        q = c["box"]
        ax.set_xlim(-0.3, q[0] + 0.3)
        ax.set_ylim(-0.3, q[1] + 0.3)
        ax.set_aspect("equal")
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("exponent of p1 = %d" % c["primes"][0])
        ax.set_ylabel("exponent of p2 = %d" % c["primes"][1])
    fig.suptitle("target cells (blue), uncovered hull region = coverage gap (red hatched), source maximal cells (green outlines)", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)


def cube_faces(lo, hi):
    x0, y0, z0 = lo
    x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    idx = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)]
    return [[v[i] for i in f] for f in idx]


def source_target_3d(ctl, out):
    c = ctl["C"]
    fig = plt.figure(figsize=(10, 4.8))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    q = c["box"]
    for base in product(*[range(m) for m in q]):
        if base == (0, 0, 0):
            continue
        ax.add_collection3d(Poly3DCollection(cube_faces(base, tuple(b + 1 for b in base)), facecolor="#cfe3f7", edgecolor="#4a7fb5", alpha=0.18))
    ax.add_collection3d(Poly3DCollection(cube_faces((0, 0, 0), (1, 1, 1)), facecolor="#f4b6b6", edgecolor="#b03030", alpha=0.10))
    sw = c["specified_witness_certificate"]["certificate"]
    sc = sw["source_cell"]
    vs = verts(sc)
    ax.add_collection3d(Poly3DCollection([[vs[0], vs[1], vs[3], vs[2]]], facecolor="#2e9b4f", edgecolor="#1b6b2f", alpha=0.55))
    w = [float(Fr(x)) for x in sw["witness"]]
    ax.scatter([w[0]], [w[1]], [w[2]], color="k", s=30)
    ax.text(w[0], w[1], w[2], "  w=(2/3,2/3,2/3)", fontsize=8)
    ax.set_xlim(0, q[0]); ax.set_ylim(0, q[1]); ax.set_zlim(0, q[2])
    ax.set_title("Control C (E2-P1): target Z^3, box (2,2,2)\ntarget = 7 unit cubes (blue); corner cube (red) is uncovered", fontsize=8)
    ax2 = fig.add_subplot(1, 2, 2)
    labels = ["source cell P((0,0,2); (0,1,-1),(1,0,-1))", "witness w", "max_i w_i / o_i"]
    ax2.axis("off")
    ax2.text(0.0, 0.9, "Exact certificate (independently verified)", fontsize=10, weight="bold")
    ax2.text(0.0, 0.72, "w = base + (2/3) g + (2/3) h  in the source cell", fontsize=9)
    ax2.text(0.0, 0.58, "max_i w_i = 2/3 < 1  =>  w in the open corner cube", fontsize=9)
    ax2.text(0.0, 0.44, "U' = { z in [0,2]^3 : max z_i >= 1 }   (P3-T3(a))", fontsize=9)
    ax2.text(0.0, 0.30, "for each of the %d maximal target cells an exact\nviolated inequality is listed in P3_CONTROLS.json" % len(c["target_maximal"]), fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)


def obstruction_witness(ctl, d3, out):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
    fl = d3["lattice_model"]["failures"]
    from collections import Counter
    cnt = Counter((r["index"], tuple(map(tuple, r["basis"]))) for r in fl)
    labs = ["idx %d  [%s]" % (k[0], ",".join("".join(map(str, row)) for row in k[1])) for k in cnt]
    ax[0].barh(range(len(cnt)), list(cnt.values()), color="#b03030")
    ax[0].set_yticks(range(len(cnt)))
    ax[0].set_yticklabels(labs, fontsize=6)
    ax[0].set_xlabel("failing boxes in {1,2}^3 (target Z^3, pure-lattice model)")
    ax[0].set_title("Lattices of index <= 8 with U not in U'", fontsize=9)
    s1 = d3["S1"]["table"]
    contained = sum(t["count"] for t in s1 if t["verdict"] == "CONTAINED")
    fail = sum(t["count"] for t in s1 if t["verdict"] == "NOT_CONTAINED")
    s2 = d3["S2"]
    ax[1].bar(["S1 contained", "S1 failures\n(target Z^3)", "S2 rectangular\nnontrivial: exact fails"],
              [contained, fail, len(s2["exact_failures"])], color=["#4a7fb5", "#b03030", "#1b6b2f"])
    ax[1].set_title("FIELD-I three-coordinate search outcomes", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    ctl = json.load(open(os.path.join(ROOT, "data", "P3_CONTROLS.json")))
    d3 = json.load(open(os.path.join(ROOT, "results", "P3_3D.json")))
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    planar_gap_geometry(ctl, os.path.join(ROOT, "figures", "planar_gap_geometry.png"))
    source_target_3d(ctl, os.path.join(ROOT, "figures", "source_target_3d.png"))
    obstruction_witness(ctl, d3, os.path.join(ROOT, "figures", "obstruction_witness.png"))
    print("figures written")
