"""Figures 1-5 of the v0.2 programme (Sections 2-4, 6)."""
from figlib import *
from lattice_cells import *
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union, polygonize
from fractions import Fraction as Fr

def planar_polys(C):
    polys, lines = [], []
    for c in C.get(2, ()):
        u, (g, h) = c
        polys.append(Polygon([u, add(u, g), add(add(u, g), h), add(u, h)]))
    for c in C.get(1, ()):
        u, (g,) = c
        lines.append(LineString([u, add(u, g)]))
    return polys, lines

def planar_holes(C):
    polys, lines = planar_polys(C)
    pu = unary_union(polys) if polys else None
    allw = unary_union([p.boundary for p in polys] + lines)
    faces = list(polygonize(allw))
    holes = [f for f in faces if pu is None or not pu.buffer(1e-9).contains(f.representative_point())]
    return holes, pu, faces

def embedded_planar(C):
    """True iff any two cells (dim>=1) meet exactly in the convex hull of their common vertices."""
    from shapely.geometry import MultiPoint
    items = []
    for d in (1, 2):
        for c in C.get(d, ()):
            vs = vertices(c)
            if d == 1:
                u, (g,) = c; geo = LineString([u, add(u, g)])
            else:
                u, (g, h) = c; geo = Polygon([u, add(u, g), add(add(u, g), h), add(u, h)])
            items.append((c, vs, geo))
    bad = 0
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            (c1, v1, g1), (c2, v2, g2) = items[i], items[j]
            inter = g1.intersection(g2)
            common = v1 & v2
            exp = MultiPoint(list(common)).convex_hull if common else None
            if inter.is_empty and exp is None: continue
            if exp is None or inter.is_empty or inter.symmetric_difference(exp).area > 1e-9 or inter.symmetric_difference(exp).length > 1e-9:
                bad += 1
    return bad == 0, bad

