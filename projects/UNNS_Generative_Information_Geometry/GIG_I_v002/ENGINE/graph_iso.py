"""GIG-I v002 -- exact graph isomorphism for the (small, <=720 vertex) induced swap graphs.

Colour refinement is used ONLY to prune; every positive answer is an explicit vertex bijection that is verified
edge-by-edge, and every negative answer comes from an exhaustive individualisation-refinement search in which each
pruning step uses an isomorphism-invariant test.  Hashes / WL signatures are never used as proof.
Graphs are adjacency lists (list of lists of ints); edge colours / vertex names are ignored.
"""
from collections import Counter


def wl_hash(adj, rounds=None):
    """cheap 1-WL multiset hash (FILTER ONLY)."""
    n = len(adj)
    col = [len(a) for a in adj]
    for _ in range(rounds or n):
        sig = [(col[v], tuple(sorted(col[u] for u in adj[v]))) for v in range(n)]
        ids = {s: i for i, s in enumerate(sorted(set(sig)))}
        new = [ids[s] for s in sig]
        if len(set(new)) == len(set(col)):
            col = new
            break
        col = new
    return tuple(sorted(Counter(sig).items()))


def _refine(adjs, cols, ecs=None):
    """joint colour refinement of the disjoint family `adjs` (list of adjacency lists) with initial colours `cols`
    (list of lists).  Colour names are canonical (ranked signatures) so equal colours are comparable across graphs."""
    while True:
        if ecs is None:
            sigs = [[(cols[g][v], tuple(sorted(cols[g][u] for u in adjs[g][v]))) for v in range(len(adjs[g]))]
                    for g in range(len(adjs))]
        else:
            sigs = [[(cols[g][v], tuple(sorted((cols[g][u], c) for u, c in zip(adjs[g][v], ecs[g][v]))))
                     for v in range(len(adjs[g]))] for g in range(len(adjs))]
        allsig = sorted({s for gs in sigs for s in gs})
        ids = {s: i for i, s in enumerate(allsig)}
        new = [[ids[s] for s in gs] for gs in sigs]
        if len({c for gs in new for c in gs}) == len({c for gs in cols for c in gs}):
            return new
        cols = new


def _consistent(cols):
    a, b = Counter(cols[0]), Counter(cols[1])
    return a == b


def _is_iso(adjA, adjB, f, ecA=None, ecB=None):
    if len(set(f)) != len(adjA):
        return False
    for v, nb in enumerate(adjA):
        if ecA is None:
            if sorted(f[u] for u in nb) != sorted(adjB[f[v]]):
                return False
        elif sorted((f[u], c) for u, c in zip(nb, ecA[v])) != sorted(zip(adjB[f[v]], ecB[f[v]])):
            return False
    return True


def find_isomorphism(adjA, adjB, ecA=None, ecB=None):
    """return a list f (f[v] = image of vertex v of A in B) or None if the graphs are not isomorphic.
    Optional ecA/ecB: edge colours parallel to the adjacency lists (ecA[v][i] = colour of edge v--adjA[v][i]);
    then only colour-preserving isomorphisms are accepted."""
    if len(adjA) != len(adjB) or sum(map(len, adjA)) != sum(map(len, adjB)):
        return None
    if sorted(map(len, adjA)) != sorted(map(len, adjB)):
        return None
    n = len(adjA)
    if n == 0:
        return []
    ecs = None if ecA is None else [ecA, ecB]
    start = _refine([adjA, adjB], [[0] * n, [0] * n], ecs)
    if not _consistent(start):
        return None
    return _search(adjA, adjB, start, ecA, ecB)


def _search(adjA, adjB, cols, ecA=None, ecB=None):
    n = len(adjA)
    cA, cB = Counter(cols[0]), Counter(cols[1])
    # all classes singleton in A  => candidate bijection
    if all(c == 1 for c in cA.values()):
        pos = {c: v for v, c in enumerate(cols[1])}
        f = [pos[cols[0][v]] for v in range(n)]
        return f if _is_iso(adjA, adjB, f, ecA, ecB) else None
    # smallest non-singleton class
    target = min((c for c in cA if cA[c] > 1), key=lambda c: (cA[c], c))
    v = next(i for i in range(n) if cols[0][i] == target)
    top = max(max(cols[0]), max(cols[1])) + 1
    for u in range(n):
        if cols[1][u] != target:
            continue
        c0 = list(cols[0])
        c1 = list(cols[1])
        c0[v] = top
        c1[u] = top
        nxt = _refine([adjA, adjB], [c0, c1], None if ecA is None else [ecA, ecB])
        if not _consistent(nxt):
            continue
        f = _search(adjA, adjB, nxt, ecA, ecB)
        if f is not None:
            return f
    return None


def are_isomorphic(adjA, adjB):
    return find_isomorphism(adjA, adjB) is not None


def verify_bijection(adjA, adjB, f, ecA=None, ecB=None):
    return _is_iso(adjA, adjB, f, ecA, ecB)
