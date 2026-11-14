import json, os, math, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from graphent import *
from paths import *
plt.rcParams.update({'font.size': 9, 'font.family': 'serif', 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150})
C1, C2, C3, C4 = '#1f4e79', '#c0504d', '#4f8a3c', '#7f7f7f'
def save(f, n): f.savefig(os.path.join(FIG, n), bbox_inches='tight'); plt.close(f)

# Fig 1: the 4-cycle word and arithmetic labels
f, ax = plt.subplots(figsize=(4.8, 3.4))
pos = {2: (0, 1), 8: (2, 1), 36: (2, 0), 9: (0, 0)}
edges = [(2, 8, r'$N{=}1$: $\times 4$', (1, 1.14), 'center'), (9, 36, r'$N{=}1$: $\times 4$', (1, -0.14), 'center'),
         (2, 9, r'$N{=}2$: $\times 9/2$', (-0.12, .5), 'right'), (8, 36, r'$N{=}2$: $\times 9/2$', (2.12, .5), 'left')]
for u, v, lab, tp, ha in edges:
    (x0, y0), (x1, y1) = pos[u], pos[v]
    ax.plot([x0, x1], [y0, y1], color=C1, lw=1.8, zorder=1); ax.text(tp[0], tp[1], lab, ha=ha, va='center', fontsize=8, color=C4)
for v, (x, y) in pos.items():
    ax.scatter([x], [y], s=520, color='white', edgecolor=C1, lw=1.8, zorder=2); ax.text(x, y, str(v), ha='center', va='center', zorder=3)
ax.set_xlim(-1.3, 3.3); ax.set_ylim(-0.4, 1.4); ax.axis('off')
ax.set_title(r'The 4-cycle $2-8-36-9$: word $U_1U_2D_1D_2$ (scaling by 4 commutes with $U_2$)', fontsize=8.5)
save(f, 'fig1_four_cycle.pdf')

# Fig 2: F_m drawn (m=3 and m=6)
def draw_theta(ax, m, x=None):
    ax.scatter([0, 4], [0, 0], s=160, color=C1, zorder=3); ax.plot([0, 4], [0, 0], color=C2, lw=2.2, zorder=1)
    ax.text(0, -0.28, r'$x$', ha='center'); ax.text(4, -0.28, r'$4x$', ha='center')
    ys = np.linspace(-1, 1, m) * (1.3 if m > 1 else 0) + 0
    for j, yy in enumerate(np.linspace(0.45, 2.4, m)):
        ax.plot([0, 1.3, 2.7, 4], [0, yy, yy, 0], color=C3, lw=1.1, zorder=1)
        ax.scatter([1.3, 2.7], [yy, yy], s=22, color='white', edgecolor=C3, zorder=2)
f, axs = plt.subplots(1, 2, figsize=(8.2, 2.8))
for ax, m in zip(axs, (3, 8)):
    draw_theta(ax, m); ax.set_title(f'$F_{{{m}}}$: hub edge $x$---$4x$ and {m} paths of length 3', fontsize=9); ax.axis('off'); ax.set_ylim(-0.6, 2.7)
save(f, 'fig2_Fm_theta.pdf')

# Fig 3: arithmetic labelled F_3 (x=8)
x = 8; V = F_vertices(x); f, ax = plt.subplots(figsize=(5.6, 3.3))
ax.scatter([0, 4], [0, 0], s=620, color='white', edgecolor=C1, lw=1.8, zorder=3); ax.plot([0, 4], [0, 0], color=C2, lw=2.2, zorder=1)
ax.text(0, 0, '8', ha='center', va='center', zorder=4); ax.text(4, 0, '32', ha='center', va='center', zorder=4)
ax.text(2, -0.18, '$N=1$ (scaling edge)', ha='center', fontsize=8, color=C2)
ys = [0.9, 1.7, 2.5]
for N, yy in zip([2, 4, 8], ys):
    y = x * (N + 1) ** 2 // N
    ax.plot([0, 1.3, 2.7, 4], [0, yy, yy, 0], color=C3, lw=1.1, zorder=1)
    ax.scatter([1.3, 2.7], [yy, yy], s=620, color='white', edgecolor=C3, zorder=3)
    ax.text(1.3, yy, str(y), ha='center', va='center', fontsize=8, zorder=4); ax.text(2.7, yy, str(4 * y), ha='center', va='center', fontsize=8, zorder=4)
    ax.text(2, yy + 0.2, f'$N={N}$', ha='center', fontsize=8, color=C4)
ax.set_xlim(-0.5, 4.5); ax.set_ylim(-0.5, 3.0); ax.axis('off'); ax.set_title(r'$F(8)=F_3$ in $G$: $y_N=8(N{+}1)^2/N$, $N\mid 8$, $N\geq 2$', fontsize=9)
save(f, 'fig3_F8_labelled.pdf')

