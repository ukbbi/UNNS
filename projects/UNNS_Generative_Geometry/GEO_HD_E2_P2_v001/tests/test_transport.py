import os, sys, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import lattice_transport as lt  # noqa: E402
import graver_transport as gt  # noqa: E402
import cell_transport as ct  # noqa: E402
import fibre_transport as ft  # noqa: E402
from build_p2 import fibre_of  # noqa: E402


def cx(P, b, q):
    F = fibre_of(P, b, q)
    return ct.ct0.build_complex(F, ft.oriented(gt.graver_fast(P, b, q)), 2)


class T(unittest.TestCase):
    def test_specimen_survival(self):
        s = ct.abstract_survival(cx((3, 7), 5, (4, 4)), cx((3, 7), 4, (4, 4)))
        self.assertEqual((s[1]["source"], s[1]["preserved"], s[1]["lost"]), (11, 3, 8))
        self.assertEqual((s[2]["source"], s[2]["preserved"]), (1, 0))
        s = ct.abstract_survival(cx((5, 11), 27, (6, 6)), cx((5, 11), 18, (6, 6)))
        self.assertEqual((s[1]["source"], s[1]["preserved"], s[1]["lost"]), (5, 5, 0))

    def test_planar_containment(self):
        r = ct.planar_transport(cx((3, 7), 5, (4, 4)), cx((3, 7), 4, (4, 4)), 4)
        self.assertEqual(r["union_relation"], "U_SUBSET_U2")
        self.assertEqual(r["witness_target_not_in_source"], ["0", "2"])
        r = ct.planar_transport(cx((3, 7), 4, (4, 4)), cx((3, 7), 5, (4, 4)), 4)   # reversed direction
        self.assertEqual(r["union_relation"], "U2_SUBSET_U")

    def test_prediction_equals_direct(self):
        P, b, b2, q = (3, 7), 5, 4, (4, 4)
        c1, c2 = cx(P, b, q), cx(P, b2, q)
        surv = set(gt.predict(ft.oriented(gt.graver_fast(P, b, q)), P, b2)["survive"])
        F2 = set(fibre_of(P, b2, q))
        for j in (1, 2):
            pred = {k for k, c in c1[j].items() if all(v in F2 for v in c.verts) and all(g in surv for g in c.gens)}
            self.assertEqual(pred, set(c1[j]) & set(c2[j]))


if __name__ == "__main__":
    unittest.main()
