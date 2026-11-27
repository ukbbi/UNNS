"""Figures for the report (needs matplotlib). Reads results/; computes only elementary curves."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from dirichlet import zeta, B_bracket
from generative_record import replay
from endpoint_engine import endpoint_census, unpack

R = lambda n: json.load(open(os.path.join(ROOT, "results", n)))
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
BLUE, TEAL, RED, GREY = "#2b6cb0", "#0f8b7d", "#b83232", "#6b7280"


def save(fig, name):
    fig.savefig(os.path.join(HERE, name), bbox_inches="tight", metadata={"CreationDate": None})
    plt.close(fig)


def fig_tree():
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    pos = {(): (4, 3), (1,): (2, 1.7), (2,): (6, 1.7), (1, 1): (1, .3), (1, 2): (3, .3),
           (2, 1): (5, .3), (2, 2): (7, .3)}
    from prime_dynamics import least_source
    for w, (x, y) in pos.items():
        K, a, b = least_source(w)
        E = K * a // b
        assert replay(K, w)[-1] == E
        if w:
            px, py = pos[w[:-1]]
            ax.plot([px, x], [py - .22, y + .3], color=GREY, lw=1)
            ax.text((px + x) / 2 + (-.22 if x < px else .22), (py + y) / 2, "%d" % w[-1], ha="center")
        ax.add_patch(FancyBboxPatch((x - .62, y - .22), 1.24, .5, boxstyle="round,pad=0.03",
                                    fc="#eaf1fa", ec=BLUE))
        ax.text(x, y + .11, "$E=%d$" % E, ha="center", va="center")
        ax.text(x, y - .09, "$K=%d$" % K, ha="center", va="center", fontsize=8, color=GREY)
    ax.set_xlim(0, 8); ax.set_ylim(0, 3.45); ax.axis("off")
    save(fig, "fig_tree.pdf")


def fig_pressure():
    sc = R("analytic.json")["sigma_c"][0]
    xs = [1.12 + i * (1.88 - 1.12) / 120 for i in range(121)]
    fig, ax = plt.subplots(figsize=(6.6, 3.4))
    ax.plot(xs, [B_bracket(s, 4000)[0] for s in xs], color=BLUE, label=r"$B(\sigma)$: growth per depth")
    ax.plot(xs, [zeta(2 * s) - 1 for s in xs], color=TEAL, ls="--",
            label=r"$G_1(\sigma)=\zeta(2\sigma)-1$")
    ax.axhline(1, color=GREY, lw=.8); ax.axvline(sc, color=RED, lw=.9)
    ax.axvline(1, color=GREY, lw=.8, ls=":")
    ax.text(sc + .02, 2.2, r"$\sigma_c\approx %.5f$" % sc, color=RED)
    ax.text(1.005, 3.2, r"$\sigma=1$", color=GREY)
    ax.set_ylim(0, 4); ax.set_xlim(.98, 1.9); ax.set_xlabel(r"$\sigma$"); ax.legend(frameon=False)
    save(fig, "fig_pressure.pdf")


def fig_region():
    sc = R("analytic.json")["sigma_c"][0]
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.axvspan(sc, 2.6, ymin=1 / 3.4, color=TEAL, alpha=.18)
    ax.axvspan(0, sc, color=RED, alpha=.10)
    ax.axvline(sc, color=RED); ax.axvline(1, color=GREY, ls=":")
    ax.plot([0, 1], [1, 0], color=BLUE, lw=1.2)
    ax.axhline(0, color=GREY, lw=.8)
    ax.text(2.03, 1.3, "sum over depths\nconverges", ha="center", color=TEAL)
    ax.text(.55, 1.5, "sum over depths\ndiverges ($t=1$)", ha="center", color=RED)
    ax.text(.08, .45, "fixed depth:\n$a+b=1$", color=BLUE, fontsize=8.5)
    ax.text(2.03, -.55, "$b<0$: open", ha="center", color=GREY)
    ax.set_xlim(0, 2.6); ax.set_ylim(-1, 2.4)
    ax.set_xlabel(r"$a=\mathrm{Re}\,s$"); ax.set_ylabel(r"$b=\mathrm{Re}(s+u)$")
    save(fig, "fig_region.pdf")


def fig_growth():
    cen = [R("census_stage_%s.json" % s) for s in "ABCDE"]
    orb = R("generation.json")["source_one_orbit"]
    sc = R("analytic.json")["sigma_c"][0]
    X = [c["X"] for c in cen]
    fig, ax = plt.subplots(figsize=(6.6, 3.3))
    ax.semilogx(X, [c["log_C_over_log_X"] for c in cen], "o-", color=TEAL, label=r"$\log C(X)/\log X$")
    ax.semilogx(X, [c["log_A_over_log_X"] for c in cen], "s-", color=BLUE, label=r"$\log A(X)/\log X$")
    ax.semilogx([o["X"] for o in orb], [o["log_ratio"] for o in orb], "^-", color="#8a5cc2",
                label=r"$\log N_1(X)/\log X$")
    ax.axhline(sc, color=RED); ax.text(1200, sc + .03, r"proved limit $\sigma_c$", color=RED)
    ax.set_ylim(.5, 1.7); ax.set_xlabel("$X$"); ax.legend(frameon=False, ncol=3, loc="lower right",
                                                          fontsize=8.5)
    save(fig, "fig_growth.pdf")


def fig_depth():
    cen = [R("census_stage_%s.json" % s) for s in "CDE"]
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    for c, col in zip(cen, (BLUE, TEAL, RED)):
        tot = c["A"]
        ax.plot(range(len(c["A_k"])), [v / tot for v in c["A_k"]], "o-", color=col, ms=4,
                label=r"$X=10^{%d}$" % round(math.log10(c["X"])))
    ax.set_xlabel("depth $k$"); ax.set_ylabel(r"$A_k(X)/A(X)$"); ax.legend(frameon=False)
    save(fig, "fig_depth.pdf")


def fig_A2():
    a = R("analytic.json")
    X = [r["X"] for r in a["A2"]]
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    ax.loglog(X, [r["residual_minus_c"] for r in a["A2"]], "o", color=BLUE, label="observed gap")
    C = a["A2"][-1]["scaled_by_X^(1/6)"]
    ax.loglog(X, [C * x ** (-1 / 6) for x in X], "--", color=GREY, label=r"reference $\propto X^{-1/6}$")
    ax.set_xlabel("$X$"); ax.set_ylabel(r"$A_2/\sqrt{X}-\frac{\kappa}{2}\log X-c$")
    ax.legend(frameon=False)
    save(fig, "fig_A2.pdf")


if __name__ == "__main__":
    for f in (fig_tree, fig_pressure, fig_region, fig_growth, fig_depth, fig_A2):
        f()
    print("figures written")
