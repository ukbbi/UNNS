"""v004 fast symbolic route engine for 'linear-form' states.
A state is  cst * prod_i l_i^{e_i}  with each l_i = a t + b a primitive linear form (a>0, gcd(a,b)=1) in the class parameter t.
Moves (all are genuine SELECT-II moves, identities in Z[t]):
  forward  N = d  or  N = d*l   (N | state, N+1 = d  resp. d a t + d b + 1)
  backward q = d  or  q = d*l   (q^2 | state, label N = q-1)
Quadratic-or-higher labels are pruned (heuristic restriction: the engine may miss routes, never invents them;
every returned route is re-verified by poly_check, which shares no code with this module)."""
from math import gcd
from itertools import product
from sympy import factorint

_DIV = {}
def divisors_of(n):
    if n not in _DIV:
        f = factorint(n); ds = [1]
        for p, e in f.items(): ds = [d * p ** k for d in ds for k in range(e + 1)]
        _DIV[n] = sorted(ds)
    return _DIV[n]

def norm(forms):
    return tuple(sorted(forms.items()))

def linform(a, b):
    g = gcd(a, abs(b)) or 1
    return (a // g, b // g), g

def moves(state):
    cst, forms = state; fd = dict(forms); out = []
    ds = divisors_of(cst)
    for d in ds:
        # forward N = d
        out.append((('+', (d,)), (cst // d * (d + 1) ** 2, forms)))
        for (l, e) in forms:
            a, b = l
            # forward N = d*l
            lp, g = linform(d * a, d * b + 1)
            nf = dict(fd); nf[l] -= 1
            if nf[l] == 0: del nf[l]
            nf[lp] = nf.get(lp, 0) + 2
            out.append((('+', (d * a, d * b)), (cst // d * g * g, norm(nf))))
    for d in ds:
        if d >= 2 and cst % (d * d) == 0:
            out.append((('-', (d - 1,)), (cst // (d * d) * (d - 1), forms)))
        if cst % (d * d) == 0:
            for (l, e) in forms:
                if e >= 2:
                    a, b = l
                    lp, g = linform(d * a, d * b - 1)
                    nf = dict(fd); nf[l] -= 2
                    if nf[l] == 0: del nf[l]
                    nf[lp] = nf.get(lp, 0) + 1
                    out.append((('-', (d * a, d * b - 1)), (cst // (d * d) * g, norm(nf))))
    return out

class Cap(Exception): pass
def expand(level, seen, par, depth, limit=None):
    nxt = []
    for S in level:
        for lab, T in moves(S):
            if T not in seen:
                seen[T] = depth; par[T] = (S, lab); nxt.append(T)
        if limit is not None and len(seen) > limit: raise Cap()
    return nxt

def search(A, Z, K, cap=3_000_000):
    """bidirectional shortest symbolic path A -> Z of length <= K; returns list of (dir,labelcoeffs) or None"""
    if A == Z: return []
    da = {A: 0}; pa = {A: None}; fa = [A]; ra = 0
    db = {Z: 0}; pb = {Z: None}; fb = [Z]; rb = 0
    for _ in range(K):
        try:
            if len(da) <= len(db): fa = expand(fa, da, pa, ra + 1, cap - len(db)); ra += 1
            else: fb = expand(fb, db, pb, rb + 1, cap - len(da)); rb += 1
        except Cap:
            return None
        small, large = (da, db) if len(da) < len(db) else (db, da)
        best = None
        for k in small:
            if k in large:
                s = da[k] + db[k]
                if best is None or s < best[0]: best = (s, k)
        if best and best[0] <= K:
            k = best[1]; fwd = []; x = k
            while pa[x] is not None:
                px, lab = pa[x]; fwd.append(lab); x = px
            fwd.reverse(); bwd = []; x = k
            while pb[x] is not None:
                px, lab = pb[x]; bwd.append(('-' if lab[0] == '+' else '+', lab[1])); x = px
            return fwd + bwd
    return None

def start_states(B, C, M, r):
    """n+1 = C*s, s = M t + r :  A = B (C s)^2 , Z = B C s ; also returns pivot label (n = C M t + C r - 1)."""
    lp, g = linform(M, r)
    cst = B * C * C * g * g; Zc = B * C * g
    A = (cst, (((lp), 2),)); Z = (Zc, (((lp), 1),))
    return A, Z

def pivot_route(B, C, M, r, K4=4):
    A, Z = start_states(B, C, M, r)
    st = search(A, Z, K4)
    if st is None: return None
    n_label = (C * M, C * r - 1)
    return C * M, C * r - 1, [('+', n_label)] + [(d, list(l)) for d, l in st]

def general_route(B, M, r, K, cap=3_000_000):
    """route from B(Mt+r) to B(Mt+r+1), n = M t + r  (pure SELECT-II moves, linear-form states)."""
    lp, g = linform(M, r) if r != 0 else ((1, 0), M)
    lq, h = linform(M, r + 1)
    A = (B * g, ((lp, 1),)); Z = (B * h, ((lq, 1),))
    st = search(A, Z, K, cap)
    if st is None: return None
    return [(d, list(l)) for d, l in st]
