"""GEO-I v009 figures (7), all from exact computed objects."""
import os, sys, json, pickle
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d_))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import coverage as C, modular_layers as ML, small_box as SB, hollow as H, cell_cover as CCv, binary5 as B5
from lattice_model import Lat
FIG = os.path.join(ROOT, 'figures'); DATA = os.path.join(ROOT, 'output', 'data'); os.makedirs(FIG, exist_ok=True)
def cellpoly(c): u, g, h = c; return [u, (u[0]+g[0], u[1]+g[1]), (u[0]+g[0]+h[0], u[1]+g[1]+h[1]), (u[0]+h[0], u[1]+h[1])]
def allc(d, s, Q): return [(u, g, h) for (u, (g, h)) in C.complex_data(Lat(d, d, d, s), Q)['cells'][2]]
def draw(ax, d, s, Q, cells, alpha=.4):
    for c in cells: ax.add_patch(Polygon(cellpoly(c), closed=True, fc='#9ecae1', ec='k', lw=.3, alpha=alpha))
    F = ML.fibre(d, s, Q); ax.scatter([p[0] for p in F], [p[1] for p in F], s=8, c='k', zorder=3)
    ax.add_patch(Polygon(C.hull(sorted(F)), closed=True, fill=False, ec='r', lw=1.1)); ax.set_aspect('equal'); ax.set_xlim(-1, Q[0]+1); ax.set_ylim(-1, Q[1]+1)
def fl(p): return [(float(Fr(x)), float(Fr(y))) for x, y in p]

