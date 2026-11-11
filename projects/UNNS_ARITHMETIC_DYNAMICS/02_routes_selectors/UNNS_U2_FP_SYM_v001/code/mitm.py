from u1_bnd_lib import *
def grow(a, r):
    par = {a: None}; dist = {a: 0}; fr = [a]
    for d in range(1, r + 1):
        nf = []
        for x in fr:
            for y in neighbours_fast(x):
                if y not in dist: dist[y] = d; par[y] = x; nf.append(y)
        fr = nf
    return dist, par
def chain(par, v):
    p = [v]
    while par[v] is not None: v = par[v]; p.append(v)
    return p
def mitm_path(a, b, ra, rb):
    da, pa = grow(a, ra); db, pb = grow(b, rb)
    hits = [v for v in da if v in db]
    if not hits: return None, len(da), len(db)
    v = min(hits, key=lambda z: da[z] + db[z])
    return chain(pa, v)[::-1] + chain(pb, v)[1:], len(da), len(db)
if __name__ == "__main__":
    import sys, time
    t = time.time()
    p, na, nb = mitm_path(661, 673, 4, 3); print("B4(661),B3(673) hit:", p is not None, na, nb, time.time() - t, flush=True)
    p2, na, nb = mitm_path(661, 673, 4, 4); print(p2, len(p2) - 1 if p2 else None, na, nb, time.time() - t, flush=True)
