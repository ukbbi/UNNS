"""Fast smoke tests (seconds). Run: python3 tests/test_benchmarks.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'code'))
from fractions import Fraction as Fr
from math import gcd
from geo1lib import *
assert fibre(72) == [2,3,6] and [(d-1, 72*(d-1)//d**2) for d in fibre(72)] == [(1,18),(2,16),(5,10)]
assert R(144) == 5 and fibre(144) == [2,3,4,6,12]
assert R(3600) == 11 and R(44100) == 15
assert fibre_q(Fr(2304,5)) == [6,16] and 48 not in fibre_q(Fr(2304,5)) and gcd(6,16) == 2
assert [m for _, m in succ(6)] == [24,27,32,49]
assert orbit(72, 8) == [72,108,144,288,432,576,1152,1728]
assert 4*4*Fr(49,6) == Fr(9,2)*Fr(784,27)          # the relation behind 6 -> 784
x = Fr(67500**2, 11); ys = [x]
for _ in range(16): ys.append(Fr(Cstep(ys[-1])))
assert ys[8] == 9*ys[0] and len(fibre_q(ys[8])) == len(fibre_q(ys[0])) + 2
print("all smoke tests passed")
