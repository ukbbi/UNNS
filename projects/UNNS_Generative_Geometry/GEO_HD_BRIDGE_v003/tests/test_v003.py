import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, "src")); sys.dont_write_bytecode = True
from fractions import Fraction as Fr
import rational_geometry as R, collective_regimes as C, history_invariants as H

def test_family2_first():
    x, y = Fr(25 * 13 * 13, 5 * 13 - 1), Fr(25 * 13 * 13, 8)
    rx, ry = R.record(x), R.record(y)
    assert rx['D'] == ry['D'] == {65} and len(rx['G']) == 2 and len(ry['G']) == 4

def test_realised_from_F():
    rec = R.record(Fr(25 * 13 * 13, 8)); s = R.split_graver(rec)
    assert s['F_only_prediction_ok'] and len(s['dormant']) == 2

def test_tower11_and_tower5():
    assert C.tower_formula_ok(C.S11, 11, 8, 9, 3) == [] and C.tower_formula_ok(C.S5, 5, 3, 4, 5) == []

def test_rigid_with_G5():
    xs, infos = C.orbit(Fr(126 * 126, 5), 12)
    assert all(i['G'] == 5 for i in infos[:-1]) and all(xs[i + 3] == 4 * xs[i] for i in range(9))

def test_pair_order_invariant():
    for A in [(3, 5, 6), (3, 5, 6, 7), (5, 9)]:
        r = H.analyse_content(A)
        assert r['bit_constant_on_components'] and r['both_orders_present'] and not r['adjacent_2_4_in_some_word']

def test_shards():
    for s in ("Z0", "Z1", "Z3", "Z5"):
        assert subprocess.run([sys.executable, os.path.join(ROOT, "RUN_VERIFY.py"), "--shard", s], capture_output=True).returncode == 0
