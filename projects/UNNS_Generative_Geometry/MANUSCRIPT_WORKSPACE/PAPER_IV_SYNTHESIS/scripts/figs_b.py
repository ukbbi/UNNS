import sys, itertools; sys.path.insert(0, '.')
from figlib4 import *
import hist, eng3, trans3
from fractions import Fraction as Fr
def Tm(m, w):
    for N in w: m = m*(N+1)**2//N
    return m
# ---------------- Fig 9 abstract loss vs realised containment (Paper I Prop. topology (b), cited finite-exact)
fig, ax = newfig(2.9, (0, 12.4, 0, 5.6))
mbox(ax, 0.2, 3.3, 4.6, 1.6, "abstract complex\n$\\mathrm{K_{abs}}(\\Lambda,Q)$\n$\\beta=(1,5,0)$", "space", 6.6)
mbox(ax, 7.6, 3.3, 4.6, 1.6, "abstract complex\n$\\mathrm{K_{abs}}(\\Lambda',Q)$\n$\\beta=(1,2,6)$", "space", 6.6)
mbox(ax, 0.2, 0.5, 4.6, 1.6, "realised union $U$\n$\\beta=(1,2,0)$", "obj", 6.6)
mbox(ax, 7.6, 0.5, 4.6, 1.6, "realised union $U'\\supsetneq U$\n$\\beta=(1,0,0)$", "obj", 6.6)
sarrow(ax, (4.8, 4.1), (7.6, 4.1), 'est', "8 edges and a square lost abstractly", off=(0, 0.35))
sarrow(ax, (4.8, 1.3), (7.6, 1.3), 'est', "all lost cells lie in $U'$", off=(0, 0.35))
sarrow(ax, (2.5, 3.3), (2.5, 2.1), 'obs', "")
sarrow(ax, (9.9, 3.3), (9.9, 2.1), 'obs', "")
ax.text(6.2, 2.7, "no inclusion of $\\mathrm{K_{abs}}$ into $U$ is a homotopy equivalence", fontsize=6.0, ha="center")
tag(ax, "specimen $21^8/5\\to21^8/4$ (Paper I Prop. topology(b), FINITE-EXACT, cited not recomputed)")
save(fig, "fig09_abstract_vs_realised")
# ---------------- Fig 10 swap graphs for {2,3,14}
def swapgraph(m):
    perms = [p for p in itertools.permutations((2, 3, 14)) if hist.admissible(m, p)]
    E = []
    for p in perms:
        for i in range(2):
            q = p[:i]+(p[i+1], p[i])+p[i+2:]
            if q in perms and p < q: E.append((p, q))
    return perms, E
fig, axs = plt.subplots(1, 3, figsize=(W, 2.5))
DATA = {}
for ax, m in zip(axs, (14, 28, 21)):
    perms, E = swapgraph(m); n = len(perms)
    ax.set_aspect("equal"); ax.axis("off")
    pos = {p: (math.cos(2*math.pi*i/max(n, 1)+0.5), math.sin(2*math.pi*i/max(n, 1)+0.5)) for i, p in enumerate(perms)}
    for p, q in E: seg(ax, pos[p], pos[q], c="#555")
    for p in perms: node(ax, *pos[p], "".join(f"{a}," for a in p)[:-1], r=0.0, fs=5.4, ec="none")
    for p in perms: ax.plot(*pos[p], "o", c=SRC, ms=3.2, zorder=1)
    # components
    par = {p: p for p in perms}
    def f(a):
        while par[a] != a: a = par[a]
        return a
    for p, q in E: par[f(p)] = f(q)
    nu = len({f(p) for p in perms})
    ax.set_title(f"$m={m}$: {n} admissible orders, $\\nu={nu}$", fontsize=6.6)
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.5, 1.5)
    DATA[m] = (n, len(E), nu)
fig.text(0.5, 0.0, "exact: vertices = admissible orderings of $\\{2,3,14\\}$ at source $m$; edges = legal adjacent swaps (Paper II Thm. 2314)", ha="center", fontsize=6)
save(fig, "fig10_swap_components")
json.dump({str(k): v for k, v in DATA.items()}, open("../results/fig10_data.json", "w"))
# ---------------- Fig 11 loop and void: route cube of 72^r
fig, axs = plt.subplots(1, 2, figsize=(W, 2.8))
ax = axs[0]; ax.set_aspect("equal"); ax.axis("off")
H2 = [(1, 1) + b for b in itertools.product(((1, 2), (2, 1)), repeat=2) for b in [sum(b, ())]] if False else []
words = []
for b1 in ((1, 2), (2, 1)):
    for b2 in ((1, 2), (2, 1)): words.append((1, 1) + b1 + b2)
