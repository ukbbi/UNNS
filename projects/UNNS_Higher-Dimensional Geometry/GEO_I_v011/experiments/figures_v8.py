"""GEO-I v008 figures (7).  All plot computed exact objects except fig6 left panel (labelled ILLUSTRATIVE)."""
import os, sys, json
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d_))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import coverage as C, modular_layers as ML, small_box as SB, hollow as H, cell_cover as CCv, binary_min as BM, binary_01 as B, centre_collisions as CC, rank_reduction as RR
from lattice_model import Lat, U_betti
FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True); DATA = os.path.join(ROOT, 'output', 'data')


def cellpoly(c): u, g, h = c; return [u, (u[0]+g[0], u[1]+g[1]), (u[0]+g[0]+h[0], u[1]+g[1]+h[1]), (u[0]+h[0], u[1]+h[1])]


def draw(ax, d, s, Q, cells, hl=(), alpha=.45):
    for c in cells: ax.add_patch(Polygon(cellpoly(c), closed=True, fc='#9ecae1', ec='k', lw=.4, alpha=alpha))
    for c, col in hl: ax.add_patch(Polygon(cellpoly(c), closed=True, fc=col, ec='k', lw=.8, alpha=.7))
    F = ML.fibre(d, s, Q); ax.scatter([p[0] for p in F], [p[1] for p in F], s=10, c='k', zorder=3)
    ax.add_patch(Polygon(C.hull(sorted(F)), closed=True, fill=False, ec='r', lw=1.1)); ax.set_aspect('equal'); ax.set_xlim(-1, Q[0]+1); ax.set_ylim(-1, Q[1]+1)


def allc(d, s, Q): return [(u, g, h) for (u, (g, h)) in C.complex_data(Lat(d, d, d, s), Q)['cells'][2]]


# 1 small-box region vs solved region
d = 13; fig, axs = plt.subplots(1, 2, figsize=(11, 5))
for ax, s in zip(axs, (5, 8)):
    m = SB.record_min(d, s)
    for u in range(0, 2*d):
        for v in range(0, 2*d):
            if (u, v) == (0, 0): col = 'k'
            elif max(u, v) >= d: col = '#d9d9d9'
            else: col = '#fdae6b' if SB.squareless(d, s, (d+u, d+v)) else '#a1d99b'
            ax.add_patch(plt.Rectangle((u-.5, v-.5), 1, 1, fc=col, ec='w', lw=.3))
    ax.set_xlim(-.5, 2*d-.5); ax.set_ylim(-.5, 2*d-.5); ax.set_aspect('equal'); ax.plot([d-.5]*2, [-.5, 2*d-.5], 'k:', lw=.8); ax.plot([-.5, 2*d-.5], [d-.5]*2, 'k:', lw=.8)
    ax.set_title('d=13, s=%d: (u,v)=Q-(d,d).  grey: solved by G7-T1 (max Q>=2d); green: small box with a square cell;\norange: squareless (v<m_s(u), G8-S); black: hollow box. All coloured small boxes CHECKED covered.' % s, fontsize=7)
