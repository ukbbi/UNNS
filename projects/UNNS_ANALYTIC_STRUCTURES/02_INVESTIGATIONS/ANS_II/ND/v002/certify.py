"""Directed-rounding (MPFR) certificate for the abscissa of 2/sqrt3. Needs gmpy2 and numpy.

v002: the v001 program with explicit validity checks on the trial weights (UNNS Research Collective review).

The weights theta come from the floating-point minimiser of ANS-II v002; any weights give valid
inequalities, so only the evaluation below has to be rigorous. Every elementary operation is an
MPFR operation rounded in the direction needed."""
import math, os, sys, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "v002"))
import gmpy2
from gmpy2 import mpfr

from rate import Grammar, TWO_OVER_SQRT3

PREC = 80
D = gmpy2.context(precision=PREC, round=gmpy2.RoundDown)
U = gmpy2.context(precision=PREC, round=gmpy2.RoundUp)
A_LOW, A_HIGH = 2.06055, 2.06072
HALF_EPS = 2.0 ** -40          # the doubles tested lie strictly inside the printed interval


def exponents(N):
    """{p: X_p(N)} = 2 v_p(N+1) - v_p(N) by trial division through a smallest-factor table."""
    out = {}
    for m, f in ((N, -1), (N + 1, 2)):
        while m > 1:
            p = SPF[m] or m
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            out[p] = out.get(p, 0) + f * e
    return out


def sieve(n):
    spf = [0] * (n + 1)
    for p in range(2, int(n ** 0.5) + 1):
        if not spf[p]:
            for m in range(p * p, n + 1, p):
                if not spf[m]:
                    spf[m] = p
    return spf


SPF = []
LOGS = {}


def log_iv(n):
    r = LOGS.get(n)
    if r is None:
        r = LOGS[n] = (D.log(n), U.log(n))
    return r


def term_iv(a, theta, logmu_lo, logmu_hi, X):
    """Interval for exp(a * (-log mu + sum_q theta_q X_q log q)); a > 0, theta >= 0 exact doubles."""
    lo, hi = D.minus(logmu_hi), U.minus(logmu_lo)
    for q, x in X.items():
        t = theta.get(q, 0.0)
        if t:
            llo, lhi = log_iv(q)
            tx_lo, tx_hi = D.mul(t, x), U.mul(t, x)
            lo = D.add(lo, D.mul(tx_lo, llo if x > 0 else lhi))
            hi = U.add(hi, U.mul(tx_hi, lhi if x > 0 else llo))
    return D.exp(D.mul(a, lo)), U.exp(U.mul(a, hi))


def letters(M):
    """(log mu interval, exponents) for nesting letters N <= M and the letter 2/sqrt3."""
    for N in range(1, M + 1):
        (a_lo, a_hi), (b_lo, b_hi) = log_iv(N + 1), log_iv(N)
        yield (D.sub(D.mul(2, a_lo), b_hi), U.sub(U.mul(2, a_hi), b_lo), exponents(N))
    (l2, h2), (l3, h3) = log_iv(2), log_iv(3)
    yield (D.sub(l2, U.div(h3, 2)), U.sub(h2, D.div(l3, 2)), {2: 1.0, 3: -0.5})


def check_weights(theta, upper, M):
    """The certificates need finite weights in [0, upper] indexed by primes of the alphabet.
    Raises instead of asserting, so that python -O cannot switch the check off."""
    for q, t in theta.items():
        if not (isinstance(q, int) and 2 <= q <= M + 1 and (SPF[q] == 0)):
            raise ValueError("weight index is not a prime of the alphabet: %r" % (q,))
        if not (math.isfinite(t) and 0.0 <= t <= upper):
            raise ValueError("trial weight outside [0, %r] at %r: %r" % (upper, q, t))


def lower_certificate(a, theta, M):
    check_weights(theta, 1.0, M)
    total = mpfr(0)
    g_lo, g_hi = {}, {}
    for lm_lo, lm_hi, X in letters(M):
        t_lo, t_hi = term_iv(a, theta, lm_lo, lm_hi, X)
        total = D.add(total, t_lo)
        for q, x in X.items():
            if x:
                g_lo[q] = D.add(g_lo.get(q, mpfr(0)), D.mul(x, t_lo if x > 0 else t_hi))
                g_hi[q] = U.add(g_hi.get(q, mpfr(0)), U.mul(x, t_hi if x > 0 else t_lo))
    # convexity: min over [0,1]^primes >= value + sum_q min over theta_q' of g_q (theta_q' - theta_q)
    bound = total
    for q in g_lo:
        t = theta.get(q, 0.0)
        llo, lhi = log_iv(q)
        lo = D.mul(D.mul(a, g_lo[q]), llo if g_lo[q] >= 0 else lhi)
        hi = U.mul(U.mul(a, g_hi[q]), lhi if g_hi[q] >= 0 else llo)
        # h(g) = min(-g t, g (1 - t)) is concave in g, so its minimum over [lo, hi] is at an end
        vals = []
        for g in (lo, hi):
            vals.append(min(D.mul(D.minus(g), t), D.mul(g, D.sub(1, t) if g >= 0 else U.sub(1, t))))
        bound = D.add(bound, min(vals))
    return bound


def upper_certificate(a, theta, M):
    check_weights(theta, 0.10, M)
    total = mpfr(0)
    for lm_lo, lm_hi, X in letters(M):
        total = U.add(total, term_iv(a, theta, lm_lo, lm_hi, X)[1])
    t = max(theta.values())
    c = D.mul(a, D.sub(1, U.mul(2, t)))                    # c = a (1 - 2t), rounded down
    assert c > 1
    exponent = U.sub(1, c)                                  # 1 - c, rounded up
    lo_log, hi_log = log_iv(M)
    tail = U.div(U.exp(U.mul(exponent, lo_log if exponent < 0 else hi_log)), D.sub(c, 1))
    return U.add(total, tail), tail


def run(M_low=200000, M_high=1000000, report=print):
    global SPF
    t0 = time.time()
    SPF = sieve(M_high + 1)
    G = Grammar(TWO_OVER_SQRT3, M_low)
    a_lo, a_hi = A_LOW + HALF_EPS, A_HIGH - HALF_EPS
    th_low, _ = G.minimise(a_lo, {}, sweeps=40, tol=1e-12)
    th_up, _ = G.minimise(a_hi, {}, sweeps=8, cap=0.10)
    th_low = {int(p): float(t) for p, t in th_low.items() if t > 0}
    th_up = {int(p): float(t) for p, t in th_up.items() if t > 0}
    low = lower_certificate(a_lo, th_low, M_low)
    report("lower certificate minus 1: %.3e (%.0f s)" % (float(low - 1), time.time() - t0))
    up, tail = upper_certificate(a_hi, th_up, M_high)
    report("upper certificate minus 1: %.3e, tail %.3e (%.0f s)" % (float(up - 1), float(tail), time.time() - t0))
    return {"a_low": a_lo, "a_high": a_hi, "interval": [A_LOW, A_HIGH], "M_low": M_low, "M_high": M_high,
            "lower_minus_1": float(D.sub(low, 1)), "upper_minus_1": float(U.sub(up, 1)), "tail": float(tail),
            "precision_bits": PREC, "gmpy2": gmpy2.version(), "mpfr": gmpy2.mpfr_version(),
            "lower_ok": bool(low >= 1), "upper_ok": bool(up < 1)}


if __name__ == "__main__":
    print(run())
