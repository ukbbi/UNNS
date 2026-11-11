"""Sanity run of the identity-search tool on the known successor family n = 24t+19 (points (n,n+1)); expects length 6."""
import json, time, sys
import fibparam as fp
def search_pts(pts, K=6, node_cap=60000):
    J = len(pts); E = fp.vocab(pts); nb = fp.nbrs_factory(E, J)
    A = tuple(x for x, y in pts); B = tuple(y for x, y in pts)
    da = {A: 0}; fa = [A]; db = {B: 0}; fb = [B]; ra = rb = 0
    def grow(front, dist, d):
        nxt = []
        for S in front:
            for nv in nb(S):
                if nv not in dist:
                    dist[nv] = d; nxt.append(nv)
                    if len(dist) > node_cap: return nxt
        return nxt
    for it in range(K):
        if len(da) <= len(db): fa = grow(fa, da, ra + 1); ra += 1
        else: fb = grow(fb, db, rb + 1); rb += 1
        sm, lg = (da, db) if len(da) < len(db) else (db, da)
        hits = [v for v in sm if v in lg]
        if hits: v = min(hits, key=lambda z: da.get(z, 99) + db.get(z, 99)); return da[v] + db[v], len(E)
    return None, len(E)
pts = [(24 * t + 19, 24 * t + 20) for t in (5000, 7001, 9100)]
L, V = search_pts(pts)
json.dump({"family": "n=24t+19, successor identity (class I of U1-BND)", "found_length": L, "vocabulary_size": V, "expected_length": 6, "ok": L == 6}, open(sys.argv[1], "w"), indent=1)
print(L, V)
