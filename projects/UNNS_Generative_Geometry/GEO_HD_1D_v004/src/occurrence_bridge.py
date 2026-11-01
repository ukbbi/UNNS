"""HD-1D v003 builder (D-Q3): occurrence-fibre bridge.  Histories h = (m0, labels), fibre sequence F(h) = (D(m_0..m_l)).

A legal swap at position i changes exactly the entry D(m_{i+1}) (v001 locality).  Its LOCAL DISCREPANCY is
        Delta(h,i) = D(m_{i+1}(h)) symmetric-difference D(m_{i+1}(h')),      non-empty by Lemma L.
For an index d >= 2 define the d-restricted swap graph G_d on a set of histories:
   mode 'preserve'  : a legal swap is kept iff d not in Delta (rho_d unchanged),
   mode 'after'     : a legal swap at i is kept iff d not in Delta  OR  d did not occur in D(m_0..m_i) (before the changed entry).
Both modes only delete edges of the unrestricted swap graph, so classes can only split: #classes(G_d) >= #classes(G)."""
from collections import defaultdict
from select_history import complete_histories, fibre, run, is_admissible
from route_complex import legal_swap_positions, do_swap


def _fibres(h, cache):
    s = cache.get(h)
    if s is None:
        s = tuple(frozenset(fibre(m)) for m in run(*h)); cache[h] = s
    return s


def discrepancy(h, i, cache=None):
    cache = {} if cache is None else cache
    a, b = _fibres(h, cache), _fibres(do_swap(h, i), cache)
    assert all(a[j] == b[j] for j in range(len(a)) if j != i + 1)
    return a[i + 1] ^ b[i + 1]


def components(hists, keep):
    """union-find components of the swap graph on `hists` keeping an edge (h,i) iff keep(h,i)"""
    idx = {h: k for k, h in enumerate(hists)}; par = list(range(len(hists)))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for h in hists:
        for i in legal_swap_positions(h):
            if keep(h, i): par[f(idx[h])] = f(idx[do_swap(h, i)])
    cl = defaultdict(list)
    for h in hists: cl[f(idx[h])].append(h)
    return list(cl.values())


def restricted_counts(t, ds, modes=("preserve", "after")):
    hists = list(complete_histories(t)); cache = {}
    dis = {}
    def D(h, i):
        k = (h, i)
        if k not in dis: dis[k] = discrepancy(h, i, cache)
        return dis[k]
    base = len(components(hists, lambda h, i: True))
    out = {"n_histories": len(hists), "classes_unrestricted": base}
    for d in ds:
        for mode in modes:
            if mode == "preserve": keep = lambda h, i, d=d: d not in D(h, i)
            else: keep = lambda h, i, d=d: (d not in D(h, i)) or not any(d in F for F in _fibres(h, cache)[:i + 1])
            out[(d, mode)] = len(components(hists, keep))
    return out, hists, cache