# ------------------------------------------------------------------ Figure 1: three objects
def fig01():
    lat = lambda v: (v[0]-v[1]) % 4 == 0
    q = (4, 4)
    F = fibre(lat, q); C = cells(lat, q)
    f = fvec(C); bt = betti(C); holes, pu, faces = planar_holes(C)
    emb, nbad = embedded_planar(C)
    fig, ax = plt.subplots(1, 3, figsize=(W, 2.45))
    # (a) fibre
    a = ax[0]
    a.add_patch(Rectangle((0, 0), 4, 4, fc="none", ec=GREY, lw=0.8, ls=(0, (3, 2))))
    a.scatter([p[0] for p in F], [p[1] for p in F], s=22, color=SRC, zorder=4)
    a.scatter([0], [0], s=26, facecolor="w", edgecolor="k", lw=0.8, zorder=4)
    a.annotate("$0\\notin F$", (0, 0), (0.2, -0.45), fontsize=7)
    for p in F: a.annotate(f"({p[0]},{p[1]})", p, (p[0]+0.12, p[1]+0.17), fontsize=6)
    style_axes2(a, (-0.6, 4.7), (-0.6, 4.7), range(5), range(5))
    a.set_xlabel("exponent vectors $(a,b)$; box dashed", fontsize=6.3, labelpad=2)
    a.set_title(f"fibre $F$: {len(F)} points", fontsize=8)
    # (b) abstract complex : graph with curved edges, 2-cell as highlighted cycle
    b = ax[1]
    from matplotlib.patches import FancyArrowPatch
    sq = [c for c in C[2]][0]; sqv = vertices(sq)
    for (u, (g,)) in sorted(C[1]):
        v = add(u, g)
        on_sq = (u in sqv and v in sqv)
        rad = 0.22 if (hash((u, v)) % 2) else -0.22
        b.add_patch(FancyArrowPatch(u, v, arrowstyle="-", connectionstyle=f"arc3,rad={rad}", color=SRC,
                                    lw=2.4 if on_sq else 0.7, zorder=2, shrinkA=2, shrinkB=2))
    b.scatter([p[0] for p in F], [p[1] for p in F], s=22, color=SRC, zorder=4)
    style_axes2(b, (-0.6, 4.7), (-0.6, 4.7), range(5), range(5), grid=False)
    b.set_title(f"$K_{{\\mathrm{{abs}}}}$: ${f}$, $b_1={bt[1]}$", fontsize=8)
    b.set_xlabel("abstract: curved arcs are formal edges;\nthick cycle = boundary of the 2-cell", fontsize=6.3, labelpad=2)
    # (c) union
    c = ax[2]
    for hf in holes:
        xs, ys = hf.exterior.xy
        c.add_patch(MPoly(list(zip(xs, ys)), fc="w", ec=UNC_E, hatch="////", lw=0.6, zorder=3))
    for p in [pu] if pu.geom_type == "Polygon" else list(pu.geoms):
        xs, ys = p.exterior.xy
        c.add_patch(MPoly(list(zip(xs, ys)), fc=SRC_L, ec=SRC, lw=0.9, zorder=1))
    for (u, (g,)) in sorted(C[1]):
        v = add(u, g); c.plot([u[0], v[0]], [u[1], v[1]], color=SRC, lw=1.0, zorder=2)
    c.scatter([p[0] for p in F], [p[1] for p in F], s=16, color=SRC, zorder=5)
    style_axes2(c, (-0.6, 4.7), (-0.6, 4.7), range(5), range(5))
    c.set_title(f"union $U$: $b_1={len(holes)}$ (holes hatched)", fontsize=8)
    c.set_xlabel("straight-line realisation; edges cross the\nsquare, so $K_{\\mathrm{emb}}$ is not defined", fontsize=6.3, labelpad=2)
    for t, a_ in zip("abc", ax): tag(a_, t)
    fig.suptitle("Specimen $21^8/5$: $\\Lambda=\\{a\\equiv b\\ (4)\\}$ on the box $Q=[0,4]^2$ (exact enumeration)", fontsize=8, y=1.02)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig01_three_objects")
    DATA["fig01"] = dict(lattice="a=b mod 4", box=list(q), fibre=[list(p) for p in sorted(F)], fvector_Kabs=list(f), betti_Kabs=bt,
                         realised_b1_union=len(holes), K_emb_defined=bool(emb), n_noncommon_face_pairs=nbad,
                         note="b1(U) computed by polygonize on exact integer coordinates (floating-point geometry library); "
                              "the release reports realised Betti (1,2,0) and abstract (1,5,0) for this specimen")
    assert bt == [1, 5, 0] and len(holes) == 2 and not emb