# 1 exceptional square and both holes
d, s = 11, 3; t = pow(s, -1, d); T = H.hollow_triangles(d, s)
fig, ax = plt.subplots(figsize=(6, 6)); draw(ax, d, s, (d, d), allc(d, s, (d, d)))
for tri, col in zip(T, ('#fb6a4a', '#74c476')): ax.add_patch(Polygon(tri, closed=True, fc=col, ec='k', lw=1, alpha=.8))
ax.set_title('Hollow box d=11 s=3: cells of U (blue), hull H0 (red), holes T1 (red fill), T2 (green fill); t=s^-1=%d' % t, fontsize=8)
fig.savefig(os.path.join(FIG, 'fig1_hollow_holes.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 2 continued-fraction boundary decomposition: sail chain of Gamma_{d,s} for Fibonacci-type pairs
def sail(d, s):
    pts = [(0, d)]; m = d
    for i in range(1, d + 1):
        v = (s * i) % d if i < d else 0
        if v < m: m = v; pts.append((i, v))
    return pts
def cf(a, b):
    q = []
    while b: q.append(a // b); a, b = b, a % b
    return q
fig, axs = plt.subplots(1, 3, figsize=(14, 4.8))
for ax, (d, s) in zip(axs, ((89, 34), (89, 5), (97, 12))):
    S = sail(d, s); F = ML.fibre(d, s, (d, d))
    ax.scatter([p[0] for p in F], [p[1] for p in F], s=3, c='#bbb'); ax.plot([p[0] for p in S], [p[1] for p in S], 'r.-', lw=1.2, ms=5)
    for a, b in zip(S, S[1:]): ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-', color='r'))
    ax.set_aspect('equal'); ax.set_title('d=%d s=%d: sail A->B (%d vertices), d/s=%s' % (d, s, len(S), cf(d, s)), fontsize=8)
fig.savefig(os.path.join(FIG, 'fig2_cf_boundary.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 3 local hole exclusion: the exact uncovered region of the hollow box is T1 u T2 (no counterexample)
fig, axs = plt.subplots(1, 3, figsize=(14, 4.8))
for ax, (d, s) in zip(axs, ((13, 5), (16, 3), (21, 8))):
    pcs = C.uncovered(Lat(d, d, d, s), (d, d)); draw(ax, d, s, (d, d), allc(d, s, (d, d)), alpha=.25)
    for p in pcs: ax.add_patch(Polygon(fl(p), closed=True, fc='#fb6a4a', ec='k', lw=.6, alpha=.8))
    tot = sum(abs(C.area2(p)) for p in pcs); ax.set_title('d=%d s=%d: uncovered area = d (%s = %d), pieces=%d, no further hole' % (d, s, tot / 2, d, len(pcs)), fontsize=7)
fig.savefig(os.path.join(FIG, 'fig3_hole_exclusion.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 4 small-box cap region
d, s, Q = 11, 3, (14, 13); F0 = ML.fibre(d, s, (d, d)); FQ = ML.fibre(d, s, Q)
fig, ax = plt.subplots(figsize=(6.5, 6)); H0 = C.hull(sorted(F0)); HQ = C.hull(sorted(FQ))
ax.add_patch(Polygon(HQ, closed=True, fc='#fdd0a2', ec='b', lw=1.2)); ax.add_patch(Polygon(H0, closed=True, fc='#c7e9c0', ec='r', lw=1.2))
ax.scatter([p[0] for p in FQ], [p[1] for p in FQ], s=8, c='k'); ax.plot([d, d, 0], [0, d, d], 'k:', lw=.8); ax.set_aspect('equal')
ax.set_title('Cap C_Q = H_Q minus H_0 (orange), H_0 (green), Q=%s, d=11 s=3' % (Q,), fontsize=8)
fig.savefig(os.path.join(FIG, 'fig4_cap_region.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 5 squareless vs non-squareless cap coverings (certified)
def find(sq):
    for d in range(7, 14):
        for s in SB.units(d):
            for u in range(1, d):
                for v in range(1, d):
                    if SB.squareless(d, s, (d+u, d+v)) == sq and u >= 2 and v >= 2: return d, s, (d+u, d+v)
fig, axs = plt.subplots(1, 2, figsize=(11, 5.4))
for ax, sq in zip(axs, (True, False)):
    d, s, Q = find(sq); cert, _ = CCv.cover_certificate(d, s, Q); cells = [tuple(map(tuple, x)) for x in cert['cells']]
    draw(ax, d, s, Q, cells)
    for pc in cert['pieces']: ax.add_patch(Polygon(fl(pc['poly']), closed=True, fill=False, ec='b', lw=.5))
    ax.set_title('%s: d=%d s=%d Q=%s, certified cover by %d cells' % ('squareless' if sq else 'non-squareless', d, s, Q, len(cells)), fontsize=8)
fig.savefig(os.path.join(FIG, 'fig5_cap_covers.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 6 nullity-five collision types of the 12 minimal boxes
res = json.load(open(os.path.join(DATA, 'v9_binary5.json'))); rows = []
for n, sig, mr in res:
    C_ = B5.code_masks(sig); col = B5.collisions(C_); typ = {}
    for U, x, S, y, T in col:
        k = (len(S), len(T)); k = tuple(sorted(k)); typ[k] = typ.get(k, 0) + 1
    rows.append((n, typ))
kinds = sorted({k for _, t_ in rows for k in t_}); fig, ax = plt.subplots(figsize=(10, 4.5)); bottom = [0] * len(rows)
for k in kinds:
    vals = [t_.get(k, 0) for _, t_ in rows]; ax.bar(range(len(rows)), vals, bottom=bottom, label='partition sizes %s' % (k,)); bottom = [a + b for a, b in zip(bottom, vals)]
ax.set_xticks(range(len(rows))); ax.set_xticklabels(['p=%d' % n for n, _ in rows], fontsize=7); ax.set_ylabel('shared-centre collisions'); ax.legend(fontsize=7)
ax.set_title('Nullity 5: the 12 minimal boxes, collisions by circuit-partition sizes (r,t)', fontsize=9)
fig.savefig(os.path.join(FIG, 'fig6_nullity5_collisions.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 7 minimum witness rank over ALL non-embedded spanning nullity-5 supports, by support size
r5 = pickle.load(open(os.path.join(DATA, 'v9_orbits_k5.pkl'), 'rb')); hist = {}
for m in sorted(r5):
    for R in r5[m]:
        if B5.rank_of(list(R)) != 5: continue
        C_ = B5.code_masks(list(R))
        if B5.embedded(C_): continue
        rk = B5.min_rank(C_, len(R)); hist.setdefault(m, {}); hist[m][rk] = hist[m].get(rk, 0) + 1
json.dump({str(m): v for m, v in hist.items()}, open(os.path.join(DATA, 'v9_minrank_all_nonembedded_k5.json'), 'w'))
fig, ax = plt.subplots(figsize=(10, 4.5)); ranks = sorted({r for v in hist.values() for r in v})
bottom = [0] * len(hist); xs = sorted(hist)
for rk in ranks:
    vals = [hist[m].get(rk, 0) for m in xs]; ax.bar(xs, vals, bottom=bottom, label='min witness rank %d' % rk); bottom = [a + b for a, b in zip(bottom, vals)]
ax.set_xlabel('support size p (number of coordinates of the reduced box)'); ax.set_ylabel('non-embedded orbits'); ax.legend()
ax.set_title('Nullity 5: minimum witness rank of every non-embedded spanning support (support reduction never raises it)', fontsize=9)
fig.savefig(os.path.join(FIG, 'fig7_minrank_reduction.png'), dpi=140, bbox_inches='tight'); plt.close(fig)
print('7 figures; non-embedded k=5 min-rank histogram', {m: hist[m] for m in sorted(hist)})
