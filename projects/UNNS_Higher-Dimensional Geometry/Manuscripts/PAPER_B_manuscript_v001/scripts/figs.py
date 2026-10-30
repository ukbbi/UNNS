#!/usr/bin/env python3
"""Generates the 14 figures of Paper B from exact data computed with geo2.py.
Usage: python3 figs.py          (writes ../tex/figures/*.pdf and ../tex/figures/figure_data.json)
Every 3-D picture shows a genuinely 3-dimensional object (E_3 triangle, octahedron in the hyperplane sum x_i = 2, the cube AG(3,2));
nothing is presented as a rendering of higher-dimensional geometry."""
import json, itertools, collections, math, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, FancyArrowPatch, Rectangle, FancyBboxPatch, Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from geo2 import *

matplotlib.rcParams.update({'pdf.fonttype': 42, 'font.size': 9, 'axes.titlesize': 10, 'figure.dpi': 150,
                            'axes.spines.top': False, 'axes.spines.right': False})
OUT = '../tex/figures/'
os.makedirs(OUT, exist_ok=True)
PAL = ['#0072B2', '#D55E00', '#009E73', '#CC79A7', '#E69F00', '#56B4E9', '#999999']
DATA = {}


def E(n):
    return {w for w in range(1 << n) if bin(w).count('1') % 2 == 0}


def lab(w, n):
    return ''.join(str(i + 1) for i in range(n) if w >> i & 1)


def arcs(ax, n, blocks, y0=0.0, colors=None, label=True):
    """draw coordinates 1..n on a line and each block (a set of coordinates) as a chain of arcs"""
    for i in range(n):
        ax.plot([i], [y0], 'o', color='k', ms=4)
        ax.text(i, y0 - 0.28, str(i + 1), ha='center', va='top', fontsize=8)
    for bi, b in enumerate(blocks):
        idx = [i for i in range(n) if b >> i & 1]
        c = (colors or PAL)[bi % len(colors or PAL)]
        for u, v in zip(idx, idx[1:]):
            w = v - u
            ax.add_patch(Arc(((u + v) / 2, y0), w, 0.9 * w + 0.4, theta1=0, theta2=180, color=c, lw=1.8))
        ax.plot(idx, [y0] * len(idx), 'o', color=c, ms=6)
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(y0 - 0.9, y0 + 0.5 * n * 0.6 + 0.4)
    ax.axis('off')


# ---------------------------------------------------------------- fig01: lattice slice (n=3)
def fig01():
    fig = plt.figure(figsize=(7.4, 3.3))
    ax = fig.add_subplot(121, projection='3d')
    pts = [(a, b, c) for a in range(-1, 3) for b in range(-1, 3) for c in range(-1, 3) if (a + b + c) % 2 == 0]
    P = np.array(pts)
    ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=8, color='#bbbbbb', depthshade=False)
    for e in itertools.product([0, 1], repeat=3):
        for d in range(3):
            if e[d] == 0:
                f = list(e); f[d] = 1
                ax.plot([e[0], f[0]], [e[1], f[1]], [e[2], f[2]], color='#888888', lw=0.6)
    fib = [(1, 1, 0), (1, 0, 1), (0, 1, 1)]
    F = np.array(fib)
    ax.scatter(F[:, 0], F[:, 1], F[:, 2], s=40, color=PAL[1], depthshade=False)
    ax.scatter([0], [0], [0], s=40, color='k', depthshade=False)
    tri = [fib[0], fib[1], fib[2], fib[0]]
    ax.plot([t[0] for t in tri], [t[1] for t in tri], [t[2] for t in tri], color=PAL[1], lw=1.8)
    for t, nm in zip(fib, ['110', '101', '011']):
        ax.text(t[0] + .1, t[1] + .1, t[2] + .1, nm, fontsize=8)
    ax.text(-0.35, -0.2, -0.1, '0', fontsize=8)
    ax.set_xlabel('$\\alpha_1$'); ax.set_ylabel('$\\alpha_2$'); ax.set_zlabel('$\\alpha_3$')
    ax.set_title('$\\Lambda_M\\cap[-1,2]^3$ and the unit box', fontsize=9)
    ax.view_init(22, 35)
    ax2 = fig.add_subplot(122)
    V = {'110': (0, 1), '101': (-0.87, -0.5), '011': (0.87, -0.5)}
    for a, b in itertools.combinations(V, 2):
        ax2.plot([V[a][0], V[b][0]], [V[a][1], V[b][1]], color=PAL[1], lw=2)
        mx = (V[a][0] + V[b][0]) / 2; my = (V[a][1] + V[b][1]) / 2
        c = ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))
        ax2.text(mx * 1.18, my * 1.18, 'circuit ' + c, fontsize=7.5, ha='center')
    for k, v in V.items():
        ax2.plot(*v, 'o', color=PAL[1], ms=7); ax2.text(v[0], v[1] + 0.12 if k == '110' else v[1] - 0.22, k, ha='center', fontsize=9)
    ax2.set_xlim(-1.5, 1.5); ax2.set_ylim(-1.1, 1.3); ax2.set_aspect('equal'); ax2.axis('off')
    ax2.set_title('fibre of $E_3$: nonzero codewords and the three cells', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT + 'fig01_lattice_slice.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig02: circuit decompositions of E4
def fig02():
    n = 4
    parts = [(0b0011, 0b1100), (0b0101, 0b1010), (0b1001, 0b0110)]
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 1.9))
    for ax, P in zip(axs, parts):
        arcs(ax, n, P, colors=[PAL[0], PAL[1]])
        ax.set_title('$\\{%s\\}\\ \\sqcup\\ \\{%s\\}$' % (lab(P[0], n), lab(P[1], n)), fontsize=9)
    fig.suptitle('three decompositions of $1111$ into disjoint circuits ($E_4$)', fontsize=9, y=1.0)
    fig.tight_layout(); fig.savefig(OUT + 'fig02_circuit_decompositions.pdf'); plt.close(fig)
    DATA['fig02'] = [[lab(b, n) for b in P] for P in parts]


