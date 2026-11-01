"""A4-T5/T6: Betti evolution along the l=11 (G=11) and l=5 (G=5) towers, from the frozen GEO-I engine.
S_k(11) = 2^2 3^(3+k) 5^4 ; state at period start k is S_k^2/11.   S_k(5)=126*2^k ; state S_k^2/5."""
import _paths, json, sys, time
from fractions import Fraction as Fr
from collective_regimes import S11, S5
from geometric_transitions import geo_row

def row11(k):
    r = geo_row(Fr(S11(k) ** 2, 11)); r['k'] = k; return r
def row5(k):
    r = geo_row(Fr(S5(k) ** 2, 5)); r['k'] = k; return r

if __name__ == '__main__':
    which, k0, k1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    f = row11 if which == '11' else row5; rows = []
    for k in range(k0, k1 + 1):
        t = time.time(); rows.append(f(k)); rows[-1]['sec'] = round(time.time() - t, 2)
        json.dump(rows, open(out, 'w'))
