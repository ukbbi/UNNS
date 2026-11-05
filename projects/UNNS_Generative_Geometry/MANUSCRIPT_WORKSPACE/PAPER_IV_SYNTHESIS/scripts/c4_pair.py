import json, sys
from fractions import Fraction as Fr
from eng3 import *
res = {}
for S0 in (126, 3094):
    x = Fr(S0 * S0, 5); ok = True; Ds = []
    for k in range(12):
        y = x
        for _ in range(3): y = C(y)
        ok &= (y == 4 * x) and LG(Dset(x)) == (S0 * 2**k, 5)
        x = y
    seq = []
    for k in range(0, 15):
        S = S0 * 2**k; D = sorted(d for d in divisors(factor(S)) if d >= 2 and d % 5 == 1)
        seq.append({'k': k, 'nD': len(D), 'b': betti(complex_of(D), 2)[2]})
    res[S0] = {'orbit_law_periods': 12, 'ok': bool(ok), 'seq': seq}
    print(S0, ok, [s['b'] for s in seq][-4:], flush=True)
json.dump(res, open('../results/c4_pair.json', 'w'))
