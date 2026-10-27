"""Deterministic fast tests (seconds). Run: python3 tests/test_geo2.py"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'geometry'))
from geo2lib import *
def prof(x): return analyse(x)
p = prof(72);       assert (p['R'], p['d_amb'], p['d_aff'], p['axis']['d_cell']) == (3, 2, 2, 1)
p = prof(144);      assert (p['R'], p['d_aff'], p['axis']['d_cell'], p['axis']['cells_per_dim']) == (5, 2, 2, [5, 5, 1])
p = prof(3600);     assert p['axis']['cells_per_dim'] == [11, 17, 8, 1] and p['axis']['betti']['2'] == [1, 0, 0, 0]
p = prof(44100);    assert p['R'] == 15 and p['axis']['d_cell'] == 3 and p['axis']['cells_per_dim'] == [15, 28, 18, 4]
p = prof(210 ** 4); assert p['R'] == 80 and p['axis']['cells_per_dim'] == [80, 212, 210, 92, 15]
p = prof(Fr(2304, 5))
assert p['axis']['cells_per_dim'] == [2] and p['axis']['components'] == 2
assert p['move']['cells_per_dim'] == [2, 1] and p['move']['components'] == 1
assert sorted(map(tuple, p['graver_region'])) == [(1, 1), (3, -1), (4, 0)]
p = prof(Fr(19600, 3)); assert p['move']['betti']['2'] == [1, 1, 0] and p['axis']['betti']['2'] == [3, 0] and p['axis']['components'] == 3
p = prof(Fr(1600, 3)); assert p['move']['betti']['2'] == [1, 1] and p['axis']['components'] == 3
# boundary of boundary vanishes on a 4-cell
cells = build_cells(fibre_points(*coords(210 ** 4)), set(unit_moves(4)), 4); assert homology(cells)[1]
print('all geometry tests passed')
