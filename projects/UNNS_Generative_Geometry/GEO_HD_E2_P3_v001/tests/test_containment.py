import unittest
from fractions import Fraction as Fr
import _path  # noqa
import exact_containment as ec
import certificate_check as cc


def unit_cells(q, k, skip_origin=True):
    from itertools import product
    cells = []
    for base in product(*[range(m) for m in q]):
        verts = list(product(*[(b, b + 1) for b in base]))
        if skip_origin and (0,) * k in verts:
            continue
        cells.append((base, [tuple(int(i == j) for i in range(k)) for j in range(k)]))
    return cells


class TestContainment(unittest.TestCase):
    def test_triangle_cut_noncontained_3d(self):
        T = unit_cells((2, 2, 2), 3)
        r = ec.decide_union([((0, 0, 2), [(0, 1, -1), (1, 0, -1)])], T, 3)
        self.assertEqual(r["verdict"], "NOT_CONTAINED")
        ok, why = cc.verify_noncontainment(r["certificate"], r["target_maximal"], 3)
        self.assertTrue(ok, why)

    def test_witness_two_thirds_certificate(self):
        T = [ec.Target(b, g, 3) for b, g in ec.geometric_maximal(unit_cells((2, 2, 2), 3), 3)]
        cert = ec.noncontainment_certificate((0, 0, 2), [(0, 1, -1), (1, 0, -1)], (Fr(2, 3),) * 3, T, 3)
        ok, why = cc.verify_noncontainment(cert, [t.as_json() for t in T], 3)
        self.assertTrue(ok, why)

    def test_contained_planar_split(self):
        # a diagonal cell inside two unit squares' union
        T = [((0, 0), [(1, 0), (0, 1)]), ((1, 0), [(1, 0), (0, 1)]), ((0, 1), [(1, 0), (0, 1)]), ((1, 1), [(1, 0), (0, 1)])]
        r = ec.decide_union([((0, 1), [(1, -1), (1, 1)])], T, 2)
        self.assertEqual(r["verdict"], "CONTAINED")
        for c in r["certificates"]:
            self.assertTrue(cc.verify_containment(c, r["target_maximal"], 2)[0])

    def test_boundary_point_not_counted_as_outside(self):
        # point (1,0) is on the shared boundary of two cells: contained (closed cells), no strict-boundary error
        T = [((0, 0), [(1, 0)]), ((1, 0), [(1, 0)])]
        r = ec.decide_union([((1, 0), [])], T, 2)
        self.assertEqual(r["verdict"], "CONTAINED")

    def test_lower_dimensional_gap_detected(self):
        # two squares with a missing middle segment: segment [(1,0),(1,1)] is covered only if a cell contains it
        T = [((0, 0), [(1, 0), (0, 1)])]
        r = ec.decide_union([((1, 0), [(0, 1)])], T, 2)
        self.assertEqual(r["verdict"], "CONTAINED")        # boundary of the square
        r2 = ec.decide_union([((2, 0), [(0, 1)])], T, 2)
        self.assertEqual(r2["verdict"], "NOT_CONTAINED")
        self.assertTrue(cc.verify_noncontainment(r2["certificate"], r2["target_maximal"], 2)[0])

    def test_overlapping_target_cells(self):
        T = [((0, 0), [(2, 0), (0, 2)]), ((1, 1), [(2, 0), (0, 2)])]      # overlapping squares (improper overlap)
        r = ec.decide_union([((0, 0), [(3, 0)])], T, 2)
        self.assertEqual(r["verdict"], "NOT_CONTAINED")                   # (3,0) is outside both
        r = ec.decide_union([((1, 1), [(1, 1)])], T, 2)
        self.assertEqual(r["verdict"], "CONTAINED")

    def test_hull_gap_decomposition(self):
        pts = [(1, 0), (0, 1), (1, 1)]
        g = ec.gap_decomposition(pts, [((1, 0), [(0, 1)]), ((0, 1), [(1, 0)])], 2)
        self.assertGreater(len(g["gap_pieces"]), 0)


if __name__ == "__main__":
    unittest.main()
