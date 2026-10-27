#!/usr/bin/env python3
"""GEO-I v012 figures -> figures_v12/*.png (matplotlib needed for figures only)"""
import os, sys
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import gcd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import cap_cover as C, cap_cells as K
OUT = os.path.join(ROOT, 'figures_v12'); os.makedirs(OUT, exist_ok=True)
# 1 ---- cell cover of a mixed box, Omega types
fig, axs = plt.subplots(1, 2, figsize=(11.5, 5.4))
for ax, (d, s, u, v) in zip(axs, ((13, 5, 6, 4), (21, 8, 12, 15))):
    cells, Om, F = C.construct(d, s, u, v); col = {'L': 'tab:blue', 'D': 'tab:orange', 'B': 'tab:green', 'T': 'tab:red'}
    for tag, c in cells: ax.add_patch(Polygon(K.corners(c), closed=True, alpha=0.30, fc=col[tag], ec=col[tag], lw=0.7))
    H = K.hull(list(F)); ax.add_patch(Polygon(H, closed=True, fill=False, ec='k', lw=1.4))
    ax.axvline(d, color='gray', ls=':'); ax.axhline(d, color='gray', ls=':')
    ax.scatter(*zip(*F), s=5, c='k'); ax.scatter(*zip(*Om), s=26, c='crimson', zorder=3)
    ax.set_aspect('equal'); ax.set_title('d=%d s=%d Q=(d+%d,d+%d): Omega (red), L/D/bottom/left cells' % (d, s, u, v), fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig1_mixed_cap_cells.png'), dpi=130); plt.close()
# 2 ---- G12-T1 margin: max(...)/xy over all Pareto-minimal points
xs, ys = [], []
for d in range(5, 61):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        t = pow(s, -1, d)
        for x in range(1, d):
            y = (s * x) % d
            if y == 0 or any(((j - s * i) % d == 0) and (i, j) not in ((0, 0), (x, y)) for i in range(x + 1) for j in range(y + 1)): continue
            xs.append(x * y); ys.append(max(y + x * (d - s), (d - t) * y + x) / (x * y))
fig, ax = plt.subplots(figsize=(6.5, 4)); ax.scatter(xs, ys, s=4); ax.axhline(1, color='r', ls='--'); ax.set_xscale('log'); ax.set_ylim(0.9, max(ys) * 1.05 if max(ys) < 8 else 8)
ax.set_xlabel('xy'); ax.set_ylabel('max(y+(d-s)x, (d-t)y+x) / xy'); ax.set_title('G12-T1: ratio >= 1 at every Pareto-minimal point (d<=60, %d points)' % len(xs), fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig2_arith_margin.png'), dpi=130); plt.close()
print('ok', len(xs))
