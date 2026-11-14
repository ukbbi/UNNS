import json, math, csv
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from paths import *
from ugraph import *
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150,
                     'font.family': 'DejaVu Sans', 'mathtext.fontset': 'dejavusans'})
C = {'fwd': '#2a7f62', 'inv': '#b5473a', 'a': '#3b6ea5', 'b': '#c98b2b', 'g': '#777777', 'p': '#7a5195'}
def save(name): plt.savefig(f'{FIG}/{name}.pdf', bbox_inches='tight'); plt.savefig(f'{FIG}/{name}.png', bbox_inches='tight', dpi=200); plt.close()
def lab(x, y):
    s, N = label_of(x, y); return f'{s}{N}'

# ---------- Fig 1: ball of radius 3 about 1
B = ball(1, 3); layers = {}
for v, d in B.items(): layers.setdefault(d, []).append(v)
fig, ax = plt.subplots(figsize=(6.6, 5.2)); pos = {}
radii = {0: 0, 1: 1.0, 2: 2.1, 3: 3.3}
for d, vs in layers.items():
    vs = sorted(vs)
    for i, v in enumerate(vs):
        ang = (2 * math.pi * (i + 0.5) / len(vs)) + (0.0 if d != 1 else 0)
        pos[v] = (radii[d] * math.cos(ang) if d else 0, radii[d] * math.sin(ang) if d else 0)
seen = set()
for v in B:
    for w in nbrs(v):
        if w in B and (w, v) not in seen:
            seen.add((v, w)); (x1, y1), (x2, y2) = pos[v], pos[w]
            lo, hi = (v, w) if v < w else (w, v)
            ax.plot([x1, x2], [y1, y2], color='#9aa5b1', lw=1.0, zorder=1)
for v, (x, y) in pos.items():
    ax.scatter([x], [y], s=520 if B[v] < 3 else 380, color=['#f4d58d', '#a9d1c1', '#b6c9e2', '#e3e3e3'][B[v]], edgecolor='#333', lw=0.7, zorder=2)
    ax.text(x, y, str(v), ha='center', va='center', fontsize=8 if v < 1000 else 7, zorder=3)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('The ball $B_3(1)$ in $G$ (18 vertices; shells of size 1, 1, 3, 13)', fontsize=9)
save('fig1_ball_of_one')

# ---------- Fig 2: degrees and edge ratio
Dm = 20000; degs = np.array([degree_formula(x) for x in range(1, Dm)])
fig, ax = plt.subplots(1, 3, figsize=(9.6, 2.9))
vals, cnts = np.unique(degs, return_counts=True)
ax[0].bar(vals, cnts, color=[C['a'] if v != 2 else C['b'] for v in vals]); ax[0].set_yscale('log')
ax[0].set_xlabel('degree $\\deg_G(x)$'); ax[0].set_ylabel(f'number of $x<{Dm}$'); ax[0].set_title('(a) degree distribution; no vertex of degree 3', fontsize=8)
ax[0].set_xticks(range(1, int(vals.max()) + 1, 2) if vals.max() < 30 else range(1, int(vals.max()), 4))
Ns = np.arange(1, 21); ax[1].plot(Ns, Ns + 2 + 1 / Ns, 'o-', color=C['a'], ms=3); ax[1].axhline(4, color=C['g'], ls=':')
ax[1].set_xlabel('label $N$'); ax[1].set_ylabel('edge ratio $y/x=(N+1)^2/N$'); ax[1].set_title('(b) edge ratio $\\geq 4$', fontsize=8)
pr = [x for x in range(2, 4000) if sp.isprime(x)]
ax[2].scatter(range(1, Dm, 7), degs[::7], s=1.5, color=C['a'], alpha=.5); ax[2].set_xlabel('$x$'); ax[2].set_ylabel('$\\deg_G(x)$'); ax[2].set_title('(c) degree is $\\tau(x)+\\#\\{q\\geq2:q^2\\mid x\\}$', fontsize=8)
plt.tight_layout(); save('fig2_degrees_ratio')

