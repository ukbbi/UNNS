"""R3-F: collective map C(x)=x+L^2/G on rational states with modulus l (prime), x = t S^2 / l.
Class S_l : (S,l) with gcd(S,l)=1, D_l(S)={d|S, d>=2, d=1 mod l} nonempty, lcm D_l(S)=S, gcd{d-1}=l.
Local theorem (proved in theory/COLLECTIVE_REGIMES.md): for 1<=t<tau, C(tS^2/l)=(t+1)S^2/l, where tau is the first t>=2 with D(tS^2/l) != D(S^2/l)."""
import _paths
from fractions import Fraction as Fr
from math import gcd
from geo1lib import fibre_q, Lof, Gof, factor

def info(x):
    D = fibre_q(x)
    if not D: return None
    return {'D': frozenset(D), 'L': Lof(D), 'G': Gof(D)}

def orbit(x, n):
    xs = [Fr(x)]; infos = []
    for _ in range(n):
        i = info(xs[-1]); infos.append(i)
        xs.append(xs[-1] + Fr(i['L'] ** 2, i['G']))
    infos.append(info(xs[-1]))
    return xs, infos

def divisors_of(S):
    f = factor(S); ds = [1]
    for p, e in f.items(): ds = [d * p ** i for d in ds for i in range(e + 1)]
    return sorted(ds)

def D_mod(S, l): return frozenset(d for d in divisors_of(S) if d >= 2 and d % l == 1 % l)

def in_class(S, l):
    D = D_mod(S, l)
    if not D or gcd(S, l) != 1: return False
    L = 1; G = 0
    for d in D: L = L * d // gcd(L, d); G = gcd(G, d - 1)
    return L == S and G == l

def tau(S, l):
    D0 = info(Fr(S * S, l))['D']
    for t in range(2, l):
        i = info(Fr(t * S * S, l))
        if i is None or i['D'] != D0: return t
    return l            # reaches t = l: x becomes the integer S^2 (leaves the modular regime)

def stage_decomposition(S, l, nsteps):
    """follow the orbit from S^2/l; report event steps, event times in the current frame and frame multipliers."""
    xs, infos = orbit(Fr(S * S, l), nsteps)
    ev = []; frame = S; tstart = 1; last = 0
    for n in range(1, nsteps + 1):
        if infos[n]['D'] != infos[n - 1]['D']:
            tt = xs[n] * l / (frame * frame)           # t in the frame before the event
            ev.append({'step': n, 'stage_length': n - last, 't_event': str(tt), 'L_before': infos[n - 1]['L'], 'L_after': infos[n]['L'],
                       'new_indices': len(infos[n]['D'] - infos[n - 1]['D'])})
            frame = infos[n]['L']; last = n
    return xs, infos, ev

def S11(k): return 2 ** 2 * 3 ** (3 + k) * 5 ** 4
def S5(k): return 126 * 2 ** k

def tower_formula_ok(S0fun, l, P, rho2, K):
    """x_{P k + j} = (j+1) S_k^2 / l for 0<=j<P ... checked against the frozen map for k<=K."""
    xs, infos = orbit(Fr(S0fun(0) ** 2, l), P * K)
    bad = []
    for n in range(P * K):
        k, j = divmod(n, P)
        if xs[n] != Fr((j + 1) * S0fun(k) ** 2, l): bad.append(n)
        if infos[n]['G'] != l or infos[n]['L'] != S0fun(k): bad.append(('LG', n))
    return bad
