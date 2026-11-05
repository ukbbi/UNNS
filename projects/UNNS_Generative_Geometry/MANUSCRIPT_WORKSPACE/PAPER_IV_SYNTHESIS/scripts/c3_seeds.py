import sys, json, itertools
from fractions import Fraction as Fr
from eng3 import *
def tower_ok(S0, ell, rho, per, mult, K=4):
    x = Fr(S0 * S0, ell)
    for k in range(K):
        y = x
        for _ in range(per): 
            y = C(y)
            if y is None: return False
        if y != mult * x: return False
        x = y
    return True
def betti_seq(S0, ell, rho, K):
    out = []
    for k in range(K + 1):
        S = S0 * rho ** k; D = sorted(d for d in divisors(factor(S)) if d >= 2 and d % ell == 1)
        out.append((len(D), betti(complex_of(D), 2)[2]))
    return out
ell, rho, per, mult = 5, 2, 3, 4
primes = [2, 3, 7, 13, 17, 19, 23, 29]
res = []
for a in range(0, 3):
  for combo in itertools.product(range(0, 4), range(0, 3), range(0, 2), range(0, 2)):
    S0 = 2**a * 3**combo[0] * 7**combo[1] * 13**combo[2] * 17**combo[3]
    if S0 % 5 == 0 or S0 == 1: continue
    x0 = Fr(S0 * S0, ell)
    D = Dset(x0)
    if not D: continue
    L, G = LG(D)
    if L != S0 or G != ell: continue
    if not tower_ok(S0, ell, rho, per, mult, 4): continue
    bs = betti_seq(S0, ell, rho, 12)
    res.append((S0, bs))
    print(S0, [b for _, b in bs][-3:], [n for n, _ in bs][-2:], flush=True)
json.dump(res, open('../results/c3_seeds.json', 'w'))