# ---------- Fig 3: cycles
def draw_cycle(ax, vs, title):
    n = len(vs); ang = [math.pi / 2 + 2 * math.pi * i / n for i in range(n)]
    P = [(math.cos(a), math.sin(a)) for a in ang]
    for i in range(n):
        v, w = vs[i], vs[(i + 1) % n]; (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        ax.plot([x1, x2], [y1, y2], color='#555', lw=1.2, zorder=1)
        lo, hi = min(v, w), max(v, w)
        N = next(N for N in divisors(lo) if lo // N * (N + 1) ** 2 == hi); k = lo // N
        mx, my = (x1 + x2) / 2 * 1.18, (y1 + y2) / 2 * 1.18
        ax.text(mx, my, f'$N={N},\\,k={k}$', fontsize=7, ha='center', va='center', color=C['b'])
    for (x, y), v in zip(P, vs):
        ax.scatter([x], [y], s=700, color='#cfe0f1', edgecolor='#333', zorder=2); ax.text(x, y, str(v), ha='center', va='center', fontsize=8)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.5, 1.5); ax.set_aspect('equal'); ax.axis('off'); ax.set_title(title, fontsize=9)
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.6))
draw_cycle(ax[0], [2, 8, 36, 9], '4-cycle $2-8-36-9$ (girth)'); draw_cycle(ax[1], [6, 24, 96, 784, 27], '5-cycle $6-24-96-784-27$ (odd girth)')
plt.tight_layout(); save('fig3_cycles')

# ---------- Fig 4: residue map for successor identities
U1 = json.load(open(f'{INH}/u1_identities.json'))
cls = {}
for d in U1:
    for r in range(24):
        if r % d['modulus'] == d['residue'] % d['modulus']: cls[r] = (d['name'], len(d['steps']))
fig, ax = plt.subplots(figsize=(7.4, 1.9)); cols = {4: '#a9d1c1', 5: '#f4d58d', 6: '#e8a598'}
for r in range(24):
    n, L = cls[r]
    ax.add_patch(plt.Rectangle((r, 0), 1, 1, facecolor=cols[L], edgecolor='white'))
    ax.text(r + .5, .6, n, ha='center', va='center', fontsize=10); ax.text(r + .5, .25, str(r), ha='center', va='center', fontsize=7, color='#444')
ax.set_xlim(0, 24); ax.set_ylim(0, 1); ax.axis('off')
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=cols[l], label=f'{l} moves') for l in (4, 5, 6)], ncol=3, loc='upper center', bbox_to_anchor=(.5, -.02), frameon=False, fontsize=8)
ax.set_title('Residue classes of $n$ mod 24 and the length of the identity for $d(n,n+1)$ (letter = class A--I)', fontsize=8.5)
save('fig4_residue_map')

# ---------- Fig 5: distributions
ds = {int(k): v for k, v in json.load(open(f'{DATA}/successor_distances_independent.json')).items()}
dq = {int(k): v for k, v in json.load(open(f'{DATA}/square_distances_independent.json')).items()}
pdist = {int(k): v for k, v in json.load(open(f'{DATA}/prime_distances_lt400.json')).items()}
fig, ax = plt.subplots(1, 4, figsize=(11.2, 2.8))
def hist(a, data, col, ttl, rng):
    v = list(data.values()); c = [v.count(i) for i in rng]; a.bar(rng, c, color=col); a.set_xticks(list(rng)); a.set_title(ttl, fontsize=8); a.set_ylabel('count')
hist(ax[0], ds, C['a'], f'$d(n,n+1)$, $n\\leq{max(ds)}$', range(2, 7))
hist(ax[1], dq, C['b'], f'$d(n^2,(n+1)^2)$, $n\\leq{max(dq)}$', range(1, 6))
hist(ax[2], pdist, C['p'], '$d(p,p^+)$, $p<400$', range(4, 9))
byres = [np.mean([ds[n] for n in ds if n % 24 == r]) for r in range(24)]
ax[3].bar(range(24), byres, color=C['a']); ax[3].set_xlabel('$n$ mod 24'); ax[3].set_title('mean $d(n,n+1)$ by residue', fontsize=8); ax[3].set_ylim(2, 6)
for a in ax[:3]: a.set_xlabel('distance')
plt.tight_layout(); save('fig5_distributions')

