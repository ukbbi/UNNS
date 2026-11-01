import unittest
from fractions import Fraction as Fr
import _path  # noqa
import coverage_gap as cg
import planar_residual as pr
import audit_p3 as au


class TestPlanar(unittest.TestCase):
    def test_control_a_inherited(self):
        tr = cg.transition(Fr(21 ** 8, 5))
        res, F2, c2 = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
        self.assertEqual(res["verdict"], "CONTAINED")
        cl = cg.classify_target_planar(tr["P"], tr["b2"], tr["q"])
        self.assertEqual(cl["class"], "INHERITED_G12T8")
        self.assertEqual((cl["d"], cl["s"]), (2, 1))
        g = cg.coverage_gap_record(tr["P"], tr["b2"], tr["q"], F2, c2)
        self.assertTrue(g["hull_covered"])                 # exact cross-check of G12-T8 on this instance

    def test_control_b_residual_hollow(self):
        tr = cg.transition(Fr(55 ** 12, 27))
        res, F2, c2 = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
        self.assertEqual(res["verdict"], "CONTAINED")
        cl = cg.classify_target_planar(tr["P"], tr["b2"], tr["q"])
        self.assertEqual(cl["class"], "RESIDUAL_EXCEPTIONAL_HOLLOW_BOX")
        g = cg.coverage_gap_record(tr["P"], tr["b2"], tr["q"], F2, c2)
        self.assertFalse(g["hull_covered"])
        self.assertEqual(g["n_gap_pieces"], 6)

    def test_independent_normal_form_agrees(self):
        for x in (Fr(21 ** 8, 5), Fr(55 ** 12, 27)):
            tr = cg.transition(x)
            a = cg.planar_normal_form(tr["P"], tr["b2"], tr["q"])
            b = au.independent_normal_form(tr["P"], tr["b2"], tr["q"])
            self.assertEqual((a["d"], a["a"], a["c"], a["s"], tuple(a["Qn"])), (b["d"], b["a"], b["c"], b["s"], tuple(b["Qn"])))

    def test_audit_agrees_on_controls(self):
        for x in (Fr(21 ** 8, 5), Fr(55 ** 12, 27)):
            tr = cg.transition(x)
            res, _, _ = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
            ind = au.audit_verdict(tr["P"], tr["q"], tr["b"], tr["b2"], res["verdict"])
            self.assertTrue(au.verify_engine_result(res, ind, 2)[0])

    def test_rectangular_target_theorem_instance(self):
        # first rows of the pilot where target lattice is rectangular: must be contained
        rows, sk, _ = pr.sweep([2, 3, 5, 7], 3, 40, 2)
        n = 0
        for r in rows:
            o = pr.evaluate_planar(r, with_reverse=False, gap=False)
            if o["target_class"] in ("RESIDUAL_D1_RECTANGULAR", "TARGET_Z2_TRIVIAL"):
                n += 1
                self.assertEqual(o["verdict"], "CONTAINED")
        self.assertGreater(n, 0)


if __name__ == "__main__":
    unittest.main()
