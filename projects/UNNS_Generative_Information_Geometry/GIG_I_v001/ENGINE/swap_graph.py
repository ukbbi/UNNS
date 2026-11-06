"""GIG-I v001 -- legal-swap graph G_t of a history fibre, recombination classes, accessibility balls.

A legal adjacent swap exchanges two ADJACENT DISTINCT labels of a history when the swapped word is still
admissible from the same source (actual intermediate-state admissibility, by simulation).  A swap preserves
source, content and endpoint, so swap edges never leave a fibre, a (source, content) piece, or a content class.
"""
from collections import deque, Counter
from history_fibres import is_admissible


def legal_swap_neighbours(h):
    m0, L = h
    out = []
    for i in range(len(L) - 1):
        if L[i] != L[i + 1]:
            L2 = L[:i] + (L[i + 1], L[i]) + L[i + 2:]
            if is_admissible(m0, L2):
                out.append((m0, L2))
    return out


def swap_graph(histories):
    """adjacency lists (by index) of the swap graph on the given list of histories.
    Raises if the list is not closed under legal swaps (it must be a union of whole pieces)."""
    hs = list(histories)
    idx = {h: i for i, h in enumerate(hs)}
    adj = [[] for _ in hs]
    for i, h in enumerate(hs):
        for g in legal_swap_neighbours(h):
            if g not in idx:
                raise ValueError("history list not closed under legal swaps: %r" % (g,))
            adj[i].append(idx[g])
        adj[i].sort()
    return adj


def components(adj):
    """connected components (recombination classes) as lists of vertex indices."""
    seen = [False] * len(adj)
    comps = []
    for s in range(len(adj)):
        if seen[s]:
            continue
        seen[s] = True
        comp, q = [s], deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    comp.append(y)
                    q.append(y)
        comps.append(sorted(comp))
    return comps


def distances_from(adj, s):
    """BFS distances from s (dict, reachable vertices only)."""
    d = {s: 0}
    q = deque([s])
    while q:
        x = q.popleft()
        for y in adj[x]:
            if y not in d:
                d[y] = d[x] + 1
                q.append(y)
    return d


def ball_profile(adj):
    """for each vertex v the list [|B_0(v)|, |B_1(v)|, ..., |B_ecc(v)|] (ball sizes by legal-swap distance)."""
    prof = []
    for v in range(len(adj)):
        cnt = Counter(distances_from(adj, v).values())
        out, tot = [], 0
        for r in range(max(cnt) + 1):
            tot += cnt[r]
            out.append(tot)
        prof.append(out)
    return prof


def ball_size(profile_v, r):
    """|B_r(v)| from a vertex profile (saturates at the component size)."""
    return profile_v[min(r, len(profile_v) - 1)]


def max_component_diameter(adj):
    prof = ball_profile(adj)
    return max(len(p) - 1 for p in prof) if prof else 0


def ball_product(prof, r):
    """P_r = prod_v |B_r(v)| as an exact integer: I_r = log2(P_r) / N."""
    p = 1
    for pv in prof:
        p *= ball_size(pv, r)
    return p


def ball_multiset(prof, r):
    return tuple(sorted(Counter(ball_size(pv, r) for pv in prof).items()))


def ball2_check(adj):
    """Proposition (radius-2 formula).  In a triangle-free graph in which two vertices at distance 2 have at most 2 common
    neighbours (true for every induced subgraph of the permutohedron graph),
        |B_2(v)| = 1 + d(v) + sum_{x ~ v} (d(x) - 1) - q(v),
    where q(v) = number of z at distance 2 with exactly 2 common neighbours = number of 4-cycles through v.
    Returns (formula_holds_for_all_v, max_common_neighbours_seen, triangle_free)."""
    n = len(adj)
    nb = [set(a) for a in adj]
    ok, maxc, tri = True, 0, True
    prof = ball_profile(adj)
    for v in range(n):
        for x in adj[v]:
            if nb[v] & nb[x]:
                tri = False
        cnt = Counter()
        for x in adj[v]:
            for z in adj[x]:
                if z != v:
                    cnt[z] += 1
        q = sum(1 for z, c in cnt.items() if z not in nb[v] and c == 2)
        maxc = max([maxc] + list(cnt.values()))
        formula = 1 + len(adj[v]) + sum(len(adj[x]) - 1 for x in adj[v]) - q
        ok &= (formula == ball_size(prof[v], 2))
    return ok, maxc, tri
