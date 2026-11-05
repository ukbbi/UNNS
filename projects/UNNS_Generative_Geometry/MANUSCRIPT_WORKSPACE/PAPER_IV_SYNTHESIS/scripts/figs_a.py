import sys; sys.path.insert(0, '.')
from figlib4 import *
import hist, eng3
from fractions import Fraction as Fr
# ---------------- Fig 1 architecture
fig, ax = newfig(3.4, (0, 12.4, 0, 6.6))
mbox(ax, 0.1, 5.0, 12.1, 1.3, "Inherited sources (frozen): Foundations Vol. I-II (SELECT-II, FIELD-I), GEO-I Papers A, B, releases.\nNot re-proved here; inherited verification status NOT_RERUN.", "neutral", 5.8)
cols = [(0.1, "Paper I (v0.4)", "lattices, Graver sets,\nabstract vs realised\ncells; dimension 2 vs 3"),
        (3.2, "Paper II (v0.4)", "histories, swaps, block\nrewrites, endpoint kernel,\nroute complexes"),
        (6.3, "Paper III (v0.4)", "collective map, events,\ndivisor-interval rule,\nzig-zag identity, towers")]
for x, t, b in cols:
    mbox(ax, x, 2.6, 2.9, 1.9, f"{t}\n{b}", "space", 6.0)
    sarrow(ax, (x+1.45, 5.0), (x+1.45, 4.5), 'est')
mbox(ax, 9.6, 2.6, 2.6, 1.9, "I, II, III cite one\nanother only through\nproved statements", "neutral", 6.4)
mbox(ax, 0.1, 0.1, 12.1, 1.5, "Paper IV: nine synthesis propositions SIV-P1 to P9 (new proofs from the three sources),\nthe global diagram (Fig. 21), exact obstructions, open construction obligations", "result", 6.9)
for x, _, _ in cols: sarrow(ax, (x+1.45, 2.6), (x+1.45, 1.6), 'fact')
save(fig, "fig01_architecture")
# ---------------- Fig 2 states and objects
fig, ax = newfig(3.4, (0, 12.4, 0, 6.6))
mbox(ax, 0.1, 0.3, 3.9, 5.8, "", "neutral"); mbox(ax, 4.2, 0.3, 3.9, 5.8, "", "neutral"); mbox(ax, 8.3, 0.3, 4.0, 5.8, "", "neutral")
ax.text(2.05, 5.8, "histories  $(m_0;w)$", ha="center", fontsize=7.3, fontweight="bold")
ax.text(6.15, 5.8, "integers  $t\\geq1$", ha="center", fontsize=7.3, fontweight="bold")
ax.text(10.3, 5.8, "rationals  $x=a/b$", ha="center", fontsize=7.3, fontweight="bold")
L = [("labels $N$, $N\\mid m$ at each step", 4.8), ("content $c\\in\\mathbf{N}^A$", 4.0), ("swap class", 3.2), ("fibre sequence $F(h)$", 2.4), ("route complexes (Paper II)", 1.6)]
M = [("endpoint $t$", 4.8), ("$D(t)=\\{d\\geq2:d^2\\mid t\\}$", 4.0), ("$\\Lambda=\\mathbf{Z}^k$, $\\mathrm{Gr}=\\{\\pm e_p\\}$", 3.2), ("$K_{\\rm move}(t)=K(D(t))$", 2.4), ("predecessors $\\leftrightarrow D(t)$", 1.6)]
R_ = [("$D(x)$, $d^2\\mid a,\\ d\\equiv1\\ (b)$", 4.8), ("$\\Lambda_b$, box, fibre $F$", 4.0), ("Graver set $\\mathrm{Gr}_q$", 3.2), ("$K_{\\rm move}(x)=K(D(x))$", 2.4), ("$C(x)=x+L^2/G$", 1.6)]
for (txts, x0) in ((L, 0.3), (M, 4.4), (R_, 8.5)):
    for t, y in txts: mbox(ax, x0, y-0.3, 3.5, 0.6, t, "obj", 6.4)
ax.text(2.05, 0.55, "SELECT-II steps $T_N$", ha="center", fontsize=5.8, style="italic")
ax.text(6.15, 0.55, "integers: both sides ($b=1$)", ha="center", fontsize=6.2, style="italic")
ax.text(10.3, 0.55, "FIELD-I and the map $C$", ha="center", fontsize=6.2, style="italic")
save(fig, "fig02_states_objects")
# ---------------- Fig 3 endpoint projection
fig, ax = newfig(3.2, (0, 12.4, 0, 6.2))
Hs = [(1, w) for w in hist.histories(1, 72)] + [(3, w) for w in hist.histories(3, 72)] + [(10, w) for w in hist.histories(10, 72)]
for i, (m0, w) in enumerate(Hs):
    y = 5.2 - i*0.95
    mbox(ax, 0.1, y-0.3, 3.0, 0.6, f"$({m0};{','.join(map(str,w))})$", "obj", 6.6)
    sarrow(ax, (3.1, y), (5.3, 3.4), 'est')
