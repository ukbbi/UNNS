"""GIG-I v004 tests.  python -m unittest discover -s TESTS -v   (optional: GIG_FROZEN_SRC for the read-only frozen cross-check)"""
import hashlib
import json
import os
import random
import sys
import unittest
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
sys.path.insert(0, os.path.join(ROOT, "EXPERIMENTS"))
import _v3path  # noqa: E402
import threshold_closure as tc  # noqa: E402
import cell_boundary as cb  # noqa: E402
import source_filtration as sf  # noqa: E402
import hole_survival as H  # noqa: E402
import h3_survival as H3  # noqa: E402


def check_manifest(root):
    with open(os.path.join(root, "MANIFEST.json")) as fh:
        man = json.load(fh)
    for rel, h in man["files"].items():
        with open(os.path.join(root, rel), "rb") as f:
            assert hashlib.sha256(f.read()).hexdigest() == h, rel


def z_bounds(C, m):
    cx = cb.Complex(tc.source_mask(C, m), 6)
    loc = cx.local.get(2, {})
    if any(g not in loc for g in H.Z):
        return None
    zl = sum(1 << loc[g] for g in H.Z)
    return cb._reduce(zl, dict(cb.image_pivots(cx.rows.get(3, []))))[0] == 0


class Frozen(unittest.TestCase):
    def test_v001_v002_v003_hashes(self):
        for r in (_v3path.V001, _v3path.V002, _v3path.V003):
            check_manifest(r)


class H2Pattern(unittest.TestCase):
    def test_PS0_combinatorial_facts(self):
        c = H.check_cycle_and_cochain()
        self.assertTrue(c["z_is_cycle"])
        self.assertEqual(c["phi_of_z"], 1)
        self.assertEqual(len(c["obstructed_3faces"]), 6)
        self.assertEqual(sorted(tuple(len(b) for b in f) for f in c["obstructed_3faces"]), [(4, 1, 1)] * 6)
        self.assertEqual(len(H.Z), 96)
        self.assertEqual(len(H.PZ), 43)

    def test_gate_sets(self):
        gs = H.gate_sets()
        names = {a: sorted("".join(str(r) for r in range(6) if I >> r & 1) for I in S) for a, S in gs.items()}
        self.assertEqual(names, {0: ["024"], 1: ["125", "15"], 3: ["3", "34", "345", "35"]})
        for a in H.GATES:
            self.assertEqual(set(H.PT[H.GATES[a][0]]) - set(H.PZ), set(H.PT[H.GATES[a][1]]) - set(H.PZ))

    def test_anchors_thresholds(self):
        self.assertEqual(H.thresholds([2, 3, 4, 5, 8, 9])[0], 288)
        self.assertEqual(sorted(set(H.thresholds([2, 3, 4, 5, 8, 9])[1])), [576, 864, 1440])
        self.assertEqual(H.thresholds([2, 3, 6, 7, 8, 9])[0], 432)
        self.assertEqual(sorted(set(H.thresholds([2, 3, 6, 7, 8, 9])[1])), [864, 1296, 3024])

    def test_T_form_equals_gate_form(self):
        rnd = random.Random(1)
        for _ in range(300):
            lab = sorted(rnd.sample(range(1, 25), 6))
            m = rnd.choice([1, 12, 72, 288, 432, 720, 1440, 2880, 5040])
            self.assertEqual(H.survives(lab, m), H.survives_gates(lab, m))

    def test_PS1_soundness_exact_homology(self):
        rnd = random.Random(2)
        tested = pos = 0
        conts = [(2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9), (2, 3, 8, 9, 10, 11)]
        conts += [tuple(sorted(rnd.sample(range(1, 21), 6))) for _ in range(25)]
        for C in conts:
            for r in sf.regimes(C):
                b = z_bounds(C, r["L"])
                if b is None:
                    continue
                tested += 1
                if H.survives_gates(list(C), r["L"]):
                    pos += 1
                    self.assertFalse(b, (C, r["L"]))
        self.assertGreater(tested, 50)
        self.assertGreaterEqual(pos, 2)

    def test_PS2_gate0_universal_filling(self):
        self.assertEqual(len(H.universal_filling(0)), 34)
        self.assertIsNone(H.universal_filling(1))
        self.assertIsNone(H.universal_filling(3))

    def test_PS4_existence_small(self):
        found = [C for C in combinations(range(1, 13), 6) if H.hole_regime_exists(list(C))[0]]
        self.assertEqual(found, [(2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9)])

    def test_hole_regime_beta2_one(self):
        for C in ((2, 3, 4, 5, 8, 9), (2, 3, 6, 7, 8, 9), (2, 3, 8, 9, 10, 11)):
            Kz = H.hole_regime_exists(list(C))[1] if C != (2, 3, 8, 9, 10, 11) else 720
            self.assertEqual(cb.Complex(tc.source_mask(C, Kz), 6).betti()[2], 1)


class H3Pattern(unittest.TestCase):
    def test_patterns(self):
        for c in ("H3-1", "H3-2"):
            P = H3.Pattern(c)
            self.assertTrue(P.z_is_cycle)
            self.assertEqual(P.phi_of_z, 1)
            self.assertEqual(len(P.obstructed), 6)

    def test_predicted_regimes(self):
        P1, P2 = H3.Pattern("H3-1"), H3.Pattern("H3-2")
        self.assertEqual(P1.hole_regime_exists([2, 3, 4, 5, 8, 9, 14]), (True, 4032))
        self.assertEqual(P1.hole_regime_exists([2, 3, 6, 7, 8, 9, 14]), (True, 6048))
        self.assertEqual(P2.hole_regime_exists([2, 3, 4, 5, 8, 9, 15]), (True, 4320))
        self.assertEqual(P2.hole_regime_exists([2, 3, 6, 7, 8, 9, 15]), (True, 6480))
        self.assertFalse(P1.hole_regime_exists([2, 3, 4, 5, 8, 9, 15])[0])

    def test_betti3(self):
        cx = cb.Complex(tc.source_mask((2, 3, 4, 5, 8, 9, 15), 4320), 7)
        self.assertEqual(cx.betti(), (1, 0, 0, 1, 0, 0, 0))


@unittest.skipUnless(os.path.exists(os.path.join(ROOT, "RESULTS", "results.json")), "results.json not generated")
class Recorded(unittest.TestCase):
    def test_results(self):
        with open(os.path.join(ROOT, "RESULTS", "results.json")) as fh:
            r = json.load(fh)
        c = r["E15"]["completeness_census"]
        self.assertEqual(c["SOUNDNESS_pred_true_but_z_bounds"], [])
        self.assertEqual(c["regimes_with_beta2_positive"], 158)
        self.assertEqual(len(c["beta2_regimes_unexplained_by_parametric_mechanism"]), 106)
        self.assertEqual(c["NECESSITY_exceptions_pred_false_but_z_survives"], [])
        for n, case in r["E16"]["cases"].items():
            self.assertTrue(case["z3"]["is_cycle"] and case["phi3"]["kills_all_4face_boundaries"] and case["z3_fate"]["all_fillings_verified"])
        for e in r["E17"]:
            self.assertTrue(e["completed"] and e["poset_exact_match"])
        for v in r["E16"]["parametric_existence"]["exact_verification"]:
            self.assertTrue(v["beta3_positive"])


if __name__ == "__main__":
    unittest.main()
