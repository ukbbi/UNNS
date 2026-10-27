"""GEO-I v005 figures, all built from verified/shipped data or exact recomputation (no hand-drawn values).   usage: figures_v5.py"""
import os, sys, json, itertools
from math import gcd
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from pure_lattice import fibre, inv
from uniform_coverage import proof_cells, layers
from planar_embed import embedded
from lattice_model import Lat, complex_data
import coverage as C

OUT = os.path.join(HERE, '..', 'figures'); DATA = os.path.join(HERE, '..', 'output', 'data'); os.makedirs(OUT, exist_ok=True)
def jl(p): return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
BLUE, ORANGE, GREEN, RED, GREY = '#2a6fb0', '#e08a1e', '#3a9a5b', '#c0392b', '#888888'


def fig_status():
    rows = jl(os.path.join(DATA, 'stabilization_certificates.jsonl')) + jl(os.path.join(DATA, 'stabilization_extended.jsonl'))
    cert = {(r['d'], r['s']) for r in rows if not r['violations'] and r.get('d', 0) > 1}
    for (d, s) in list(cert):
        cert.add((d, inv(s, d)))
    dmax = max(d for d, _ in cert) if cert else 13
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    for d in range(2, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) != 1: continue
            if s in (1, d - 1): c, m = GREEN, 's'
            elif (d, s) in cert: c, m = BLUE, 'o'
            else: c, m = GREY, 'x'
            ax.scatter(d, s / d, c=c, marker=m, s=26)
    ax.scatter([], [], c=GREEN, marker='s', label='s = ±1: PROVED for every d (layer construction)')
    ax.scatter([], [], c=BLUE, marker='o', label='other s: exact base-window certificate (+ translation lemma S4)')
    ax.set_xlabel('d'); ax.set_ylabel('s / d'); ax.set_title('G5-C1  uniform planar stabilization:  U = conv(F) for all Q ≥ (d,d), Q ≠ (d,d)')
    ax.legend(loc='lower right', fontsize=8); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig1_stabilization_status.png'), dpi=150); plt.close(fig)


def _draw_cells(ax, d, s, Q, cells, hull=True, alpha=.18, lw=.6):
    F = fibre(d, s, Q)
    for (u, g, h) in cells:
        P = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
        ax.add_patch(Polygon(P, closed=True, fc=BLUE, ec=BLUE, alpha=alpha, lw=lw))
    if hull:
        H = C.hull(F); H = H + [H[0]]; ax.plot([p[0] for p in H], [p[1] for p in H], c=RED, lw=1.3)
    ax.scatter([p[0] for p in F], [p[1] for p in F], c='k', s=7, zorder=3)
    ax.set_aspect('equal'); ax.set_xlim(-.5, Q[0] + .5); ax.set_ylim(-.5, Q[1] + .5); ax.set_xticks([]); ax.set_yticks([])


