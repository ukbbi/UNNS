"""figures for GEO_HD_BRIDGE_v002 (matplotlib; derived from results/*.json -- not part of any proof)"""
import _paths  # noqa
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(n): return json.load(open(os.path.join(ROOT, "results", n)))

def fig1():
    g = J("GEOMETRY_STATES.json")["B3"]
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    for name, c in (("1^7", "#1f77b4"), ("2,2,3,3,3,3", "#d62728")):
        r = g[name]; steps = range(len(r["states"]))
        ax[0].plot(steps, [len(p) for p in r["primes"]], "o-", c=c, label=name)
        ax[1].plot(steps, [x[0] + 1 for x in [[sum(1 for _ in q)] for q in r["q"]]], alpha=0)
        ax[1].plot(steps, [ (lambda q: __import__("math").prod(v + 1 for v in q) - 1)(q) for q in r["q"]], "s-", c=c, label=name)
        ax[2].plot(steps, [sum(2 * v + 1 for v in q) if False else __import__("math").prod(2 * v + 1 for v in q) - 2 ** len(q) for q in r["q"]], "^-", c=c, label=name)
    ax[0].set_title("ambient dimension k(m_i)  (GEO-I box dimension)"); ax[1].set_title("|D(m_i)| = |F(m_i)|"); ax[2].set_title("total cells of K(m_i)")
    for a in ax: a.set_xlabel("step i"); a.grid(alpha=.3)
    ax[0].set_yticks([1, 2]); ax[0].legend(title="labels")
    fig.suptitle("B3: 4 -> 65536. Both routes stay contractible (Betti (1,0,..)); the recombined route passes through the 2-dimensional pieces (mixed index 6)", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "fig1_B3_geometry.png"), dpi=130); plt.close(fig)

def fig2():
    r = J("REGIME_I.json")["entry_time"]["histogram"]
    ks = sorted(int(k) for k in r); vs = [r[str(k)] for k in ks]
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    ax[0].bar(ks, vs, color="#2a7"); ax[0].set_yscale("log"); ax[0].set_xlabel("entry time e(t) into the rigid set t in {1,2,3}"); ax[0].set_ylabel("#squarefree t <= 3e5")
    ax[0].set_title("regime I: exact transient length depends on t alone")
    import field_regimes as FR
    ps = FR.orbit_pairs(5 * 4 * 4, 24)
    ax[1].step(range(len(ps)), [p[1] for p in ps], where="post", c="#444")
    for i, p in enumerate(ps):
        if p[2] > 1: ax[1].axvline(i, c="#d62728", alpha=.5, lw=1)
    ax[1].set_title("t_n for x_0 = 80 = 4^2 * 5 (red: births, sigma -> sigma*u)"); ax[1].set_xlabel("n"); ax[1].set_ylabel("t_n")
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "fig2_regime_I.png"), dpi=130); plt.close(fig)

def fig3():
    e = J("EVENT_CORRESPONDENCE.json")["pair_classification"]["counts"]
    js = sorted({int(k.strip("()").split(",")[0]) for k in e})
    def get(j, r, v): return e.get("(%d, %s, %s)" % (j, r, v), 0)
    fig, ax = plt.subplots(1, 2, figsize=(11, 3.6))
    ax[0].bar([j - .27 for j in js], [get(j, "False", "False") for j in js], .27, label="unreachable by SELECT-II", color="#999")
    ax[0].bar(js, [get(j, "True", "False") for j in js], .27, label="reachable, events differ", color="#d62728")
    ax[0].bar([j + .27 for j in js], [get(j, "True", "True") for j in js], .27, label="event-equivalent (x_m = 4^j x_n)", color="#2a7")
    ax[0].set_xlabel("collective births j between x_n and x_m"); ax[0].set_ylabel("pairs"); ax[0].legend(fontsize=8); ax[0].set_title("regime-I pairs vs SELECT-II histories")
    f = [x for x in J("SINGLE_EDGE_COINCIDENCES.json")["family"] if x["squarefree"]]
    ax[1].plot([x["a"] for x in f], [x["collective_events"] for x in f], "o-", c="#d62728", label="collective events (C^k)")
    ax[1].plot([x["a"] for x in f], [1 for _ in f], "s-", c="#2a7", label="SELECT-II events (one edge N = 2^a-1)")
    ax[1].set_xlabel("a  (N = 2^a - 1 squarefree)"); ax[1].legend(fontsize=8); ax[1].set_title("same endpoint (2^a s)^2, different event records")
    fig.tight_layout(); fig.savefig(os.path.join(ROOT, "figures", "fig3_event_map.png"), dpi=130); plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig3(); print("figures written")
