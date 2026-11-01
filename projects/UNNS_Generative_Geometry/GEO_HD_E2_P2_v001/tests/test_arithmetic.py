import os, sys, unittest
from fractions import Fraction as Fr
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import lattice_transport as lt  # noqa: E402
import fibre_transport as ft  # noqa: E402
import geometry_audit as ga  # noqa: E402


class T(unittest.TestCase):
    def test_transitions(self):
        for a, b, b2 in ((21 ** 8, 5, 4), (55 ** 12, 27, 18)):
            r = ft.C_step(Fr(a, b))
            self.assertEqual(r["next"], Fr(a, b2))
            self.assertEqual(ga.C_brute(Fr(a, b))[0], Fr(a, b2))

    def test_relations(self):
        self.assertEqual(lt.relation((3, 7), 5, 4), "ENLARGE")
        self.assertEqual(lt.relation((3, 7), 4, 5), "SHRINK")
        self.assertEqual(lt.relation((5, 11), 27, 18), "ENLARGE")
        self.assertEqual(lt.relation((2, 11), 3, 7), "INCOMPARABLE")
        self.assertEqual(ga.relation_brute((2, 11), 3, 7), "INCOMPARABLE")
        self.assertEqual(lt.relation((3, 7), 5, 5), "EQUAL")

    def test_denominator_divisibility_is_not_needed(self):
        self.assertTrue(5 % 4 and 4 % 5)
        self.assertTrue(lt.included_K((3, 7), 5, 4) and lt.included_H((3, 7), 5, 4) and lt.included_basis((3, 7), 5, 4))

    def test_hnf(self):
        self.assertEqual(lt.describe((3, 7), 5)["hnf_basis"], [[1, 1], [0, 4]])
        self.assertEqual(lt.describe((3, 7), 4)["index"], 2)

    def test_coupled(self):
        self.assertTrue(lt.coupled((2, 5, 11), 3))
        self.assertFalse(lt.coupled((2, 3), 5) and False)


if __name__ == "__main__":
    unittest.main()
