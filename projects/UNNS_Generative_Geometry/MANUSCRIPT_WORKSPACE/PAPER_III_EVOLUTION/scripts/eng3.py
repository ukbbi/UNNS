"""Paper III exact engine (stdlib only, integer/Fraction arithmetic).  Independent of the BRIDGE source code.
FIELD-I map, occurrence sets for rationals, divisor-interval move complex K(D), GF(p) homology."""
from fractions import Fraction as Fr
from math import gcd, isqrt
from functools import reduce
import itertools

def lcm(a, b): return a // gcd(a, b) * b
def factor(n):
    f = {}; p = 2
    while p * p <= n:
        while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
        p += 1 if p == 2 else 2
    if n > 1: f[n] = f.get(n, 0) + 1
    return f
def divisors(f):
    ds = [1]
    for p, e in f.items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
    return sorted(ds)
def sqpart(a):
    """s with s^2 | a maximal"""
    s = 1
    for p, e in factor(a).items(): s *= p ** (e // 2)
    return s
def Dset(x):
    """occurrence set D(x), x=a/b reduced: d>=2, d^2|a, d=1 mod b"""
    x = Fr(x); a, b = x.numerator, x.denominator
    return [d for d in divisors(factor(sqpart(a))) if d >= 2 and (d - 1) % b == 0]
def LG(D):
    return reduce(lcm, D), reduce(gcd, [d - 1 for d in D])
def C(x):
    x = Fr(x); D = Dset(x)
    if not D: return None
    L, G = LG(D); return x + Fr(L * L, G)
def orbit(x, n):
    x = Fr(x); out = [x]
    for _ in range(n):
        y = C(out[-1])
        if y is None: break
        out.append(y)
    return out
# --- stage sieve
def Q(d, G):
    r = G // gcd(d - 1, G); q = 1
    for p, e in factor(d).items():
        g = 0; t = G
        while t % p == 0: t //= p; g += 1
        q *= p ** (2 * e + g)
    return lcm(r, q)
# --- complex K(D)
def edges(D):
    D = sorted(set(D)); pts = set(D) | {1}; E = set()
    for i, u in enumerate(D):
        for v in D[i + 1:]:
            g = gcd(u, v); l = lcm(u, v)
            if not any(w != u and w != v and w % g == 0 and l % w == 0 for w in pts): E.add((u, v))
    return E
def evec(D):
    fs = {d: factor(d) for d in D}; pr = sorted({p for f in fs.values() for p in f})
    return pr, {d: tuple(fs[d].get(p, 0) for p in pr) for d in D}
def rankQ(vs):
    M = [[Fr(c) for c in v] for v in vs]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        pv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if pv is None: continue
        M[r], M[pv] = M[pv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r
def lexpos(g):
    for c in g:
        if c: return c > 0
    return False
def complex_of(D, kmax=8):
    """cells[j]: tuples of sorted vertex-tuples? we store each cell as (base, gens) and also frozenset of its vertices"""
    D = sorted(set(D))
    if not D: return {'D': [], 'cells': [[]], 'E': set()}
    pr, vec = evec(D); inv = {v: d for d, v in vec.items()}
    E = edges(D); Es = {frozenset(e) for e in E}
    mv = set()
    for u, v in E:
        g = tuple(b - a for a, b in zip(vec[u], vec[v])); mv.add(g if lexpos(g) else tuple(-c for c in g))
    mv = sorted(mv); add = lambda a, g: tuple(x + y for x, y in zip(a, g))
    cells = [[(d, ()) for d in D]]
    c1 = []
    for d in D:
        for g in mv:
            w = inv.get(add(vec[d], g))
            if w is not None and frozenset((d, w)) in Es: c1.append((d, (g,)))
    cells.append(c1); j = 1
    while cells[j] and j < kmax:
        nxt = []
        for (d, gens) in cells[j]:
            for g in mv:
                if g <= gens[-1]: continue
                if rankQ(list(gens) + [g]) < j + 1: continue
                allg = gens + (g,); vs = [vec[d]]
                for h in allg: vs = vs + [add(v, h) for v in vs]
                if len(set(vs)) != 2 ** (j + 1) or any(v not in inv for v in vs): continue
                ok = True
                for v0 in vs:
                    for h in allg:
                        w = add(v0, h)
                        if w in set(vs) and frozenset((inv[v0], inv[w])) not in Es: ok = False; break
                    if not ok: break
                if ok: nxt.append((d, allg))
        cells.append(nxt); j += 1
    while len(cells) > 1 and not cells[-1]: cells.pop()
    return {'D': D, 'pr': pr, 'vec': vec, 'inv': inv, 'cells': cells, 'E': E}
def _bd(cell, K):
    d, gens = cell; vec, inv = K['vec'], K['inv']; out = {}
    add = lambda a, g: tuple(x + y for x, y in zip(a, g))
    for i, g in enumerate(gens):
        rest = gens[:i] + gens[i + 1:]; s = 1 if i % 2 == 0 else -1
        for face, sg in (((inv[add(vec[d], g)], rest), s), ((d, rest), -s)):
            out[face] = out.get(face, 0) + sg
    return out
def rank_mod(cols, p):
    piv = {}; r = 0
    for col in cols:
        c = {k: v % p for k, v in col.items() if v % p}
        while c:
            k0 = min(c)
            if k0 in piv:
                pc = piv[k0]; f = c[k0] * pow(pc[k0], -1, p) % p
                for k, v in pc.items():
                    nv = (c.get(k, 0) - f * v) % p
                    if nv: c[k] = nv
                    else: c.pop(k, None)
            else: piv[k0] = c; r += 1; break
    return r
def betti(K, p=2, check=True):
    cells = K['cells']
    if not cells[0]: return [], [], []
    idx = [{c: i for i, c in enumerate(cs)} for cs in cells]; r = [0]; bds = []
    for j in range(1, len(cells)):
        cols = []
        for c in cells[j]:
            col = {idx[j - 1][f]: s for f, s in _bd(c, K).items() if s % p}; cols.append(col)
        bds.append(cols); r.append(rank_mod(cols, p))
    if check:   # d^2 = 0
        for j in range(2, len(cells)):
            for col in bds[j - 1]:
                acc = {}
                for i, s in col.items():
                    for k, t in bds[j - 2][i].items(): acc[k] = acc.get(k, 0) + s * t
                assert all(v % p == 0 for v in acc.values()), 'd^2 != 0'
    r.append(0); f = [len(c) for c in cells]
    return f, r, [f[j] - r[j] - r[j + 1] for j in range(len(f))]
def bettiD(D, p=2):
    K = complex_of(D); f, r, b = betti(K, p)
    while b and b[-1] == 0 and len(b) > 1: b = b[:-1]
    return b
def ncomp(D, E):
    par = {d: d for d in D}
    def fd(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for u, v in E: par[fd(u)] = fd(v)
    return len({fd(d) for d in D})
# --- cell sets (for transition calculus): a cell = frozenset of its vertices (distinct cells have distinct vertex sets here) plus dimension
def cellsets(K):
    out = []
    for j, cs in enumerate(K['cells']):
        s = set()
        for (d, gens) in cs:
            vs = [K['vec'][d]]
            for h in gens: vs = vs + [tuple(a + b for a, b in zip(v, h)) for v in vs]
            s.add(frozenset(K['inv'][v] for v in vs))
        out.append(s)
    return out
