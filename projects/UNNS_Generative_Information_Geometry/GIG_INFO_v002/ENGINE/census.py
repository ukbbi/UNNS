"""GIG-INFO v002 -- the six-label census as a finite system ensemble.
A SYSTEM X is a pair (content C of 6 distinct labels in 1..16, regime): a regime is a distinct non-empty admissibility set A_C(m) (v003 source_filtration.regimes).
Its histories are the N = |A| admissible arrangements of C; its swap graph is the induced permutohedron graph; K its permutohedral complex.
Y(X) = 1 iff beta_2(K; GF(2)) > 0.  The frozen v004 census is the baseline (158 regimes with beta_2>0); here every regime is re-enumerated and every Betti vector is recomputed
with the independent v001 engine (history_complex.betti), so the baseline is cross-checked, not trusted."""
import hashlib, itertools, json, os
import _vpath  # noqa: F401
import source_filtration as sf
import history_complex as hc

LMAX = 16


def contents(lmax=LMAX):
    return itertools.combinations(range(1, lmax + 1), 6)


def enumerate_regimes(lmax=LMAX):
    """list of (content, L, N, mask) in a deterministic order."""
    out = []
    for C in contents(lmax):
        for r in sf.regimes(C):
            out.append((C, r["L"], r["N"], r["mask"]))
    return out


def frozen_positive_regimes():
    """(content, L, beta2) of the v004 census with beta_2>0, plus the sha-256 of the frozen results file."""
    p = os.path.join(_vpath.PATHS["V004"], "RESULTS", "results.json")
    raw = open(p, "rb").read()
    res = json.loads(raw)
    pos = res["E15"]["completeness_census"]["beta2_regimes"]
    return [(tuple(x["content"]), x["L"], x["beta2"]) for x in pos], hashlib.sha256(raw).hexdigest(), res["E15"]["completeness_census"]["regimes"]


def adjacency(mask):
    """swap-graph adjacency of the arrangement set `mask` (bit i = i-th permutation of range(6)): dict vertex -> tuple of neighbours (pure python)."""
    perms, idx = hc.perms(6), hc.perm_index(6)
    verts = [i for i in range(720) if mask >> i & 1]
    adj = {}
    for v in verts:
        p = perms[v]
        nb = []
        for j in range(5):
            u = idx[p[:j] + (p[j + 1], p[j]) + p[j + 2:]]
            if mask >> u & 1:
                nb.append(u)
        adj[v] = tuple(nb)
    return adj


def ball_histograms(adj):
    """(h1, h2): sorted ((size, count), ...) of |B_1(v)| and |B_2(v)| over all vertices (exact, pure python)."""
    from collections import Counter
    c1, c2 = Counter(), Counter()
    for v, nb in adj.items():
        c1[1 + len(nb)] += 1
        s = {v}
        s.update(nb)
        for u in nb:
            s.update(adj[u])
        c2[len(s)] += 1
    return tuple(sorted(c1.items())), tuple(sorted(c2.items()))
