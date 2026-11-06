import json, os, sys, unittest
from fractions import Fraction
from math import gcd, log2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import obs
ROOT = _path.ROOT
R = json.load(open(os.path.join(ROOT, "RESULTS", "E01_information_recovery.json")))
A1, A2 = (2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9)


class T(unittest.TestCase):
    def test_survival_laws(self):
        for C, m0, g in ((A1, 288, 30), (A2, 432, 42)):
            an = obs.Anchor(C, m0)
            self.assertEqual(an.beta2, 1)
            for t in range(1, 61):
                self.assertEqual(an.state(obs.System(C, m0 * t)) == 1, gcd(t, g) == 1)

    def test_entropy_of_survival(self):
        for tag, k in (("A1", 16), ("A2", 17)):
            p = k / 60
            h = -p * log2(p) - (1 - p) * log2(1 - p)
            self.assertAlmostEqual(float(R[tag]["ensembles"]["sources_60_binaryY"]["levels"]["O0"]["H(Y)"]), h, places=12)
        self.assertAlmostEqual(float(R["A1"]["ensembles"]["sources_60_binaryY"]["levels"]["O0"]["H(Y)"]), 0.83664, places=5)

    def test_profile_60_sources_degenerate(self):
        for tag in ("A1", "A2"):
            for lev, v in R[tag]["ensembles"]["sources_60_binaryY"]["levels"].items():
                self.assertEqual(float(v["H(Y|O)"]), 0.0)
                self.assertEqual(v["observation_classes"], 8)

    def test_N_injective_on_comparable_window(self):
        for tag in ("A1", "A2"):
            Ns = [c["N"] for c in R[tag]["classes"] if c["state"] != "NA"]
            self.assertEqual(len(Ns), 8)
            self.assertEqual(len(set(Ns)), 8)
        self.assertEqual(sorted(c["N"] for c in R["A1"]["classes"] if c["state"] != "NA"), [372, 408, 444, 480, 612, 648, 684, 720])

    def test_equal_N_pair_A2_needs_NA(self):
        a, b = obs.System(A2, 648), obs.System(A2, 432)
        an = obs.Anchor(A2, 432)
        self.assertEqual(a.N, b.N)
        self.assertEqual((an.state(a), an.state(b)), ("NA", 1))
        self.assertNotEqual(a.O1, b.O1)

    def test_A1_relabelling_pair(self):
        a, b = obs.System(A1, 2160), obs.System(A1, 2880)
        sigma = [2, 0, 1, 3, 5, 4]
        self.assertEqual({tuple(sigma[x] for x in p) for p in a.A}, set(b.A))
        self.assertEqual((a.O1, a.betti, a.fvec), (b.O1, b.betti, b.fvec))
        an = obs.Anchor(A1, 288)
        self.assertEqual((an.state(a), an.state(b)), ("NA", 0))

    def test_additivity_A1_and_interaction_A2(self):
        N = {tuple(sorted(c["cap_valuations"].items())): c["N"] for c in R["A1"]["classes"] if c["state"] != "NA"}
        base = N[(("2", 5), ("3", 2), ("5", 0))]
        self.assertEqual(base, 372)
        self.assertEqual(N[(("2", 6), ("3", 3), ("5", 1))], 372 + 36 + 72 + 240)
        self.assertFalse(R["A2"]["additivity"]["N_equals_N0_plus_sum_delta_over_indicators"])

    def test_certificates(self):
        for tag in ("A1", "A2"):
            self.assertTrue(R[tag]["certificates_all_verified"])
            self.assertEqual(len(R[tag]["certificates"]), 8)


if __name__ == "__main__":
    unittest.main()
