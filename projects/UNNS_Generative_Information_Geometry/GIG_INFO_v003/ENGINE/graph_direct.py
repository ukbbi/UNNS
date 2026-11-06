"""Definition-level (no numpy, no masks) swap-graph invariants of a set of orderings: degrees, squares, ball sizes by BFS, and the T1 identity check."""
from collections import Counter


def swaps(p):
    for j in range(len(p) - 1):
        yield p[:j] + (p[j + 1], p[j]) + p[j + 2:]


def graph(A):
    A = set(A)
    return {p: [q for q in swaps(p) if q in A] for p in A}


def ball2(G, w):
    b1 = set(G[w]) | {w}
    b2 = set(b1)
    for u in G[w]:
        b2 |= set(G[u])
    return len(b1), len(b2)


def squares_through(G, w):
    """4-cycles w-u-v-x-w with u != x  (each square counted once per vertex)."""
    cnt = 0
    nb = G[w]
    seen = Counter()
    for u in nb:
        for v in G[u]:
            if v != w:
                seen[v] += 1
    return sum(c * (c - 1) // 2 for c in seen.values())


def profile(A):
    G = graph(A)
    d = {w: len(G[w]) for w in G}
    q = {w: squares_through(G, w) for w in G}
    b2 = {w: ball2(G, w)[1] for w in G}
    t1 = all(b2[w] == 1 + d[w] + sum(d[u] - 1 for u in G[w]) - q[w] for w in G)
    return {"N": len(G), "E": sum(d.values()) // 2, "sq": sum(q.values()) // 4, "h1": sorted(Counter(d[w] + 1 for w in G).items()), "hq": sorted(Counter(q.values()).items()),
            "h2": sorted(Counter(b2.values()).items()), "SB2": sum(b2.values()), "SB22": sum(v * v for v in b2.values()), "Sd2": sum(v * v for v in d.values()), "T1_identity_holds_at_every_vertex": t1}
