"""GIG-I v003 -- recognising 3-dimensional permutohedral cells from the UNCOLOURED swap graph (GIG-T19 / GIG-T20).

Graph-derived 3-cell:  a vertex set S of G_A such that
  (i)  the induced subgraph G_A[S] is isomorphic to the graph of Q3 (cube), C6 x K2 (hexagonal prism) or the truncated
       octahedron (graph of P_4), and
  (ii) no vertex outside S has two neighbours in S                       ("convexity" -- eliminates Petrie-type look-alikes).
Its boundary 2-cells are the graph-derived squares/hexagons (v002) whose vertex set lies in S.
Everything here uses only adjacency; no colours, no permutations."""
import _v2path  # noqa: F401
from itertools import permutations
import cell_signature as cs


# ----------------------------------------------------------------------------- pattern graphs
def _perm_cayley(n):
    P = list(permutations(range(n)))
    idx = {p: i for i, p in enumerate(P)}
    adj = [[] for _ in P]
    for p in P:
        for j in range(n - 1):
            q = p[:j] + (p[j + 1], p[j]) + p[j + 2:]
            adj[idx[p]].append(idx[q])
    return adj


def pattern_graphs():
    cube = [[v ^ (1 << b) for b in range(3)] for v in range(8)]
    prism = []
    for layer in range(2):
        for i in range(6):
            nb = [layer * 6 + (i + 1) % 6, layer * 6 + (i - 1) % 6, (1 - layer) * 6 + i]
            prism.append(nb)
    return {"cube": cube, "hexagonal prism": prism, "truncated octahedron": _perm_cayley(4)}


def _bfs_order(adj):
    order, seen = [0], {0}
    for v in order:
        for u in adj[v]:
            if u not in seen:
                seen.add(u)
                order.append(u)
    return order


class Host:
    """bit-set adjacency of a host graph."""

    def __init__(self, adj):
        self.n = len(adj)
        self.adj = adj
        self.nb = [sum(1 << u for u in a) for a in adj]


def induced_copies(pattern, host, starts=None):
    """all vertex sets S of `host` with host[S] isomorphic to `pattern` (induced), as frozensets of host vertex indices.
    Exhaustive backtracking in BFS order of the pattern, candidates by bit-set intersection of the already-placed neighbours,
    induced-ness enforced by excluding neighbours of already-placed non-neighbours."""
    order = _bfs_order(pattern)
    pos = {v: i for i, v in enumerate(order)}
    pn = [[pos[u] for u in pattern[v]] for v in order]          # neighbours by order index
    m = len(order)
    earlier_nb = [[u for u in pn[i] if u < i] for i in range(m)]
    earlier_non = [[u for u in range(i) if u not in pn[i]] for i in range(m)]
    out = set()
    img = [0] * m
    nbm = host.nb

    def rec(i, used):
        if i == m:
            out.add(frozenset(img))
            return
        cand = -1
        for u in earlier_nb[i]:
            cand &= nbm[img[u]]
        cand &= ~used
        for u in earlier_non[i]:
            cand &= ~nbm[img[u]]
        while cand:
            b = cand & -cand
            cand ^= b
            v = b.bit_length() - 1
            img[i] = v
            rec(i + 1, used | b)
    for s in (range(host.n) if starts is None else starts):
        img[0] = s
        rec(1, 1 << s)
    return out


def convex_ok(host, S):
    """no vertex outside S has two neighbours in S."""
    seen1 = seen2 = 0
    sm = 0
    for v in S:
        sm |= 1 << v
        a = host.nb[v]
        seen2 |= seen1 & a
        seen1 |= a
    return seen2 & ~sm == 0


def graph_three_cells(adj, host=None):
    """{type name: [frozenset S]} -- graph-derived 3-cells of the (uncoloured) swap graph."""
    host = host or Host(adj)
    pats = pattern_graphs()
    res = {}
    for name, g in pats.items():
        # start search only from host vertices of sufficient degree
        starts = [v for v in range(host.n) if len(adj[v]) >= 3]
        found = induced_copies(g, host, starts)
        res[name] = sorted((S for S in found if convex_ok(host, S)), key=sorted)
    return res


def graph_skeleton_ranks(adj, host=None):
    """f_0..f_3, rank d_1..d_3 and beta_0..beta_2 computed from the uncoloured graph alone (3-skeleton);
    beta_2 uses only the 3-skeleton and is valid as the second Betti number of the full complex."""
    host = host or Host(adj)
    n = len(adj)
    sq, hx, pet = cs.graph_two_cells(adj)
    cells3 = graph_three_cells(adj, host)
    eid = {}
    for v in range(n):
        for u in adj[v]:
            if v < u:
                eid[(v, u)] = len(eid)
    two = [(c, "square") for c in sq] + [(c, "hexagon") for c in hx]
    row2 = []
    two_sets = []
    for c, _ in two:
        r = 0
        for i in range(len(c)):
            a, b = c[i], c[(i + 1) % len(c)]
            r ^= 1 << eid[(min(a, b), max(a, b))]
        row2.append(r)
        two_sets.append(frozenset(c))
    all3 = [(S, name) for name, L in cells3.items() for S in L]
    row3 = []
    for S, name in all3:
        r = 0
        for j, T in enumerate(two_sets):
            if T <= S:
                r |= 1 << j
        row3.append(r)
    r1 = n - components_count(adj) if n else 0   # rank d_1 = n - #components
    r2 = cs._rank(row2)
    r3 = cs._rank(row3)
    f = (n, len(eid), len(two), len(all3))
    b0 = n - r1
    b1 = f[1] - r1 - r2
    b2 = f[2] - r2 - r3
    return {"f": f, "rank": (r1, r2, r3), "beta012": (b0, b1, b2), "cells3_by_type": {k: len(v) for k, v in cells3.items()},
            "row3": row3}


