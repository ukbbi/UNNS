#!/usr/bin/env python3
"""
Independent check of the corrected quantizer bound (AR-3.1).  Standard library only.
Deliberately imports NOTHING from esc_i.py or admissibility.py: own random generator, own quantizer, own arithmetic.

Claim being tested.  System: T = V diag(lam, mu) V^-1, |lam| > |mu|.  Orbit: y_(n+1) = Q_k(T y_n), where Q_k rounds each
coordinate to k significant bits.  In eigen-coordinates z = V^-1 y, at every step
    |V^-1 (Q_k(T y) - T y)|_inf  <=  kappa_inf(V) * |lam| * 2^-k * |z|_inf ,   kappa_inf(V) = |V|_inf |V^-1|_inf.
The original (falsified) conversion omitted the factor |lam|; this script counts violations of both.

Usage:  python independent_check_ar31.py [seed] [number_of_systems]      (defaults: 12345, 400)
Expected: 0 violations of the corrected bound for every seed; many violations of the original bound.
"""
import math, random, sys
from fractions import Fraction as F

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 12345
n_sys = int(sys.argv[2]) if len(sys.argv) > 2 else 400
rnd = random.Random(seed)

def inf(M): return max(abs(M[0]) + abs(M[1]), abs(M[2]) + abs(M[3]))
def inv(M): d = M[0]*M[3] - M[1]*M[2]; return (M[3]/d, -M[1]/d, -M[2]/d, M[0]/d)
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def ap(M, v): return (M[0]*v[0] + M[1]*v[1], M[2]*v[0] + M[3]*v[1])

def quant(x, k):
    """Round x to k significant bits (nearest, ties upward). Exponent found by search, not by bit tricks."""
    if x == 0: return F(0)
    a = abs(x); e = 0
    while F(2)**e > a: e -= 1
    while F(2)**(e + 1) <= a: e += 1               # 2^e <= |x| < 2^(e+1)
    q = F(2)**(e - k + 1)
    return math.floor(x / q + F(1, 2)) * q

viol_new = viol_old = steps = 0
worst = 0.0
for _ in range(n_sys):
    while True:
        V = tuple(F(rnd.randint(-6, 6), 2) for _ in range(4))
        if V[0]*V[3] - V[1]*V[2] != 0: break
    lam = F(rnd.randint(5, 24), 4) * rnd.choice([-1, 1])
    mu = F(rnd.randint(0, int(abs(lam)*4) - 1), 4) * rnd.choice([-1, 1])
    k = rnd.choice([4, 8, 12])
    kappa = inf(V) * inf(inv(V))
    eta_new, eta_old = kappa * abs(lam) / 2**k, kappa / 2**k
    Vi = inv(V); T = mul(mul(V, (lam, F(0), F(0), mu)), Vi)
    y = ap(V, (F(1), F(1, 2)))
    for _ in range(40):
        z = ap(Vi, y); nz = max(abs(z[0]), abs(z[1]))
        yt = ap(T, y); yq = (quant(yt[0], k), quant(yt[1], k))
        e = ap(Vi, (yq[0] - yt[0], yq[1] - yt[1]))
        r = max(abs(e[0]), abs(e[1])) / nz
        steps += 1; viol_new += r > eta_new; viol_old += r > eta_old
        worst = max(worst, float(r / eta_new)); y = yq

print(f"seed {seed}; systems {n_sys}; steps checked {steps}")
print(f"violations of corrected bound  kappa*|lam|*2^-k : {viol_new}")
print(f"violations of original bound   kappa*2^-k       : {viol_old}")
print(f"max observed error / corrected bound            : {worst:.3f}")
print("RESULT:", "corrected bound holds" if viol_new == 0 else "CORRECTED BOUND VIOLATED -- investigate")
sys.exit(0 if viol_new == 0 else 1)