# ---------- Fig 6: worked identity trajectories
t = sp.symbols('t')
def traj_succ(name, tv):
    d = next(x for x in U1 if x['name'] == name); n = int(sp.sympify(d['n'], locals={'t': t}).subs(t, tv))
    xs = [n]; labs = []
    for s in d['steps']:
        N = int(sp.sympify(s['N'], locals={'t': t}).subs(t, tv)); sg = '+' if s['direction'] == 'forward' else '-'
        xs.append(move(xs[-1], sg, N)); labs.append(f'{sg}{N}')
    return xs, labs
SQ = json.load(open(f'{INH}/u2sq_square_identities.json'))
def traj_sq(n):
    r = n % 24; tv = n // 24; xs = [n * n]; labs = []
    for sg, e in SQ['classes'][str(r)]['steps']:
        N = int(sp.sympify(e, locals={'t': t}).subs(t, tv)); xs.append(move(xs[-1], sg, N)); labs.append(f'{sg}{N}')
    return xs, labs
items = [('successor, $n=163$ (class I, $t=6$)', *traj_succ('I', 6)), ('successor, $n=8t+7$ with $t=20$ (class G)', *traj_succ('G', 20)), ('squares, $23^2\\to24^2$ (identity $r=23$)', *traj_sq(23))]
fig, ax = plt.subplots(1, 3, figsize=(10.4, 3.0))
for a, (ttl, xs, labs) in zip(ax, items):
    a.plot(range(len(xs)), [math.log10(x) for x in xs], '-', color='#bbb', zorder=1)
    for i, x in enumerate(xs):
        a.scatter([i], [math.log10(x)], s=22, color=C['a'], zorder=2); a.annotate(str(x) if x < 10**8 else f'{x:.1e}', (i, math.log10(x)), textcoords='offset points', xytext=(0, 6), fontsize=5.5, ha='center')
    for i, l in enumerate(labs):
        a.text(i + .5, (math.log10(xs[i]) + math.log10(xs[i + 1])) / 2 - 0.0, l, fontsize=6, color=C['fwd'] if l[0] == '+' else C['inv'], ha='center', va='top' if True else 'bottom')
    a.set_title(ttl, fontsize=8); a.set_xlabel('step'); a.set_ylabel('$\\log_{10}$ of state'); a.margins(y=.18)
plt.tight_layout(); save('fig6_worked_paths')

# ---------- Fig 7: power lifting schematic
x, y, N = 3, 16, 3; k = 3
fig, ax = plt.subplots(figsize=(7.2, 2.2))
chain = [x ** (k - j) * y ** j for j in range(k + 1)]
for i, v in enumerate(chain):
    ax.scatter([i], [0], s=1500, color='#cfe0f1', edgecolor='#333', zorder=2)
    ax.text(i, 0, f'$x^{{{k-i}}}y^{{{i}}}$' if 0 < i < k else (f'$x^{k}$' if i == 0 else f'$y^{k}$'), ha='center', va='center', fontsize=10)
    ax.text(i, -.33, f'{v}', ha='center', fontsize=8, color='#444')
for i in range(k):
    ax.annotate('', (i + .22, 0), (i + .78, 0), arrowprops=dict(arrowstyle='<->', color='#555'))
    ax.text(i + .5, .13, f'$+{N}$', ha='center', fontsize=9, color=C['fwd'])
ax.set_xlim(-.5, k + .5); ax.set_ylim(-.5, .5); ax.axis('off')
ax.set_title(f'Power lifting along the edge $x={x}\\sim y={y}$ ($N={N}$): the chain of $k={k}$ edges from $x^k$ to $y^k$', fontsize=9)
save('fig7_power_lifting')

