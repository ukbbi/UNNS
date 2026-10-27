#!/usr/bin/env python3
"""GEO-I v003 figures (matplotlib).  All geometry is recomputed exactly by the library; floats are used for drawing only."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d in ('geometry', 'topology', 'frozen', 'experiments'): sys.path.insert(0, os.path.join(ROOT, d))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from fractions import Fraction as Fr
import intersections as X
from realization import fibre_complex, fibre_complex_data, cover_cells
from validation import edge_level_audit
from subdivision import planar_subdivision, planar_cells_for_homology
from chain_complex import betti
import high_dimensional as HD
import benchmarks as B
OUT = os.path.join(ROOT, 'figures'); DATA = os.path.join(ROOT, 'output', 'data')
C = {'edge': '#3b6ea8', 'cross': '#c0392b', 'occ': '#1f2d3d', 'aux': '#e69f00', 'cell': '#9fc5e8', 'abs': '#c0392b', 'U': '#2a7f62'}
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 130})

def fl(p): return tuple(float(c) for c in p)

def fig1():
    fc = fibre_complex(Fr(82944, 5)); F = fc['F']
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for (u, gens) in fc['cells'][2]:
        v = [u, X.add(u, gens[0]), X.add(X.add(u, gens[0]), gens[1]), X.add(u, gens[1])]
        ax.add_patch(Polygon([fl(p) for p in v], closed=True, fc=C['cell'], ec='none', alpha=.35, zorder=1))
    for (u, (g,)) in fc['cells'][1]:
        v = X.add(u, g); crossing = {(u, v), (v, u)} & {((1, 1), (5, 1)), ((2, 2), (4, 0)), ((5, 1), (1, 1)), ((4, 0), (2, 2))}
        ax.plot([u[0], v[0]], [u[1], v[1]], color=C['cross'] if crossing else C['edge'], lw=2.4 if crossing else 1.2, zorder=2, alpha=1 if crossing else .8)
    for p in F: ax.plot(*p, 'o', color=C['occ'], ms=7, zorder=4); ax.annotate('%s' % (p,), p, textcoords='offset points', xytext=(6, 6), fontsize=9)
    ax.plot(3, 1, 'D', color=C['aux'], ms=9, zorder=5, mec='k'); ax.annotate('(3,1): crossing\nnot an occurrence,\nnot in $\\Lambda_5$', (3, 1), textcoords='offset points', xytext=(40, 26), fontsize=9, bbox=dict(fc='white', ec='none', alpha=.85), arrowprops=dict(arrowstyle='-', color='gray'))
    ax.set_xlim(0.4, 5.8); ax.set_ylim(-0.6, 2.7); ax.set_aspect('equal'); ax.set_xlabel('exponent of 2'); ax.set_ylabel('exponent of 3')
    ax.set_title('Figure 1.  $x = 82944/5 = 2^{10}3^4/5$: two Graver edges cross\nat a non-occurrence point', fontsize=9.5)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig1_crossing_witness.png')); plt.close(fig)

def fig2():
    fc = fibre_complex(Fr(82944, 5)); cov = cover_cells(fc['cells']); allc = [c for d in fc['cells'] for c in d]
    sub = planar_subdivision(cov, fc['F'], refine=allc)
    V = sub['vertices']; fig, axs = plt.subplots(1, 2, figsize=(10.4, 4.0))
    ax = axs[0]
    for (u, (g,)) in fc['cells'][1]:
        v = X.add(u, g); ax.plot([u[0], v[0]], [u[1], v[1]], color=C['abs'], lw=1.4)
    for p in fc['F']: ax.plot(*p, 'o', color=C['occ'], ms=6)
    ax.set_title('$K_{abs}$: 4 vertices, 6 edges, 1 square\nBetti $(1,2,0)$ -- the two crossing edges are not joined', fontsize=9.5)
    ax = axs[1]
    for f in sub['faces']:
        ax.add_patch(Polygon([fl(v) for v in f], closed=True, fc=C['cell'], ec='none', alpha=.35))
    for (a, b) in sub['edges']: ax.plot([float(a[0]), float(b[0])], [float(a[1]), float(b[1])], color=C['U'], lw=1.4)
    for v in V:
        kind = sub['prov'][v]['kind']
        if kind == 'occurrence': ax.plot(float(v[0]), float(v[1]), 'o', color=C['occ'], ms=6)
        else: ax.plot(float(v[0]), float(v[1]), 'D', color=C['aux'], ms=8, mec='k'); ax.annotate('auxiliary vertex (3,1)\nprovenance: crossing of\n(1,1)-(5,1) and (2,2)-(4,0)', (float(v[0]), float(v[1])), textcoords='offset points', xytext=(8, -36), fontsize=8)
    ax.set_title('$K_{emb}$ (exact subdivision): 5 vertices, 8 edges, 4 triangles\nBetti $(1,0,0)$', fontsize=9.5)
    for ax in axs: ax.set_aspect('equal'); ax.set_xlim(0.4, 5.8); ax.set_ylim(-0.6, 2.7)
    fig.suptitle('Figure 2.  Abstract complex versus exact embedded subdivision (auxiliary vertices are never occurrences)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig2_subdivision.png')); plt.close(fig)

def fig3():
    x, ps = HD.realize((2, 2, 3), (3, 3, 3), 5); fc = fibre_complex(x); ea = edge_level_audit(fc['cells'])
    fig = plt.figure(figsize=(10.4, 4.6)); ax = fig.add_subplot(121, projection='3d')
    cp = set()
    for pr in ea['crossing_pairs']:
        for e in pr: cp.add(tuple(sorted(e)))
    for (u, (g,)) in fc['cells'][1]:
        v = X.add(u, g); key = tuple(sorted((u, v)))
        ax.plot(*zip(u, v), color=C['cross'] if key in cp else C['edge'], lw=2.2 if key in cp else .7, alpha=1 if key in cp else .35)
    P = fc['F']; ax.scatter(*zip(*P), color=C['occ'], s=12)
    for pt in ea['crossing_points']: ax.scatter(*[float(Fr(c)) if isinstance(c, str) else float(c) for c in pt], color=C['aux'], marker='D', s=40, edgecolor='k', zorder=9)
    ax.set_title('$x=%s$, primes %s\n%d occurrences; crossing edges red, crossing points orange' % (x, fc['ps'], len(P)), fontsize=9)
    ax.set_xlabel('e(%d)' % fc['ps'][0]); ax.set_ylabel('e(%d)' % fc['ps'][1]); ax.set_zlabel('e(%d)' % fc['ps'][2])
    ax2 = fig.add_subplot(122, projection='3d')
    fk = fibre_complex_data((3, 5, 7), (3, 3, 2), 8)
    for (u, (g,)) in fk['cells'][1]:
        v = X.add(u, g); ax2.plot(*zip(u, v), color=C['edge'], lw=.8, alpha=.6)
    ax2.scatter(*zip(*fk['F']), color=C['occ'], s=12)
    for (u, gens) in fk['cells'][2]:
        pass
    ax2.set_title('Klein-four class $b=8$, residues $(3,5,7)$, box $(3,3,2)$:\nno edge crossing, yet 2-cells overlap (Graver diagonal $(0,0,2)$)', fontsize=9)
    fig.suptitle('Figure 3.  Three-dimensional obstructions: a genuine 3-D edge crossing, and a cell-only obstruction', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig3_3d_intersections.png')); plt.close(fig)

def fig4():
    rec = json.load(open(os.path.join(ROOT, 'output', 'certificates', 'e10_examples.json'))).get('4D_edge_crossing')
    if not rec: return
    x = Fr(rec['x']); fc = fibre_complex(x); ea = edge_level_audit(fc['cells'])
    prs = sorted(ea['crossing_pairs'], key=lambda p: sorted(p))
    (e1, e2) = sorted(tuple(sorted(e)) for e in prs[0])
    a, a2 = e1; c, c2 = e2; g = X.sub(a2, a); h = X.sub(c2, c)
    # plane through a spanned by g,h : chart p = a + s g + t h
    def chart(p):
        d = [Fr(p[i] - a[i]) for i in range(4)]
        for i in range(4):
            for j in range(i + 1, 4):
                det = g[i] * h[j] - g[j] * h[i]
                if det == 0: continue
                s_ = (d[i] * h[j] - d[j] * h[i]) / det; t_ = (g[i] * d[j] - g[j] * d[i]) / det
                if all(d[k] == s_ * g[k] + t_ * h[k] for k in range(4)): return (s_, t_)
                return None
        return None
    pts = {p: chart(p) for p in fc['F']}; inpl = {p: q for p, q in pts.items() if q is not None}
    levels = sorted({p[3] for p in fc['F']})
    fig = plt.figure(figsize=(11, 4.2)); ax = fig.add_subplot(1, 3, 1)
    for (u, (gg,)) in fc['cells'][1]:
        v = X.add(u, gg)
        if u in inpl and v in inpl:
            key = tuple(sorted((u, v))); ax.plot([float(inpl[u][0]), float(inpl[v][0])], [float(inpl[u][1]), float(inpl[v][1])], color=C['cross'] if key in (e1, e2) else C['edge'], lw=2.4 if key in (e1, e2) else 1)
    for p, q in inpl.items(): ax.plot(float(q[0]), float(q[1]), 'o', color=C['occ'], ms=5)
    ax.set_title('the plane spanned by the crossing pair\n g=%s, h=%s (chart coordinates s,t)' % (g, h), fontsize=8); ax.set_aspect('equal'); ax.set_xlabel('s'); ax.set_ylabel('t')
    for k, lv in enumerate(levels[1:3]):
        ax = fig.add_subplot(1, 3, k + 2, projection='3d'); lv_pts = [p for p in fc['F'] if p[3] == lv]
        for (u, (gg,)) in fc['cells'][1]:
            v = X.add(u, gg)
            if u[3] == lv and v[3] == lv: ax.plot(*zip(u[:3], v[:3]), color=C['edge'], lw=.9)
        if lv_pts: ax.scatter(*zip(*[p[:3] for p in lv_pts]), color=C['occ'], s=12)
        ax.set_title('3-D section $e_4=%d$ (%d occurrences)' % (lv, len(lv_pts)), fontsize=8); ax.tick_params(labelsize=6)
    fig.suptitle('Figure 4.  4-D fibre x = %s (primes %s): the crossing is planar but lives in R^4; sections show how it hides' % (rec['x'], rec['primes']), fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig4_4d_sections.png')); plt.close(fig)

def fig5():
    e2 = B.e2(24); t = [r['t'] for r in e2]
    b2 = [(list(r['betti_abs']) + [0, 0, 0])[2] for r in e2]; b1 = [(list(r['betti_abs']) + [0, 0, 0])[1] for r in e2]
    bu = [(list(r['betti_U']) + [0, 0, 0])[2] for r in e2]
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.step(t, b2, where='post', color=C['abs'], lw=2, label='$\\beta_2(K_{abs})=\\lfloor t/4\\rfloor$ (grows without bound)')
    ax.plot(t, b1, color=C['abs'], ls='--', label='$\\beta_1(K_{abs})=2$'); ax.plot(t, bu, color=C['U'], lw=2, label='$\\beta_2(U_x)=0$ (planar set)')
    ax.set_xlabel('$t$   ($x_t = 2^{10+2t}3^4/5$)'); ax.set_ylabel('Betti number'); ax.legend(fontsize=8, frameon=False)
    ax.set_title('Figure 5.  The abstract $\\beta_2$ is unbounded; the geometric image has none', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig5_x_t_family.png')); plt.close(fig)

def fig6():
    p = os.path.join(DATA, 'e9_orbits.json')
    if not os.path.exists(p): return
    d = json.load(open(p)); names = [k for k in d if k != '_meta']
    fig, axs = plt.subplots(1, len(names[:4]), figsize=(3.4 * len(names[:4]), 3.4), sharey=False)
    if len(names[:4]) == 1: axs = [axs]
    for ax, nm in zip(axs, names[:4]):
        rs = d[nm]; n = [r['n'] for r in rs]
        ax.plot(n, [r['betti_abs_Q'][1] if len(r['betti_abs_Q']) > 1 else 0 for r in rs], color=C['abs'], label='$\\beta_1(K_{abs})$')
        ax.plot(n, [(r['betti_U'][1] if r['betti_U'] and len(r['betti_U']) > 1 else float('nan')) for r in rs], color=C['U'], label='$\\beta_1(U)$')
        ax.set_title(nm.split('[')[0].strip(), fontsize=8); ax.set_xlabel('step $n$')
    axs[0].legend(fontsize=7, frameon=False)
    fig.suptitle('Figure 6.  Collective-orbit states: abstract $\\beta_1$ saturation versus the geometric image', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'fig6_orbit_betti.png')); plt.close(fig)

def fig7():
    import csv
    p = os.path.join(DATA, 'scan_k2.csv')
    if not os.path.exists(p): return
    rows = list(csv.DictReader(open(p))); qs = sorted({int(r['q1']) for r in rows}); mx = max(qs)
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.8))
    for ax, key, ttl in ((axs[0], 'betti_abs', '$\\beta_1(K_{abs})>0$'), (axs[1], 'betti_U', '$\\beta_1(U)>0$')):
        grid = [[0] * mx for _ in range(mx)]; tot = [[0] * mx for _ in range(mx)]
        for r in rows:
            b = [int(v) for v in r[key].split('|')] + [0, 0]
            tot[int(r['q2']) - 1][int(r['q1']) - 1] += 1; grid[int(r['q2']) - 1][int(r['q1']) - 1] += (b[1] > 0)
        frac = [[(grid[i][j] / tot[i][j] if tot[i][j] else 0) for j in range(mx)] for i in range(mx)]
        im = ax.imshow(frac, origin='lower', extent=(.5, mx + .5, .5, mx + .5), cmap='viridis', vmin=0, vmax=1)
        ax.set_xlabel('$q_1$'); ax.set_ylabel('$q_2$'); ax.set_title('fraction of residue classes with ' + ttl, fontsize=9)
    fig.colorbar(im, ax=axs, shrink=.8)
    fig.suptitle('Figure 7.  k=2 scan: abstract $\\beta_1$ is generic, geometric $\\beta_1$ is rare', fontsize=10)
    fig.savefig(os.path.join(OUT, 'fig7_b1_heatmap.png'), bbox_inches='tight'); plt.close(fig)

if __name__ == '__main__':
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        try: f(); print('ok', f.__name__)
        except Exception as e: print('FAILED', f.__name__, repr(e)); raise
