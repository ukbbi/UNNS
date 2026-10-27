"""GEO-I v006 figures, generated from exact data (shipped JSON + exact recomputation).  usage: figures_v6.py"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(ROOT, d_))
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from math import gcd
import modular_layers as ML, binary_01 as B
DATA = os.path.join(ROOT, 'output', 'data'); FIG = os.path.join(ROOT, 'figures'); os.makedirs(FIG, exist_ok=True)
rows = lambda p: [json.loads(l) for l in open(p)]
inv = lambda s, d: next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)

# F1 proved vs unresolved parameter classes
import glob
win = {(r['d'], r['s']) for f in glob.glob(os.path.join(DATA, 'window_full_*.jsonl')) for r in rows(f) if not r['unresolved']}
part = {(r['d'], r['s']) for fn in ('general_s_d2_14.jsonl', 'general_s_d15_70.jsonl') for r in rows(os.path.join(DATA, fn)) if r['n_bad'] == 0}
fig, ax = plt.subplots(figsize=(8.5, 6)); dm = 37
for d in range(2, dm + 1):
    for s in range(1, d):
        if gcd(s, d) != 1: continue
        key = (d, s) if inv(s, d) >= s else (d, inv(s, d))
        if s in (1, d - 1): c = '#1b7837'
        elif d <= 21 or key in win: c = '#5aae61'
        elif key in part: c = '#c2e699'
        else: c = '#d9d9d9'
        ax.scatter(d, s, s=9, c=c, marker='s')
for c, l in (('#1b7837', 's = +-1: PROVED for all d (v005)'), ('#5aae61', 'other s: complete window CHECKED (d<=21 v005, 22..30 v006)'), ('#c2e699', 'other s: small boxes CHECKED + random audits (d=31..37 partial)'), ('#d9d9d9', 'not run (UNAVAILABLE)')):
    ax.plot([], [], 's', c=c, label=l)
ax.set_xlabel('d'); ax.set_ylabel('s (units mod d)'); ax.legend(loc='upper left', fontsize=7)
ax.set_title('G6-C1: status of U = conv(F) by (d,s)'); fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig1_stabilization_status.png'), dpi=140); plt.close(fig)

# F2 proof cells of the cover (exact)
fig, axs = plt.subplots(1, 2, figsize=(11, 5))
for ax, (d, s, Q) in zip(axs, [(11, 4, (30, 30)), (13, 5, (26, 40))]):
    cells, reg = ML.proof_cells(d, s, Q); F = ML.fibre(d, s, Q)
    for (u, gg, hh) in cells:
        P = [u, (u[0] + gg[0], u[1] + gg[1]), (u[0] + gg[0] + hh[0], u[1] + gg[1] + hh[1]), (u[0] + hh[0], u[1] + hh[1])]
        sq = (abs(gg[0]) == d and gg[1] == 0 and hh[0] == 0 and abs(hh[1]) == d) or (abs(hh[0]) == d and hh[1] == 0 and gg[0] == 0 and abs(gg[1]) == d)
        ax.add_patch(Polygon(P, closed=True, fc='#9ecae1' if sq else '#fd8d3c', ec='k', lw=.3, alpha=.45))
    ax.scatter(*zip(*F), s=5, c='k'); ax.set_xlim(-1, Q[0] + 1); ax.set_ylim(-1, Q[1] + 1); ax.set_aspect('equal')
    ax.set_title('(d,s)=(%d,%d), Q=%s, %s: %d cells (squares blue, sail/chain orange)' % (d, s, Q, reg, len(cells)), fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig2_modular_layers_cover.png'), dpi=140); plt.close(fig)

# F3 hollow box
import coverage as C
from lattice_model import Lat
hs = json.load(open(os.path.join(DATA, 'hollow_general_s.json')))
fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
d, s = 13, 5; t = inv(s, d); pcs = C.uncovered(Lat(d, d, d, s), (d, d)); ax = axs[0]
for p in pcs: ax.add_patch(Polygon([(float(x), float(y)) for x, y in p], closed=True, fc='#de2d26', alpha=.6, ec='k', lw=.5))
F = ML.fibre(d, s, (d, d)); ax.scatter(*zip(*F), c='k', s=14); ax.set_xlim(-1, d + 1); ax.set_ylim(-1, d + 1); ax.set_aspect('equal')
ax.set_title('uncovered part of conv(F) at Q=(d,d), (d,s)=(13,5): the two triangles T1,T2 (area d/2 each)', fontsize=8)
ax = axs[1]; xs = [r for r in hs['rows'] if 'beta1' in r]
ax.scatter([r['d'] for r in xs], [r['beta1'] for r in xs], s=6, label='beta1, s != -1 (all = 2)'); ax.plot(range(3, 21), range(3, 21), 'r--', label='s = -1: beta1 = d (v005)')
ax.set_xlabel('d'); ax.set_ylabel('beta_1(U at (d,d))'); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig3_hollow_box_homology.png'), dpi=140); plt.close(fig)

# F4 min witness rank vs number of coordinates
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4)); ax = axs[0]
ns = list(range(4, 9)); cnt = []
for n in ns:
    r = json.load(open(os.path.join(DATA, 'binrank_n%d.json' % n))); cnt.append(sum(r['minimal_boxes_by_min_span'].values()))
ax.bar([n - .2 for n in ns], cnt, .4, label='minimal boxes found (all with min span 3)'); ax.set_yscale('log'); ax.set_xlabel('coordinates n'); ax.set_ylabel('# minimal 0/1 boxes (binary lattices)')
ax2 = ax.twinx(); ax2.plot(ns, [3] * len(ns), 'ro-', label='max over census of min witness span'); ax2.set_ylim(0, 6); ax2.set_ylabel('min witness span'); ax.legend(loc='upper left', fontsize=7); ax2.legend(loc='upper right', fontsize=7)
ax.set_title('census (completeness: n<=6 full; n=7 rank<=4; n=8 rank<=3)', fontsize=8)
ax = axs[1]
for n, col in ((4, 'C0'), (5, 'C1'), (6, 'C2')):
    h = B.analyse([1] * n)['span_hist']; ks = sorted(h); ax.bar([k + (n - 5) * .25 for k in ks], [h[k] for k in ks], .25, label='parity n=%d (min span %d)' % (n, min(ks)))
ax.set_xlabel('witness span'); ax.set_ylabel('# witnesses'); ax.set_yscale('log'); ax.legend(fontsize=8); ax.set_title('minimum vs individual witness span (parity lattices at 1^n)', fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig4_witness_rank_vs_dimension.png'), dpi=140); plt.close(fig)

# F5 4/5/6-coordinate examples
fig, axs = plt.subplots(1, 3, figsize=(12, 3.8))
for ax, n in zip(axs, (4, 5, 6)):
    a = B.analyse([1] * n); h = a['span_hist']; ax.bar([str(k) for k in sorted(h)], [h[k] for k in sorted(h)], color='C%d' % (n - 4))
    ax.set_title('parity, n=%d, box 1^n: %d witnesses, min span %d, support %s' % (n, a['n_witnesses'], a['min_span'], a['support_sizes']), fontsize=8); ax.set_xlabel('witness span'); ax.set_ylabel('count')
fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig5_four_five_six_coordinate_examples.png'), dpi=140); plt.close(fig)

# F6 certification vs enumeration
cb = json.load(open(os.path.join(DATA, 'cert_benchmark.json'))); fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
lab = ['%d/%d %s' % (r['d'], r['s'], tuple(r['Q'])) for r in cb]; x = range(len(cb))
axs[0].bar([i - .2 for i in x], [r['proof_cells'] for r in cb], .4, label='proof-cell certificate'); axs[0].bar([i + .2 for i in x], [r.get('generic_2cells', 0) for r in cb], .4, label='all 2-cells (generic)')
axs[0].set_yscale('log'); axs[0].set_xticks(list(x)); axs[0].set_xticklabels(lab, rotation=60, fontsize=6); axs[0].legend(fontsize=7); axs[0].set_ylabel('cells'); axs[0].set_title('certificate size (generic not run for d>21 or large Q)', fontsize=8)
axs[1].scatter([r['fibre'] for r in cb], [r['proof_seconds'] for r in cb], label='proof-cell'); axs[1].scatter([r['fibre'] for r in cb if 'generic_seconds' in r], [r['generic_seconds'] for r in cb if 'generic_seconds' in r], label='generic')
axs[1].set_xlabel('|F|'); axs[1].set_ylabel('seconds'); axs[1].legend(fontsize=8); fig.tight_layout(); fig.savefig(os.path.join(FIG, 'fig6_certification_vs_enumeration.png'), dpi=140); plt.close(fig)
print('figures written')