# Fig 4: entropy vs bounds
ms = np.arange(2, 401); lam = [float(lam_m(int(m))) for m in ms]
h = np.log(lam)
f, ax = plt.subplots(figsize=(5.4, 3.4))
ax.plot(ms, np.log(ms), color=C4, ls='--', label=r'$\log m$ (max-degree bound)')
ax.plot(ms, h, color=C1, lw=2, label=r'$h_{\rm NB}(F_m)=\log\lambda_m$')
ax.plot(ms, np.log(ms) / 3, color=C2, ls=':', label=r'$\frac{1}{3}\log m$')
ax.plot(ms, np.log(ms) / 4, color=C3, ls='-.', label=r'$\frac{1}{4}\log m$ (inherited lower bound)')
ax.set_xscale('log'); ax.set_xlabel('$m$'); ax.set_ylabel('entropy (nats)'); ax.legend(frameon=False, fontsize=8)
save(f, 'fig4_entropy_curves.pdf')

# Fig 5: gap
f, ax = plt.subplots(figsize=(5, 3))
ax.plot(ms, h - np.log(ms) / 3, color=C1, label=r'$\log\lambda_m-\frac{1}{3}\log m$'); ax.plot(ms, 1 / (3 * ms ** (1 / 3)), color=C2, ls='--', label=r'$1/(3m^{1/3})$')
ax.set_xscale('log'); ax.set_xlabel('$m$'); ax.legend(frameon=False); save(f, 'fig5_gap.pdf')

# Fig 6: spectrum of B_m (m=5)
f, axs = plt.subplots(1, 2, figsize=(7.6, 3.4))
for ax, m in zip(axs, (3, 9)):
    de, B = nb_matrix(Fm_edges(m)); w = np.linalg.eigvals(B.astype(float))
    t = np.linspace(0, 2 * np.pi, 400); ax.plot(np.cos(t), np.sin(t), color=C4, lw=.6)
    ax.scatter(w.real, w.imag, s=22, color=C1, zorder=3); L = float(lam_m(m)); ax.plot(L * np.cos(t), L * np.sin(t), color=C2, lw=.6, ls=':')
    ax.set_aspect('equal'); ax.set_title(f'spectrum of $B_{{{m}}}$ ($\\lambda_{{{m}}}={L:.4f}$)', fontsize=9); ax.axhline(0, color='k', lw=.3); ax.axvline(0, color='k', lw=.3)
save(f, 'fig6_spectrum.pdf')

# Fig 7: periodic path counts
pc = json.load(open(os.path.join(DATA, 'prime_counts.json')))
f, ax = plt.subplots(figsize=(5.4, 3.3))
for m, col in zip((2, 3, 4, 6, 8), (C1, C2, C3, C4, '#8064a2')):
    ns = list(range(1, 25)); y = [max(pc[f'{m},{n}'], 0.5) for n in ns]
    ax.plot(ns, y, marker='o', ms=3, color=col, label=f'$m={m}$')
ax.set_yscale('log'); ax.set_xlabel('$n$'); ax.set_ylabel(r'primitive closed NB walks $\pi_n$'); ax.legend(frameon=False, ncol=2, fontsize=8)
save(f, 'fig7_periodic_counts.pdf')

# Fig 8: max entropy chain (m=4), schematic
lam4 = float(lam_m(4)); m = 4
f, ax = plt.subplots(figsize=(5.2, 3.9)); ax.axis('off')
ax.add_patch(plt.Circle((0, 0), .45, fc='white', ec=C2, lw=2)); ax.text(0, 0, 'D', ha='center', va='center', fontsize=12)
for j in range(m):
    ang = np.pi / 2 - (j + .5) * np.pi / m * 1.0 + np.pi / 2 * 0; px, py = 3.2, 1.2 - j * .95
    ax.add_patch(plt.Circle((px, py), .36, fc='white', ec=C3, lw=1.5)); ax.text(px, py, f'$P_{j+1}$', ha='center', va='center')
    ax.add_patch(FancyArrowPatch((.45, 0.05), (px - .36, py), arrowstyle='->', mutation_scale=9, color=C4, lw=.8, connectionstyle='arc3,rad=0.1'))
ax.text(1.7, 1.75, r'probability $1/m$ each', ha='center', fontsize=8, color=C4)
pd = m / (m + (m - 1) * lam4); pp = (m / lam4) / ((m / lam4) + (m - 1)) if False else None
ax.text(-.2, -1.1, f'$P_i\\to D$: {pd:.3f}', fontsize=8); ax.set_xlim(-1, 4); ax.set_ylim(-1.8, 2.2)
ax.set_title(f'Maximal-entropy chain on the label shift of $F_4$ ($\\lambda_4={lam4:.4f}$)', fontsize=9)
save(f, 'fig8_chain.pdf')