# ---------------------------------------------------------------- fig03: cells by dimension
def fig03():
    codes = {'$E_3$': E(3), '$E_4$': E(4)}
    for nm, X in (('$k{=}4,p{=}6$', [8, 9, 10, 11, 12, 13]), ('$\\mathrm{AG}(3,2)$', [8, 9, 10, 11, 12, 13, 14, 15])):
        codes[nm] = set(code_from_points(X)[0].values())
    res = {}
    for nm, Cw in codes.items():
        n = max(w.bit_length() for w in Cw)
        n = 3 if nm == '$E_3$' else (4 if nm == '$E_4$' else (6 if 'p{=}6' in nm else 8))
        cl = cells(Cw, n)
        cnt = collections.Counter(len(k[0]) for k in cl)
        res[nm] = {0: len(Cw) - 1, **dict(cnt)}
    DATA['fig03'] = {k: {str(a): b for a, b in v.items()} for k, v in res.items()}
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    names = list(res)
    w = 0.2
    maxd = max(max(v) for v in res.values())
    for d in range(maxd + 1):
        vals = [res[nm].get(d, 0) for nm in names]
        bars = ax.bar(np.arange(len(names)) + (d - maxd / 2) * w, vals, w, label='dim %d' % d, color=PAL[d % len(PAL)])
        for b, v in zip(bars, vals):
            if v:
                ax.text(b.get_x() + b.get_width() / 2, v * 1.05, str(v), ha='center', fontsize=7)
    ax.set_yscale('log'); ax.set_xticks(np.arange(len(names))); ax.set_xticklabels(names)
    ax.set_ylabel('number of cells'); ax.legend(frameon=False, fontsize=8, ncol=4)
    ax.set_title('admissible cells by dimension (0-cells are the nonzero codewords)', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT + 'fig03_admissible_cells.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig04: embedded vs non-embedded
def fig04():
    fig = plt.figure(figsize=(7.4, 3.4))
    ax = fig.add_subplot(121)
    V = {'110': (0, 1), '101': (-0.87, -0.5), '011': (0.87, -0.5)}
    for a, b in itertools.combinations(V, 2):
        ax.plot([V[a][0], V[b][0]], [V[a][1], V[b][1]], color=PAL[0], lw=2)
    for k, v in V.items():
        ax.plot(*v, 'o', color=PAL[0], ms=7); ax.text(v[0], v[1] + 0.13 if k == '110' else v[1] - 0.25, k, ha='center', fontsize=9)
    ax.set_aspect('equal'); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.1, 1.4); ax.axis('off')
    ax.set_title('$E_3$: embedded (cells meet in vertices)', fontsize=9)
    ax3 = fig.add_subplot(122, projection='3d')
    v = {'12': (1, 0, 0), '34': (-1, 0, 0), '13': (0, 1, 0), '24': (0, -1, 0), '14': (0, 0, 1), '23': (0, 0, -1)}
    sq = {'A': (['13', '14', '24', '23'], PAL[0]), 'B': (['12', '14', '34', '23'], PAL[1]), 'C': (['12', '13', '34', '24'], PAL[2])}
    # order vertices around each square
    for nm, (vs, c) in sq.items():
        poly = Poly3DCollection([[v[x] for x in vs]], alpha=0.35, facecolor=c, edgecolor=c, lw=1.2)
        ax3.add_collection3d(poly)
    for k, p in v.items():
        ax3.scatter(*p, color='k', s=14, depthshade=False); ax3.text(p[0] * 1.15, p[1] * 1.15, p[2] * 1.15, k, fontsize=8)
    ax3.scatter(0, 0, 0, color='r', s=18, depthshade=False)
    ax3.set_xlim(-1.2, 1.2); ax3.set_ylim(-1.2, 1.2); ax3.set_zlim(-1.2, 1.2)
    ax3.set_axis_off(); ax3.view_init(20, 30)
    ax3.set_title('$E_4$: three squares through the centre (hyperplane $\\sum x_i=2$)', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT + 'fig04_embedded_vs_nonembedded.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig05: rank-3 collision
def fig05():
    n = 4
    S = (0b0011, 0b1100); T = (0b0101, 0b1010); x = 0b1001
    A = generators(S, x, n); B = generators(T, x, n)
    M = np.array(A + B)
    rk = rank_int(A + B)
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.imshow(M, cmap='RdBu', vmin=-1.6, vmax=1.6)
    names = ['$g_1$ (block 12)', '$g_2$ (block 34)', '$h_1$ (block 13)', '$h_2$ (block 24)']
    for i in range(4):
        for j in range(4):
            ax.text(j, i, '%+d' % M[i, j] if M[i, j] else '0', ha='center', va='center', fontsize=10)
    ax.set_xticks(range(4)); ax.set_xticklabels(['coord %d' % (i + 1) for i in range(4)])
    ax.set_yticks(range(4)); ax.set_yticklabels(names); ax.xaxis.tick_top()
    for s in ax.spines.values(): s.set_visible(False)
    fig.text(0.5, 0.01, '$g_1+g_2=h_1+h_2=(-1,1,1,-1)$,  rank$=%d$ (base point $x=1001$, exact elimination)' % rk, ha='center', fontsize=9)
    fig.tight_layout(rect=(0, 0.06, 1, 1)); fig.savefig(OUT + 'fig05_rank3_collision.pdf'); plt.close(fig)
    DATA['fig05'] = dict(matrix=M.tolist(), rank=rk)


# ---------------------------------------------------------------- fig06: shortening
def fig06():
    fig, axs = plt.subplots(1, 3, figsize=(7.6, 2.3))
    n = 5
    ax = axs[0]
    arcs(ax, 5, (0b00011, 0b01100), colors=[PAL[0], PAL[1]])
    for b, c in ((0b00101, PAL[2]), (0b01010, PAL[3])):
        pass
    ax.set_title('$E_5$: $U=\\{1,2,3,4\\}$ has partitions\n$12|34$ and $13|24$', fontsize=8)
    ax = axs[1]
    arcs(ax, 4, (0b0101, 0b1010), colors=[PAL[2], PAL[3]])
    ax.set_title('shorten at $5$: $E_4$ (circuits avoiding $5$);\nthe partition $13|24$ survives, so still non-embedded', fontsize=8)
    ax = axs[2]
    ax.axis('off')
    ax.text(0.5, 0.6, '$E_4$ shortened at $1$ is $E_3$:\nno set has two partitions,\nso $E_3$ is embedded', ha='center', va='center', fontsize=8.5)
    ax.text(0.5, 0.12, '$E_4$ is minimal; $E_5$ is not', ha='center', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT + 'fig06_shortening.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig07: affine reduction
def cube_xyz(x):
    return (x & 1, (x >> 1) & 1, (x >> 2) & 1)


def fig07():
    fig = plt.figure(figsize=(7.6, 2.5))
    cl = json.load(open('../logs/classify.json'))
    reps = [('$k{=}3$, $p{=}4$', None, [4, 5, 6, 7])]
    # k=3 on AG(2,2) square; k=4 three classes on AG(3,2) cube
    ax = fig.add_subplot(1, 4, 1)
    sqp = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}
    for a, b in ((0, 1), (1, 3), (3, 2), (2, 0)):
        ax.plot([sqp[a][0], sqp[b][0]], [sqp[a][1], sqp[b][1]], color='#999999', lw=1)
    for q in range(4): ax.plot(*sqp[q], 'o', color=PAL[0], ms=7)
    ax.set_title('$k=3$: all of $\\mathrm{AG}(2,2)$\n($E_4$)', fontsize=8); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-.3, 1.3); ax.set_ylim(-.3, 1.3)
    DATA['fig07'] = {}
    for idx, info in enumerate(cl['k4']['info']):
        ax = fig.add_subplot(1, 4, idx + 2, projection='3d')
        X = set(info['rep'])
        allp = [8 + t for t in range(8)]
        for e in itertools.product([0, 1], repeat=3):
            for d in range(3):
                if e[d] == 0:
                    f = list(e); f[d] = 1
                    ax.plot([e[0], f[0]], [e[1], f[1]], [e[2], f[2]], color='#aaaaaa', lw=0.7)
        for q in allp:
            c = cube_xyz(q)
            if q in X: ax.scatter(*c, color=PAL[1], s=34, depthshade=False)
            else: ax.scatter(*c, facecolors='white', edgecolors='#777777', s=34, depthshade=False)
        ax.set_axis_off(); ax.view_init(20, 35)
        ax.set_title('$k=4$, $p=%d$ (%d labelled)' % (info['p'], info['orbit_size']), fontsize=8)
        DATA['fig07']['k4_p%d' % info['p']] = sorted(X)
    fig.suptitle('minimal reduced boxes as subsets of $\\mathrm{AG}(k-1,2)$ (filled points)', fontsize=9, y=1.0)
    fig.tight_layout(); fig.savefig(OUT + 'fig07_affine_reduction.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig08: five partitions
def fig08():
    X = [8, 9, 10, 11, 12, 13]; n = 6
    Cw = set(code_from_points(X)[0].values()); cs = circuits_of(Cw)
    parts = sorted(one_partitions(cs, n), key=lambda P: (len(P), P))
    fig, axs = plt.subplots(1, 5, figsize=(7.8, 1.9))
    for ax, P in zip(axs, parts):
        arcs(ax, n, P, colors=PAL)
        ax.set_title('$m=%d$' % len(P), fontsize=8)
    fig.tight_layout(); fig.savefig(OUT + 'fig08_two_partitions.pdf'); plt.close(fig)
    DATA['fig08'] = [[lab(b, n) for b in P] for P in parts]


# ---------------------------------------------------------------- fig09: Fano plane
def fig09():
    X = [8, 9, 10, 11, 12, 13]; n = 6; k = 4
    Cw = set(code_from_points(X)[0].values()); cs = circuits_of(Cw); full = (1 << n) - 1
    parts = sorted(one_partitions(cs, n), key=lambda P: (len(P), P))
    # classes of C/<1>
    classes = sorted({min(w, w ^ full) for w in Cw if w not in (0, full)})
    assert len(classes) == 7
    # choose a basis of the quotient
    basis = []
    for c in classes:
        if rank_bits(basis + [c, full]) > rank_bits(basis + [full]) if basis else True:
            if rank_bits(basis + [c] + [full]) == len(basis) + 2:
                basis.append(c)
        if len(basis) == 3: break
    coords = {}
    for a in itertools.product([0, 1], repeat=3):
        if a == (0, 0, 0): continue
        w = 0
        for ai, b in zip(a, basis):
            if ai: w ^= b
        coords[min(w, w ^ full)] = a
    pos = {(1, 0, 0): (0, 1.0), (0, 1, 0): (-0.87, -0.5), (0, 0, 1): (0.87, -0.5)}
    def P_of(a): return np.array(pos[a])
    for a in coords.values():
        if a not in pos:
            s = [i for i in range(3) if a[i]]
            if len(s) == 2:
                u = [tuple(1 if j == i else 0 for j in range(3)) for i in s]
                pos[a] = tuple((np.array(pos[u[0]]) + np.array(pos[u[1]])) / 2)
            else:
                pos[a] = (0.0, 0.0)
    owner = {}
    for pi, P in enumerate(parts):
        for w in span_words(list(P)):
            if w not in (0, full): owner[min(w, w ^ full)] = pi
    fig, ax = plt.subplots(figsize=(4.2, 3.7))
    inv = {v: k for k, v in coords.items()}
    # lines
    allpts = list(coords.values())
    seen = set()
    for a, b in itertools.combinations(allpts, 2):
        c = tuple((x + y) % 2 for x, y in zip(a, b))
        line = frozenset([a, b, c])
        if line in seen: continue
        seen.add(line)
        L = list(line)
        pts = np.array([pos[q] for q in L])
        # draw as a segment through the 3 points, or circle for the inner triangle
        if (1, 1, 0) in line and (0, 1, 1) in line and (1, 0, 1) in line:
            ax.add_patch(plt.Circle((0, 0), 0.5 * 0.9, fill=False, color='#cccccc', lw=0.8))
        else:
            xs = sorted(pts.tolist(), key=lambda t: (t[0], t[1]))
            ax.plot([xs[0][0], xs[-1][0]], [xs[0][1], xs[-1][1]], color='#cccccc', lw=0.8, zorder=0)
    twod = [pi for pi, P in enumerate(parts) if len(P) == 3][0]
    # highlight the 2-dim part line
    L = [coords[c] for c, o in owner.items() if o == twod]
    for q in L:
        ax.plot(*pos[q], 'o', ms=15, color=PAL[1], zorder=2)
    for c, o in owner.items():
        if o != twod:
            ax.plot(*pos[coords[c]], 'o', ms=13, color=PAL[0], zorder=2)
    for c, a in coords.items():
        ax.text(pos[a][0], pos[a][1], '%d' % (parts.index(next(P for P in parts if min(w for w in [c]) is not None and c in {min(x_, x_ ^ full) for x_ in span_words(list(P))})) + 1 if False else owner[c] + 1), ha='center', va='center', color='white', fontsize=8, zorder=3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('$C/\\langle 1\\rangle \\cong \\mathrm{F}_2^3$: points labelled by the partition\n(orange: the 2-dimensional part)', fontsize=8)
    fig.tight_layout(); fig.savefig(OUT + 'fig09_vsp_fano.pdf'); plt.close(fig)
    DATA['fig09'] = dict(parts=[[lab(b, n) for b in P] for P in parts])


# ---------------------------------------------------------------- fig10: counting identity
def fig10():
    cl = json.load(open('../logs/classify.json'))
    info = cl['k5']['info']
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    labels = []
    left = np.zeros(len(info))
    ms = [2, 3, 4]
    for mi, m in enumerate(ms):
        vals = np.array([sum(1 for x in i['m'] if x == m) * ((1 << m) - 2) for i in info])
        ax.barh(range(len(info)), vals, left=left, color=PAL[mi], label='$m=%d$: $n_m(2^m-2)$' % m)
        left += vals
    assert all(abs(v - 30) < 1e-9 for v in left)
    ax.set_yticks(range(len(info))); ax.set_yticklabels(['$p=%d$, $n_2=%d$' % (i['p'], i['n2']) for i in info], fontsize=7)
    ax.axvline(30, color='k', lw=0.8, ls='--'); ax.text(30.3, -0.9, '$2^5-2=30$', fontsize=8)
    ax.set_xlabel('contribution to $\\sum_P(2^{m_P}-2)$'); ax.legend(frameon=False, fontsize=8, loc='lower right')
    ax.invert_yaxis()
    fig.tight_layout(); fig.savefig(OUT + 'fig10_counting_identity.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig11: n2 vs p
def fig11():
    cl = json.load(open('../logs/classify.json'))
    rec = json.load(open('../logs/k6_records.json'))['k6']
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    cols = {3: PAL[0], 4: PAL[1], 5: PAL[2], 6: PAL[3]}
    for k in (3, 4, 5):
        ps = [i['p'] for i in cl['k%d' % k]['info']]; ns = [i['n2'] for i in cl['k%d' % k]['info']]
        ax.scatter(ps, ns, color=cols[k], s=26, label='$k=%d$' % k, zorder=3)
    ps = [r[0] for r in rec]; ns = [r[1] for r in rec]
    ax.scatter(ps, ns, color=cols[6], s=16, alpha=0.75, label='$k=6$ (215)', zorder=2)
    xs = np.arange(3, 34)
    ax.plot(xs, xs - 1, color='k', lw=1, label='$n_2=p-1$')
    ax.axvline(9, color='#888888', ls='--', lw=0.9); ax.text(9.2, 2, '$p=9$', fontsize=8, color='#555555')
    ax.set_xlabel('reduced length $p$'); ax.set_ylabel('two-block partitions $n_2$')
    ax.legend(frameon=False, fontsize=8, loc='lower right')
    ax.set_title('all minimal classes $k\\leq 6$: $n_2\\geq p-1$ for $p\\geq 9$ (sharp at $p=16,32$)', fontsize=9)
    fig.tight_layout(); fig.savefig(OUT + 'fig11_n2_bound.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig12: classification
def fig12():
    cl = json.load(open('../logs/classify.json'))
    rec = json.load(open('../logs/k6_records.json'))['k6']
    fig, axs = plt.subplots(1, 4, figsize=(7.8, 2.4), sharey=False)
    for ax, k in zip(axs, (3, 4, 5, 6)):
        if k < 6:
            c = collections.Counter(i['p'] for i in cl['k%d' % k]['info'])
        else:
            c = collections.Counter(r[0] for r in rec)
        ps = sorted(c)
        ax.bar(ps, [c[p] for p in ps], color=PAL[k - 3])
        ax.set_title('$k=%d$: %d classes' % (k, sum(c.values())), fontsize=8)
        ax.set_xlabel('$p$', fontsize=8)
    axs[0].set_ylabel('classes', fontsize=8)
    fig.tight_layout(); fig.savefig(OUT + 'fig12_classification.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig13: E8 chain
def fig13():
    fig, ax = plt.subplots(figsize=(7.4, 2.7))
    cols = [8, 7, 6, 5, 4]
    for ci, n in enumerate(cols):
        x0 = ci * 1.5
        ax.add_patch(Rectangle((x0 - 0.1, -0.05), 1.15, 8 * 0.3 + 0.1, fill=False, ec=PAL[ci % 5] if n > 4 else PAL[2], lw=1.5 if n > 4 else 2.6))
        for j in range(8):
            alive = j < n
            ax.plot([x0 + 0.5], [j * 0.3 + 0.15], 'o', ms=5, color='k' if alive else '#dddddd', mfc='k' if alive else 'white')
        ax.text(x0 + 0.5, 8 * 0.3 + 0.2, '$E_{%d}$' % n, ha='center', fontsize=10)
        if ci < 4:
            ax.annotate('', xy=(x0 + 1.4, 1.2), xytext=(x0 + 1.1, 1.2), arrowprops=dict(arrowstyle='->'))
            ax.text(x0 + 1.25, 1.35, 'shorten', fontsize=6.5, ha='center')
    ax.text(0.5, -0.45, '$k=7$, $n_2=0$', ha='center', fontsize=8)
    ax.text(6 + 0.5, -0.45, 'minimal ($k=3$, $n_2=3$)', ha='center', fontsize=8, color=PAL[2])
    ax.set_xlim(-0.4, 7.6); ax.set_ylim(-0.7, 3.0); ax.axis('off')
    fig.tight_layout(); fig.savefig(OUT + 'fig13_E8_nonminimal.pdf'); plt.close(fig)


# ---------------------------------------------------------------- fig14: dependency diagram
def fig14():
    import subprocess
    subprocess.run(['dot','-Tpdf','fig14.dot','-o',OUT+'fig14_dependencies.pdf'],check=True)


if __name__ == '__main__':
    for f in (fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14):
        f(); print(f.__name__, 'ok', flush=True)
    json.dump(DATA, open(OUT + 'figure_data.json', 'w'), indent=1)