# ---------- Fig 8: primes
fig, ax = plt.subplots(1, 2, figsize=(10, 3.2))
for a, (p, q, dd) in zip(ax, [(61, 67, 7), (661, 673, 8)]):
    pth = geodesic(p, q, dd)
    for i, v in enumerate(pth):
        a.scatter([i], [math.log10(v)], s=26, color=C['p'] if i in (0, len(pth) - 1) else C['a'], zorder=2)
        a.annotate(str(v), (i, math.log10(v)), textcoords='offset points', xytext=(0, 6), fontsize=6, ha='center')
    a.plot(range(len(pth)), [math.log10(v) for v in pth], color='#bbb', zorder=1)
    for i in range(len(pth) - 1):
        l = lab(pth[i], pth[i + 1]); a.text(i + .5, (math.log10(pth[i]) + math.log10(pth[i + 1])) / 2, l, fontsize=6, color=C['fwd'] if l[0] == '+' else C['inv'], ha='center', va='top')
    a.set_title(f'a shortest path from the prime {p} to the prime {q} (length {dd})', fontsize=8); a.set_xlabel('step'); a.set_ylabel('$\\log_{10}$ of state'); a.margins(y=.2)
plt.tight_layout(); save('fig8_prime_paths')

# ---------- Fig 9: ball growth
fig, ax = plt.subplots(figsize=(4.8, 3.2))
for v, c in zip((1, 2, 6, 30, 163), ['#3b6ea5', '#c98b2b', '#2a7f62', '#7a5195', '#b5473a']):
    sizes = [len(ball(v, r)) for r in range(0, 5)]
    ax.semilogy(range(5), sizes, 'o-', ms=3, color=c, label=f'$v={v}$')
ax.set_xlabel('radius $r$'); ax.set_ylabel('$|B_r(v)|$'); ax.legend(frameon=False, fontsize=7); ax.set_title('Ball growth', fontsize=9)
save('fig9_ball_growth')

# ---------- Fig 10: Fibonacci
CC = json.load(open(f'{INH}/u2fpsym_class_certificates.json'))
F = [0, 1]
for _ in range(400): F.append(F[-1] + F[-2])
bsym = sp.symbols('b')
fig, ax = plt.subplots(1, 2, figsize=(10, 3.0))
ax[0].bar(range(12), [len(CC[str(r)]['labels']) for r in range(12)], color=C['a']); ax[0].set_xticks(range(12))
ax[0].set_xlabel('$k$ mod 12'); ax[0].set_ylabel('moves of the certified route'); ax[0].axhline(12, color=C['g'], ls=':'); ax[0].set_title('(a) certified route lengths (max 12)', fontsize=8)
for k, col in [(100, C['a']), (101, C['b']), (103, C['fwd']), (107, C['p'])]:
    r = k % 12; c = CC[str(r)]; h = k // 2; A_, B_ = F[h - 1], F[h]; xx = F[k]; tr = [xx]
    for sg_, pair in zip([l[0] for l in c['labels']], c['labels_ring']):
        N_ = int(sp.sympify(pair[0], locals={'b': bsym}).subs(bsym, B_) + sp.sympify(pair[1], locals={'b': bsym}).subs(bsym, B_) * A_)
        xx = move(xx, sg_, N_); tr.append(xx)
    assert xx == F[k + 1]
    ax[1].plot(range(len(tr)), [math.log(v) / math.log(F[k]) for v in tr], 'o-', ms=3, color=col, label=f'$k={k}$ (class {r})')
ax[1].set_xlabel('step'); ax[1].set_ylabel('$\\log(\\text{state})/\\log F_k$'); ax[1].legend(frameon=False, fontsize=7); ax[1].set_title('(b) intermediate states rise to a small power of $F_k$', fontsize=8)
plt.tight_layout(); save('fig10_fibonacci')
print('figures ok')