mbox(ax, 5.3, 3.0, 1.2, 0.8, "$t=72$", "space", 7)
ax.text(2.0, 0.55, "all complete histories ending at 72: 4", ha="center", fontsize=6.3)
n32 = len(hist.histories(32, 13122)); cs = {w for w in hist.histories(32, 13122)}
mbox(ax, 7.6, 3.6, 4.6, 1.5, "source 32, endpoint $13122$:\n$(2,2,2,2)$ and $(1,8,8)$\nboth admissible, same endpoint,\ndifferent content", "obj", 6.4)
sarrow(ax, (7.6, 4.3), (6.5, 3.5), 'est')
mbox(ax, 7.6, 0.8, 4.6, 1.9, f"endpoint projection $\\pi_{{\\rm end}}$:\nhistories $\\to\\mathbf{{Z}}$ is not injective\n(P1). Histories from source 32 to\n13122: {n32}", "result", 6.4)
tag(ax, "exact; computed by the SELECT-II engine (see Appendix F)")
save(fig, "fig03_endpoint_fibres")
# ---------------- Fig 4 ancestry tree of 72
fig, ax = newfig(3.6, (0, 12.4, 0, 6.9))
def Ds(t):
    d = eng3.Dset(t); return "$\\emptyset$" if not d else "{" + ",".join(map(str, d)) + "}"
paths = [(1, (1, 2, 1)), (1, (1, 1, 2)), (3, (3, 2)), (10, (5,))]
ys = [5.6, 4.1, 2.4, 0.9]
mbox(ax, 10.0, 2.95, 2.3, 0.9, f"72\n$D=${Ds(72)}", "space", 6.6)
for (m0, w), y in zip(paths, ys):
    m = m0; chain = [m]
    for N in w: m = m*(N+1)**2//N; chain.append(m)
    n = len(chain)
    for i, mm in enumerate(chain[:-1]):
        xc = 7.9 - 2.7*(n-2-i)
        mbox(ax, xc-1.0, y-0.4, 2.0, 0.8, f"{mm}\n$D=${Ds(mm)}", "obj", 6.0)
        tgt = (xc+2.7-1.0, y) if i < n-2 else (10.0, 3.4)
        sarrow(ax, (xc+1.0, y), tgt, 'est', f"$N={w[i]}$", off=(0, 0.22) if i < n-2 else (-0.5, 0.2))
ax.text(0.1, 6.55, "four complete histories to 72 (sources 1, 1, 3, 10); node: value and occurrence set; predecessors of 72: $t(d-1)/d^2$, $d\\in D(72)$", fontsize=6.2)
tag(ax, "exact (SELECT-II engine; Paper II Thm. predecessors)")
save(fig, "fig04_ancestry_72")
# ---------------- Fig 5 valuation kernel
fig, ax = plt.subplots(figsize=(W, 2.9))
def dl(N):
    v = lambda n, p: sum(1 for _ in iter(lambda: None, 1) if False) or (lambda nn: next(i for i in range(60) if nn % p**(i+1)))(n) if n % p == 0 else 0
    def vp(n, p):
        e = 0
        while n % p == 0: n //= p; e += 1
        return e
    return (2*vp(N+1, 2)-vp(N, 2), 2*vp(N+1, 3)-vp(N, 3))
for name, w, c, ls in (("$(2,2,2,2)$", (2, 2, 2, 2), "#1f5fa8", "-"), ("$(1,8,8)$", (1, 8, 8), "#c0392b", "--")):
    p = [(0, 0)]
    for N in w:
        d = dl(N); p.append((p[-1][0]+d[0], p[-1][1]+d[1]))
    ax.plot([a for a, b in p], [b for a, b in p], c=c, ls=ls, marker="o", ms=3, lw=1.2, label=f"labels {name}")
    for a, b in p: pass