# ------------------------------------------------------------------ Figure 2: equal fibres, incomparable lattices
def fig02():
    L3 = lambda v: (v[0]+v[1]) % 2 == 0
    L7 = lambda v: (v[0]-v[1]) % 3 == 0
    lo, hi = -2, 5
    grid = [(i, j) for i in range(lo, hi+1) for j in range(lo, hi+1)]
    fig, ax = plt.subplots(1, 3, figsize=(W, 2.3))
    for a, (name, L, col, ttl) in zip(ax[:2], (("3", L3, SRC, "$\\Lambda_3=\\{a+b\\ \\mathrm{even}\\}$"), ("7", L7, TGT, "$\\Lambda_7=\\{a\\equiv b\\ (3)\\}$"))):
        pts = [p for p in grid if L(p)]
        a.scatter([p[0] for p in pts], [p[1] for p in pts], s=11, color=col, zorder=3, marker="o" if col == SRC else "s")
        a.add_patch(Rectangle((0, 0), 1, 1, fc=GREY, alpha=0.35, ec="k", lw=0.8, zorder=1))
        a.plot([1], [1], marker="o", ms=9, mfc="none", mec="k", mew=1.3, zorder=4)
        style_axes2(a, (lo-0.5, hi+0.5), (lo-0.5, hi+0.5), range(lo, hi+1, 1), range(lo, hi+1, 1))
        a.set_title(ttl, fontsize=8.5, color=col)
    witness2(ax[0], (2, 0)); ax[0].annotate("$(2,0)\\in\\Lambda_3\\setminus\\Lambda_7$", (2, 0), (-1.9, -1.6), fontsize=6.5)
    witness2(ax[1], (3, 0)); ax[1].annotate("$(3,0)\\in\\Lambda_7\\setminus\\Lambda_3$", (3, 0), (-1.9, -1.6), fontsize=6.5)
    c = ax[2]
    both = [p for p in grid if L3(p) and L7(p)]; only3 = [p for p in grid if L3(p) and not L7(p)]; only7 = [p for p in grid if L7(p) and not L3(p)]
    c.scatter([p[0] for p in only3], [p[1] for p in only3], s=11, color=SRC, marker="o", zorder=3, label="$\\Lambda_3$ only")
    c.scatter([p[0] for p in only7], [p[1] for p in only7], s=11, color=TGT, marker="s", zorder=3, label="$\\Lambda_7$ only")
    c.scatter([p[0] for p in both], [p[1] for p in both], s=22, color="k", marker="D", zorder=4, label="both $=\\Lambda_{21}$")
    c.add_patch(Rectangle((0, 0), 1, 1, fc=GREY, alpha=0.35, ec="k", lw=0.8, zorder=1))
    c.plot([1], [1], marker="o", ms=9, mfc="none", mec="k", mew=1.3, zorder=4)
    style_axes2(c, (lo-0.5, hi+0.5), (lo-0.5, hi+0.5), range(lo, hi+1, 1), range(lo, hi+1, 1))
    c.set_title("overlay", fontsize=8.5)
    fig.legend(*c.get_legend_handles_labels(), loc="lower center", ncol=3, fontsize=6.5, bbox_to_anchor=(0.82, -0.17), frameon=False, handletextpad=0.2, columnspacing=0.8)
    for t, a_ in zip("abc", ax): tag(a_, t)
    fig.suptitle("$484/3$ and $484/7$: primes $(2,11)$, box $[0,1]^2$; equal fibre $F=F'=\\{(1,1)\\}$ (circled), incomparable lattices", fontsize=8, y=1.02)
    fig.tight_layout(w_pad=0.6)
    save(fig, "fig02_equal_fibres")
    # exact verification of the claims
    q = (1, 1)
    assert fibre(L3, q) == [(1, 1)] and fibre(L7, q) == [(1, 1)]
    assert L3((2, 0)) and not L7((2, 0)) and L7((3, 0)) and not L3((3, 0))
    # lattice definitions agree with chi_b
    chi = lambda m, v: pow(2, v[0], m) * pow(11, v[1], m) % m
    assert all((chi(3, v) == 1) == L3(v) for v in grid if v[0] >= 0 and v[1] >= 0)
    assert all((chi(7, v) == 1) == L7(v) for v in grid if v[0] >= 0 and v[1] >= 0)
    DATA["fig02"] = dict(primes=[2, 11], box=[1, 1], fibre_3=[[1, 1]], fibre_7=[[1, 1]], witnesses={"in_L3_not_L7": [2, 0], "in_L7_not_L3": [3, 0]}, window=[lo, hi])

