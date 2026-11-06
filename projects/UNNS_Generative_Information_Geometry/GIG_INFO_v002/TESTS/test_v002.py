import gzip, csv, json, os, sys, unittest
from collections import Counter
from fractions import Fraction
from math import log2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import pair_cert as pc
import history_complex as hc
ROOT = _path.ROOT
R = json.load(open(os.path.join(ROOT, "RESULTS", "E11_equal_count_pairs.json")))
C = json.load(open(os.path.join(ROOT, "RESULTS", "E10_census.json")))
P = json.load(open(os.path.join(ROOT, "CERTIFICATES", "pair_480_800.json")))
CONTENT = (2, 3, 4, 5, 8, 15)


class T(unittest.TestCase):
    def test_census_matches_frozen(self):
        self.assertEqual((C["contents"], C["regimes"], C["beta2_positive_recomputed"]), (8008, 346859, 158))
        self.assertTrue(C["positive_sets_identical"])
        self.assertEqual(C["beta2_histogram"], {"0": 346701, "1": 157, "3": 1})

    def test_csv_consistent(self):
        n = pos = 0
        with gzip.open(os.path.join(ROOT, "RESULTS", "census_regimes.csv.gz"), "rt") as f:
            rd = csv.DictReader(f)
            for r in rd:
                n += 1
                pos += int(r["betti2"]) > 0
        self.assertEqual((n, pos), (346859, 158))

    def test_pair_counts(self):
        self.assertEqual(R["cross_pairs_equal_N_different_Y"], 326912)
        self.assertEqual(R["same_content_pairs_equal_N_different_Y"], 72)
        self.assertEqual(R["positives_with_a_same_content_partner"], 51)
        self.assertEqual(R["positives_vs_negatives_remaining"], {"N": 158, "OE": 151, "OF": 0, "OX": 8, "O1a": 66, "O1b": 0, "O1": 0})

    def test_entropy_levels(self):
        for e, ens in R["ensembles"].items():
            self.assertGreater(float(ens["O0"]["H(Y|O)"]), 0, e)
            self.assertEqual(ens["O0"]["mixed_classes"], 59)
            for lev in ("OF", "O1b", "O1"):
                self.assertEqual(ens[lev]["mixed_classes"], 0, (e, lev))
                self.assertEqual(float(ens[lev]["H(Y|O)"]), 0.0)
            for lev in ("OE", "OX", "O1a"):
                self.assertGreater(ens[lev]["mixed_classes"], 0, (e, lev))
        a = R["ensembles"]["E_all"]["O0"]
        p = 158 / 346859
        self.assertAlmostEqual(float(a["H(Y)"]), -p * log2(p) - (1 - p) * log2(1 - p), places=12)

    def test_h_y_given_n_from_counts(self):
        with gzip.open(os.path.join(ROOT, "RESULTS", "census_regimes.csv.gz"), "rt") as f:
            by = {}
            for r in csv.DictReader(f):
                by.setdefault(int(r["N"]), Counter())[int(int(r["betti2"]) > 0)] += 1
        tot = sum(sum(c.values()) for c in by.values())
        H = 0.0
        for c in by.values():
            n = sum(c.values())
            for v in c.values():
                if v != n:
                    H -= v / tot * log2(v / n)
        self.assertAlmostEqual(H, float(R["ensembles"]["E_all"]["O0"]["H(Y|O)"]), places=12)

    def test_arithmetic_pair(self):
        a, b = pc.admissible_orderings(CONTENT, 480), pc.admissible_orderings(CONTENT, 800)
        self.assertEqual((len(a), len(b)), (396, 396))
        self.assertNotEqual(set(a), set(b))

    def test_cellular_certificate_independent(self):
        A = pc.admissible_orderings(CONTENT, 480)
        z = [tuple(tuple(b) for b in f) for f in P["positive"]["certificate"]["cycle"]]
        phi = [tuple(tuple(b) for b in f) for f in P["positive"]["certificate"]["cochain"]]
        self.assertEqual(pc.verify(A, z, phi), (True, "ok"))
        # tampering with the cycle or the cochain must be rejected
        self.assertEqual(pc.verify(A, z[1:], phi), (False, "z not a cycle"))
        self.assertFalse(pc.verify(A, z, [])[0])

    def test_negative_has_no_cycle_class_two_routes(self):
        by = pc.complex_of(pc.admissible_orderings(CONTENT, 800))
        self.assertEqual(pc.betti2_by_ranks(by)[:2], (0, 0))
        self.assertIsNone(pc.find_certificate(by))
        mask = hc.vertex_mask(pc.admissible_orderings(CONTENT, 800), 6)
        self.assertEqual(hc.betti(mask, 6), (1, 0, 0, 0, 0, 0))

    def test_positive_two_engines(self):
        by = pc.complex_of(pc.admissible_orderings(CONTENT, 480))
        self.assertEqual(pc.betti2_by_ranks(by)[:2], (1, 1))
        self.assertEqual([len(by[d]) for d in range(5)], [396, 900, 669, 173, 10])


if __name__ == "__main__":
    unittest.main()
