"""Figures for GEO-I v002. Every plotted vertex/edge/face is read from the exact complexes built by geometry/geo2lib.py."""
import sys, os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'geometry'))
from geo2lib import *
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
FD = os.path.join(ROOT, 'figures'); os.makedirs(FD, exist_ok=True)
plt.rcParams.update({'font.size': 8, 'figure.dpi': 150})
def complex_of(x, moves='axis'):
    ps, q, b = coords(x); F = fibre_points(ps, q, b)
    M = set(unit_moves(len(ps))) if moves == 'axis' else set(graver_region(ps, q, b))
    return ps, q, b, F, build_cells(F, M, len(ps))
def proj(v, mode):
    v = np.array(v, float)
    if len(v) == 3: return v
    return np.array([v[0] + .55 * v[3], v[1] + .35 * v[3], v[2] + .45 * v[3]])
def draw(ax, cells, mode=3, layers=('v', 'e', 'f', 'c'), vcol='C0', title='', labels=None):
    if 'c' in layers and len(cells) > 3:
        for (u, g) in cells[3]:
            vs = cell_vertices(u, g); P = np.array([proj(v, mode) for v in vs])
            # draw cube edges lightly via faces below; colour the solid by translucent bounding faces
    if 'f' in layers and len(cells) > 2:
        polys = []
        for (u, g) in cells[2]:
            a, b = g; pts = [u, add(u, a), add(add(u, a), b), add(u, b)]
            polys.append([proj(p, mode) for p in pts])
        ax.add_collection3d(Poly3DCollection(polys, alpha=.18, facecolor='C1', edgecolor='none'))
    if 'c' in layers and len(cells) > 3:
        polys = []
        for (u, g) in cells[3]:
            for i in range(3):
                rest = [g[j] for j in range(3) if j != i]
                for base in (u, add(u, g[i])):
                    pts = [base, add(base, rest[0]), add(add(base, rest[0]), rest[1]), add(base, rest[1])]
                    polys.append([proj(p, mode) for p in pts])
        ax.add_collection3d(Poly3DCollection(polys, alpha=.10, facecolor='C2', edgecolor='none'))
    if 'e' in layers and len(cells) > 1:
        segs = [[proj(u, mode), proj(add(u, g[0]), mode)] for (u, g) in cells[1]]
        ax.add_collection3d(Line3DCollection(segs, colors='k', linewidths=.8))
    P = np.array([proj(u, mode) for (u, _) in cells[0]])
    ax.scatter(P[:, 0], P[:, 1], P[:, 2], c=vcol, s=14, depthshade=False)
    if labels:
        for (u, _) in cells[0]: ax.text(*proj(u, mode), labels(u), fontsize=5)
    ax.set_title(title, fontsize=8); ax.set_box_aspect((1, 1, 1))
    lo = P.min(0) - .3; hi = P.max(0) + .3; ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.set_zlim(lo[2], hi[2])
# V1 : 3600, layers separated
ps, q, b, F, cells = complex_of(3600)
fig = plt.figure(figsize=(10, 2.9))
for i, (lay, tt) in enumerate((('v', '0-cells: 11 vertices'), ('ve', '+ 17 edges'), ('vef', '+ 8 square faces'), ('vefc', '+ 1 cube (3-cell)'))):
    ax = fig.add_subplot(1, 4, i + 1, projection='3d'); draw(ax, cells, 3, tuple(lay), title=tt)
    ax.set_xlabel('a2', labelpad=-8); ax.set_ylabel('a3', labelpad=-8); ax.set_zlabel('a5', labelpad=-8)
fig.suptitle('E1: fibre of 3600 = 2^4 3^2 5^2 (box 3x2x2 minus origin), coordinate complex, layers shown separately; cube = {1,2}x{0,1}x{0,1}', fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FD, 'fig_V1_3600_cells.png')); plt.close(fig)
# V2 : 4D projection 44100 vs 210^4, then slices
fig = plt.figure(figsize=(10, 4.0))
for col, (x, name) in enumerate(((44100, '44100 = 210^2: 15 vertices, no 4-cell'), (210 ** 4, '210^4: 80 vertices, 4-cell {1,2}^4 present'))):
    ps, q, b, F, cells = complex_of(x)
    ax = fig.add_subplot(1, 2, col + 1, projection='3d'); draw(ax, cells, 4, ('v', 'e', 'f'), title='oblique projection of ' + name)
    if col == 0:
        ax.scatter(*proj((0, 0, 0, 0), 4), marker='x', c='r', s=30)
    else:
        vs = cell_vertices((1, 1, 1, 1), ((0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)))
        P = np.array([proj(v, 4) for v in vs]); ax.scatter(P[:, 0], P[:, 1], P[:, 2], c='r', s=18, depthshade=False)
fig.suptitle('E2/E3: 4D fibres, coordinates (a2,a3,a5,a7). Red x = removed origin (44100); red points = the certified 4-cell {1,2}^4 (210^4)', fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FD, 'fig_V2_4D_projection.png')); plt.close(fig)
def slice_cells(cells, s):
    out = [[c for c in cells[0] if c[0][3] == s]]
    for j in range(1, min(len(cells), 4)):
        out.append([(u, g) for (u, g) in cells[j] if u[3] == s and all(gg[3] == 0 for gg in g)])
    return [[(u[:3], tuple(gg[:3] for gg in g)) for (u, g) in lvl] for lvl in out]
fig = plt.figure(figsize=(10, 6))
spec = [(44100, [0, 1], 0), (210 ** 4, [0, 1, 2], 1)]
for x, slices, row in spec:
    ps, q, b, F, cells = complex_of(x)
    for i, s_ in enumerate(slices):
        sc = slice_cells(cells, s_); ax = fig.add_subplot(2, 3, row * 3 + i + 1, projection='3d')
        draw(ax, sc, 3, ('v', 'e', 'f', 'c'), title='%s, slice a7=%d: %s cells' % ('44100' if row == 0 else '210^4', s_, '/'.join(str(len(l)) for l in sc)))
