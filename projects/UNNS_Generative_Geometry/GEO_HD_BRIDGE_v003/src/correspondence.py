"""R3-H: which pairs of iterates of a modular tower are related by a SELECT-II multiplier R(N)=(N+1)^2/N (N | numerator), and
at which correspondence level (1 numerical, 3 event: number of D-changes along the collective segment vs 1 for one edge)."""
import _paths
from fractions import Fraction as Fr
from collective_regimes import orbit

def R_index(r):
    """N with R(N)=r (None if r is not a SELECT-II multiplier).  (N+1)^2/N is reduced, so N = denominator."""
    N = r.denominator
    return N if r == Fr((N + 1) ** 2, N) else None

def coincidences(S, l, nmax):
    xs, infos = orbit(Fr(S * S, l), nmax)
    rows = []
    for n in range(nmax):
        for m in range(n + 1, nmax + 1):
            N = R_index(xs[m] / xs[n])
            if N is None or xs[n].numerator % N: continue
            ev = sum(1 for i in range(n + 1, m + 1) if infos[i]['D'] != infos[i - 1]['D'])
            edge_event = 1 if infos[m]['D'] != infos[n]['D'] else 0
            rows.append({'n': n, 'm': m, 'N': N, 'collective_events': ev, 'edge_events': edge_event, 'level3': ev == edge_event})
    return rows

def predicted(xs_formula_t, P, rho2, nmax):
    """arithmetic prediction from x_{Pk+j} = rho2^k (j+1) x_0 : pairs (n,m) with ratio rho2^a v/u = R(N), N | numerator(x_n)."""
    out = []
    for n in range(nmax):
        k, j = divmod(n, P); u = j + 1
        for m in range(n + 1, nmax + 1):
            k2, j2 = divmod(m, P); v = j2 + 1; a = k2 - k
            N = R_index(Fr(rho2 ** a * v, u))
            if N is not None and xs_formula_t(n).numerator % N == 0: out.append((n, m, N))
    return out