ax.set_xlabel("$\\sum_N v_2((N+1)^2/N)$"); ax.set_ylabel("$\\sum_N v_3((N+1)^2/N)$")
ax.set_title("source 32: two label contents, one displacement vector $V_A(c-c')=0$ (Paper II Thm. kernel)", fontsize=7.5)
ax.legend(frameon=False); ax.grid(alpha=0.3, lw=0.4)
save(fig, "fig05_kernel_ambiguity")
# ---------------- Fig 6 occurrence projection / dormant relations (Paper III Thm R3T1(i), r=13)
r = 13; xr = Fr(25*r*r, 5*r-1); yr = Fr(25*r*r, 8)
assert eng3.Dset(xr) == eng3.Dset(yr) == [65]
fig, axs = plt.subplots(1, 2, figsize=(W, 2.7))
for ax, ttl, vecs in ((axs[0], "$x_{13}=4225/64$: $\\mathrm{Gr}=\\{\\pm(1,1)\\}$", [(1, 1)]), (axs[1], "$y_{13}=4225/8$: $\\mathrm{Gr}=\\{\\pm(1,1),\\pm(1,-1)\\}$", [(1, 1), (1, -1)])):
    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(ttl, fontsize=7)
    ax.add_patch(Rectangle((0, 0), 1, 1, fc="#eef3f9", ec=SRC, lw=0.8)); ax.text(0.5, -0.25, "box $[0,1]^2$", ha="center", fontsize=6)
    for gx in range(-2, 3):
        for gy in range(-2, 3): ax.plot(gx, gy, ".", c="#b0b8bf", ms=2)
    for v in vecs:
        for s in (1, -1): ax.annotate("", xy=(s*v[0], s*v[1]), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=TGT, lw=1.2))
    ax.plot([1], [1], "o", c="k", ms=4); ax.text(1.12, 1.1, "$D=\\{65\\}$", fontsize=6.3)
    ax.plot([0], [0], "s", c="k", ms=3)
fig.suptitle("same active primes $\\{5,13\\}$, same box, same $D(x)=D(y)=\\{65\\}$, different primitive systems (Paper III Thm. R3T1(i); $D$ recomputed)", fontsize=6.6, y=0.02)
save(fig, "fig06_equalD_diffGr")
# ---------------- Fig 7 possibility vs realisation
fig, ax = newfig(3.2, (0, 12.4, 0, 6.2))
box(ax, 0.2, 0.2, 12.0, 5.8, "", fc="#f7f8f9", ec="#6b7780")
box(ax, 0.7, 0.6, 9.6, 4.6, "", fc="#eaf1f8", ec=SRC)
box(ax, 1.2, 1.0, 6.6, 3.4, "", fc=KEEP_L, ec=KEEP)
ax.text(0.45, 5.7, "relations of the lattice $\\Lambda_b$ ($d\\equiv1$ mod $b$; arithmetic availability)", fontsize=6.5, va="center")
ax.text(0.95, 4.9, "primitive relations $\\mathrm{Gr}_q$ (Paper I)", fontsize=6.5, va="center")
ax.text(1.45, 4.1, "realised moves = edges of $K_{\\rm move}$ (function of $D$)", fontsize=6.5, va="center")
ax.text(1.45, 3.1, "SIV-P3(a): realised set grows along every orbit\n(Lemma M)", fontsize=6.3, va="center")
ax.text(1.45, 2.0, "dormant: $e_i-e_j\\in\\mathrm{Gr}(x)$ at $x=P^2/\\ell$,\nactive at $y=(Pq)^2/\\ell$ (Paper III Thm. A4T1)", fontsize=6.3, va="center")
ax.text(7.95, 3.0, "primitive but not\nrealised ('dormant')", fontsize=5.8, ha="left")
ax.text(7.95, 1.6, "primitive status can\nbe lost (Paper I,\nThm. laws, L1)", fontsize=5.6, ha="left", color=LOST)
save(fig, "fig07_possible_vs_realised")
# ---------------- Fig 8 planar vs 3D
fig, axs = plt.subplots(1, 2, figsize=(W, 2.8))
ax = axs[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_title("planar: $\\Lambda\\subseteq\\Lambda'\\subseteq\\mathbf{Z}^2\\Rightarrow U\\subseteq U'$ (Paper I Thm. planar)", fontsize=6.8)
for gx in range(5):
    for gy in range(4):
        sub_ = (gx+gy) % 2 == 0
        ax.plot(gx, gy, "o", ms=3.2 if sub_ else 2, c=SRC if sub_ else "#9aa5ad")
ax.add_patch(Rectangle((0, 0), 4, 3, fc="none", ec="k", lw=0.8)); ax.text(2, -0.6, "$\\Lambda$ (dark) $\\subseteq\\mathbf{Z}^2$, any box", ha="center", fontsize=6.2)
ax = axs[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_title("three dimensions: $\\Lambda=2E_3\\subseteq2\\mathbf{Z}^3$, $Q=(2,4,2)$: $U\\not\\subseteq U'$ (Thm. C1)", fontsize=6.8)
pts = [(x, y, z) for x in (0, 2) for y in (0, 2, 4) for z in (0, 2) if (x+y+z) % 4 == 0]
P = lambda p: (p[0]+0.5*p[2], p[1]+0.35*p[2])
for p in [(x, y, z) for x in (0, 2) for y in (0, 2, 4) for z in (0, 2)]:
    ax.plot(*P(p), "o", ms=2, c="#9aa5ad")
for p in pts: ax.plot(*P(p), "o", ms=3.6, c=LOST)
ax.text(2.5, -0.9, "dark: points of $2E_3$ in the box (exact lattice; cells not drawn)", ha="center", fontsize=6.2)
save(fig, "fig08_planar_vs_3d")
print("figs_a done")
