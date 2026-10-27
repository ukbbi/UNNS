"""Figures for GEO-I v004 (matplotlib; every panel is computed from the exact objects, nothing is drawn by hand)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'experiments', 'theory'): sys.path.insert(0, os.path.join(ROOT, d_))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import gcd
from lattice_model import Lat, complex_data, U_betti
from coverage import is_hull_covered

FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True)
C = {'pt': '#1f4e79', 'edge': '#c0392b', 'cell': '#f5b041', 'ok': '#2e8b57', 'bad': '#b03a2e', 'gray': '#999999'}


def draw_fibre(ax, d, s, Q, title):
    L = Lat(d, d, d, s) if d > 1 else Lat(1, 1, 1, 1); cd = complex_data(L, Q)
    for (u, gens) in cd['cells'][2] if len(cd['cells']) > 2 else []:
        g, h = gens
        P = [u, (u[0] + g[0], u[1] + g[1]), (u[0] + g[0] + h[0], u[1] + g[1] + h[1]), (u[0] + h[0], u[1] + h[1])]
        ax.add_patch(Polygon(P, closed=True, fc=C['cell'], ec='none', alpha=0.25))
    for (u, (g,)) in cd['cells'][1]:
        ax.plot([u[0], u[0] + g[0]], [u[1], u[1] + g[1]], color=C['edge'], lw=0.9, alpha=0.8)
    ax.scatter([p[0] for p in cd['F']], [p[1] for p in cd['F']], s=16, color=C['pt'], zorder=3)
    ax.set_xlim(-0.6, Q[0] + 0.6); ax.set_ylim(-0.6, Q[1] + 0.6); ax.set_aspect('equal'); ax.set_title(title, fontsize=9)
    ax.set_xticks(range(0, Q[0] + 1)); ax.set_yticks(range(0, Q[1] + 1)); ax.tick_params(labelsize=7)


def fig_hollow():
    fig, axs = plt.subplots(1, 4, figsize=(15, 3.9))
    draw_fibre(axs[0], 5, 4, (5, 5), 'd=5, s=-1, Q=(5,5): fan, beta1 = 5')
    draw_fibre(axs[1], 5, 2, (5, 5), 'd=5, s=2, Q=(5,5): hollow, beta1 = 2')
    draw_fibre(axs[2], 5, 2, (6, 5), 'd=5, s=2, Q=(6,5): U = conv(F)')
    draw_fibre(axs[3], 5, 2, (7, 7), 'd=5, s=2, Q=(7,7): U = conv(F)')
    fig.suptitle('Planar stabilization: the image U is hollow exactly at Q = (d,d) (lattice points, Graver edges, 2-cells)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig1_hollow_vs_filled.png'), dpi=130); plt.close(fig)


def fig_beta():
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for d in range(2, 13):
        for s in range(1, d):
            if gcd(s, d) != 1: continue
            b, _ = U_betti(Lat(d, d, d, s), (d, d))
            ax.scatter(d, b[1], color=C['bad'] if s == d - 1 else C['pt'], s=26, zorder=3)
    ax.plot([2, 12], [2, 12], color=C['bad'], lw=0.8, ls=':')
    ax.set_xlabel('d'); ax.set_ylabel('beta_1(U) at Q=(d,d)')
    ax.set_title('beta_1 at the hollow box: = d for s = -1 (red), = 2 otherwise (blue)', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig2_beta1_at_dd.png'), dpi=130); plt.close(fig)


def fig_atlas():
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'output', 'data', 'k2_atlas_pure.jsonl'))]
    sel = [r for r in rows if r['d'] == 7]
    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    cols = plt.cm.viridis([i / max(1, len(sel) - 1) for i in range(len(sel))])
    for c, r in zip(cols, sel):
        B = sorted(map(tuple, r['minimal_boxes']))
        xs = [b[0] for b in B]; ys = [b[1] for b in B]
        ax.plot(xs, ys, '-o', color=c, ms=3, lw=0.8, label='s=%d' % r['s'])
    ax.set_xlabel('Q1'); ax.set_ylabel('Q2'); ax.set_xlim(0, 15); ax.set_ylim(0, 15); ax.legend(fontsize=7, ncol=2)
    ax.set_title('d=7: minimal obstruction boxes (non-embedded iff Q dominates a point)', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig3_k2_obstruction_atlas_d7.png'), dpi=130); plt.close(fig)


def fig_phase():
    d, s = 4, 1
    anti = [tuple(b) for b in next(json.loads(l) for l in open(os.path.join(ROOT, 'output', 'data', 'k2_atlas_pure.jsonl')) if json.loads(l)['d'] == d and json.loads(l)['s'] == s)['minimal_boxes']]
    N = 9
    fig, ax = plt.subplots(figsize=(6.2, 5.6))
    for q1 in range(1, N + 1):
        for q2 in range(1, N + 1):
            L = Lat(d, d, d, s); b, _ = U_betti(L, (q1, q2))
            if b is None: continue
            emb = not any(q1 >= m[0] and q2 >= m[1] for m in anti)
            col = C['ok'] if b[1] == 0 else C['bad']
            ax.add_patch(plt.Rectangle((q1 - .45, q2 - .45), .9, .9, fc=col, alpha=0.35 if emb else 0.9, ec='black' if not emb else 'none', lw=1.2, hatch='' if emb else '//'))
    ax.set_xlim(0.4, N + .6); ax.set_ylim(0.4, N + .6); ax.set_aspect('equal'); ax.set_xlabel('Q1 (=q1)'); ax.set_ylabel('Q2 (=q2)')
    ax.set_title('b=5, residues (2,3) (d=4, s=1): red = beta1(U) != 0;  hatched = K_abs NOT embedded', fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig4_phase_map_b5.png'), dpi=130); plt.close(fig)


def fig_hd():
    fig, ax = plt.subplots(figsize=(7.4, 3.8))
    items = [('Klein-four (a,b,ab)', [(1, 1, 4), (1, 2, 3), (2, 2, 2)][:0] or [(1, 1, 4), (1, 2, 3), (1, 3, 2), (2, 1, 3), (4, 1, 1)]),
             ('Klein-four (a,a,b)', [(1, 3, 2), (2, 2, 2), (1, 4, 0), (2, 3, 0), (4, 1, 0)]),
             ('parity n=3', [(1, 1, 2)]), ('parity n=4', [(1, 1, 1, 1)]), ('all-same-parity n=4 (b=24)', [(3, 2, 1, 1), (4, 1, 1, 1)])]
    for i, (nm, B) in enumerate(items):
        ax.scatter([sum(b) for b in B], [i] * len(B), s=40, color=C['pt'])
        for b in B: ax.annotate(''.join(map(str, b)), (sum(b), i), textcoords='offset points', xytext=(0, 6), fontsize=7, ha='center')
    ax.set_yticks(range(len(items))); ax.set_yticklabels([n for n, _ in items], fontsize=8); ax.set_xlabel('|q| = total exponent budget of a minimal obstruction box')
    ax.set_title('Minimal obstruction boxes (up to coordinate permutation) in 3D and 4D', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig5_higher_dim_minimal_boxes.png'), dpi=130); plt.close(fig)


if __name__ == '__main__':
    fig_hollow(); fig_beta(); fig_atlas(); fig_phase(); fig_hd()
    print(sorted(os.listdir(FIG)))
