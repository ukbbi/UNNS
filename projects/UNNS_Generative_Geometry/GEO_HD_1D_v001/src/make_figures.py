"""HD-1D v001: figures (matplotlib).  python src/make_figures.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from itertools import product
from route_complex import route_cube_family, cube_histories
from select_history import complete_histories, run, fibre

def fig_72():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    pos = {1: (0, 1), 4: (1, 1), 16: (2, 1.5), 18: (2, 0.5), 3: (1, 2.4), 10: (1, -0.6), 72: (3, 1)}
    edges = [(1, 4, 1), (4, 16, 1), (4, 18, 2), (16, 72, 2), (18, 72, 1), (3, 16, 3), (10, 72, 5)]
    for a, b, l in edges:
        (x0, y0), (x1, y1) = pos[a], pos[b]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=1.4, color="#444", shrinkA=16, shrinkB=16))
        ax.text((x0 + x1) / 2 + (0.25 if (a, b) == (10, 72) else 0), (y0 + y1) / 2 + (0.07 if (a, b) != (10, 72) else -0.12), "N=%d" % l, fontsize=8, color="#a33", ha="center")
    for s, (x, y) in pos.items():
        D = fibre(s)
        ax.text(x, y, "%d\nD=%s" % (s, "{" + ",".join(map(str, D)) + "}" if D else "{}"), ha="center", va="center", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="#eef" if s != 72 else "#fe8", ec="#337"))
    ax.set_title("The four complete histories of 72 (classes: {h1,h2} | {h3} | {h4})"); ax.axis("off"); ax.set_xlim(-0.4, 3.5); ax.set_ylim(-1.1, 3)
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "histories_72.png"), dpi=130); plt.close(fig)

def fig_cubes():
    fig = plt.figure(figsize=(9, 4.2))
    for k, r in enumerate((2, 3)):
        ax = fig.add_subplot(1, 2, k + 1)
        base, pos = route_cube_family(r)
        vs = cube_histories(base, pos)
        for bits, h in vs:
            if r == 2: x, y = bits[0] * 2 + 0.0, bits[1] * 2
            else: x, y = bits[0] * 2 + bits[2] * 0.9, bits[1] * 2 + bits[2] * 0.9
            ax.plot(x, y, "o", color="#337")
            blocks = "".join(str(h[1][r + 2 * j]) + str(h[1][r + 2 * j + 1]) + ("|" if j < r - 1 else "") for j in range(r))
            ax.text(x, y + 0.12, blocks, ha="center", fontsize=8)
        for bits, h in vs:
            for j in range(r):
                if bits[j] == 0:
                    b2 = bits[:j] + (1,) + bits[j + 1:]
                    def xy(b):
                        if r == 2: return b[0] * 2.0, b[1] * 2.0
                        return b[0] * 2 + b[2] * 0.9, b[1] * 2 + b[2] * 0.9
                    (x0, y0), (x1, y1) = xy(bits), xy(b2)
                    ax.plot([x0, x1], [y0, y1], "-", color="#999", lw=1)
        ax.set_title("r=%d: %d histories of 72^%d (prefix 1^%d, blocks 12/21)" % (r, 2 ** r, r, r), fontsize=9); ax.axis("off"); ax.set_aspect("equal")
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "route_cubes.png"), dpi=130); plt.close(fig)

def fig_projection():
    d = json.load(open(os.path.join(ROOT, "data", "D_B3_72_POWERS.json")))
    rs = [1, 2, 3]
    H = [d["table"][r - 1]["H"] for r in rs]; C = [d["detail"][str(r)]["swap_classes"] for r in rs]
    G = [d["detail"][str(r)]["source_content_groups"] for r in rs]; B = [d["table"][r - 1]["binom_2r_r"] for r in rs]
    fig, ax = plt.subplots(figsize=(6.4, 4))
    w = 0.2; xs = range(len(rs))
    for i, (lab, vals, col) in enumerate((("complete histories H(72^r)", H, "#337"), ("swap classes", C, "#a33"), ("(source,content) groups", G, "#3a3"), ("binomial bound C(2r,r)", B, "#aaa"))):
        ax.bar([x + (i - 1.5) * w for x in xs], vals, w, label=lab, color=col)
    ax.set_yscale("log"); ax.set_xticks(list(xs)); ax.set_xticklabels(["r=%d" % r for r in rs]); ax.legend(fontsize=7)
    ax.set_title("Many histories project to one endpoint 72^r", fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "history_projection.png"), dpi=130); plt.close(fig)

if __name__ == "__main__":
    fig_72(); fig_cubes(); fig_projection(); print("figures written")