# ------------------------------------------------------------------ Figure 3: three-stage collective transition (P=110)
def fig03():
    E3 = lambda v: sum(v) % 2 == 0
    Z3 = lambda v: True
    q = (2, 2, 2)
    Cs, Ct = cells(E3, q), cells(Z3, q)
    fs, ft = fvec(Cs), fvec(Ct)
    bs, bt_ = betti(Cs), betti(Ct)
    persist = [len(Cs[d] & Ct[d]) for d in sorted(Cs)]
    assert fs == (13, 45, 36, 3) and ft == (26, 51, 33, 7) and persist == [13, 0, 0, 0] and bs == [1, 6, 6, 0] and bt_ == [1, 0, 0, 0]
    fig = plt.figure(figsize=(W, 4.1))
    gs = fig.add_gridspec(2, 2, height_ratios=[0.8, 2.0], hspace=0.2, wspace=0.3)
    # top: chain of three states
    top = fig.add_subplot(gs[0, :]); top.axis("off"); top.set_xlim(0, 3.0); top.set_ylim(0, 1)
    boxes = [("$x_0=110^4/3$", "$\\Lambda=E_3$,  $|F|=13$", SRC), ("$x_1=2\\cdot110^4/3$", "$\\Lambda=E_3$,  $|F|=13$  (same $(\\Lambda,Q)$)", SRC), ("$x_2=110^4$", "$\\Lambda=\\mathbf{Z}^3$,  $|F|=26$", TGT)]
    xs = [0.02, 1.03, 2.04]
    for (t1, t2, col), x0 in zip(boxes, xs):
        top.add_patch(Rectangle((x0, 0.08), 0.92, 0.84, fc="w", ec=col, lw=1.2, ls="-" if col == SRC else (0, (4, 2))))
        top.text(x0+0.46, 0.66, t1, ha="center", va="center", fontsize=8); top.text(x0+0.46, 0.30, t2, ha="center", va="center", fontsize=6.8)
    for x0 in (0.96, 1.97):
        top.annotate("", (x0+0.07, 0.5), (x0-0.02, 0.5), arrowprops=dict(arrowstyle="-|>", lw=1.0))
        top.text(x0+0.025, 0.62, "$\\mathcal{C}$", ha="center", fontsize=8)
    # bottom-left: 3D points
    a = fig.add_subplot(gs[1, 0], projection="3d")
    setup3d(a, (0, 0, 0), (2, 2, 2), view=(20, -58), ticks=[[0, 1, 2]]*3)
    wirebox(a, (0, 0, 0), (2, 2, 2), color=GREY, lw=0.5)
    Fs = fibre(E3, q); Ft = [p for p in fibre(Z3, q) if p not in set(Fs)]
    pts3(a, Fs, color=SRC, s=20, depthshade=False, marker="o", label="$F(E_3)$, 13 pts (persist)")
    pts3(a, Ft, facecolor="w", edgecolor=TGT, s=20, depthshade=False, marker="s", linewidths=1.0, label="new points of $F(\\mathbf{Z}^3)$, 13 pts")
    a.legend(loc="upper center", fontsize=6, frameon=False, bbox_to_anchor=(0.5, -0.1), ncol=1)
    a.set_title("fibres in $[0,2]^3$", fontsize=7.8, y=0.98)
    # bottom-right: f-vector bars
    b = fig.add_subplot(gs[1, 1])
    dims = np.arange(4); wd = 0.36
    for i, d in enumerate(dims):
        n_s, n_t, kp = fs[d], ft[d], persist[d]
        b.bar(i-wd/2-0.01, kp, wd, color=KEEP, edgecolor="k", lw=0.5)
        b.bar(i-wd/2-0.01, n_s-kp, wd, bottom=kp, color=LOST, edgecolor="k", lw=0.5, hatch="..", alpha=0.85)
        b.bar(i+wd/2+0.01, kp, wd, color=KEEP, edgecolor="k", lw=0.5)
        b.bar(i+wd/2+0.01, n_t-kp, wd, bottom=kp, color=TGT_L, edgecolor=TGT, lw=0.6, hatch="//")
        b.text(i-wd/2-0.01, n_s+1.2, str(n_s), ha="center", fontsize=6.5); b.text(i+wd/2+0.01, n_t+1.2, str(n_t), ha="center", fontsize=6.5)
    b.set_xticks(dims); b.set_xticklabels(["vertices", "edges", "squares", "cubes"], fontsize=7); b.set_ylim(0, 60)
    b.set_ylabel("number of cells", labelpad=1); b.grid(True, axis="y", lw=0.3, color="#ddd")
    from matplotlib.patches import Patch
    b.legend(handles=[Patch(fc=KEEP, ec="k", label="persists"), Patch(fc=LOST, ec="k", hatch="..", label="lost (source only)"), Patch(fc=TGT_L, ec=TGT, hatch="//", label="new (target only)")],
             loc="upper right", fontsize=6, framealpha=0.95)
    b.set_title("cells of $K_{\\mathrm{abs}}$ (left bar $E_3$, right bar $\\mathbb{Z}^3$)", fontsize=7.3)
    b.set_xlabel(f"Betti numbers of $K_{{\\mathrm{{abs}}}}$: ${tuple(bs)}\\to{tuple(bt_)}$", fontsize=7, labelpad=2)
    tag(a, "a"); tag(b, "b")
    fig.suptitle("Three-stage orbit $P^4/3\\to2P^4/3\\to P^4$, $P=110$, $Q=[0,2]^3$ (exact enumeration)", fontsize=7.8, y=0.995)
    save(fig, "fig03_three_stage")
    DATA["fig03"] = dict(P=110, box=[2, 2, 2], fvec_source=list(fs), fvec_target=list(ft), persisting=persist, betti_source=bs, betti_target=bt_,
                         graver_E3_vs_Z3_disjoint=True)

