#!/usr/bin/env python3
"""GEO-I v011 figures -> figures_v11/*.png  (matplotlib required for figures only)"""
import os, sys, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import circuit_partitions as CP, cap_cells as K
OUT = os.path.join(ROOT, 'figures_v11'); os.makedirs(OUT, exist_ok=True); D = os.path.join(ROOT, 'output', 'data')
# 1 ---- the W2 inequality
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for p in (9, 10, 12, 16, 24, 40):
    ms = list(range(3, p // 2 + 1)); ax[0].plot(ms, [p * (2 ** m / m - 2) / (2 ** m - 2) for m in ms], 'o-', label='p=%d' % p)
ax[0].axhline(1, color='k', ls='--'); ax[0].set_xlabel('number of blocks m of a partition of 1'); ax[0].set_ylabel('p (2^m/m - 2) / (2^m - 2)'); ax[0].set_title('G11-L6: every block count 3 <= m <= p/2 has ratio >= 1 once p >= 9'); ax[0].legend(); ax[0].set_ylim(0.8, 6)
for k, col in ((3, 'C0'), (4, 'C1'), (5, 'C2'), (6, 'C3')):
    pts = []
    for r in json.load(open(os.path.join(D, 'v10_binary%d.json' % k)))['minimal']: pts.append((r['p'], r['two_circuit_partitions_of_1']))
    ax[1].scatter(*zip(*pts), s=14, c=col, label='nullity %d (%d classes)' % (k, len(pts)))
xs = list(range(4, 34)); ax[1].plot(xs, [x - 1 for x in xs], 'k--', label='p-1 (proved lower bound, p>=9)'); ax[1].set_yscale('log')
ax[1].set_xlabel('p = number of points'); ax[1].set_ylabel('two-block partitions n_2'); ax[1].set_title('all 231 classified minimal classes sit above p-1'); ax[1].legend(fontsize=8)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig1_w2_inequality.png'), dpi=130); plt.close()
# 2 ---- vector-space partition profile
fig, ax = plt.subplots(1, 3, figsize=(12, 3.6))
for a, k in zip(ax, (4, 5, 6)):
    cnt = {}
    for r in json.load(open(os.path.join(D, 'v10_binary%d.json' % k)))['minimal']:
        X = r['support']; c = CP.circuits(X, k); P = CP.partitions(c, len(X))
        for Pp in P: cnt[len(Pp)] = cnt.get(len(Pp), 0) + 1
    ms = sorted(cnt); a.bar([str(m) for m in ms], [cnt[m] for m in ms]); a.set_yscale('log'); a.set_title('nullity %d: all partitions of 1, by block count m' % k, fontsize=9); a.set_xlabel('m (part of dimension m-1 in F_2^{k-1})')
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig2_vector_space_partition.png'), dpi=130); plt.close()
# 3 ---- one-sided cap cover
d, s, u = 13, 5, 6; cells, M, g = K.proof_cells_onesided(d, s, u); fig, ax = plt.subplots(figsize=(7, 5))
Q = (d + u, d); F = K.fibreQ(d, s, Q); H = K.hull(list(F))
ax.add_patch(Polygon(H, closed=True, fc='#eef', ec='k', lw=1))
for i, c in enumerate(cells):
    col = 'C3' if i == len(cells) - 1 else 'C%d' % (i % 3)
    ax.add_patch(Polygon([(float(x), float(y)) for x, y in K.corners(c)], closed=True, fc=col, alpha=0.35, ec=col))
ax.scatter(*zip(*F), s=10, c='k'); ax.plot([d, d], [0, d], 'k:'); ax.scatter([M[0] + d], [M[1]], c='r', zorder=5, s=30)
ax.set_aspect('equal'); ax.set_title('G11-L3: one-sided cap of Q=(%d,%d), s=%d: sweep cells + bottom cell (red)' % (Q[0], Q[1], s), fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, 'fig3_onesided_cap_cells.png'), dpi=130); plt.close()
print(os.listdir(OUT))
