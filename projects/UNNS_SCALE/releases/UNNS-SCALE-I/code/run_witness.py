"""Explicit, hand-checkable route witnesses (upper bounds on distance)."""
import json, os
from collections import deque
from scale_lib import build_graph

def path(adj, a, b):
    par = {a: None}; q = deque([a])
    while q:
        u = q.popleft()
        if u == b: break
        for v in adj[u]:
            if v not in par: par[v] = u; q.append(v)
    p = []; x = b
    while x is not None: p.append(x); x = par[x]
    return p[::-1]

def label(u, v):
    for N in range(1, 10**4):
        if u * (N + 1) ** 2 == v * N: return "+%d" % N          # v = u(N+1)^2/N, N | u
        if v * (N + 1) ** 2 == u * N: return "-%d" % N          # v = u N/(N+1)^2
    return None

def legal(p):
    for u, v in zip(p, p[1:]):
        l = label(u, v)
        N = int(l[1:])
        if l[0] == "+": assert u % N == 0 and u // N * (N + 1) ** 2 == v
        else: assert u % (N + 1) ** 2 == 0 and u // (N + 1) ** 2 * N == v
    return True

g = build_graph(2_000_000)
out = {}
for name, a, b in [("base d(1,2)", 1, 2), ("scaled d(2,4) [B=2]", 2, 4),
                   ("base d(7,8)", 7, 8), ("scaled d(70,80) [B=10]", 70, 80)]:
    p = path(g, a, b)
    out[name] = {"path": p, "labels": [label(u, v) for u, v in zip(p, p[1:])], "length": len(p) - 1, "legal": legal(p)}
    print(name, out[name])
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "results", "witness_paths.json"), "w"), indent=1)


# ---- exact (untruncated) lower-bound certificates --------------------------
from scale_lib import factor, neighbours

def ball(u, r):
    """Exact ball of radius r about u in the infinite graph G (no truncation)."""
    seen = {u}; fr = [u]
    for _ in range(r):
        new = []
        for x in fr:
            for (_, _, v) in neighbours(factor(x)):
                if v not in seen:
                    seen.add(v); new.append(v)
        fr = new
    return seen

def certify_gt(a, b, D):
    """Return True if d_G(a,b) > D is certified: B_r(a) and B_s(b) disjoint, r+s = D."""
    r = (D + 1) // 2; s = D - r
    return ball(a, r).isdisjoint(ball(b, s))

cert = {}
for name, (a, b), upper in [("d(1,2)", (1, 2), 5), ("d(7,8)", (7, 8), 4)]:
    cert[name] = {"upper_bound_by_path": upper, "d>upper-1 certified": certify_gt(a, b, upper - 1),
                  "=> exact distance": upper if certify_gt(a, b, upper - 1) else None}
cert["strict_shortcut_B=2"] = ("d(2,4) <= 4 < 5 = d(1,2)" if cert["d(1,2)"]["=> exact distance"] == 5 else "not certified")
cert["strict_shortcut_B=10"] = ("d(70,80) <= 3 < 4 = d(7,8)" if cert["d(7,8)"]["=> exact distance"] == 4 else "not certified")
print(cert)
out["certificates"] = cert
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "results", "witness_paths.json"), "w"), indent=1)