# ------------------------------------------------------------------ Figure 4: planar Graver-edge transport, h = 8
def fig04():
    h = 8; q = (h, h)
    lat = lambda v: (v[0]-v[1]) % 4 == 0; latp = lambda v: (v[0]-v[1]) % 2 == 0
    Cs, Ct = cells(lat, q), cells(latp, q)
    Vs1 = {vertices(c) for c in Cs[1]}; Vt1 = {vertices(c) for c in Ct[1]}
    fig, ax = plt.subplots(1, 3, figsize=(W, 2.65), gridspec_kw=dict(width_ratios=[1, 1, 1]))
    nk = nl = 0
    for c in sorted(Cs[1]):
        u, (g,) = c; kept = vertices(c) in Vt1
        nk += kept; nl += (not kept)
        if kept: ax[0].plot([u[0], u[0]+g[0]], [u[1], u[1]+g[1]], color=KEEP, lw=1.9, zorder=3)
        else: ax[0].plot([u[0], u[0]+g[0]], [u[1], u[1]+g[1]], color=LOST, lw=0.55, ls=(0, (1, 1.6)), zorder=2)
    for c in Ct[1]:
        u, (g,) = c; kept = vertices(c) in Vs1
        ax[1].plot([u[0], u[0]+g[0]], [u[1], u[1]+g[1]], color=KEEP if kept else TGT, lw=1.9 if kept else 0.6, ls="-" if kept else (0, (3, 1.5)), zorder=3 if kept else 2)
    for a_, L, col, ttl in ((ax[0], lat, SRC, "source $\\Lambda$"), (ax[1], latp, TGT, "target $\\Lambda'$")):
        pts = fibre(L, q); a_.scatter([p[0] for p in pts], [p[1] for p in pts], s=5, color=col, zorder=4)
        style_axes2(a_, (-0.5, h+0.5), (-0.5, h+0.5), range(0, h+1, 2), range(0, h+1, 2)); a_.set_title(ttl+" edges", fontsize=7.8)
    ax[0].set_xlabel(f"{nk} edges persist (green), {nl} lost (red dotted)", fontsize=6.3, labelpad=2)
    ax[1].set_xlabel(f"{len(Ct[1])} edges; the {nk} green ones persist", fontsize=6.3, labelpad=2)
    g = ax[2]
    srcG = [(1, 1), (4, 0), (0, 4), (1, -3), (3, -1), (2, -2)]; tgtG = [(1, 1), (1, -1), (2, 0), (0, 2)]
    srcPts = [(s*a, s*b) for (a, b) in srcG for s in (1, -1)]; tgtPts = [(s*a, s*b) for (a, b) in tgtG for s in (1, -1)]
    common = [p for p in srcPts if p in tgtPts]
    g.scatter([p[0] for p in srcPts if p not in common], [p[1] for p in srcPts if p not in common], s=26, color=SRC, marker="o", zorder=4, label="$\\mathrm{Gr}(\\Lambda)$")
    g.scatter([p[0] for p in tgtPts if p not in common], [p[1] for p in tgtPts if p not in common], s=26, color=TGT, marker="s", zorder=4, label="$\\mathrm{Gr}(\\Lambda')$")
    g.scatter([p[0] for p in common], [p[1] for p in common], s=60, color=KEEP, marker="D", edgecolor="k", linewidths=0.5, zorder=5, label="common: $\\pm(1,1)$")
    g.plot([0], [0], "k+", ms=5)
    for (a, b) in srcG[1:]:
        g.annotate(f"({a},{b})", (a, b), (a+0.12, b+0.2), fontsize=5.3, color=SRC)
    for (a, b) in tgtG[1:]:
        g.annotate(f"({a},{b})", (a, b), (a-0.9, b-0.55), fontsize=5.3, color=TGT)
    style_axes2(g, (-4.9, 4.9), (-4.9, 4.9), range(-4, 5, 2), range(-4, 5, 2))
    g.set_title("Graver sets (symmetric)", fontsize=7.8)
    g.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=5.8, frameon=False, handletextpad=0.2, borderaxespad=0)
    for t, a_ in zip("abc", ax): tag(a_, t)
    fig.suptitle("Planar family $21^{2h}/5\\to21^{2h}/4$, $h=8$: transport of edges of $K_{\\mathrm{abs}}$ (exact enumeration)", fontsize=7.8, y=1.01)
    fig.tight_layout(w_pad=0.5)
    save(fig, "fig04_planar_edges")
    c_r = [len([n for n in range(h) if n % 4 == r]) for r in range(4)]
    assert nk == sum(x*x for x in c_r) - 1
    DATA["fig04"] = dict(h=h, edges_source=len(Cs[1]), edges_target=len(Ct[1]), edges_kept=nk, edges_lost=nl, formula_Ekept=sum(x*x for x in c_r)-1)