def components_count(adj):
    n = len(adj)
    seen = [False] * n
    c = 0
    for s in range(n):
        if not seen[s]:
            c += 1
            st = [s]
            seen[s] = True
            while st:
                v = st.pop()
                for u in adj[v]:
                    if not seen[u]:
                        seen[u] = True
                        st.append(u)
    return c


# ------------------------------------------------------------------ general face patterns (all dimensions)
def face_pattern(blocks):
    """graph of the permutohedral face with the given block sizes (>1): Cayley graph of the product of symmetric groups."""
    from itertools import product
    Ps = [list(permutations(range(b))) for b in blocks]
    idxs = [{p: i for i, p in enumerate(P)} for P in Ps]
    verts = list(product(*[range(len(P)) for P in Ps]))
    vid = {v: i for i, v in enumerate(verts)}
    adj = [[] for _ in verts]
    for v in verts:
        for t, P in enumerate(Ps):
            p = P[v[t]]
            for j in range(len(p) - 1):
                q = p[:j] + (p[j + 1], p[j]) + p[j + 2:]
                w = list(v)
                w[t] = idxs[t][q]
                adj[vid[v]].append(vid[tuple(w)])
    return adj


def face_types(k, dmin=1):
    """all block-size multisets (each >1, sorted decreasing) with sum <= k."""
    out = []

    def rec(rem, mx, cur):
        if cur:
            out.append(tuple(cur))
        for b in range(min(mx, rem), 1, -1):
            rec(rem - b, b, cur + [b])
    rec(k, k, [])
    return [t for t in out if sum(b - 1 for b in t) >= dmin]


def n_faces(k, blocks):
    """number of faces of P_k of the given type (ordered set partitions with block-size multiset `blocks` + singletons)."""
    import math
    from collections import Counter
    sizes = list(blocks) + [1] * (k - sum(blocks))
    c = Counter(sizes)
    arr = math.factorial(len(sizes))
    for m in c.values():
        arr //= math.factorial(m)
    return arr * (math.factorial(k) // math.prod(math.factorial(s) for s in sizes))


def rooted_check(k, blocks, host):
    """vertex-transitive pattern => every copy through the identity has an embedding with pattern vertex 0 -> identity (vertex 0).
    Returns (raw induced copies through the root, convex ones, expected number of faces through the root)."""
    import math
    pat = face_pattern(blocks)
    nv = len(pat)
    S = induced_copies(pat, host, [0])
    conv = [s for s in S if convex_ok(host, s)]
    return len(S), len(conv), n_faces(k, blocks) * nv // math.factorial(k)


# ------------------------------------------------------------------ the complete graph-derived complex (all dimensions)
def graph_complex(adj, k):
    """face poset of K_A reconstructed from the UNCOLOURED graph only (hypothesis: A has the cube-product property, k<=7):
    dim 0,1 = vertices, edges; dim 2 = 4-cycles and non-Petrie chordless 6-cycles; dim>=3 = convex induced copies of the face graphs.
    Returns dict with f, boundary ranks, Betti numbers and the cells (for inspection)."""
    host = Host(adj)
    n = len(adj)
    cells = {0: [frozenset([v]) for v in range(n)]}
    eid = {}
    for v in range(n):
        for u in adj[v]:
            if v < u:
                eid[(v, u)] = len(eid)
    cells[1] = [frozenset(e) for e in eid]
    sq, hx, pet = cs.graph_two_cells(adj)
    cells[2] = [frozenset(c) for c in sq] + [frozenset(c) for c in hx]
    for blocks in face_types(k, 3):
        d = sum(b - 1 for b in blocks)
        pat = face_pattern(blocks)
        if len(pat) > n:
            continue
        starts = [v for v in range(n) if len(adj[v]) >= d]
        found = induced_copies(pat, host, starts)
        cells.setdefault(d, []).extend(sorted((S for S in found if convex_ok(host, S)), key=sorted))
    f = tuple(len(cells.get(d, ())) for d in range(k))
    ranks = [0] * (k + 1)
    for d in range(1, k):
        lower = cells.get(d - 1, [])
        if not cells.get(d):
            continue
        rows = []
        if d == 1:
            for c in cells[1]:
                rows.append(sum(1 << v for v in c))
        else:
            # facets: lower cells whose vertex set is contained; index lower cells by a vertex to prune
            byv = {}
            for j, T in enumerate(lower):
                byv.setdefault(min(T), []).append(j)
            for S in cells[d]:
                r = 0
                for j, T in enumerate(lower):
                    if T <= S:
                        r |= 1 << j
                rows.append(r)
        ranks[d] = cs._rank(rows)
    betti = tuple(f[d] - ranks[d] - ranks[d + 1] for d in range(k))
    return {"f": f, "ranks": tuple(ranks[1:k]), "betti": betti, "cells": cells}
