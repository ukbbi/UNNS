import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import lattice_transport as lt  # noqa: E402
import graver_transport as gt  # noqa: E402
import geometry_audit as ga  # noqa: E402


class T(unittest.TestCase):
    def test_graver_sets(self):
        G = gt.graver_fast((3, 7), 5, (4, 4))
        G2 = gt.graver_fast((3, 7), 4, (4, 4))
        self.assertEqual(len(G), 12)
        self.assertEqual(len(G2), 8)
        self.assertEqual(sorted(set(G) & set(G2)), [(-1, -1), (1, 1)])
        self.assertEqual(sorted(G), sorted(ga.graver((3, 7), (4, 4), 5)))

    def test_region_is_graver_cap_box(self):
        big = set(gt.graver_fast((3, 7), 5, (9, 9)))
        for h in (1, 2, 3, 5):
            small = set(gt.graver_fast((3, 7), 5, (h, h)))
            self.assertEqual(small, {g for g in big if max(map(abs, g)) <= h})

    def test_survival_and_order_rule(self):
        for g in [(1, 1), (4, 0), (0, 4), (1, -3), (3, -1), (2, -2)]:
            s = gt.survives(g, (3, 7), 4)
            self.assertEqual(s, g == (1, 1))
            if gt.order_rule_blocks(g, (3, 7), 4):
                self.assertFalse(s)
        self.assertTrue(all(gt.order_rule_blocks(g, (3, 7), 4) for g in [(4, 0), (0, 4), (1, -3), (3, -1), (2, -2)]))
        self.assertFalse(gt.order_rule_blocks((1, 1), (3, 7), 4))

    def test_family_formula(self):
        self.assertEqual(gt.family_counts(4)["E_kept"], 3)
        self.assertEqual(gt.family_counts(4)["E_lost"], 8)
        for h in (8, 12):
            self.assertEqual(gt.family_counts(h)["E_kept"], (h // 4) ** 2 * 4 - 1)


if __name__ == "__main__":
    unittest.main()
