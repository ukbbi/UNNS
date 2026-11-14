"""UNNS_PRIME_DYN_v001 -- exact engine for forward UNNS transitions in valuation coordinates.
Written for this release from the definitions of Section 2; shares no code with the U4 releases.

State: x as an exponent dictionary {prime: exponent}.  Forward transition T_N(x) = x (N+1)^2 / N, N | x, N >= 2.
"""
import math
from functools import lru_cache
import sympy
from mpmath import mp, mpf, log, floor

mp.dps = 60

@lru_cache(maxsize=None)
def factor(n):
    return dict(sympy.factorint(n))

def to_int(e):
    return math.prod(p ** k for p, k in e.items())

def from_int(x):
    return dict(factor(x))

def val(x, p):
    k = 0
    while x % p == 0:
        x //= p; k += 1
    return k

def step_big(x, N):
    """Reference big-integer transition; raises if illegal."""
    assert N >= 2 and x % N == 0
    return x // N * (N + 1) ** 2

def step_expo(e, fN):
    """Valuation law applied to an exponent dict: fN = factorisation of N (dict), uses factor(N+1)."""
    N = to_int(fN)
    for q, k in fN.items():
        assert e.get(q, 0) >= k, "illegal move"
    fN1 = factor(N + 1)
    out = dict(e)
    for q in set(fN) | set(fN1):
        v = out.get(q, 0) - fN.get(q, 0) + 2 * fN1.get(q, 0)
        assert v >= 0
        if v: out[q] = v
        else: out.pop(q, None)
    return out

# ---------------------------------------------------------------- prime-fire rules
def r_maxpp(e):
    """largest prime-power part p^{v_p}; decided by logarithms with an exact integer fallback when two are within 1e-7."""
    ks = sorted(e, key=lambda p: -e[p] * math.log(p))
    if len(ks) > 1 and abs(e[ks[0]] * math.log(ks[0]) - e[ks[1]] * math.log(ks[1])) < 1e-7:
        return max(e, key=lambda p: p ** e[p])
    return ks[0]
def r_minpp(e): return min(e, key=lambda p: p ** e[p])
def r_spf(e):   return min(e)
def r_lpf(e):   return max(e)
RULES = {'MAXPP': r_maxpp, 'MINPP': r_minpp, 'SPF': r_spf, 'LPF': r_lpf}

def fire_prime(e, p):
    """Valuation-law step for N = p (prime)."""
    return step_expo(e, {p: 1})

def run_prime_fire(x0, rule, steps):
    """Return the itinerary (list of fired primes) and the list of states (exponent dicts) for `steps` steps."""
    e = from_int(x0); it = []; states = [e]
    for _ in range(steps):
        p = rule(e)
        it.append(p)
        e = fire_prime(e, p)
        states.append(e)
    return it, states

def run_prime_fire_big(x0, rule, steps):
    """Independent big-integer implementation: factor the integer at every step; no exponent bookkeeping."""
    x = x0; it = []
    for _ in range(steps):
        f = factor(x)
        assert math.prod(q ** k for q, k in f.items()) == x
        p = rule(f)
        it.append(p)
        x = step_big(x, p)
    return it

# ---------------------------------------------------------------- two-valuation tail
LN2 = log(mpf(2)); LN3 = log(mpf(3))
A = log(mpf(18)); B = log(mpf(48)); L = A + B           # L = ln 864
THETA = B / L

def transient(it):
    """Index after the last firing of a prime >= 5 (0 if none)."""
    T = 0
    for i, p in enumerate(it):
        if p >= 5: T = i + 1
    return T

def maxpp_full(x0, nexact, nrest=0):
    """MAXPP from x0: `nexact` steps by exact exponent-dictionary dynamics (all primes, no reduction),
    recording (alpha,beta)=(v2,v3) before each step; then `nrest` further steps with the proved two-counter reduction.
    Returns (itinerary, ab, T) with T = index after the last firing of a prime >= 5 within the exact stage."""
    e = from_int(x0); it = []; ab = []
    for _ in range(nexact):
        ab.append((e.get(2, 0), e.get(3, 0)))
        p = r_maxpp(e); it.append(p); e = fire_prime(e, p)
    T = transient(it)
    a, b = e.get(2, 0), e.get(3, 0)
    for _ in range(nrest):
        ab.append((a, b))
        if sgn_f(a, b) > 0: it.append(2); a, b = a - 1, b + 2
        else: it.append(3); a, b = a + 4, b - 1
    return it, ab, T

def tail_state(x0, nsteps_hint=None):
    """Run MAXPP until no prime >= 5 is in play and return (T, alpha, beta, itinerary_so_far)
    using the exponent dictionary; the 'in play' test is: support is {2,3} (all large primes exhausted)
    or the next several firings are 2/3 and the max prime power is 2^a or 3^b (checked by the theory)."""
    raise NotImplementedError

LN2F = math.log(2); LN3F = math.log(3)
def sgn_f(a, b):
    """sign of f = a ln2 - b ln3 (exact decision: float with a certified margin, else 60-digit mpmath)."""
    f = a * LN2F - b * LN3F
    if abs(f) > 1e-7: return 1 if f > 0 else -1
    g = a * LN2 - b * LN3
    return 1 if g > 0 else (-1 if g < 0 else 0)

def mawpp_two_counter(alpha, beta, n):
    """Iterate the two-counter system (alpha,beta) under MAXPP for n steps; returns itinerary (2/3) and final state."""
    out = []
    for _ in range(n):
        sg = sgn_f(alpha, beta)
        assert sg != 0
        if sg > 0:
            out.append(2); alpha, beta = alpha - 1, beta + 2
        else:
            out.append(3); alpha, beta = alpha + 4, beta - 1
        assert alpha >= 0 and beta >= 0
    return out, (alpha, beta)

def factor_complexity(w, k):
    if all(isinstance(c, int) and 0 < c < 10 for c in w):
        s = ''.join(map(str, w)); return len({s[i:i + k] for i in range(len(s) - k + 1)})
    return len({tuple(w[i:i + k]) for i in range(len(w) - k + 1)})

def smallest_period(w, maxp):
    n = len(w)
    for q in range(1, maxp + 1):
        if all(w[i] == w[i + q] for i in range(n - q)):
            return q
    return None