# ------------------------------------------------------------------ Figure 5 (section 6): abstract loss vs realised containment
def fig05():
    h = 4; q = (h, h)
    lat = lambda v: (v[0]-v[1]) % 4 == 0; latp = lambda v: (v[0]-v[1]) % 2 == 0
    Cs, Ct = cells(lat, q), cells(latp, q)
    e1 = ((0, 4), ((4, 0),)); e2 = ((0, 4), ((1, -3),))
    assert e1 in Cs[1] and e2 in Cs[1] and e1 not in Ct[1] and e2 not in Ct[1]
    # containment (exact, 40 points on each lost edge)
    for (u, (g,)) in (e1, e2):
        for t in range(0, 41):
            p = tuple(Fr(a)+Fr(t, 40)*b for a, b in zip(u, g))
            assert in_union(Ct, p)
    cov_cell = ((0, 2), ((0, 2), (1, -1)))
    assert cov_cell in Ct[2]
    # e1 = two target edges
    e1a, e1b = ((0, 4), ((2, 0),)), ((2, 4), ((2, 0),))
    assert e1a in Ct[1] and e1b in Ct[1]
    fig, ax = plt.subplots(1, 3, figsize=(W, 2.45))
    def base(a, L, col):
        pts = fibre(L, q); a.scatter([p[0] for p in pts], [p[1] for p in pts], s=10, color=col, zorder=5)
        style_axes2(a, (-0.5, 4.5), (-0.5, 4.5), range(5), range(5))
    # (a) source with the two lost edges
    a = ax[0]; base(a, lat, SRC)
    for (u, (g,)) in sorted(Cs[1]):
        a.plot([u[0], u[0]+g[0]], [u[1], u[1]+g[1]], color=SRC_L, lw=0.8, zorder=1)
    for (u, (g,)) in (e1, e2):
        a.plot([u[0], u[0]+g[0]], [u[1], u[1]+g[1]], color=LOST, lw=1.8, ls=(0, (1, 1.4)), zorder=3)
    a.set_title("source $K_{\\mathrm{abs}}$", fontsize=8)
    a.text(2.0, 4.12, "$e_1$", color=LOST, fontsize=8, ha="center"); a.text(0.12, 2.5, "$e_2$", color=LOST, fontsize=8)
    a.set_xlabel("lost: generators $(4,0)$, $(1,-3)$ are not target Graver", fontsize=6.0, labelpad=2)
    # (b) target complex pieces
    b = ax[1]; base(b, latp, TGT)
    u, (g, hh) = cov_cell
    P = [u, add(u, g), add(add(u, g), hh), add(u, hh)]
    b.add_patch(MPoly(P, fc=TGT_L, ec=TGT, lw=1.0, ls="--", zorder=1))
    for (u_, (g_,)) in (e1a, e1b):
        b.plot([u_[0], u_[0]+g_[0]], [u_[1], u_[1]+g_[1]], color=TGT, lw=1.8, ls="--", zorder=3)
    b.set_title("target cells over $e_1,e_2$", fontsize=8)
    b.set_xlabel("$e_1$ = two $(2,0)$-edges; $e_2$ = diagonal of\nthe shaded 2-cell $\\Pi((0,2);(0,2),(1,-1))$", fontsize=6.0, labelpad=2)
    # (c) union overlay
    c = ax[2]
    holesT, puT, _ = planar_holes(Ct)
    for p in [puT] if puT.geom_type == "Polygon" else list(puT.geoms):
        xs, ys = p.exterior.xy; c.add_patch(MPoly(list(zip(xs, ys)), fc=TGT_L, ec=TGT, lw=0.8, ls="--", zorder=1))
    holesS, puS, _ = planar_holes(Cs)
    for p in [puS] if puS.geom_type == "Polygon" else list(puS.geoms):
        xs, ys = p.exterior.xy; c.add_patch(MPoly(list(zip(xs, ys)), fc="none", ec=SRC, lw=1.0, zorder=2))
    for (u_, (g_,)) in (e1, e2):
        c.plot([u_[0], u_[0]+g_[0]], [u_[1], u_[1]+g_[1]], color=LOST, lw=1.8, ls=(0, (1, 1.4)), zorder=4)
    base(c, latp, TGT)
    c.set_title("unions: $U\\subseteq U'$", fontsize=8)
    c.set_xlabel("teal: $U'$; blue outline: $U$; red dotted:\n$e_1,e_2\\notin K_{\\mathrm{abs}}(\\Lambda',Q)$ but $\\subset U'$", fontsize=6.0, labelpad=2)
    for t, a_ in zip("abc", ax): tag(a_, t)
    fig.suptitle("Lost abstractly, retained geometrically: $21^8/5\\to21^8/4$ ($h=4$), $Q=[0,4]^2$ (exact check at 41 points per edge)", fontsize=7.6, y=1.01)
    fig.tight_layout(w_pad=0.5)
    save(fig, "fig07_lost_edges_retained")
    DATA["fig07"] = dict(h=h, lost_edges=[[list(e1[0]), list(e1[1][0])], [list(e2[0]), list(e2[1][0])]], covering_cell=[list(cov_cell[0]), [list(x) for x in cov_cell[1]]],
                         exact_points_checked_per_edge=41, note="e1 is the union of two target edges; e2 is a diagonal of a target 2-cell")

def run():
    fig01(); fig02(); fig03(); fig04(); fig05()
if __name__ == "__main__":
    run(); print("A ok")
