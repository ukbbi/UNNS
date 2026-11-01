import os, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, 'src')); sys.dont_write_bytecode = True
from fractions import Fraction as Fr
import activation_family as A, move_complex as M, dynamic_activation as T, verify_v004 as V

def test_b41_family():
    a = A.analyse(2, 3, [5, 11], 17)
    assert a['D_x'] == [55] and a['D_y'] == [55, 85, 187] and a['all_dormant_at_x'] and a['all_active_at_y']
    m = M.move_complex(Fr(935 ** 2, 3)); assert m['betti_gf2'] == [1, 1] and m['cells2'] == 0 and m['axis_edges'] == 0

def test_beta1_formula():
    for k in (2, 3, 4):
        x, y, P = A.make(*A.default_instance(k)); assert M.move_complex(y)['betti_gf2'] == [1, k * (k - 1) // 2]

def test_reached_orbit():
    r = T.classify(2, 3, [5, 11], 2); assert r['class'] == 'REACHED' and r['steps'] == 8
    assert T.classify(2, 3, [5, 11], 17)['class'] == 'BLOCKED'

def test_monotone_D():
    x = Fr(126 ** 2, 5)
    for _ in range(20):
        D = V.Dset(x); x2 = V.Cmap(x); assert D <= V.Dset(x2); x = x2

def test_integer_contractible():
    assert V.betti_state(Fr(900)) == [1, 0, 0]

def test_verifier_fast():
    for k in ('Z1', 'Z2', 'Z3', 'Z4', 'Z6', 'Z7'): V.SHARDS[k](False)
    assert not V.FAILS
