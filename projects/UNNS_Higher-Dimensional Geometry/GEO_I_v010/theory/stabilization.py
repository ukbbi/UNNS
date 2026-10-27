"""GEO-I v004, Programme A (k=2): planar stabilization.  Exact statements and finite certificates.

SCALING REDUCTION (S1).  For k=2, Lambda = ker(Z^2 -> (Z/b)^x) has fibre isomorphic (by an axis-wise affine rescaling that preserves
Graver moves, cells and U's topology) to the pure lattice  L(d,s) = {(i,j): j = s*i mod d}  in the box Q=(floor(q1/a), floor(q2/c)),
where d | gcd(o1,o2), a=o1/d, c=o2/d, s in (Z/d)^x.   (d = |<p1> ∩ <p2>| .)
CORRECTED STABILIZATION CONJECTURE / THEOREM (G4-C1).  The v003 guess  q_i > o_i  =>  beta1(U)=0  is FALSE (certified counterexample
b=15, (p1,p2)=(7,2)-type fibres, see output/reports).  The correct statement is: for d >= 2 and Q1,Q2 >= d with Q != (d,d),
        U = conv(F)  (hence contractible, beta_1 = 0),
while at Q=(d,d)   U is hollow and beta_1 = B(d,s) = d if s = -1 (mod d) else 2.   d=1 (Lambda = (o1 Z)x(o2 Z)): U is always contractible.
Status.  PROVED by hand (MATHEMATICS.md): the scaling reduction S1; the translation lemma S4 (so a finite base window decides all boxes for a given (d,s));
the hollow value beta_1 = d at Q=(d,d) for s = -1 (explicit fan graph) and the d=1 case.  PROVED BY EXACT COMPUTATION (computer-assisted, every step exact rational
arithmetic): U = conv(F) on the whole base window [d,3d-1]^2 minus {(d,d)} for EVERY (d,s) with 2 <= d <= 13, hence (S4) for all boxes Q >= (d,d), Q != (d,d);
the hollow values B(d,s) for d <= 13.  OPEN: the statement for general d (d >= 14 is not certified), and B(d,s) = 2 for s != -1 in general."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice_model import Lat
from coverage import uncovered


def data_to_pure(o1, o2, d, s, q):
    a, c = o1 // d, o2 // d
    return Lat(d, d, d, s), (q[0] // a, q[1] // c)


def predicted_beta1(d, s, Q):
    """beta_1(U) predicted by the corrected theorem (None outside its scope)."""
    if d == 1: return 0
    if Q[0] < d or Q[1] < d: return None
    if tuple(Q) != (d, d): return 0
    return d if (s + 1) % d == 0 else 2


def hull_covered(d, s, Q):
    """exact test U == conv(F) (empty uncovered region)."""
    return not uncovered(Lat(d, d, d, s), Q)


# ---------------------------------------------------------------------------------------------- realization of a pure model by primes
def _is_prime(n):
    if n < 2: return False
    i = 2
    while i * i <= n:
        if n % i == 0: return False
        i += 1
    return True


def prime_in_class(r, b, avoid=()):
    """smallest prime p = r (mod b), p not in avoid (Dirichlet: exists; found by search)."""
    p = r % b or b
    while True:
        if _is_prime(p) and p not in avoid: return p
        p += b


def realize(o1, o2, d, s, bmax=400):
    """find (b, (r1,r2)) whose relation lattice equals Lat(o1,o2,d,s) exactly (checked on a full window), plus prime representatives."""
    from math import gcd
    from arith import order_mod, in_lambda
    L = Lat(o1, o2, d, s)
    for b in range(2, bmax + 1):
        U = [r for r in range(2, b) if gcd(r, b) == 1]
        for r1 in U:
            if order_mod(r1, b) != o1: continue
            for r2 in U:
                if order_mod(r2, b) != o2: continue
                R = 2 * max(o1, o2)
                if all(in_lambda((r1, r2), b, (x, y)) == ((x, y) in L) for x in range(-R, R + 1) for y in range(-R, R + 1)):
                    p1 = prime_in_class(r1, b); p2 = prime_in_class(r2, b, avoid=(p1,))
                    return {'b': b, 'res': (r1, r2), 'primes': (p1, p2)}
    return None
