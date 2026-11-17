"""UNNS-SCALE-I v003 -- symbolic path identities in residue classes (exact, sympy).

A state is a polynomial S(t) in Z[t] kept as  cont * prod f_i^{m_i}  (f_i primitive irreducible,
positive leading coefficient).  Forward move  +N,  N = d * prod f_i^{e_i}  (d | cont, e_i <= m_i):
        S -> (S/N) (N+1)^2.
Backward move  -N,  q = N+1 = d * prod f_i^{e_i}  (d^2 | cont, 2 e_i <= m_i, q nonconstant or >= 2):
        S -> (S/q^2) (q-1).
Every move is a polynomial identity in Z[t]; legality for an integer t needs N >= 1 (resp. q >= 2)
and all cofactors >= 1, which holds for t >= t0 (computed exactly, see t0_of).
"""
from itertools import product
from math import isqrt
import sympy as sp
from sympy import Poly, ZZ

t = sp.symbols('t')
_FL = {}      # poly coefficient tuple -> (cont, [(Poly, mult)])
_DIV = {}


def pkey(p):
    return tuple(int(c) for c in p.all_coeffs())


def P(coeffs):
    return Poly(list(coeffs), t, domain=ZZ)


def factor_poly(p):
    k = pkey(p)
    if k not in _FL:
        if p.degree() <= 0:
            _FL[k] = (int(p.as_expr()), [])
        else:
            cont, facs = p.factor_list()
            cont = int(cont); out = []
            for f, m in facs:
                if f.LC() < 0:
                    f = -f
                    if m % 2 == 1:
                        cont = -cont
                out.append((f, m))
            _FL[k] = (cont, out)
    return _FL[k]


def divisors_of(n):
    if n not in _DIV:
        _DIV[n] = sorted(sp.divisors(n))
    return _DIV[n]


class State:
    __slots__ = ("cont", "facs", "key")

    def __init__(self, cont, facs):
        # facs: dict pkey -> [Poly, mult]
        self.cont = cont
        self.facs = facs
        self.key = (cont, tuple(sorted((k, v[1]) for k, v in facs.items())))

    def poly(self):
        r = P([self.cont])
        for k, (f, m) in self.facs.items():
            r = r * f ** m
        return r


def state_from_poly(p):
    cont, fl = factor_poly(p)
    facs = {}
    for f, m in fl:
        k = pkey(f)
        if k in facs: facs[k][1] += m
        else: facs[k] = [f, m]
    return State(cont, facs)


def _mul_state(cont, facs_a, extra_poly, power):
    """Return State for cont * prod facs_a * extra_poly^power."""
    facs = {k: [v[0], v[1]] for k, v in facs_a.items() if v[1] > 0}
    c, fl = factor_poly(extra_poly)
    cont = cont * (c ** power)
    for f, m in fl:
        k = pkey(f)
        if k in facs: facs[k][1] += m * power
        else: facs[k] = [f, m * power]
    return State(cont, facs)


