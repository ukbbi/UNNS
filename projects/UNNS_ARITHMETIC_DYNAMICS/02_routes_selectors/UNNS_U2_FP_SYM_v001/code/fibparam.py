"""Search for 'two-parameter' path identities x=F_k -> y=F_{k+1} valid on Fibonacci pairs of a residue class of k."""
import sys, time, itertools, json
from math import isqrt
def fibs(n):
    F = [0, 1]
    while len(F) <= n: F.append(F[-1] + F[-2])
    return F
F = fibs(2200)
def vocab(pts):
    J = len(pts); E = {}
    for c in range(1, 13): E.setdefault(tuple([c] * J), str(c))
    forms = []
    for a in range(-3, 4):
        for b in range(-3, 4):
            if a == 0 and b == 0: continue
            for c in range(-2, 3):
                for d in (1, 2, 3, 4, 6, 8, 12, 24):
                    vals = []
                    for (x, y) in pts:
                        num = a * x + b * y + c
                        if num <= 0 or num % d: vals = None; break
                        vals.append(num // d)
                    if vals:
                        v = tuple(vals)
                        if v not in E:
                            E[v] = f"({a}x{b:+d}y{c:+d})/{d}"; forms.append((v, E[v]))
    base = [f for f in forms if f[1].endswith("/1") and abs(int(f[1][1:].split("x")[0]) if True else 0) <= 2][:60]
    small = [(tuple(x for x, y in pts), "x"), (tuple(y for x, y in pts), "y"), (tuple(x + y for x, y in pts), "x+y"), (tuple(y - x for x, y in pts), "y-x"), (tuple(2*x for x, y in pts), "2x"), (tuple(2*y for x, y in pts), "2y")]
    for (u, su), (w, sw) in itertools.combinations_with_replacement(small, 2):
        v = tuple(p * q for p, q in zip(u, w))
        if v not in E: E[v] = f"[{su}*{sw}]"
    return E
def nbrs_factory(E, J):
    items = list(E.items())
    def nbrs(S):
        out = {}
        for v, s in items:
            if all(x % y == 0 for x, y in zip(S, v)):
                out.setdefault(tuple(x // y * (y + 1) ** 2 for x, y in zip(S, v)), ("+", s))
                N = tuple(x // y for x, y in zip(S, v))
                out.setdefault(tuple(x // n * (n + 1) ** 2 for x, n in zip(S, N)), ("+", "S/" + s))
            if all(y >= 2 and x % (y * y) == 0 for x, y in zip(S, v)):
                out.setdefault(tuple(x // (y * y) * (y - 1) for x, y in zip(S, v)), ("-", "q=" + s))
            if all(x % y == 0 for x, y in zip(S, v)):
                qs = []; ok = True
                for x, y in zip(S, v):
                    tt = x // y; q = isqrt(tt)
                    if q * q != tt or q < 2: ok = False; break
                    qs.append(q)
                if ok: out.setdefault(tuple(y * (q - 1) for y, q in zip(v, qs)), ("-", "q=sqrt(S/" + s + ")"))
        out.pop(S, None); return out
    return nbrs
def search(P, r, K=6, J=3, node_cap=60000, tlimit=120):
    ks = [r + P * j for j in range(4, 4 + J)]
    pts = [(F[k], F[k + 1]) for k in ks]
    E = vocab(pts); nb = nbrs_factory(E, J); t0 = time.time()
    A = tuple(x for x, y in pts); B = tuple(y for x, y in pts)
    da = {A: 0}; pa = {A: None}; fa = [A]; db = {B: 0}; pb = {B: None}; fb = [B]; ra = rb = 0
    def grow(front, dist, par, d):
        nxt = []
        for S in front:
            if time.time() - t0 > tlimit: return nxt, True
            for nv, lab in nb(S).items():
                if nv not in dist:
                    dist[nv] = d; par[nv] = (S, lab); nxt.append(nv)
                    if len(dist) > node_cap: return nxt, True
        return nxt, False
    for it in range(K):
        if len(da) <= len(db): fa, cap = grow(fa, da, pa, ra + 1); ra += 1
        else: fb, cap = grow(fb, db, pb, rb + 1); rb += 1
        small, large = (da, db) if len(da) < len(db) else (db, da)
        hits = [v for v in small if v in large]
        if hits:
            v = min(hits, key=lambda z: da.get(z, 99) + db.get(z, 99))
            def chain(par, v):
                o = []
                while par[v] is not None: p, l = par[v]; o.append(l); v = p
                return o[::-1]
            f = chain(pa, v); g = chain(pb, v); g = [("-" if l[0] == "+" else "+", l[1]) for l in reversed(g)]
            return da[v] + db[v], f + g, len(f), len(E)
        if cap: return None, "cap/time", len(da), len(db), len(E)
    return None, "none", len(E)
if __name__ == "__main__":
    P, r, K = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    t = time.time(); print(json.dumps([P, r, search(P, r, K), round(time.time() - t, 1)]), flush=True)