fig.suptitle('E2/E3: 3D slices of the 4D coordinate complexes at fixed a7 (cell counts: vertices/edges/squares/cubes). 44100: a7=0 is the punctured cube, a7=1 the full cube.', fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FD, 'fig_V2b_4D_slices.png')); plt.close(fig)
# V3 : modular geometry comparison 2304/5 and 19600/3
fig = plt.figure(figsize=(10, 7.2))
x = Fr(2304, 5); ps, q, b, F, ca = complex_of(x, 'axis'); _, _, _, _, cm = complex_of(x, 'move')
for i, (cells, tt) in enumerate(((ca, 'coordinate adjacency: 0 edges, 2 components'), (cm, 'Graver-move adjacency: 1 edge, vector (3,-1), 1 component'))):
    ax = fig.add_subplot(2, 2, i + 1)
    for u in F: ax.scatter(*u, c='C3', s=40); ax.annotate('d=%d' % d_value(ps, u), u, textcoords='offset points', xytext=(5, 5), fontsize=7)
    for (u, g) in (cells[1] if len(cells) > 1 else []):
        w = add(u, g[0]); ax.annotate('', xy=w, xytext=u, arrowprops=dict(arrowstyle='-', color='k', lw=1.5)); ax.text((u[0] + w[0]) / 2 + .1, (u[1] + w[1]) / 2 + .1, 'move %s' % (g[0],), fontsize=7)
    ax.set_xlim(-.5, 5); ax.set_ylim(-.5, 2); ax.set_xlabel('a2'); ax.set_ylabel('a3'); ax.set_title('2304/5: ' + tt, fontsize=7); ax.grid(alpha=.3)
x = Fr(19600, 3); ps, q, b, F, cm = complex_of(x, 'move'); _, _, _, _, ca2 = complex_of(x, 'axis')
ax = fig.add_subplot(2, 2, 3, projection='3d')
draw(ax, cm, 3, ('v', 'e', 'f'), title='19600/3: move complex: 5 vertices, 6 edges, 1 square -> b1 = 1 (5-cycle not filled)', labels=lambda u: 'd=%d' % d_value(ps, u))
ax.set_xlabel('a2', labelpad=-8); ax.set_ylabel('a5', labelpad=-8); ax.set_zlabel('a7', labelpad=-8)
ax = fig.add_subplot(2, 2, 4); ax.axis('off')
G = [g for g in graver_region(ps, q, b) if lexpos(g)]
ax.text(0, .95, '19600/3 = 2^4 5^2 7^2 / 3: primes (2,5,7), box 3x2x2, b=3', fontsize=7, va='top')
ax.text(0, .78, 'positive Graver moves in region: ' + ', '.join(str(g) for g in G), fontsize=7, va='top')
ax.text(0, .6, 'unfilled cycle (relation among moves):\n(1,1,0)+(0,0,-1)+(1,-1,0)+(0,0,1)+(-2,0,0) = 0\nbetti(move) = [1,1,0] (mod 2 and mod 2^31-1)\nbetti(coordinate) = [3,0]: three contractible components', fontsize=7, va='top')
fig.suptitle('E4: the same rational fibre under coordinate adjacency and primitive modular-move adjacency (move edges are geometric, not SELECT-II/FIELD-I transitions)', fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FD, 'fig_V3_modular_moves.png')); plt.close(fig)
# V4 : dynamics
R = json.load(open(os.path.join(ROOT, 'output', 'verify_full.json')))
fig, axs = plt.subplots(1, 3, figsize=(11, 3.2))
o = R['c_orbits']['g11 benchmark 67500^2/11 [C]']; n_ = [s['n'] for s in o]
axs[0].plot(n_, [s['R'] for s in o], label='R = |fibre|'); axs[0].plot(n_, [s['axis_components'] for s in o], '--', label='coordinate components (= R)')
axs[0].plot(n_, [s['move_betti'][1] for s in o], label='b1 (cubical move complex)'); axs[0].plot(n_, [s['graver'] // 2 - s['d_amb'] for s in o], ':', label='|G+| - k')
axs[0].set_title('C-orbit g=11 (67500^2/11)', fontsize=8); axs[0].set_xlabel('n'); axs[0].legend(fontsize=6)
for name, v in R['c_orbits'].items():
    if name.startswith('72'): continue
    axs[1].plot([s['n'] for s in v], [s['move_betti'][1] if len(s['move_betti']) > 1 else 0 for s in v], label=name.split(' [')[0], lw=1)
axs[1].set_title('b1 of move complex along six G>1 orbits', fontsize=8); axs[1].set_xlabel('n'); axs[1].legend(fontsize=5)
dk = dict((int(a), b) for a, b in R['select2_geometry_change']['delta_d_amb']); dc = dict((int(a), b) for a, b in R['select2_geometry_change']['delta_d_cell'])
xs = sorted(set(dk) | set(dc)); w = .38
axs[2].bar([i - w / 2 for i in xs], [dk.get(i, 0) for i in xs], w, label='change in d_amb'); axs[2].bar([i + w / 2 for i in xs], [dc.get(i, 0) for i in xs], w, label='change in d_cell')
axs[2].set_yscale('log'); axs[2].set_title('SELECT-II edges <=5000: geometry change (3124 edges)', fontsize=8); axs[2].legend(fontsize=6)
fig.tight_layout(); fig.savefig(os.path.join(FD, 'fig_V4_dynamics.png')); plt.close(fig)
print('figures ok')
