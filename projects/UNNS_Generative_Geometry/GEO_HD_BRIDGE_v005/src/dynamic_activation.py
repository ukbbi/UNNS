"""A4-T3: dynamic activation under the actual FIELD-I map C(x)=x+L^2/G.
Facts used (proved in theory/DYNAMIC_ACTIVATION.md):
 (M)  D is monotone along C-orbits: D(x) subset D(C(x)).
 (P)  from x=P^2/l: C-orbit = x_j = P^2 (m+j)/(l m), m=(P-1)/l, until the first state with D != {P}.
 (O)  if q^2 > l the first event occurs at u=m+j <= l m < q^2 m; reaching y would need D(event) subset D(y)."""
import _paths, itertools
from fractions import Fraction as Fr
from math import gcd
from geo1lib import fibre_q, Lof, Gof
from activation_family import make, evec, vsub

def Cstep(x):
    D = fibre_q(x)
    if not D: return None, None
    return x + Fr(Lof(D) ** 2, Gof(D)), frozenset(D)

def orbit_until(x, y, maxn=10 ** 6):
    """follow the actual map until x>=y or D empty. returns list of (n, state, D)"""
    out = []; cur = Fr(x); n = 0
    while n <= maxn:
        nxt, D = Cstep(cur)
        out.append((n, cur, D))
        if D is None or cur >= y: break
        cur = nxt; n += 1
    return out

def analyse_orbit(k, l, ps, q, cap=10 ** 6):
    x, y, P = make(k, l, ps, q); m = (P - 1) // l
    Dy = frozenset(fibre_q(y))
    cur = x; n = 0; first = None; mono = True; prev = None
    while cur < y and n < cap:
        nxt, D = Cstep(cur)
        if D is None: return {'status': 'D_EMPTY', 'n': n}
        if prev is not None and not (prev <= D): mono = False
        if first is None and D != frozenset([P]):
            u = cur * l * m / (P * P); first = {'n': n, 'u': str(u), 'u_over_m': str(u / m), 'state': str(cur), 'D': sorted(D)}
        prev = D; cur = nxt; n += 1
    reached = (cur == y)
    return {'k': k, 'l': l, 'q': q, 'P': P, 'm': m, 'jstar': (q * q - 1) * m, 'steps': n, 'reached_y': reached,
            'first_event': first, 'D_monotone': mono, 'q2_gt_l': q * q > l,
            'D_first_event_subset_Dy': (frozenset(first['D']) <= Dy) if first else None}

# ---------------------------------------------------------------- trajectory-level activation records
from rational_geometry import record, split_graver
from move_complex import edges_from_F, betti_1skeleton, cells_from_F

def univ_vec(ps, g):
    return tuple(sorted((p, e) for p, e in zip(ps, g) if e))

def state_summary(x):
    """exact summary of a state in universal coordinates: D, b, Graver relations, edge-realised relations, K_move betti (when no 2-cells)"""
    r = record(x); k = len(r['ps']); sp = split_graver(r)
    E = edges_from_F(r['F'], k); C = cells_from_F(r['F'], k, maxdim=2)
    return {'x': x, 'b': r['b'], 'D': frozenset(r['D']), 'ps': r['ps'],
            'Gr': {univ_vec(r['ps'], g) for g in r['G']},
            'dormant': {univ_vec(r['ps'], g) for g in sp['dormant']},
            'edge_real': {univ_vec(r['ps'], g) for g in sp['edge_realized']},
            'pos_prim': {univ_vec(r['ps'], g) for g in sp['positive_primitive']},
            'nE': len(E), 'nV': len(r['F']), 'n2': len(C[2]),
            'betti': betti_1skeleton(r['F'], E, 2) if not C[2] else None}

def trace_events(k, l, ps, q, cap=10 ** 5):
    """follow C from x; keep summaries at x, and at the states where D changes (and the step before), and at y if reached."""
    x, y, P = make(k, l, ps, q)
    rel = {(('%d' % ps[i]), ('%d' % ps[j])): tuple(sorted(((ps[i], 1), (ps[j], -1)))) for i in range(k) for j in range(k) if i != j}
    cur = x; n = 0; prevD = None; prevsum = None; log = []; first = None
    sx = state_summary(x); log.append((0, sx))
    prev = sx
    while n < cap and cur < y:
        nxt, D = Cstep(cur)
        if D is None: break
        if prevD is not None and D != prevD:
            s = state_summary(cur); log.append((n, s)); prev = s
        prevD = D; cur = nxt; n += 1
    reached = cur == y
    if reached: log.append((n, state_summary(cur)))
    return {'x': x, 'y': y, 'P': P, 'reached': reached, 'steps': n, 'log': log, 'rel': rel}

def activation_events(x0, nsteps):
    """B4-4: along the actual map, list step-level and trajectory-level events for primitive relations (universal coordinates).
    step activation:  g in Gr(x_n), E_g(x_n)=empty, E_g(x_{n+1}) non-empty            (g in Gr(x_n) is the 'existing primitive relation' test)
    creation-realisation: g not in Gr(x_n), E_g(x_{n+1}) non-empty, E_g(x_n)=empty
    trajectory activation (m<n): g in Gr(x_m) with E_g(x_m)=empty and E_g(x_n) non-empty, g never in Gr-with-E at the m..n-1 (first realisation)"""
    cur = Fr(x0); S = []; X = []
    for n in range(nsteps + 1):
        X.append(cur); S.append(state_summary(cur))
        nxt, D = Cstep(cur)
        if D is None: break
        cur = nxt
    def Eset(s):    # realised relations (all pairs in D), universal coordinates
        D = sorted(s['D']); ev = {d: evec(d) for d in D}
        return {vsub(ev[v], ev[u]) for u in D for v in D if u != v}
    E = [Eset(s) for s in S]
    ev = {'step_activation': [], 'creation_realisation': [], 'trajectory_activation': [], 'persistence_violations': 0}
    seen = set()
    for n in range(len(S) - 1):
        if not (S[n]['D'] <= S[n + 1]['D']): ev['persistence_violations'] += 1
        new = E[n + 1] - E[n]
        for g in new:
            (ev['step_activation'] if g in S[n]['Gr'] else ev['creation_realisation']).append((n, g))
    for n in range(len(S)):
        for g in E[n]:
            if g in seen: continue
            seen.add(g)
            m0 = next((m for m in range(n) if g in S[m]['Gr'] and g not in E[m]), None)
            if m0 is not None: ev['trajectory_activation'].append((m0, n, g))
    return {'X': X, 'S': S, 'events': ev}

def classify(k, l, ps, q, cap=200000):
    """exact classification of the C-orbit of x relative to y:  REACHED / OVERSHOT / BLOCKED (D leaves D(y): provably unreachable by monotonicity) / UNRESOLVED (cap)"""
    x, y, P = make(k, l, ps, q); m = (P - 1) // l
    Dy = frozenset(fibre_q(y)); cur = x; n = 0; first = None
    while n < cap:
        if cur == y: return {'class': 'REACHED', 'steps': n, 'first_u_over_m': first}
        if cur > y: return {'class': 'OVERSHOT', 'steps': n, 'first_u_over_m': first}
        nxt, D = Cstep(cur)
        if D is None: return {'class': 'D_EMPTY', 'steps': n}
        if first is None and D != frozenset([P]): first = str(cur * l * m / (P * P) / m)
        if not (D <= Dy): return {'class': 'BLOCKED', 'steps': n, 'first_u_over_m': first, 'bad': sorted(D - Dy)[:3]}
        cur = nxt; n += 1
    return {'class': 'UNRESOLVED', 'steps': n, 'first_u_over_m': first}
