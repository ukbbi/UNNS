"""The generative layer: nesting, ordered histories, and the record R(w) = (w, K(w), Q(w), E(w)).

Everything here is obtained by performing the nesting operation  M nest N = M (N+1)^2 / N.
Analytic quantities elsewhere are aggregations of these records.
"""
from fractions import Fraction
from math import gcd


def nest(x, N):
    """T_N(x) = x (N+1)^2 / N, admissible iff N | x."""
    if x % N:
        raise ValueError("inadmissible: %d does not divide %d" % (N, x))
    return x // N * (N + 1) ** 2


def replay(source, word):
    """The complete state sequence x_0, x_1, ..., x_k (raises if any step is inadmissible)."""
    states = [source]
    for N in word:
        states.append(nest(states[-1], N))
    return states


def records(X):
    """All records (w, K, Q, E) with E <= X, grown letter by letter:
       K(wN) = K(w) N/gcd(E(w),N),   E(wN) = E(w)(N+1)^2/gcd(E(w),N),   Q = E/K."""
    stack = [((), 1, 1)]
    while stack:
        w, K, E = stack.pop()
        yield w, K, Fraction(E, K), E
        N = 1
        while (N + 1) ** 2 <= X and (N + 1) ** 2 * E <= X * N:
            g = gcd(E, N)
            F = (N + 1) ** 2 * (E // g)
            if F <= X:
                stack.append((w + (N,), K * (N // g), F))
            N += 1


def orbit_histories(source, X):
    """All admissible histories starting at `source` whose endpoint is <= X (forward generation)."""
    stack = [((), source)]
    while stack:
        w, x = stack.pop()
        yield w, x
        for N in range(1, min(x, X // x) + 1):    # r_N > N, so N <= X/x is necessary
            if x % N == 0:
                y = x // N * (N + 1) ** 2
                if y > X:                          # r_N increases with N
                    break
                stack.append((w + (N,), y))


def prime_word(p, memo=None):
    """A word admissible from source 1 whose endpoint is divisible by p (ANS-T15 lemma):
       w_2 = (1);  w_p = (concatenation of w_q, v_q(p-1) times each) followed by p-1."""
    memo = {} if memo is None else memo
    if p not in memo:
        if p == 2:
            memo[p] = (1,)
        else:
            n, q, out = p - 1, 2, []
            while n > 1:
                while n % q == 0:
                    out.extend(prime_word(q, memo))
                    n //= q
                q += 1
            memo[p] = tuple(out) + (p - 1,)
    return memo[p]


def aggregation_witness(X):
    """Distinct words with identical (depth, K, E): F(s,u,t) cannot separate them."""
    seen, best = {}, None
    for w, K, Q, E in records(X):
        key = (len(w), K, E)
        if key in seen:
            cand = (E, len(w), K, sorted([seen[key], w]))
            if best is None or cand < best:
                best = cand
        else:
            seen[key] = w
    if best is None:
        return None
    E, k, K, words = best
    return {"E": E, "K": K, "depth": k, "words": [list(v) for v in words]}


def orbit_counts(source, ceilings):
    """Number of histories from `source` with endpoint <= X, for each X, in one traversal."""
    top, hist = max(ceilings), [0] * len(ceilings)
    order = sorted(range(len(ceilings)), key=lambda i: ceilings[i])
    stack = [source]
    while stack:
        x = stack.pop()
        for i in order:
            if x <= ceilings[i]:
                hist[i] += 1
                break
        for N in range(1, min(x, top // x) + 1):
            if x % N == 0:
                y = x // N * (N + 1) ** 2
                if y > top:
                    break
                stack.append(y)
    out, run = {}, 0
    for i in order:
        run += hist[i]
        out[ceilings[i]] = run
    return [out[X] for X in ceilings]