for w in words: assert hist.admissible(1, w) and Tm(1, w) == 72**2
pos = {words[0]: (0, 0), words[1]: (1.6, 0), words[3]: (1.6, 1.6), words[2]: (0, 1.6)}
for p, q in ((words[0], words[1]), (words[1], words[3]), (words[3], words[2]), (words[2], words[0])): seg(ax, pos[p], pos[q], c="#555")
for w, (x, y) in pos.items():
    node(ax, x, y, "", r=0.09, fc=SRC_L, ec=SRC); ax.text(x+(0.15 if x > 0.5 else -0.15), y+(0.22 if y > 0.5 else -0.22), "".join(map(str, w)), fontsize=6, ha="left" if x > 0.5 else "right")
ax.set_title("the 2-cube of histories $1\\to72^2$ (Paper II Thm. cube)", fontsize=6.8); ax.set_xlim(-1.4, 3.0); ax.set_ylim(-0.8, 2.3)
n_all = len(hist.histories(1, 72**2))
ax.text(0.8, -0.7, f"all histories $1\\to5184$: {n_all}", ha="center", fontsize=6)
ax = axs[1]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
mbox(ax, 0.3, 3.6, 9.4, 1.9, "combinatorial cube (4-cycle of legal swaps,\nfilled as a 2-cell in the route complex)", "obj", 6.4)
mbox(ax, 0.3, 0.6, 9.4, 2.2, "homology of the full route complex needs more:\nloops and voids are recorded by Paper II\n(Thms. sphere, loopfam); not derived here", "open", 6.4)
sarrow(ax, (5, 3.6), (5, 2.8), 'open')
save(fig, "fig11_loop_void")
# ---------------- Fig 12 endpoint move complex vs history complex
fig, axs = plt.subplots(1, 3, figsize=(W, 2.6), gridspec_kw={'width_ratios': [1.2, 1.2, 1.4]})
ax = axs[0]; ax.set_aspect("equal"); ax.axis("off")
D = eng3.Dset(72); K = eng3.complex_of(D); draw_complex(ax, D, K, scale=0.9, r=0.2); ax.set_title("$K(D(72))$: path $2-6-3$", fontsize=6.6); ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.3, 1.3)
ax = axs[1]; ax.set_aspect("equal"); ax.axis("off")
H = [(1, w) for w in hist.histories(1, 72)]
pos = {H[0]: (-0.8, 0), H[1]: (0.8, 0)}
seg(ax, pos[H[0]], pos[H[1]], c="#555")
for (m0, w), (x, y) in pos.items() if False else [(h, pos[h]) for h in H]:
    node(ax, x, y, "", r=0.09, fc=SRC_L, ec=SRC); ax.text(x, y-0.3, ",".join(map(str, w[1] if isinstance(w, tuple) and len(w) == 2 and isinstance(w[1], tuple) else w)), fontsize=6, ha="center")
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1, 1); ax.set_title("swap graph of $1\\to72$ (two vertices)", fontsize=6.6)
ax = axs[2]; ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 6)
mbox(ax, 0.2, 3.6, 9.6, 2.0, "$K(D(t))$ depends on $t$ only through $D(t)$", "obj", 6.2)
mbox(ax, 0.2, 0.4, 9.6, 2.6, "$D(900)=D(9000)$ but source 4 gives\n(2 histories, 1 class) vs (4, 2)\n$\\Rightarrow$ no map $K(D(t))\\to$ history topology\n(SIV-P5)", "result", 6.0)
sarrow(ax, (5, 3.6), (5, 3.0), 'obs')
save(fig, "fig12_endpoint_vs_history")
# ---------------- Fig 13 prediction of the next occurrence event (tower orbit)
x = Fr(126*126, 5); xs = []; Dn = []
for n in range(13):
    xs.append(x); Dn.append(len(eng3.Dset(x)))
    x = eng3.C(x)
fig, ax = plt.subplots(figsize=(W, 2.5))
ax.step(range(13), Dn, where="post", c=SRC, lw=1.4); ax.plot(range(13), Dn, "o", c=SRC, ms=3)
for n in range(1, 13):
    if Dn[n] > Dn[n-1]: ax.axvline(n, c=KEEP, lw=0.8, ls=":"); ax.text(n, Dn[n]+1.2, "event", fontsize=5.5, ha="center", color=KEEP)
