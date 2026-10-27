#!/usr/bin/env python3
"""GEO-I v010 figures (7).  python3 experiments/figures_v10.py"""
import os, sys, json, pickle, itertools
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'theory'))
import binary5 as B5, binary6 as B6
D = os.path.join(ROOT, 'output', 'data'); F = os.path.join(ROOT, 'figures'); os.makedirs(F, exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
BL, OR, GR, RD = '#2a6f97', '#e07a1f', '#4a7c59', '#b23a48'

# fig1: affine orbit counts by size
fig, ax = plt.subplots(figsize=(7.5, 4))
for m, c in ((3, BL), (4, OR), (5, GR)):
    o = pickle.load(open(os.path.join(D, 'v10_affine_orbits_m%d.pkl' % m), 'rb'))
    xs = sorted(o); ax.plot(xs, [len(o[s]) for s in xs], 'o-', ms=3, color=c, label='AG(%d,2): %d orbits (nullity %d)' % (m, sum(len(v) for v in o.values()), m + 1))
ax.set_yscale('log'); ax.set_xlabel('support size p'); ax.set_ylabel('AGL-orbits of subsets'); ax.legend(frameon=False)
ax.set_title('Fig 1. Orbits of subsets of AG(k-1,2) under AGL(k-1,2) (G10-A1 reduction)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig1_affine_orbits.png'), dpi=140); plt.close(fig)

# fig2: classification table k=3..6
rows = []
for k in (3, 4, 5, 6):
    j = json.load(open(os.path.join(D, 'v10_binary%d.json' % k)))
    rows.append((k, j['affine_orbits_nonempty'], j['spanning'], j['non_embedded'], len(j['minimal'])))
fig, ax = plt.subplots(figsize=(7.5, 4)); w = 0.2; ks = [r[0] for r in rows]
for i, (lab, c) in enumerate((('affine orbits', '#999'), ('spanning', BL), ('non-embedded', OR), ('minimal', GR))):
    ax.bar([x + (i - 1.5) * w for x in ks], [r[i + 1] for r in rows], w, label=lab, color=c)
for x, r in zip(ks, rows): ax.text(x + 0.3, r[4] + 3, str(r[4]), color=GR, fontsize=9)
ax.set_yscale('log'); ax.set_xticks(ks); ax.set_xlabel('nullity k'); ax.set_ylabel('classes'); ax.legend(frameon=False)
ax.set_title('Fig 2. Exhaustive classification, nullity 3-6 (all minimal classes: r_min = 3)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig2_classification.png'), dpi=140); plt.close(fig)

# fig3: nullity 6 minimal classes: size and number of two-blocks
j6 = json.load(open(os.path.join(D, 'v10_binary6.json')))
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.scatter([m['p'] for m in j6['minimal']], [m['two_circuit_partitions_of_1'] for m in j6['minimal']], s=14, color=BL, alpha=.7)
ax.axhline(2 ** 4, color=RD, ls='--', lw=1); ax.text(10.2, 2 ** 4 + 1.5, '2^(k-2) = 16 (K_{2,5})', color=RD)
ax.axhline(2, color='#555', ls=':', lw=1); ax.text(10.2, 3, 'W2 threshold: 2', color='#555')
ax.set_xlabel('support size p'); ax.set_ylabel('two-circuit partitions of the all-ones word')
ax.set_title('Fig 3. 215 minimal classes of nullity 6: every one has W2 (>= 16 two-blocks)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig3_nullity6_blocks.png'), dpi=140); plt.close(fig)

# fig4: minimum number of two-blocks vs k
mins = {}
for k in (3, 4, 5, 6):
    j = json.load(open(os.path.join(D, 'v10_binary%d.json' % k))); mins[k] = min(m['two_circuit_partitions_of_1'] for m in j['minimal'])