# Fig 9: three dynamics schematic
f, ax = plt.subplots(figsize=(7.4, 2.6)); ax.axis('off')
boxes = [(0.0, 'Forward arithmetic', 'strictly increasing\nno periodic orbits', C1), (0.35, 'Autonomous selection', 'MAXPP: Sturmian\n$p(k)=k+1$, entropy $0$', C3), (0.70, 'Reversible histories', 'NB entropy $\\geq\\frac{1}{3}\\log m$\n$H_{\\rm fin}=\\infty$', C2)]
for x0, t, s, c in boxes:
    ax.add_patch(plt.Rectangle((x0, .2), .30, .6, fc='white', ec=c, lw=1.8, transform=ax.transAxes)); ax.text(x0 + .15, .68, t, ha='center', fontsize=8.5, weight='bold', color=c, transform=ax.transAxes); ax.text(x0 + .15, .42, s, ha='center', va='center', fontsize=8, transform=ax.transAxes)
for a, b in [(.305, .345), (.655, .695)]:
    ax.annotate('', xy=(b, .5), xytext=(a, .5), xycoords='axes fraction', arrowprops=dict(arrowstyle='<->', color=C4))
save(f, 'fig9_three_dynamics.pdf')

# Fig 10: window entropies
w = json.load(open(os.path.join(DATA, 'window_entropy.json')))
f, ax = plt.subplots(figsize=(5, 3)); ax.plot([r[0] for r in w], [r[3] for r in w], marker='o', color=C1); ax.set_xscale('log'); ax.set_xlabel('$X$'); ax.set_ylabel(r'$h_{\rm NB}(G[1,X])$'); save(f, 'fig10_window_entropy.pdf')
print('figures ok', os.listdir(FIG))

# Fig 11: pipeline
f, ax = plt.subplots(figsize=(7.6, 1.9)); ax.axis('off')
labs = ['UNNS arithmetic\ngraph $G$', 'admissible\nhistories $X_{\\rm NB}$', 'exact spectral\ndynamics $B_{F_m}$', 'unbounded entropy\ncapacity $H_{\\rm fin}=\\infty$']
cols = [C1, C3, C4, C2]
for i, (t, c) in enumerate(zip(labs, cols)):
    x0 = i * 0.255
    ax.add_patch(plt.Rectangle((x0, .15), .2, .7, fc='white', ec=c, lw=1.8, transform=ax.transAxes)); ax.text(x0 + .1, .5, t, ha='center', va='center', fontsize=8, transform=ax.transAxes)
    if i < 3: ax.annotate('', xy=(x0 + .25, .5), xytext=(x0 + .205, .5), xycoords='axes fraction', arrowprops=dict(arrowstyle='->', color=C4))
save(f, 'fig11_pipeline.pdf')

# Fig 12: subdominant ratio and direct-edge mass
ms2 = np.arange(2, 301); L2 = np.array([float(lam_m(int(m))) for m in ms2])
f, axs = plt.subplots(1, 2, figsize=(8.4, 3.0))
axs[0].plot(ms2, np.sqrt(ms2 / L2) / L2, color=C1, label=r'$\sqrt{m/\lambda_m}/\lambda_m$'); axs[0].plot(ms2, 1 - 1 / (2 * L2), color=C2, ls='--', label=r'$1-1/(2\lambda_m)$'); axs[0].set_xscale('log'); axs[0].set_xlabel('$m$'); axs[0].legend(frameon=False, fontsize=8); axs[0].set_title('subdominant / dominant modulus', fontsize=9)
axs[1].plot(ms2, ms2 / (ms2 + 3 * L2 ** 4), color=C1); axs[1].set_xscale('log'); axs[1].set_xlabel('$m$'); axs[1].set_title(r'time on the direct edge: $m/(m+3\lambda_m^4)$', fontsize=9)
save(f, 'fig12_gap_mass.pdf')

# Fig 13: ratios of NB walk counts
f, ax = plt.subplots(figsize=(5.4, 3.2))
for m, col in zip((2, 4, 8), (C1, C2, C3)):
    de, B = nb_matrix(Fm_edges(m)); v = np.ones(len(de)); c = []
    for n in range(40): c.append(v.sum()); v = B.astype(float).dot(v); v = v / v.max(); 
    # recompute with unnormalised counts via logs
    v = np.ones(len(de)); cnts = []
    for n in range(40):
        cnts.append(v.sum()); v = B.astype(float).dot(v)
    r = [math.sqrt(cnts[n + 2] / cnts[n]) for n in range(36)]
    ax.plot(range(1, 37), r, color=col, label=f'$m={m}$'); ax.axhline(float(lam_m(m)), color=col, ls=':', lw=.8)
ax.set_xlabel('$n$'); ax.set_ylabel(r'$\sqrt{a_{n+2}/a_n}$'); ax.legend(frameon=False); save(f, 'fig13_count_ratios.pdf')
print('figs 11-13 ok')
