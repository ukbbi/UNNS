"""GEO_HD_BRIDGE v005 -- A5-T1/T2: exact stage-jumping decision of C-reachability, no step cap.
The orbit of x under the frozen FIELD-I map is followed STAGE BY STAGE with the stage sieve (stage_sieve.py): inside a stage the states
are x0 + j L^2/G, so  (target - x0)/(L^2/G)  decides landing, and the first event tau_D comes from linear congruences, not from iteration.
Outcome classes:  REACHED(steps) / OVERSHOT / BLOCKED (an event adds an occurrence outside D(target): impossible afterwards by Lemma M) /
D_EMPTY / STAGE_CAP."""
from fractions import Fraction as Fr
from math import isqrt
from stage_sieve import stage_data, first_event, Qmod
from geo1lib import fibre_q

def decide(x0, target, max_stages=64, want_log=False):
    cur = Fr(x0); target = Fr(target); steps = 0; log = []
    Dt = frozenset(fibre_q(target)) if target > 0 else frozenset()
    for st in range(max_stages):
        if cur == target: return {'class': 'REACHED', 'steps': steps, 'stages': st, 'log': log}
        if cur > target: return {'class': 'OVERSHOT', 'steps': steps, 'stages': st, 'log': log}
        S = stage_data(cur)
        if S is None: return {'class': 'D_EMPTY', 'steps': steps, 'stages': st, 'log': log}
        if not set(S['D0']) <= Dt: return {'class': 'BLOCKED', 'steps': steps, 'stages': st, 'log': log, 'bad': sorted(set(S['D0']) - Dt)[:3]}
        Delta = Fr(S['L'] ** 2, S['G']); diff = target - cur; jl = diff / Delta
        jwin = jl.numerator // jl.denominator            # floor
        ev = None
        if jwin >= 1:
            J = 8
            while True:                                   # iterative deepening: candidate bound d <= sqrt(numerator at J) grows with J
                ev = first_event(S, min(J, jwin))
                if ev is not None or J >= jwin: break
                J *= 8
        if jl.denominator == 1 and (ev is None or ev['tau'] >= jl):
            return {'class': 'REACHED', 'steps': steps + int(jl), 'stages': st + 1, 'log': log}
        if ev is None or ev['tau'] > jwin:
            return {'class': 'OVERSHOT', 'steps': steps + jwin + 1, 'stages': st + 1, 'log': log}
        tau = ev['tau']
        if want_log: log.append({'at_step': steps + tau, 'tau': tau, 'new': ev['new'], 'L': S['L'], 'G': S['G'], 'D0': list(S['D0'])})
        cur = cur + tau * Delta; steps += tau
        if not set(fibre_q(cur)) <= Dt:
            return {'class': 'BLOCKED', 'steps': steps, 'stages': st + 1, 'log': log, 'bad': sorted(set(fibre_q(cur)) - Dt)[:3]}
    return {'class': 'STAGE_CAP', 'steps': steps, 'stages': max_stages, 'log': log}


# ---------------------------------------------------------------------------------------------------------------------
# Fast exact first-event scan on the activation-family line  x_u = P^2 u/(P-1)  (stage 1 of x = P^2/l, u = m + j, m = (P-1)/l).
# D(x_u) = { d >= 2 : d | P * s(u/g),  d = 1 (mod (P-1)/g) },  g = gcd(u, P-1),  s(w) = prod p^floor(v_p(w)/2)   (P squarefree).
# The scan visits u = m+1, m+2, ... and stops at the first u whose D differs from {P}; cost O(#u) with a smallest-prime-factor table.
from math import gcd
from array import array

def _spf_table(n):
    spf = array('i', range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j: spf[j] = i
    return spf

def _divisors_small(s):
    ds = [1]; x = s; p = 2
    while p * p <= x:
        if x % p == 0:
            e = 0
            while x % p == 0: x //= p; e += 1
            ds = [d * p ** i for d in ds for i in range(e + 1)]
        p += 1
    if x > 1: ds = ds + [d * x for d in ds]
    return ds

def line_scan(P, ps, l, umax, spf=None):
    """first u in (m, umax] with D(P^2 u/(P-1)) != {P}.  returns (u, new_set) or (None, None) if none up to umax.  P = prod(ps) squarefree."""
    N = P - 1; m = N // l
    spf = spf or _spf_table(min(umax, N) + 1)
    divsP = [1]
    for p in ps: divsP = divsP + [d * p for d in divsP]
    for u in range(m + 1, umax + 1):
        g = gcd(u, N); w = u // g; b = N // g
        s = 1; x = w
        while x > 1:
            p = spf[x]
            e = 0
            while x % p == 0: x //= p; e += 1
            s *= p ** (e // 2)
        cand = set()
        sd = _divisors_small(s) if s > 1 else [1]
        for d in divsP:
            for t in sd: cand.add(d * t)
        new = sorted(d for d in cand if d >= 2 and d != P and (d - 1) % b == 0)
        if new: return u, new
    return None, None


def resolve_family(k, l, ps, q, sim_cap=200000):
    """Exact classification of the activation-family member (k,l,ps,q): stage 1 by the line scan (fast), later stages by exact simulation of the frozen map.
    Requires P = prod(ps) squarefree (true for distinct primes)."""
    from activation_family import make
    from dynamic_activation import Cstep
    x, y, P = make(k, l, ps, q); m = (P - 1) // l
    u, new = line_scan(P, ps, l, q * q * m)
    allowed = {p * q for p in ps}
    if u is None: return {'class': 'REACHED', 'steps': (q * q - 1) * m, 'stage1_event_step': None, 'note': 'no event before u=q^2 m: x_u hits y on the line'}
    if u == q * q * m: return {'class': 'REACHED', 'steps': u - m, 'stage1_event_step': u - m, 'note': 'first event coincides with y'}
    if set(new) - allowed: return {'class': 'BLOCKED', 'steps': u - m, 'stage1_event_step': u - m, 'bad': sorted(set(new) - allowed)[:4]}
    Dy = set(fibre_q(y)); cur = Fr(P * P * u, P - 1); steps = u - m; prev = frozenset(fibre_q(cur)); ev = [(steps, sorted(set(new)))]
    for i in range(sim_cap):
        if cur == y: return {'class': 'REACHED', 'steps': steps + i, 'stage1_event_step': u - m, 'later_events': ev[1:]}
        if cur > y: return {'class': 'OVERSHOT', 'steps': steps + i, 'stage1_event_step': u - m}
        D = frozenset(fibre_q(cur))
        if D != prev: ev.append((steps + i, sorted(D - prev))); prev = D
        if not D <= Dy: return {'class': 'BLOCKED', 'steps': steps + i, 'stage1_event_step': u - m, 'bad': sorted(D - Dy)[:4]}
        cur, _ = Cstep(cur)
    return {'class': 'STAGE_CAP', 'steps': steps + sim_cap, 'stage1_event_step': u - m}