k2t = json.load(open(os.path.join(D, 'v10_k2t.json')))
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.plot(list(mins), list(mins.values()), 'o', color=BL, ms=7, label='minimum over ALL minimal classes (exhaustive)')
ax.plot([r['nullity'] for r in k2t], [r['two_blocks'] for r in k2t], 's-', color=OR, ms=4, label='cut space of K_{2,t}  (= 2^(k-2) for t >= 3)')
ax.set_yscale('log', base=2); ax.set_xlabel('nullity k'); ax.set_ylabel('two-blocks'); ax.legend(frameon=False)
ax.set_title('Fig 4. Number of two-circuit partitions of 1: extremal family'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig4_two_blocks_vs_k.png'), dpi=140); plt.close(fig)

# fig5: K_{2,4} drawing with one 2-block
fig, ax = plt.subplots(figsize=(7.5, 4)); t = 4
X = (0, 1); Y = (0, -1); Z = [(i - (t - 1) / 2, 0) for i in range(t)]
I = {0, 2}
for i, z in enumerate(Z):
    ax.plot([X[0], z[0]], [X[1] * 1.6 - 0.0, z[1]], color=(RD if i in I else BL), lw=2.5)
    ax.plot([Y[0], z[0]], [Y[1] * 1.6, z[1]], color=(BL if i in I else RD), lw=2.5)
ax.scatter([X[0], Y[0]], [1.6, -1.6], s=160, color='k', zorder=3); ax.scatter([z[0] for z in Z], [0] * t, s=110, color='#ddd', edgecolor='k', zorder=3)
ax.text(0.2, 1.45, 'x'); ax.text(0.2, -1.8, 'y'); ax.set_ylim(-2.1, 2.1)
ax.set_axis_off(); ax.set_title('Fig 5. K_{2,4}: edge set = two bonds w_I (red) + w_{I^c} (blue); 2^(t-1) such pairs')
fig.tight_layout(); fig.savefig(os.path.join(F, 'fig5_k2t_blocks.png'), dpi=140); plt.close(fig)

# fig6: rigidity / counting identity
xs, ys = [], []
for m in j6['minimal']:
    sig = m['support']; C = B5.code_masks(sig); n = len(sig); cnt, tot = B6.decomposition_profile(C, n)
    xs.append(len(C) - 2 + cnt.get((1 << n) - 1, 0)); ys.append(tot)
fig, ax = plt.subplots(figsize=(5.5, 5)); ax.scatter(xs, ys, s=16, color=GR); lim = [min(xs) - 5, max(xs) + 5]; ax.plot(lim, lim, color='#999', lw=1)
ax.set_xlabel('2^k - 2 + |blocks|  (prediction)'); ax.set_ylabel('number of non-empty disjoint circuit families (computed)')
ax.set_title('Fig 6. Counting identity, 215 classes (rigidity)'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig6_counting_identity.png'), dpi=140); plt.close(fig)

# fig7: planar transfer rules
sa = json.load(open(os.path.join(D, 'v10_sail_attack.json')))
fig, ax = plt.subplots(figsize=(7.5, 4)); names = ['R-SYM', 'R-MIR', 'R-LAT', 'R-EUC']
vals = [sa['rules'][n]['n_counterexamples'] if 'n_counterexamples' in sa['rules'][n] else len(sa['rules'][n]['counterexamples']) for n in names]
ax.bar(names, vals, color=[GR if sa['rules'][n]['holds'] else RD for n in names])
for i, v in enumerate(vals): ax.text(i, v + 1, str(v) if v else 'holds', ha='center')
ax.set_ylabel('counterexamples (%d pairs (d,s), d <= %d;\nR-EUC: first-quotient classes)' % (sa['pairs'], sa['dmax']))
ax.set_title('Fig 7. Candidate Euclidean transfer rules: only the symmetry rule survives'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig7_transfer_rules.png'), dpi=140); plt.close(fig)
# fig8: explicit covers G10-S1 / G10-S2
import modular_sail as MS
from matplotlib.patches import Polygon
fig, axs = plt.subplots(1, 2, figsize=(11, 5.2))
for ax, (d, s) in zip(axs, ((13, 3), (14, 3))):
    name, cells, tr = MS.sail_cover(d, s); H = MS.hull(MS.fibre(d, s))
    ax.add_patch(Polygon(H, closed=True, fill=False, ec='#444', lw=1.2))
    cols = ['#2a6f97', '#4a7c59', '#e07a1f', '#7b5ea7', '#999']
    for i, c in enumerate(cells): ax.add_patch(Polygon(MS.corners(c), closed=True, fc=cols[i % 5], alpha=0.35, ec=cols[i % 5], lw=1))
    for T in MS.hollow_triangles(d, s): ax.add_patch(Polygon(T, closed=True, fc=RD, alpha=0.55, ec=RD))
    Fp = MS.fibre(d, s); ax.scatter([p[0] for p in Fp], [p[1] for p in Fp], s=9, color='k', zorder=3)
    ax.set_xlim(-1, d + 1); ax.set_ylim(-1, d + 1); ax.set_aspect('equal'); ax.set_title('(d,s)=(%d,%d), family %s: %d cells; holes T1, T2 in red' % (d, s, name, len(cells)), fontsize=10)
fig.suptitle('Fig 8. Explicit modular-sail covers: conv(F) minus (T1 u T2) lies in the union of the shaded Graver cells'); fig.tight_layout(); fig.savefig(os.path.join(F, 'fig8_sail_covers.png'), dpi=140); plt.close(fig)
print('ok', sorted(os.listdir(F)))
