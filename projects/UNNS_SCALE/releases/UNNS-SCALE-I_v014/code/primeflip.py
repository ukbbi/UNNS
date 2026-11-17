"""v013: Prime-flip composite bound (PROVED construction).  For a prime p > B, p not dividing B:
   tau^B_p((p+1)^2) <= d_{G_{p+2}}(B,1) + 1 + d_{G_{p+1}}(p+1,B)   whenever both distances are finite,
via  Bp ~> p  (multiplier-p copy of a path B~>1 in G_{p+2}),  p -> (p+1)^2  (forward step N=p),  (p+1)^2 ~> B(p+1)  (the (p+1)-multiple copy of a path p+1 ~> B in G_{p+1}).
Every vertex is <= (p+1)^2; since kappa >= (p+1)^2 (v011 Cor. E) the ceiling (p+1)^2 equals kappa exactly.
Necessary condition for the second distance to be finite (parity barrier in G_{p+1}): every prime r with odd exponent in p+1 has (r+1)^2 <= p+1."""
import sys, collections
sys.dont_write_bytecode = True
def adjacency(C):
    adj = collections.defaultdict(list); t = 2
    while t * t <= C:
        k = 1
        while k * t * t <= C:
            a, b = k * (t - 1), k * t * t; adj[a].append(b); adj[b].append(a); k += 1
        t += 1
    return adj
def bfs_path(adj, s, t, lim):
    """shortest path s->t using only vertices <= lim"""
    par = {s: None}; fr = [s]
    while fr and t not in par:
        nx = []
        for v in fr:
            for w in adj.get(v, ()):
                if w <= lim and w not in par: par[w] = v; nx.append(w)
        fr = nx
    if t not in par: return None
    p = []; v = t
    while v is not None: p.append(v); v = par[v]
    return p[::-1]
def bound(p, B, adj):
    p1 = bfs_path(adj, B, 1, p + 2); p2 = bfs_path(adj, p + 1, B, p + 1)
    if p1 is None or p2 is None: return None
    path = [v * p for v in p1] + [(p + 1) ** 2] + [v * (p + 1) for v in p2[1:]]
    return len(path) - 1, path
