"""UNNS-U2-001: finite-control selector for reversible SELECT-II (exact integer arithmetic).
Sigma(x, q) -> (sign, N, q').  Only the current integer x and a finite control state q are read."""
import sympy as sp
from u1_bnd_lib import IDENTITIES, SPECIAL, T, fwd, inv, is_edge, _I

READY = "READY"
_t = sp.symbols("t", integer=True, nonnegative=True)

def _state_polys(ident):
    """Exact state values s_0..s_l as rational functions of t (s_0=n, s_l=n+1)."""
    n = ident["M"] * _t + ident["r"]
    xs = [sp.Integer(1) * n]
    for d, e in ident["steps"]:
        N = e.subs(T, _t)
        x = xs[-1]
        xs.append(sp.simplify(x * (N + 1) ** 2 / N) if d == "+" else sp.simplify(x * N / (N + 1) ** 2))
    return xs

POLY = {}
for ident in IDENTITIES:
    xs = _state_polys(ident)
    POLY[ident["name"]] = (ident, [sp.lambdify(_t, p, "math") for p in xs], xs,
                           [sp.lambdify(_t, e.subs(T, _t), "math") for _, e in ident["steps"]])

def _exact(ident, i, t):
    """Integer state s_i(t) computed with Fractions-free integer arithmetic via sympy cache."""
    return int(POLY[ident["name"]][2][i].subs(_t, t))

# integer-exact evaluators (avoid float): polynomials with rational coefficients
EVAL = {}
for name, (ident, _, xs, _) in POLY.items():
    ev = []
    for p in xs:
        num, den = sp.fraction(sp.together(p))
        pn = sp.Poly(num, _t); pd = sp.Poly(den, _t)
        ev.append((pn.all_coeffs(), pd.all_coeffs()))
    EVAL[name] = ev

def _horner(coeffs, t):
    r = 0
    for c in coeffs:
        r = r * t + int(c) if c == int(c) else None
        if r is None:
            raise ValueError("non-integer coeff")
    return r

def s_val(name, i, t):
    cn, cd = EVAL[name][i]
    # coefficients may be Rational: scale
    from fractions import Fraction
    def h(cs):
        r = Fraction(0)
        for c in cs:
            r = r * t + Fraction(int(c.p), int(c.q))
        return r
    v = h(cn) / h(cd)
    assert v.denominator == 1
    return int(v)

def decode_t(name, i, x, t0):
    """Unique t >= t0 with s_i(t) = x (s_i strictly increasing); None if absent."""
    lo, hi = t0, max(t0 + 1, 1)
    while s_val(name, i, hi) < x:
        hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if s_val(name, i, mid) < x: lo = mid + 1
        else: hi = mid
    return lo if s_val(name, i, lo) == x else None

LABEL = {}
for ident in IDENTITIES:
    LABEL[ident["name"]] = [sp.lambdify(_t, e.subs(T, _t), "math") if e.free_symbols else (lambda tt, c=int(e): c)
                            for _, e in ident["steps"]]
SIGN = {ident["name"]: [d for d, _ in ident["steps"]] for ident in IDENTITIES}
T0 = {i["name"]: t0 for (nm, M, r, t0, st), i in zip(_I, IDENTITIES)}
BYNAME = {i["name"]: i for i in IDENTITIES}

def class_of(n):
    """Residue-class rule (a fixed finite table mod 24)."""
    if n % 4 == 1: return "A"
    m8 = n % 8
    if m8 == 0: return "B"
    if m8 == 2: return "C"
    if m8 == 4: return "D"
    if m8 == 6: return "E"
    if m8 == 7: return "G"
    return {3: "F", 11: "H", 19: "I"}[n % 24]

def sigma(x, q):
    """Deterministic finite-control selector. Returns (sign, N, q_next)."""
    if q == READY:
        if x == 1: return ("+", 1, ("S1", 1))
        if x == 3: return ("+", 3, ("S3", 1))
        c = class_of(x)
        t = decode_t(c, 0, x, T0[c])
        return (SIGN[c][0], int(LABEL[c][0](t)), (c, 1) if len(SIGN[c]) > 1 else READY)
    c, i = q
    if c == "S1":
        # explicit path 1->4->18->81->8->2
        path = SPECIAL[1]
        # find label to reach path[i+1] from path[i]
        a, b = path[i], path[i + 1]
        return _special_move(a, b, ("S1", i + 1) if i + 1 < len(path) - 1 else READY)
    if c == "S3":
        path = SPECIAL[3]
        a, b = path[i], path[i + 1]
        return _special_move(a, b, ("S3", i + 1) if i + 1 < len(path) - 1 else READY)
    t = decode_t(c, i, x, T0[c])
    nxt = (c, i + 1) if i + 1 < len(SIGN[c]) else READY
    return (SIGN[c][i], int(LABEL[c][i](t)), nxt)

# the special paths are finitely many fixed moves; their labels are table entries
_SP = {(1, 4): ("+", 1), (4, 18): ("+", 2), (18, 81): ("+", 2), (81, 8): ("-", 8) , (8, 2): ("-", 1),
       (3, 16): ("+", 3), (16, 4): ("-", 1)}
def _special_move(a, b, q):
    s, N = _SP[(a, b)]
    return (s, N, q)
