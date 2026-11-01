"""G2-E/F: occurrence-event correspondence between SELECT-II histories and FIELD-I regime-I trajectories.
For an integer state, D(m) = Div(sigma(m)) \\ {1}; sigma = prod p^floor(v_p/2) determines D and conversely (sigma = max D).
Event record of a trajectory = its sequence of sigma-values with consecutive repetitions removed (births/losses/reappearances are read
off from divisibility between consecutive entries)."""
import _paths  # noqa
from fractions import Fraction as Fr
from functools import lru_cache
from geo1lib import factor, divisors_from
from geo_snapshots import s_of, vp
from field_regimes import split, orbit_pairs, value, next_pair, tau


def reduced(seq):
    out = [seq[0]]
    for z in seq[1:]:
        if z != out[-1]:
            out.append(z)
    return out


def sigma_transport(m, N):
    """exact sigma(m') / sigma(m) for the SELECT-II edge m --N--> m' (square-root transport):  (N+1)/c, c = prod p^{l_p}"""
    c = 1
    for p, n in factor(N).items():
        c *= p ** ((n // 2) if vp(m, p) % 2 else (n + 1) // 2)
    return Fr(N + 1, c)


def edge_successors(x, limit):
    out = []
    for N in sorted(divisors_from(factor(x))):
        z = x * (N + 1) ** 2 // N
        if z > limit:
            break
        out.append((N, z))
    return out


def reach(x, y):
    """is y reachable from x by a SELECT-II history (any labels)?"""
    seen = {}
    def rec(z):
        if z == y: return True
        if z > y: return False
        if z in seen: return seen[z]
        r = any(rec(w) for _, w in edge_successors(z, y))
        seen[z] = r; return r
    return rec(x)


def evmatch(x, y, target):
    """exists a SELECT-II history x ~> y whose reduced sigma-sequence equals `target` (list of sigma values)?"""
    seen = {}
    def rec(z, j):
        if z == y: return j == len(target) - 1
        if (z, j) in seen: return seen[(z, j)]
        r = False
        for _, w in edge_successors(z, y):
            sw = s_of(w)
            if sw == target[j] and rec(w, j): r = True; break
            if j + 1 < len(target) and sw == target[j + 1] and rec(w, j + 1): r = True; break
        seen[(z, j)] = r; return r
    return rec(x, 0)


def collective_sigmas(x, n):
    ps = orbit_pairs(x, n)
    return [p[0] for p in ps], [value(p) for p in ps]


def classify_pairs(starts, nmax=18, span=30, maxratio_pow=6):
    """finite-exact classification of all regime-I pairs (x_n, x_m) with j >= 1 births in between and 4 x_n <= x_m <= 4^pow x_n.
    Returns counts keyed (j, reachable, event_equivalent) and the list of event-equivalent pairs violating  x_m == 4^j x_n."""
    from collections import Counter
    cnt = Counter(); viol = []; tot = 0
    for x0 in starts:
        sig, xs = collective_sigmas(x0, nmax + span + 1)
        for n in range(nmax):
            for m in range(n + 1, min(len(xs), n + span)):
                if xs[m] > xs[n] * 4 ** maxratio_pow: break
                tgt = reduced(sig[n:m + 1]); j = len(tgt) - 1
                if j == 0 or xs[m] < 4 * xs[n]: continue
                r = reach(xs[n], xs[m])
                e = evmatch(xs[n], xs[m], tgt) if r else False
                cnt[(j, r, e)] += 1; tot += 1
                if e != (xs[m] == xs[n] * 4 ** j):
                    viol.append((x0, n, m, xs[n], xs[m], j, e))
    return cnt, viol, tot


def rigid_phase_record(sigma, t):
    """B2-T10: one rigid period (3 collective steps) vs one SELECT-II step N=1, from x = sigma^2 t, t in {1,2,3}, sigma even."""
    x = sigma * sigma * t
    ps = orbit_pairs(x, 3)
    coll = reduced([p[0] for p in ps])
    xs = [value(p) for p in ps]
    sel = reduced([s_of(x), s_of(4 * x)])
    births = [tau(b) - tau(a) for a, b in zip(coll, coll[1:])]
    return {'sigma': sigma, 't': t, 'x': x, 'C3': xs[-1], 'T1': 4 * x, 'collective_sigmas': coll, 'select_sigmas': sel,
            'equal_event_record': coll == sel and xs[-1] == 4 * x, 'births': births, 'carry_step': next((i for i in range(1, 4) if ps[i][2] > 1), None)}


def family_trace(a, s):
    """x = (2^a - 1) s^2 (s even, 2^a-1 squarefree): C^k(x) = T_N(x) = (2^a s)^2 with N = 2^a - 1; collective events vs one SELECT-II edge"""
    N = 2 ** a - 1
    x = N * s * s
    y = x * (N + 1) ** 2 // N
    k = 0; ps = orbit_pairs(x, 1)
    pairs = [(split(x)[0], split(x)[1], 1)]
    cur = pairs[0]
    while value(cur) < y:
        s2, t2, u = next_pair(cur[0], cur[1]); cur = (s2, t2, u); pairs.append(cur); k += 1
    sig = reduced([p[0] for p in pairs])
    return {'a': a, 's': s, 'N': N, 'x': x, 'y': y, 'hit': value(cur) == y, 'k': k, 'collective_events': len(sig) - 1,
            'select_events': 1, 'sigma_chain': sig}


def coincidence_scan(xmax=4000, kmax=60):
    """all (N,k) with C^k(x) = T_N(x), x = 4,8,...,xmax, 1 <= k < kmax (regime I)."""
    from collections import defaultdict
    R = {Fr((N + 1) ** 2, N): N for N in range(1, 4000)}
    hits = defaultdict(list)
    for x0 in range(4, xmax, 4):
        ps = orbit_pairs(x0, kmax)
        xs = [value(p) for p in ps]
        for k in range(1, kmax):
            r = Fr(xs[k], xs[0])
            if r in R and xs[0] % R[r] == 0:
                hits[(R[r], k)].append(x0)
    return dict(hits)