fig.savefig(os.path.join(FIG, 'fig1_small_region.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 2 boundary-adjacent cell geometry, filling cells
d, s = 7, 3; fig, axs = plt.subplots(1, 2, figsize=(10, 5))
for ax, Q in zip(axs, ((7, 8), (8, 7))):
    fc = H.filling_cells(d, s); hl = [(c, '#fb6a4a' if ti == 0 else '#74c476') for nm, (c, ti, q) in fc.items() if q == Q]
    draw(ax, d, s, Q, allc(d, s, Q), hl); ax.set_title('Q=%s: filling cells (red fills T1, green fills T2), d=7 s=3' % (Q,), fontsize=8)
fig.savefig(os.path.join(FIG, 'fig2_boundary_cells.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 3 squareless interior case with cover
found = None
for d in range(9, 14):
    for s in SB.units(d):
        for u in range(1, d):
            for v in range(1, d):
                Q = (d+u, d+v)
                if SB.squareless(d, s, Q) and u >= 2 and v >= 2 and found is None: found = (d, s, Q)
d, s, Q = found; cert, _ = CCv.cover_certificate(d, s, Q); cells = [tuple(map(tuple, x)) for x in cert['cells']]
fig, ax = plt.subplots(figsize=(6, 6)); draw(ax, d, s, Q, cells)
for pc in cert['pieces']: ax.add_patch(Polygon([(float(__import__('fractions').Fraction(x)), float(__import__('fractions').Fraction(y))) for x, y in pc['poly']], closed=True, fill=False, ec='b', lw=.5))
ax.set_title('Squareless interior box d=%d s=%d Q=%s: certified subdivision (blue pieces) of conv(F) inside %d cells' % (d, s, Q, len(cells)), fontsize=7)
fig.savefig(os.path.join(FIG, 'fig3_squareless_cover.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 4 two-hole geometry
d, s = 11, 4; Q = (d, d); fig, ax = plt.subplots(figsize=(6.5, 6.5)); draw(ax, d, s, Q, allc(d, s, Q))
for tri, col in zip(H.hollow_triangles(d, s), ('#fb6a4a', '#74c476')): ax.add_patch(Polygon(tri, closed=True, fc=col, ec='k', alpha=.8))
ax.set_title('Hollow box d=11 s=4: T1 (red), T2 (green) enclosed by Graver edges; area d/2 each', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig4_two_holes.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 5 hole filling under enlargement + beta1 sequences
fig, axs = plt.subplots(1, 4, figsize=(16, 4.6)); d, s = 7, 3
for ax, Q in zip(axs[:3], ((7, 7), (7, 8), (8, 7))):
    draw(ax, d, s, Q, allc(d, s, Q)); b = U_betti(Lat(d, d, d, s), Q)[0]; ax.set_title('Q=%s  Betti=%s' % (Q, list(b)), fontsize=8)
    for p in (C.uncovered(Lat(d, d, d, s), Q) or []): ax.add_patch(Polygon([(float(x), float(y)) for x, y in p], closed=True, fc='r', alpha=.6))
for s2 in (3, 6):
    seq = [U_betti(Lat(7, 7, 7, s2), (7, h))[0][1] for h in range(7, 15)]; axs[3].plot(range(7, 15), seq, 'o-', label='d=7 s=%d' % s2)
axs[3].set_xlabel('h  (Q=(7,h))'); axs[3].set_ylabel('beta_1'); axs[3].legend(); axs[3].set_title('beta_1 along Q=(d,h); holes die at h=d+1', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig5_hole_filling.png'), dpi=130, bbox_inches='tight'); plt.close(fig)

# 6 binary collisions
sig = [2, 3, 4, 5]; fig, axs = plt.subplots(1, 2, figsize=(10, 4))
pts = {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1)}
for m in ([(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)]):
    for a, b in m: axs[0].plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], lw=3, alpha=.6)
for i, p in pts.items(): axs[0].scatter(*p, s=300, fc='w', ec='k', zorder=3); axs[0].annotate('class %d' % i, p, ha='center', va='center', fontsize=6)
axs[0].set_title('ILLUSTRATIVE: the 3 pairings of the 4 series classes of the nullity-3 minimal box; any two collide (common centre)', fontsize=7); axs[0].axis('off')
tot = {}
for comp in ([1, 1, 1, 1], [2, 1, 1, 1], [2, 2, 1, 1], [3, 1, 1, 1], [2, 2, 2, 1]):
    cols = BM.blowup_parity_columns(sig, comp); n = len(cols)
    ranks = [RR.witness_rank(n, a, b)[0] for cen, a, b in CC.collisions(cols)]; tot[str(comp)] = (len(ranks), min(ranks))
axs[1].bar(list(tot), [v[0] for v in tot.values()]); axs[1].set_ylabel('# collisions'); axs[1].set_xlabel('class sizes (blow-up)')
for i, v in enumerate(tot.values()): axs[1].annotate('min rank %d' % v[1], (i, v[0]), ha='center', va='bottom', fontsize=7)
axs[1].set_title('collisions of blow-ups (exact); minimum witness rank stays 3 (B-SERIES)', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig6_binary_collisions.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 7 min rank & essential support
ns = list(range(4, 10)); R = [json.load(open(os.path.join(DATA, 'v8_rank_n%d.json' % n))) for n in ns]
fig, axs = plt.subplots(1, 2, figsize=(11, 4))
axs[0].bar([str(n) for n in ns], [r['minimal_representatives'] for r in R], color='#6baed6'); axs[0].set_yscale('log'); axs[0].set_xlabel('n'); axs[0].set_ylabel('minimal boxes tested (basis+extras reps)')
for i, r in enumerate(R): axs[0].annotate('min rank %s' % list(r['min_rank_histogram'])[0], (i, r['minimal_representatives']), ha='center', va='bottom', fontsize=7)
axs[0].set_title('complete censuses n=4..9: every minimal box has minimum witness rank 3', fontsize=8)
axs[1].plot(ns, [r['distinct_code_invariant_classes'] for r in R], 'o-', label='all minimal classes (census)')
cls = {k: BM.classify_nullity(k) for k in (3, 4)}
import itertools
sys.path.insert(0, os.path.join(ROOT, 'tests')); sys.path.insert(0, os.path.join(ROOT, 'experiments'))
from check_nullity_classification import path1
axs[1].plot(ns, [len(path1(3, n, cls) | path1(4, n, cls)) for n in ns], 's--', label='explained by nullity 3,4 classification')
axs[1].set_xlabel('n'); axs[1].legend(); axs[1].set_title('code-invariant classes: nullity<=4 theorem vs census (rest: nullity>=5, OPEN)', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig7_min_rank_support.png'), dpi=140, bbox_inches='tight'); plt.close(fig)
print('figures done')
