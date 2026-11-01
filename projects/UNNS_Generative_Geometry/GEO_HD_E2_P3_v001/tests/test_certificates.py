import copy
import unittest
from fractions import Fraction as Fr
import _path  # noqa
import coverage_gap as cg
import exact_containment as ec
import certificate_check as cc


class TestTamper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tr = cg.transition(Fr(2 * 110 ** 4, 3))
        cls.res, _, _ = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
        tr = cg.transition(Fr(55 ** 12, 27))
        cls.pos, cls.F2, cls.c2 = cg.geometric_verdict(tr["P"], tr["b"], tr["b2"], tr["q"])
        cls.trB = tr

    def test_negative_ok(self):
        self.assertTrue(cc.verify_noncontainment(self.res["certificate"], self.res["target_maximal"], 3)[0])

    def test_tamper_witness(self):
        c = copy.deepcopy(self.res["certificate"])
        c["witness"][0] = "0"
        self.assertFalse(cc.verify_noncontainment(c, self.res["target_maximal"], 3)[0])

    def test_tamper_witness_inside_target(self):
        c = copy.deepcopy(self.res["certificate"])
        c["witness"] = ["1", "1", "1"]
        c["params"] = [str(x) for x in cc._params(c["source_cell"]["base"], c["source_cell"]["gens"], (1, 1, 1)) or []]
        self.assertFalse(cc.verify_noncontainment(c, self.res["target_maximal"], 3)[0])

    def test_tamper_inequality(self):
        c = copy.deepcopy(self.res["certificate"])
        c["violations"][0]["c"] = "1000000"
        self.assertFalse(cc.verify_noncontainment(c, self.res["target_maximal"], 3)[0])

    def test_drop_a_target_cell(self):
        c = copy.deepcopy(self.res["certificate"])
        c["violations"] = c["violations"][:-1]
        self.assertFalse(cc.verify_noncontainment(c, self.res["target_maximal"], 3)[0])

    def test_wrong_source_cell(self):
        c = copy.deepcopy(self.res["certificate"])
        c["source_cell"] = {"base": [5, 5, 5], "gens": [[1, 0, 0]]}
        self.assertFalse(cc.verify_noncontainment(c, self.res["target_maximal"], 3)[0])

    def test_positive_ok_and_tamper(self):
        T = self.pos["target_maximal"]
        for c in self.pos["certificates"]:
            self.assertTrue(cc.verify_containment(c, T, 2)[0])
        bad = copy.deepcopy(self.pos["certificates"][0])

        def corrupt(n):
            if "leaf" in n:
                n["leaf"] = (n["leaf"] + 1) % len(T)
                return True
            if "split" in n:
                return corrupt(n["lo"]) or corrupt(n["hi"])
            return False
        done = False
        for c in self.pos["certificates"]:
            c2 = copy.deepcopy(c)
            corrupt(c2["tree"])
            if not cc.verify_containment(c2, T, 2)[0]:
                done = True
                break
        self.assertTrue(done, "some corrupted leaf assignment must be rejected")

    def test_hull_tree_and_tamper(self):
        P, q, b2 = self.trB["P"], self.trB["q"], self.trB["b2"]
        F, G, cells = cg.cells_of(P, b2, q)
        g = ec.gap_decomposition(F, cells, 2)
        cert = {"hull_halfspaces": g["hull_halfspaces"], "tree": g["tree"]}
        ok, why, ngap = cc.verify_hull_tree(cert, F, g["target_maximal"], 2)
        self.assertTrue(ok, why)
        self.assertEqual(ngap, len(g["gap_pieces"]))
        # shrink the root hull: root vertices no longer all in F
        bad = copy.deepcopy(cert)
        a, c = bad["hull_halfspaces"][0]
        bad["hull_halfspaces"][0] = [a, str(Fr(c) + 100)]
        self.assertFalse(cc.verify_hull_tree(bad, F, g["target_maximal"], 2)[0])


if __name__ == "__main__":
    unittest.main()
