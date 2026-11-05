"""Shared drawing conventions for the Paper I figures (v0.2).
Colour/line conventions (colour is never the only cue: line style, marker and hatch are used as well):
  source structures  blue   (solid lines)           surviving relations  green (thick solid)
  target structures  teal   (dashed lines)          lost relations       red   (dotted)
  uncovered/excluded light orange (hatched)         exact witnesses      magenta star with black edge
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
SRC, TGT, KEEP, LOST = "#1f5fa8", "#17807e", "#2e8b3d", "#c0392b"
UNC, UNC_E, WIT, GREY = "#f8c98a", "#c47a12", "#b0189e", "#9aa5ad"
SRC_L, TGT_L = "#aecbeb", "#a9dcd9"
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8.5, "axes.labelsize": 8, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "pdf.fonttype": 42, "ps.fonttype": 42,
                     "hatch.linewidth": 0.6, "axes.linewidth": 0.6, "lines.solid_capstyle": "round"})
W = 6.2  # text width in inches

DATA = {}      # figure data records (exact inputs), written to results/FIGURE_DATA.json

def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".pdf"), bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)

def tag(ax, s, loc=None, **kw):
    """Prefix the axes title with a bold panel letter and left-align it."""
    t = ax.get_title("center") or ax.get_title("left")
    fs = ax.title.get_fontsize()
    ax.set_title("", loc="center")
    ax.set_title(f"$\\mathbf{{{s}}}$  " + t, loc="left", fontsize=fs)

def witness2(ax, p, **kw):
    ax.plot([p[0]], [p[1]], marker="*", ms=11, mfc=WIT, mec="k", mew=0.6, ls="none", zorder=10, **kw)

def witness3(ax, p, **kw):
    ax.plot([p[0]], [p[1]], [p[2]], marker="*", ms=11, mfc=WIT, mec="k", mew=0.6, ls="none", zorder=20, **kw)

def fr(x):
    from fractions import Fraction
    return str(x)

# ---------- 3D helpers
def setup3d(ax, lo, hi, view=(22, -58), labels=("$x_1$", "$x_2$", "$x_3$"), ticks=None):
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
    ax.set_box_aspect((hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2]))
    ax.view_init(*view)
    ax.set_xlabel(labels[0], labelpad=-6); ax.set_ylabel(labels[1], labelpad=-6)
    ax.text2D(0.02, 0.93, labels[2], transform=ax.transAxes, fontsize=8)
    for a in (ax.xaxis, ax.yaxis, ax.zaxis):
        a.pane.set_facecolor((1, 1, 1, 0)); a.pane.set_edgecolor((0.8, 0.8, 0.8, 1))
        a._axinfo["grid"]["color"] = (0.88, 0.88, 0.88, 1); a._axinfo["grid"]["linewidth"] = 0.4
    if ticks is None:
        ticks = [list(range(int(lo[i]), int(hi[i])+1, max(1, int((hi[i]-lo[i])//2) or 1))) for i in range(3)]
    ax.set_xticks(ticks[0]); ax.set_yticks(ticks[1]); ax.set_zticks(ticks[2])
    ax.tick_params(pad=-3, labelsize=6.5)

def box_edges(lo, hi):
    pts = {}
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                pts[(i, j, k)] = (hi[0] if i else lo[0], hi[1] if j else lo[1], hi[2] if k else lo[2])
    segs = []
    for a in pts:
        for b in pts:
            if a < b and sum(x != y for x, y in zip(a, b)) == 1:
                segs.append((pts[a], pts[b]))
    return segs

def wirebox(ax, lo, hi, color="k", lw=0.6, ls="-", alpha=1.0):
    ax.add_collection3d(Line3DCollection(box_edges(lo, hi), colors=color, linewidths=lw, linestyles=ls, alpha=alpha))

def poly3(ax, pts, fc, ec="k", alpha=0.35, lw=0.8, ls="-", hatch=None):
    p = Poly3DCollection([pts], facecolors=fc, edgecolors=ec, linewidths=lw, linestyles=ls, alpha=alpha)
    ax.add_collection3d(p)
    return p

def seg3(ax, a, b, color="k", lw=1.0, ls="-", **kw):
    ax.plot([a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color=color, lw=lw, ls=ls, **kw)

def pts3(ax, P, **kw):
    P = np.array(P, float); ax.scatter(P[:, 0], P[:, 1], P[:, 2], **kw)

def cell_corners(cell):
    """Corners of a cell (u, gens) in cyclic order for dim 2."""
    u, gens = cell
    if len(gens) == 2:
        g, h = gens
        a = np.array(u, float); g = np.array(g, float); h = np.array(h, float)
        return [tuple(a), tuple(a+g), tuple(a+g+h), tuple(a+h)]
    raise ValueError

def style_axes2(ax, xlim, ylim, xt=None, yt=None, grid=True, equal=True):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if equal: ax.set_aspect("equal")
    if xt is not None: ax.set_xticks(xt)
    if yt is not None: ax.set_yticks(yt)
    if grid: ax.grid(True, lw=0.3, color="#dddddd", zorder=0)
    for s in ax.spines.values(): s.set_linewidth(0.5)
