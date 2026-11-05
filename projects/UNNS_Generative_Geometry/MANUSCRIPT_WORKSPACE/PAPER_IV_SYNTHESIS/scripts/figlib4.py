"""Drawing conventions for Paper IV: five arrow statuses with distinct line styles (colour is never the only cue)."""
from figlib3 import *
import json, math
plt.rcParams["mathtext.fontset"]="stix"
ST = {  # status -> (colour, linewidth, linestyle, arrowstyle, name)
 'est':   ("#111111", 1.1, "-",        "-|>",   "established arrow"),
 'fact':  (KEEP,      2.3, "-",        "-|>",   "proved factorization"),
 'obs':   (LOST,      1.3, "-",        "-[",    "proved obstruction"),
 'open':  ("#6b7780", 1.1, (0,(4,2.5)),"->",    "open construction"),
 'interp':(WIT,       1.1, (0,(1,2)),  "<->",   "interpretive comparison"),
}
def sarrow(ax, p, q, status, txt="", rad=0.0, off=(0,0.12), fs=6.3, shrink=0.02):
    c, lw, ls, st, _ = ST[status]
    a = FancyArrowPatch(p, q, arrowstyle=st, mutation_scale=8 if st != "-[" else 6, color=c, lw=lw, ls=ls,
                        connectionstyle=f"arc3,rad={rad}", shrinkA=shrink*28, shrinkB=shrink*28, zorder=2)
    ax.add_patch(a)
    dx_, dy_ = q[0]-p[0], q[1]-p[1]
    cmx, cmy = (p[0]+q[0])/2 + 0.5*rad*dy_, (p[1]+q[1])/2 - 0.5*rad*dx_   # midpoint of the arc3 curve
    if status == 'obs':   # cross mark at the midpoint
        mx, my = cmx, cmy
        ax.text(mx, my, "×", color=c, fontsize=9, ha="center", va="center", zorder=4, fontweight="bold")
    if txt:
        mx, my = cmx+off[0], cmy+off[1]
        ax.text(mx, my, txt, fontsize=fs, ha="center", va="center", color=c if status != 'est' else "k", zorder=5,
                bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.9))
def legend5(ax, x, y, dy=0.36, L=0.9, fs=6.3, ncol=1):
    for i, (k, (c, lw, ls, st, name)) in enumerate(ST.items()):
        yy = y - i*dy
        sarrow(ax, (x, yy), (x+L, yy), k, shrink=0)
        ax.text(x+L+0.12, yy, name, fontsize=fs, va="center")
def mbox(ax, x, y, w, h, txt, kind="space", fs=6.8):
    fc, ec = {"space": (SRC_L, SRC), "obj": (TGT_L, TGT), "result": (KEEP_L, KEEP), "neutral": ("white", "k"), "open": ("#f0f2f3", "#6b7780")}[kind]
    box(ax, x, y, w, h, txt, fc=fc, ec=ec, fs=fs)
def newfig(h=3.0, lim=None, w=W):
    fig, ax = plt.subplots(figsize=(w, h)); clean(ax, lim); return fig, ax
def sub(figsize, nr, nc, **kw):
    return plt.subplots(nr, nc, figsize=figsize, **kw)
def tag(ax, s):
    ax.text(0.0, 1.0, s, transform=ax.transAxes, fontsize=6.3, style="italic", va="bottom")