def fig_layers():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.6))
    for ax, (d, s, Q) in zip(axs, ((5, -1, (8, 7)), (5, 1, (9, 8)), (5, -1, (10, 5)))):
        cells, _ = proof_cells(d, s, Q); _draw_cells(ax, d, s, Q, cells)
        ax.set_title('d=%d, s=%+d, Q=%s: %d proof cells cover conv(F) (red)' % (d, s, Q, len(cells)), fontsize=9)
    fig.suptitle('Layer construction (proof of G5-C1 for s = ±1): only the cells built by the proof are drawn', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig2_layer_construction.png'), dpi=150); plt.close(fig)


def fig_hollow():
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.6))
    for ax, (d, s) in zip(axs, ((6, 1), (6, 5), (7, 2))):
        L = Lat(d, d, d, s); cd = complex_data(L, (d, d)); F = cd['F']
        for (u, (g, h)) in (cd['cells'][2] if len(cd['cells']) > 2 else []):
            P = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
            ax.add_patch(Polygon(P, closed=True, fc=BLUE, ec=BLUE, alpha=.12, lw=.5))
        for (u, (g,)) in cd['cells'][1]:
            ax.plot([u[0], u[0] + g[0]], [u[1], u[1] + g[1]], c=GREEN, lw=.8)
        H = C.hull(F); H = H + [H[0]]; ax.plot([p[0] for p in H], [p[1] for p in H], c=RED, lw=1.2)
        ax.scatter([p[0] for p in F], [p[1] for p in F], c='k', s=10, zorder=3)
        ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        ax.set_title('hollow box (d,d)=(%d,%d), s=%d:  β1 = %d' % (d, d, s, d if (s + 1) % d == 0 else 2), fontsize=9)
    fig.suptitle('G5-C2  hollow box: blue = 2-cells, green = 1-cells, red = conv(F).  s=+1: one parallelogram + three arcs;  s=−1: fan graph', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig3_hollow_box.png'), dpi=150); plt.close(fig)


def fig_antichains():
    d = 6; fig, axs = plt.subplots(1, 2, figsize=(11, 5))
    for ax, s, name in ((axs[0], d - 1, 'G5-T3  s = −1'), (axs[1], 1, 'G5-T4  s = +1')):
        for q1 in range(1, 2 * d + 3):
            for q2 in range(1, 2 * d + 3):
                e = embedded(d, s, (q1, q2)); ax.scatter(q1, q2, c=(GREEN if e else RED), s=28, marker='s')
        mins = [(i, 2 * d + 1 - i) for i in range(1, 2 * d + 1)] if s != 1 else [(1, 2 * d), (2, d + 1), (d, d), (d + 1, 2), (2 * d, 1)]
        ax.scatter([m[0] for m in mins], [m[1] for m in mins], facecolors='none', edgecolors='k', s=120, lw=1.6, label='proved minimal obstruction boxes')
        ax.set_title('%s, d=%d (exact test per box; green embedded, red not)' % (name, d), fontsize=9); ax.set_xlabel('Q1'); ax.set_ylabel('Q2'); ax.legend(fontsize=8); ax.set_aspect('equal')
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig4_s_pm1_antichains.png'), dpi=150); plt.close(fig)


def fig_parity():
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    pts = {(1, 1, 0, 0): 'a', (0, 0, 1, 1): 'a', (1, 0, 1, 0): 'b', (0, 1, 0, 1): 'b', (1, 0, 0, 1): 'c', (0, 1, 1, 0): 'c'}
    # orthonormal basis of the hyperplane sum x = 2 in R^4 (all weight-2 points lie in it): project to R^3
    B = np.array([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]], float); B = B / np.linalg.norm(B, axis=1)[:, None]
    P = {p: B @ (np.array(p) - 0.5) for p in pts}
    sq = [[(0, 0, 1, 1), (0, 1, 0, 1), (1, 1, 0, 0), (1, 0, 1, 0)], [(0, 0, 1, 1), (0, 1, 1, 0), (1, 1, 0, 0), (1, 0, 0, 1)], [(0, 1, 0, 1), (0, 1, 1, 0), (1, 0, 1, 0), (1, 0, 0, 1)]]
    cols = [BLUE, ORANGE, GREEN]
    fig = plt.figure(figsize=(7, 6)); ax = fig.add_subplot(111, projection='3d')
    for s_, c in zip(sq, cols):
        ax.add_collection3d(Poly3DCollection([[P[p] for p in s_]], facecolor=c, edgecolor=c, alpha=.35))
    for p, v in P.items(): ax.scatter(*v, c='k', s=25)
    for a, b in (((0, 0, 1, 1), (1, 1, 0, 0)), ((0, 1, 0, 1), (1, 0, 1, 0)), ((0, 1, 1, 0), (1, 0, 0, 1))):
        ax.plot(*zip(P[a], P[b]), c='k', lw=2)
    ax.set_title('4D parity lattice, box (1,1,1,1): three 2-cells (squares) pairwise meet along an axis\n(not an edge of the complex): d_span = 3, support = 4, essential', fontsize=9)
    ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig5_parity4_octahedron.png'), dpi=150); plt.close(fig)


def fig_support_span():
    import collections
    pairs3 = collections.Counter(); pairs4 = collections.Counter()
    for fn, cnt in (('span_search_k3.jsonl', pairs3), ('span_search_k4.jsonl', pairs4)):
        for r in jl(os.path.join(DATA, fn)):
            for b in r.get('minimal_boxes', []): cnt[(b['min_support'], b['min_span'])] += 1
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, cnt, k in ((axs[0], pairs3, 3), (axs[1], pairs4, 4)):
        for (sup, sp), n in cnt.items():
            ax.scatter(sup, sp, s=60 + 12 * np.sqrt(n), c=(RED if sp >= 3 else BLUE), alpha=.7); ax.annotate(str(n), (sup, sp), ha='center', va='center', fontsize=8, color='w')
        ax.set_xlim(1.4, 4.6); ax.set_ylim(1.4, 4.6); ax.set_xticks([2, 3, 4]); ax.set_yticks([2, 3, 4]); ax.grid(alpha=.3)
        ax.set_xlabel('d_support of the smallest witness'); ax.set_ylabel('min d_span over witnesses of the box')
        ax.set_title('k=%d: minimal obstruction boxes (all non-direct lattice classes searched)' % k, fontsize=9)
    fig.suptitle('Support dimension and span dimension are independent; red = weak G5-C3 fails (min span ≥ 3)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig6_support_vs_span.png'), dpi=150); plt.close(fig)


def fig_irreducible():
    rows = jl(os.path.join(DATA, 'irreducible_stats.json')) if False else (json.load(open(os.path.join(DATA, 'irreducible_stats.json'))) if os.path.exists(os.path.join(DATA, 'irreducible_stats.json')) else [])
    if not rows: return
    fig, ax = plt.subplots(figsize=(9, 4.4)); w = .2
    for i, sp in enumerate(('2', '3', '4')):
        ax.bar(np.arange(len(rows)) + (i - 1) * w, [r['irr_span'].get(sp, 0) for r in rows], w, label='d_span = %s' % sp, color=[BLUE, ORANGE, RED][i])
    ax.set_xticks(range(len(rows))); ax.set_xticklabels(['%s\n%s' % (r['case'], tuple(r['box'])) for r in rows], fontsize=7); ax.set_yscale('symlog')
    ax.set_ylabel('# irreducible witnesses'); ax.legend(); ax.set_title('G5-C4 refuted: irreducible witnesses with d_span 3 and 4 exist', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'v5_fig7_irreducible_spans.png'), dpi=150); plt.close(fig)


if __name__ == '__main__':
    for f in (fig_status, fig_layers, fig_hollow, fig_antichains, fig_parity, fig_support_span, fig_irreducible):
        f(); print(f.__name__, 'ok', flush=True)