ax.set_xlabel("collective step $n$"); ax.set_ylabel("$|D(x_n)|$"); ax.grid(alpha=0.3, lw=0.4)
ax.set_title("orbit of $x_0=126^2/5$: $D$ is monotone (Lemma M); event steps are predicted by Paper III Thm. sieve (computed by direct iteration)", fontsize=6.6)
DATA = {"x0": "126^2/5", "sizes": Dn}; json.dump(DATA, open("../results/fig13_data.json", "w"))
save(fig, "fig13_event_prediction")
# ---------------- Fig 14 dormant-to-active along an actual orbit: K(D(x_n)) at n=0,3,6
fig, axs = plt.subplots(1, 3, figsize=(W, 2.5))
prevD = []
for ax, n in zip(axs, (0, 3, 9)):
    D = eng3.Dset(xs[n]); K = eng3.complex_of(D)
    new = [d for d in D if d not in prevD]; ne = [e for e in K['E'] if e[0] in new or e[1] in new]
    ax.set_aspect("equal"); ax.axis("off")
    draw_complex(ax, D, K, scale=1.0, r=0.2, fs=5.0, new_v=new if prevD else (), new_e=ne if prevD else ())
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.45)
    ax.set_title(f"$K(D(x_{{{n}}}))$: $|D|={len(D)}$, $\\beta={betti_str(eng3.bettiD(D))}$", fontsize=6.3)
    prevD = D
fig.text(0.5, 0.0, "exact complexes along the orbit of $126^2/5$ (green = occurrences and moves new since the previous panel)", ha="center", fontsize=6)
save(fig, "fig14_activation_orbit")
# ---------------- Fig 15 divisor-interval edge loss
D0 = [6, 15]; N0 = [30]
fig, axs = plt.subplots(1, 3, figsize=(W, 2.6))
ax = axs[0]; ax.axis("off"); ax.set_xlim(0, 6); ax.set_ylim(0, 6)
# divisor lattice of 30 above gcd 3 : interval [6,15] = {3,6,15,30}
for p, t in (((3, 0.8), "3"), ((1.5, 3), "6"), ((4.5, 3), "15"), ((3, 5.2), "30")):
    pass
pts = {3: (3, 0.8), 6: (1.4, 3), 15: (4.6, 3), 30: (3, 5.2)}
for a, b in ((3, 6), (3, 15), (6, 30), (15, 30)): seg(ax, pts[a], pts[b], c="#888")
for d, (px, py) in pts.items():
    ec = SRC if d in (6, 15) else (KEEP if d == 30 else "#888")
    node(ax, px, py, str(d), fc=SRC_L if d in (6, 15) else (KEEP_L if d == 30 else "white"), ec=ec, r=0.38, fs=6.5)
ax.set_title("interval $[6,15]=\\{3,6,15,30\\}$", fontsize=6.6)
for ax, D, ttl, ne in ((axs[1], D0, "before: $D=\\{6,15\\}$", ()), (axs[2], D0+N0, "after: $D\\cup\\{30\\}$", ())):
    K = eng3.complex_of(D); ax.set_aspect("equal"); ax.axis("off")
    dead = [(6, 15)] if 30 in D else ()
    draw_complex(ax, D, K, scale=0.9, r=0.22, fs=6, new_v=[30] if 30 in D else (), dead_e=dead)
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.3, 1.3); ax.set_title(ttl+f", $\\beta={betti_str(eng3.bettiD(D))}$", fontsize=6.5)
fig.text(0.5, 0.0, "the edge $6-15$ of $K(\\{6,15\\})$ is pierced by the new occurrence $30\\in[6,15]$ and is lost (dashed in the original position; Paper III Thm. A5T31, SIV-P6)", ha="center", fontsize=5.8)
save(fig, "fig15_divisor_interval")
# ---------------- Fig 16 creation / preservation / destruction (Paper III cases via exact K)
cases = [("preserved: $\\Delta\\beta=0$", [385, 27720], [11, 72]), ("$\\beta_0$ drops", [12, 35], [44, 45]), ("$\\beta_1$ created", [33, 280], [14, 20])]
fig, axs = plt.subplots(2, 3, figsize=(W, 4.0))
for j, (ttl, D, N) in enumerate(cases):
    for i, DD in enumerate((D, D+N)):
        ax = axs[i][j]; ax.set_aspect("equal"); ax.axis("off")
        K = eng3.complex_of(DD); draw_complex(ax, DD, K, scale=1.0, r=0.2, fs=4.8, new_v=N if i else (), new_e=[e for e in K['E'] if (e[0] in N or e[1] in N)] if i else ())
        ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.45)
        ax.set_title((ttl+"\n" if i == 0 else "")+f"$\\beta={betti_str(eng3.bettiD(DD))}$", fontsize=6.3)
fig.text(0.5, 0.0, "exact complexes $K(D)\\to K(D\\cup N)$ computed by the Paper III engine; top row before, bottom row after (green: new)", ha="center", fontsize=6)
save(fig, "fig16_event_types")
print("figs_b done")
