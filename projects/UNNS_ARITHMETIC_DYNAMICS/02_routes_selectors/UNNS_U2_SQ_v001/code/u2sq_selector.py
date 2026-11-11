"""UNNS-U2-SQ: finite-control square generators for reversible SELECT-II.
sigma_direct : <=5 moves between consecutive squares, control states = READY + template phases.
sigma_wrap   : 45-state wrapper around the U2-001 successor selector, <=8 moves."""
import json, os
from fractions import Fraction
from math import isqrt
import sympy as sp
from u1_bnd_lib import fwd, inv
import u2_selector as U2

_t = sp.symbols("t", positive=True)
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/square_identities.json")))
READY = "READY"
def _coeffs(expr):
    p = sp.Poly(sp.expand(expr), _t)
    return [Fraction(int(c.p), int(c.q)) for c in p.all_coeffs()]
def _hor(cs, t):
    r = Fraction(0)
    for c in cs: r = r * t + c
    return r

CLS = {}
for rs, v in DATA["classes"].items():
    r = int(rs); n = 24 * _t + r; S = sp.expand(n ** 2); states = [_coeffs(S)]; labels = []; signs = []
    for s, Ns in v["steps"]:
        N = sp.sympify(Ns, locals={"t": _t}); labels.append(_coeffs(N)); signs.append(s)
        S = sp.cancel(S * (N + 1) ** 2 / N) if s == "+" else sp.cancel(S * N / (N + 1) ** 2)
        states.append(_coeffs(sp.expand(S)))
    CLS[r] = dict(t0=v["t0"], states=states, labels=labels, signs=signs)

def _decode(r, i, x):
    c = CLS[r]; lo = c["t0"]; hi = lo + 1
    while _hor(c["states"][i], hi) < x: hi *= 2
    while lo < hi:
        mid = (lo + hi) // 2
        if _hor(c["states"][i], mid) < x: lo = mid + 1
        else: hi = mid
    return lo if _hor(c["states"][i], lo) == x else None

def _label(r, i, t):
    v = _hor(CLS[r]["labels"][i], t); assert v.denominator == 1; return int(v)

SPECIAL = {int(k): v["labels"] for k, v in DATA["special"].items()}

def sigma_direct(x, q):
    if q == READY:
        n = isqrt(x); assert n * n == x
        if n in SPECIAL:
            s, N = SPECIAL[n][0]
            return (s, N, ("S", n, 1) if len(SPECIAL[n]) > 1 else READY)
        r = n % 24; t = (n - r) // 24
        s = CLS[r]["signs"][0]
        return (s, _label(r, 0, t), ("c", r, 1) if len(CLS[r]["signs"]) > 1 else READY)
    if q[0] == "S":
        _, n, i = q; s, N = SPECIAL[n][i]
        return (s, N, ("S", n, i + 1) if i + 1 < len(SPECIAL[n]) else READY)
    _, r, i = q
    t = _decode(r, i, x)
    s = CLS[r]["signs"][i]
    return (s, _label(r, i, t), ("c", r, i + 1) if i + 1 < len(CLS[r]["signs"]) else READY)

def control_states():
    Q = {READY}
    for r, c in CLS.items(): Q |= {("c", r, i) for i in range(1, len(c["signs"]))}
    for n, L in SPECIAL.items(): Q |= {("S", n, i) for i in range(1, len(L))}
    return Q

# ---- 45-state wrapper (built on the frozen U2-001 successor selector)
SQ_READY, SQ_FINISH = "SQ_READY", "SQ_FINISH"
def sigma_wrap(x, q):
    if q == SQ_READY:
        n = isqrt(x); assert n * n == x
        if n == 1: return ("+", 1, SQ_READY)
        return ("-", n - 1, ("SUB", U2.READY))
    if q == SQ_FINISH: return ("+", x, SQ_READY)
    _, oq = q
    s, N, nq = U2.sigma(x, oq)
    return (s, N, SQ_FINISH if nq == U2.READY else ("SUB", nq))
def wrap_control_states():
    return {SQ_READY, SQ_FINISH} | {("SUB", q) for q in U2_states()}
def U2_states():
    Q = {U2.READY} | {(c, i) for c in U2.SIGN for i in range(1, len(U2.SIGN[c]))} | {("S1", i) for i in range(1, 5)} | {("S3", 1)}
    return Q

# ---- k-th powers by lifting the U2-001 successor identities (each edge x--y becomes k edges x^(k-j)y^j -- x^(k-j-1)y^(j+1))
def _iroot(x, k):
    lo, hi = 1, 1
    while hi ** k <= x: hi *= 2
    while lo < hi:
        m = (lo + hi + 1) // 2
        if m ** k <= x: lo = m
        else: hi = m - 1
    return lo
def _special_path(n):
    from u1_bnd_lib import SPECIAL
    return SPECIAL[n]
_SPL = {1: [("+", 1), ("+", 2), ("+", 2), ("-", 8), ("-", 1)], 3: [("+", 3), ("-", 1)]}
def make_sigma_power(k):
    def sigma_power(x, q):
        if q == READY:
            n = _iroot(x, k); assert n ** k == x
            if n in _SPL:
                s, N = _SPL[n][0]; i2, j2 = (0, 1) if k > 1 else (1, 0)
                return (s, N, READY if i2 == len(_SPL[n]) else ("P", n, i2, j2))
            c = U2.class_of(n); t = U2.decode_t(c, 0, n, U2.T0[c]); s = U2.SIGN[c][0]; N = int(U2.LABEL[c][0](t))
            i2, j2 = (0, 1) if k > 1 else (1, 0)
            return (s, N, READY if i2 == len(U2.SIGN[c]) else ("p", c, i2, j2))
        if q[0] == "P":
            _, n, i, j = q; path = _special_path(n); lab = _SPL[n]
            s, N = lab[i] if j else lab[i]  # the same label repeats for all k lifted moves of step i
            # (i,j) is the phase BEFORE this move
            s, N = lab[i][0], lab[i][1]
            j2 = j + 1; i2 = i
            if j2 == k: j2 = 0; i2 = i + 1
            return (s, N, READY if i2 == len(lab) else ("P", n, i2, j2))
        _, c, i, j = q   # phase before move (i,j): state is s_i^(k-j) s_(i+1)^j
        # recover t: z(t) = s_i(t)^(k-j) * s_(i+1)(t)^j  (strictly increasing)
        lo, hi = U2.T0[c], U2.T0[c] + 1
        z = lambda t: U2.s_val(c, i, t) ** (k - j) * U2.s_val(c, i + 1, t) ** j
        while z(hi) < x: hi *= 2
        while lo < hi:
            m = (lo + hi) // 2
            if z(m) < x: lo = m + 1
            else: hi = m
        assert z(lo) == x; t = lo
        s = U2.SIGN[c][i]; N = int(U2.LABEL[c][i](t))
        j2 = j + 1; i2 = i
        if j2 == k: j2 = 0; i2 = i + 1
        return (s, N, READY if i2 == len(U2.SIGN[c]) else ("p", c, i2, j2))
    return sigma_power
