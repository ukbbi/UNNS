"""GEO-I v007 figures (7 themes).  Illustrative figures are labelled ILLUSTRATIVE in the title; all others plot computed objects."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(ROOT, d_))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import corner_sail as CS, modular_layers as ML, coverage_lemmas as CL, hollow_geometry as HG, coverage as C
FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True)
COL = {'S': '#9ecae1', 'M': '#fdae6b', 'L': '#a1d99b', 'Up': '#bcbddc'}


def draw_cells(ax, d, s, Q, cells, tags=None, alpha=.55):
    for k, (u, g, h) in enumerate(cells):
        cp = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
        ax.add_patch(Polygon(cp, closed=True, fc=COL[tags[k][0]] if tags else '#cccccc', ec='k', lw=.4, alpha=alpha))
    F = ML.fibre(d, s, Q); ax.scatter([p[0] for p in F], [p[1] for p in F], s=10, c='k', zorder=3)
    hl = C.hull(sorted(F)); ax.add_patch(Polygon(hl, closed=True, fill=False, ec='r', lw=1.2))
    ax.set_aspect('equal'); ax.set_xlim(-1, Q[0] + 1); ax.set_ylim(-1, Q[1] + 1)


# 1 column-strip coverage
d, s, Q = 7, 3, (11, 16); cells, tags = CS.strip_cells(d, s, Q)
fig, ax = plt.subplots(figsize=(6, 7)); draw_cells(ax, d, s, Q, cells, tags)
ax.set_title('Fig 1. Theorem A-COL: column-strip cover of conv(F)\n(d,s,Q)=(7,3,(11,16)); S strips, M mismatch, L/Up slivers; red = conv(F)', fontsize=9)
for t, c in COL.items(): ax.plot([], [], 's', c=c, label=t)
ax.legend(loc='lower right', fontsize=7); fig.savefig(os.path.join(FIG, 'fig1_corner_sail_coverage.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 2 HYP-LL failure
ex = None
for d in range(5, 9):
    for s in CL.units(d):
        for Q in ((d, d + 2), (d + 2, d), (d, 2 * d)):
            f = CL.hypll_step_failures(d, s, Q)
            if f and ex is None: ex = (d, s, Q, f)
d, s, Q, f = ex
fig, ax = plt.subplots(figsize=(6, 6)); F = ML.fibre(d, s, Q)
ax.scatter([p[0] for p in F], [p[1] for p in F], s=14, c='k'); ax.add_patch(Polygon(C.hull(sorted(F)), closed=True, fill=False, ec='r'))
for corner, pa, pb in f:
    ax.plot([pa[0], pb[0]], [pa[1], pb[1]], 'b-', lw=2)
    for h in ((0, d), (d, 0), (0, -d), (-d, 0)):
        ax.plot([pa[0], pa[0] + h[0]], [pa[1], pa[1] + h[1]], ':', c='gray', lw=.8)
ax.set_xlim(-1, Q[0] + 1); ax.set_ylim(-1, Q[1] + 1); ax.plot([0,Q[0],Q[0],0,0],[0,0,Q[1],Q[1],0],'g--',lw=.8); ax.set_aspect('equal'); ax.set_title('Fig 2. HYP-LL failure: sail step (blue) with no legitimate completion\n(d,s,Q)=%s ; completions (+-d,0),(0,+-d) leave the box (dotted)' % ((d, s, Q),), fontsize=8)
fig.savefig(os.path.join(FIG, 'fig2_hypll_failure.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 3 local mechanism
d, s, Q = 7, 3, (11, 16); col = CS.columns(d, s, Q); fig, ax = plt.subplots(figsize=(6, 7))
cells, tags = CS.strip_cells(d, s, Q); sub = [(c, t) for c, t in zip(cells, tags) if t[0] in ('S', 'M') and t[1] in (2, 3, 4)]
draw_cells(ax, d, s, Q, [c for c, t in sub], [t for c, t in sub], alpha=.8)
for i, (b, K_, B_, T_) in col.items(): ax.annotate('b=%d,K=%d' % (b, K_), (i, -.6), fontsize=5, rotation=90, ha='center')
ax.set_title('Fig 3. The local mechanism (columns 2-5): consecutive columns differ by (1,s) or (1,s-d); strips\nhave height d; at a top mismatch K_i != K_(i+1) the M-cell closes the gap', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig3_local_mechanism.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 4 binary circuits & shared centre (ILLUSTRATIVE schematic of parity 4)
fig, axs = plt.subplots(1, 3, figsize=(9, 3.2)); pts = {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1)}
for ax, m in zip(axs, ([(1, 2), (3, 4)], [(1, 3), (2, 4)], [(1, 4), (2, 3)])):
    for i, p in pts.items(): ax.scatter(*p, s=300, fc='w', ec='k', zorder=3); ax.annotate(str(i), p, ha='center', va='center')
    for a, b in m: ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]], lw=4)
    ax.scatter(.5, .5, marker='*', s=200, c='r', zorder=4); ax.set_xlim(-.4, 1.4); ax.set_ylim(-.4, 1.4); ax.axis('off'); ax.set_aspect('equal')
    ax.set_title('partition into circuits %s' % (m,), fontsize=7)
fig.suptitle('Fig 4 (ILLUSTRATIVE). Parity-4: three square cells (circuit pairs) share the centre 1/2 (red star) => the 3 witnesses; rank 3', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig4_binary_circuits_centres.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 5 min rank vs dimension
fig, ax = plt.subplots(figsize=(6, 4)); ns = [4, 5, 6, 7, 8]; mins = []; cnt = []; comp = []
for n in ns:
    j = json.load(open(os.path.join(ROOT, 'output', 'data', 'v7_rank_n%d.json' % n)))
    mins.append(min(int(k) for k in j['minimal_boxes_by_min_rank'])); cnt.append(sum(j['minimal_boxes_by_min_rank'].values())); comp.append(n < 8)
ax.bar([str(n) + ('' if c else '*') for n, c in zip(ns, comp)], cnt, color=['#3182bd' if c else '#bdbdbd' for c in comp]); ax.set_yscale('log')
for i, (n, m, c) in enumerate(zip(ns, mins, cnt)): ax.annotate('min rank %d' % m, (i, c), ha='center', va='bottom', fontsize=8)
ax.set_xlabel('number of coordinates n  (n<=6 complete (v006 data), n=7 complete under FS, * n=8 restricted, grey)'); ax.set_ylabel('# minimal non-embedded boxes (log)')
ax.set_title('Fig 5. Minimum witness rank of every minimal box found is 3 (census n=4..8)', fontsize=9)
fig.savefig(os.path.join(FIG, 'fig5_min_rank_vs_dimension.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 6 hollow box triangles
d, s = 7, 3; t = HG.inv(s, d); F = HG.fibre_hollow(d, s); fig, ax = plt.subplots(figsize=(6, 6))
A, B_, Cc = (0, d), (d, 0), (d, d); T1 = [A, (d - t, d - 1), Cc]; T2 = [B_, (d - 1, d - s), Cc]
import itertools
for p, q in itertools.combinations(F, 2):
    if HG.is_graver(d, s, (q[0] - p[0], q[1] - p[1])): ax.plot([p[0], q[0]], [p[1], q[1]], '-', c='gray', lw=.7)
ax.add_patch(Polygon(T1, fc='#fc9272', alpha=.8)); ax.add_patch(Polygon(T2, fc='#9ecae1', alpha=.8))
ax.scatter([p[0] for p in F], [p[1] for p in F], c='k', s=14, zorder=3); ax.set_aspect('equal')
ax.set_title('Fig 6. Hollow box (d,s)=(7,3), Q=(d,d): U (grey 1-cells; no 2-cell here)\nT1, T2 are bounded complement components, area d/2 each => beta_1 >= 2', fontsize=8)
fig.savefig(os.path.join(FIG, 'fig6_hollow_triangles.png'), dpi=140, bbox_inches='tight'); plt.close(fig)

# 7 finite evidence vs proved families (ILLUSTRATIVE layout of ranges)
fig, ax = plt.subplots(figsize=(8, 3.6)); rows = [('A-COL: max(Q)>=2d, all d, all units (PROVED)', 100, '#31a354'), ('machine check of A-COL (d<=12)', 12, '#a1d99b'),
        ('G7-C1 window (v006, d<=30)', 30, '#fdae6b'), ('squareless zone (v007, d<=24)', 24, '#fdae6b'), ('hollow lower bound certificates (d<=64)', 64, '#9ecae1')]
for i, (lab, v, c) in enumerate(rows): ax.barh(i, v, color=c)
ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows], fontsize=7); ax.invert_yaxis(); ax.set_xlabel('modulus d  (green bar of the proved theorem is unbounded: truncated at 100 for display)')
ax.set_title('Fig 7 (ILLUSTRATIVE). Proved infinite family vs finite exact evidence', fontsize=9)
fig.savefig(os.path.join(FIG, 'fig7_evidence_vs_proof.png'), dpi=140, bbox_inches='tight'); plt.close(fig)
print(sorted(os.listdir(FIG)))
