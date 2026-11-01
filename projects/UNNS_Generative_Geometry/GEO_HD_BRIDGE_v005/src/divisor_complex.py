"""GEO_HD_BRIDGE v005 -- A5-T3: the move complex K(D) as a function of the occurrence set D alone.

Identification: a point alpha of the realised fibre F(x) <-> the integer d = prod p^alpha in D(x).  Box of two points u,v in
exponent coordinates  <=>  divisor interval  {w : gcd(u,v) | w | lcm(u,v)}.   The origin 0 <-> d = 1 (always a blocker).

  EDGE RULE (theorem A5-T3a):  u ~ v  iff  the divisor interval [gcd(u,v), lcm(u,v)] contains no element of D u {1} other than u, v.
  CELLS:  parallelotopes P(u; g_1..g_j): g_i lex-positive edge vectors (exponent vectors of ratios v/u), linearly independent,
          all 2^j vertices in D (their edges are then automatically K(D)-edges, A5-T3a(iii)).
Only integer arithmetic.  This module does NOT call the frozen GEO-I engine (it is cross-checked against it in verify_v005)."""
import itertools
from math import gcd

try:
    from geo1lib import factor
except Exception:                       # stand-alone fallback
    def factor(n):
        f = {}; p = 2
        while p * p <= n:
            while n % p == 0: f[p] = f.get(p, 0) + 1; n //= p
            p += 1
        if n > 1: f[n] = f.get(n, 0) + 1
        return f

def lcm(a, b): return a // gcd(a, b) * b

def exp_vectors(D):
    """universal exponent coordinates for a set of integers"""
    D = sorted(D); fs = {d: factor(d) for d in D}
    primes = sorted({p for f in fs.values() for p in f})
    return primes, {d: tuple(fs[d].get(p, 0) for p in primes) for d in D}

def interval_blockers(u, v, pts):
    """elements of pts (a set containing 1) in the divisor interval of u,v, other than u,v"""
    g = gcd(u, v); l = lcm(u, v)
    return [w for w in pts if w != u and w != v and w % g == 0 and l % w == 0]

def edges(D):
    """K(D) 1-skeleton: set of pairs (u,v), u<v"""
    D = sorted(set(D)); pts = set(D) | {1}; E = set()
    for i, u in enumerate(D):
        for v in D[i + 1:]:
            g = gcd(u, v); l = lcm(u, v)
            if not any(w != u and w != v and w % g == 0 and l % w == 0 for w in pts): E.add((u, v))
    return E

def rank_mod(cols, p):
    """rank over GF(p) of a list of sparse columns (dict row->coeff)"""
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
            else:
                piv[k0] = c; r += 1; break
    return r

def rank_Q_int(vecs):
    from fractions import Fraction as Fr
    M = [[Fr(c) for c in v] for v in vecs]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r

def lexpos(g):
    for c in g:
        if c: return c > 0
    return False

def complex_of(D, kmax=6):
    """full K(D): cells[j] = list of (base_d, gens) ; gens = sorted tuple of exponent vectors.  vertices are the integers d."""
    D = sorted(set(D)); Dset = set(D)
    if not D: return {'D': [], 'primes': [], 'vec': {}, 'cells': [[]], 'E': set(), 'moves': set()}
    primes, vec = exp_vectors(D); n = len(primes)
    inv = {v: d for d, v in vec.items()}
    E = edges(D)
    moves = set()
    for u, v in E:
        g = tuple(b - a for a, b in zip(vec[u], vec[v]))
        moves.add(g if lexpos(g) else tuple(-c for c in g))
    posmoves = sorted(moves)
    add = lambda a, g: tuple(x + y for x, y in zip(a, g))
    Eset = {frozenset(e) for e in E}
    cells = [[(d, ()) for d in D]]
    one = []
    for d in D:
        for g in posmoves:
            w = inv.get(add(vec[d], g))
            if w is not None and frozenset((d, w)) in Eset: one.append((d, (g,)))
    cells.append(one)
    j = 1
    while cells[j] and j < kmax:
        nxt = []
        for (d, gens) in cells[j]:
            for g in posmoves:
                if g <= gens[-1]: continue
                if rank_Q_int(list(gens) + [g]) < j + 1: continue
                allg = gens + (g,)
                vs = [vec[d]]
                for h in allg: vs = vs + [add(v, h) for v in vs]
                if len(set(vs)) != 2 ** (j + 1) or not all(v in inv for v in vs): continue
                # every 1-face (w, w+g_i) must be a K(D)-edge  (definition of K(D) for arbitrary D; automatic for occurrence sets of states)
                ok = True
                for bits in range(2 ** (j + 1)):
                    for i, h in enumerate(allg):
                        if not (bits >> i) & 1:
                            w0 = vec[d]
                            for t, hh in enumerate(allg):
                                if (bits >> t) & 1: w0 = add(w0, hh)
                            if frozenset((inv[w0], inv[add(w0, h)])) not in Eset: ok = False; break
                    if not ok: break
                if ok: nxt.append((d, allg))
        cells.append(nxt); j += 1
    while cells and not cells[-1]: cells.pop()
    return {'D': D, 'primes': primes, 'vec': vec, 'cells': cells, 'E': E, 'moves': moves, 'inv': inv}

def _bd(cell, vec, inv):
    d, gens = cell; out = {}
    add = lambda a, g: tuple(x + y for x, y in zip(a, g))
    for i, g in enumerate(gens):
        rest = gens[:i] + gens[i + 1:]; s = 1 if i % 2 == 0 else -1
        for face, sg in (((inv[add(vec[d], g)], rest), s), ((d, rest), -s)):
            out[face] = out.get(face, 0) + sg
    return out

def betti_ranks(K, p=2):
    """returns (cells per dim, ranks r_j of boundary d_j: C_j -> C_{j-1} (j>=1), betti list) over GF(p)"""
    cells = K['cells']; vec = K['vec']; inv = K.get('inv', {})
    f = [len(c) for c in cells]
    idx = [{c: i for i, c in enumerate(cs)} for cs in cells]
    r = [0]
    for j in range(1, len(cells)):
        cols = []
        for c in cells[j]:
            col = {}
            for face, sg in _bd(c, vec, inv).items():
                if sg % p: col[idx[j - 1][face]] = sg
            cols.append(col)
        r.append(rank_mod(cols, p))
    r.append(0)
    b = [f[j] - r[j] - r[j + 1] for j in range(len(f))]
    return f, r, b

def betti(D, p=2, kmax=6):
    K = complex_of(D, kmax); return betti_ranks(K, p)[2] if K['cells'][0] else []

def components(D, E):
    par = {d: d for d in D}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for u, v in E: par[find(u)] = find(v)
    return len({find(d) for d in D})