def moves(S):
    """All neighbours of state S: yield (direction, Npoly, newState)."""
    cont = S.cont
    items = list(S.facs.items())
    out = []
    # ---- forward  N = d * prod f^e
    for d in divisors_of(cont):
        for es in product(*[range(v[1] + 1) for _, v in items]):
            N = P([d])
            rest = {}
            for (k, (f, m)), e in zip(items, es):
                if e: N = N * f ** e
                if m - e: rest[k] = [f, m - e]
            ns = _mul_state(cont // d, rest, N + 1, 2)
            out.append(("+", N, ns))
    # ---- backward  q = N+1 = d * prod f^e,  q^2 | S
    dsq = [d for d in divisors_of(cont) if d * d <= cont and cont % (d * d) == 0]
    for d in dsq:
        for es in product(*[range(v[1] // 2 + 1) for _, v in items]):
            q = P([d]); rest = {}
            for (k, (f, m)), e in zip(items, es):
                if e: q = q * f ** e
                if m - 2 * e: rest[k] = [f, m - 2 * e]
            if q.degree() == 0 and d == 1:
                continue                                  # q = 1 is not a move
            ns = _mul_state(cont // (d * d), rest, q - 1, 1)
            out.append(("-", q - 1, ns))
    return out


def start_state(B, M, r, shift=0):
    """State of B*(M t + r + shift) as a polynomial in t."""
    return state_from_poly(P([B * M, B * (r + shift)]))


def _expand(level, seen, par, d):
    nxt = []
    for S in level:
        for (dr, N, ns) in moves(S):
            if ns.key not in seen:
                seen[ns.key] = (d, ns)
                par[ns.key] = (S.key, dr, N)
                nxt.append(ns)
    return nxt


def search(B, M, r, K, node_cap=400000):
    """Shortest symbolic path (length <= K) from B(Mt+r) to B(Mt+r+1).  Returns list of steps or None."""
    A = start_state(B, M, r); Z = start_state(B, M, r, 1)
    da = {A.key: (0, A)}; pa = {A.key: None}; fa = [A]
    db = {Z.key: (0, Z)}; pb = {Z.key: None}; fb = [Z]
    ra = rb = 0
    for _ in range(K):
        if len(da) <= len(db):
            fa = _expand(fa, da, pa, ra + 1); ra += 1
        else:
            fb = _expand(fb, db, pb, rb + 1); rb += 1
        if len(da) + len(db) > node_cap:
            return None, "cap"
        best = None
        small, large = (da, db) if len(da) < len(db) else (db, da)
        for k in small:
            if k in large:
                s = da[k][0] + db[k][0] if (k in da and k in db) else None
                if s is not None and (best is None or s < best[0]): best = (s, k)
        if best is not None and best[0] <= K:
            s, k = best
            fwd = []
            x = k
            while pa[x] is not None:
                px, dr, N = pa[x]; fwd.append((px, dr, N, x)); x = px
            fwd = fwd[::-1]
            bwd = []
            x = k
            while pb[x] is not None:
                px, dr, N = pb[x]
                # edge px --dr,N--> x in the search from Z ; reversed: x -> px with opposite direction
                bwd.append((x, '-' if dr == '+' else '+', N, px)); x = px
            steps = [(dr, N) for (_, dr, N, _) in fwd] + [(dr, N) for (_, dr, N, _) in bwd]
            return steps, "ok"
    return None, "none"


# ---------------------------------------------------------------- verification
def apply_path(B, M, r, steps):
    """Exact symbolic replay of the path with polynomial arithmetic only (no factorisation tricks).
    Returns list of states (Poly) and list of cofactors; raises on any non-polynomial division."""
    S = P([B * M, B * r]); states = [S]; cofs = []
    for (dr, N) in steps:
        if dr == '+':
            Q, R = sp.div(S, N)
            assert R.is_zero, "forward label does not divide state"
            S2 = Q * (N + 1) ** 2; cofs.append((dr, N, Q))
        else:
            q = N + 1
            Q, R = sp.div(S, q * q)
            assert R.is_zero, "backward q^2 does not divide state"
            S2 = Q * N; cofs.append((dr, N, Q))
        S = S2; states.append(S)
    return states, cofs


def t0_of(poly):
    """Least integer T >= 0 with poly(t) >= 1 for every integer t >= T (poly in Z[t])."""
    if poly.degree() <= 0:
        c = int(poly.as_expr())
        return 0 if c >= 1 else None
    if poly.LC() <= 0:
        return None
    co = [int(c) for c in poly.all_coeffs()]
    bound = 1 + max(abs(c) for c in co[1:]) // abs(co[0]) + 1
    last_bad = -1
    for x in range(0, bound + 1):
        if poly.eval(x) < 1: last_bad = x
    return last_bad + 1


def certify(B, M, r, steps):
    """Full certificate: replay symbolically, check endpoint, compute t0 over all labels/cofactors."""
    states, cofs = apply_path(B, M, r, steps)
    target = P([B * M, B * (r + 1)])
    assert states[-1] == target, "path does not end at B(n+1)"
    t0 = 0
    for (dr, N, Q) in cofs:
        for g in [Q, N]:
            z = t0_of(g)
            if z is None: return None
            t0 = max(t0, z)
    for S in states:
        z = t0_of(S)
        if z is None: return None
        t0 = max(t0, z)
    return {"length": len(steps), "t0": t0, "states": states, "cofs": cofs}
