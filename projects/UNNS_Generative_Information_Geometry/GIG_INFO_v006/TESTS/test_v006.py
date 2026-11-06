import importlib.util, json, os, random, subprocess, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import nerve, v2
import numpy as np
ROOT = _path.ROOT
def J(n): return json.load(open(os.path.join(ROOT, "RESULTS", n)))
spec = importlib.util.spec_from_file_location("sv", os.path.join(ROOT, "VERIFY", "standalone_verify.py")); sv = importlib.util.module_from_spec(spec); spec.loader.exec_module(sv)

class T(unittest.TestCase):
    def test_standalone_verifier_passes_in_subprocess(self):
        r = subprocess.run([sys.executable, os.path.join(ROOT, "VERIFY", "standalone_verify.py")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout[-800:]); self.assertIn("ALL PASS", r.stdout); self.assertIn("290 certificates", r.stdout)

    def test_verifier_rejects_tampered_certificates(self):
        recs = json.load(open(os.path.join(ROOT, "CERTIFICATES", "positives_cycle_cocycle.json")))
        r = recs[0]; good, _ = sv.check_certificate(r); self.assertTrue(good)
        bad = dict(r); bad["cocycle_edges"] = r["cocycle_edges"][1:]          # drop an edge
        self.assertFalse(sv.check_certificate(bad)[0])
        bad2 = dict(r); bad2["source"] = r["source"] * 2                       # wrong system
        self.assertFalse(sv.check_certificate(bad2)[0])
        bad3 = dict(r); bad3["cycle"] = r["cycle"][:2]                         # not a cycle through nerve edges as a triangle
        self.assertFalse(sv.check_certificate(bad3)[0])

    def test_verifier_negative_pair_has_no_cycle(self):
        A = sv.arithmetic_A((2, 4, 5, 9, 14, 15), 3780); self.assertEqual(sv.nerve_h1(sv.dead_sets(A))[0], 0)

    def test_parent_paths_fixed(self):
        P = _path._vpath.PATHS
        self.assertTrue(P["V004"].endswith("GIG_I_v004")); self.assertTrue(P["V005"].endswith("GIG_I_v005")); self.assertTrue(P["INFO005"].endswith("GIG_INFO_v005"))
        man = json.load(open(os.path.join(ROOT, "MANIFEST.json")))["parents"]
        self.assertNotEqual(man["V004"]["MANIFEST.json_sha256"], man["V005"]["MANIFEST.json_sha256"])
        self.assertEqual(man["V004"]["MANIFEST.json_sha256"][:8], "26e14d97")

    def test_core_preserves_homology_fresh(self):
        R = v2.census.enumerate_regimes(); rng = random.Random(6); n = 0
        for i in rng.sample(range(len(R)), 60):
            m = R[i][3]
            if m == (1 << 720) - 1: continue
            D = nerve.dead_sets(m)
            v, f = nerve.strong_core(D)
            self.assertEqual(nerve.complex_betti_from_facets(v, f), nerve.nerve_betti(D, 1)); n += 1
        self.assertGreater(n, 50)

    def test_census_exhaustive_summary(self):
        d = J("D21_minimal_observation.json")
        self.assertEqual((d["patterns"], d["positive_patterns"], d["positive_regimes"]), (219145, 151, 158))
        self.assertEqual(d["positives_with_Hol_0"], 0)
        Z = np.load(os.path.join(ROOT, "RESULTS", "C20_dead_patterns.npz"))
        self.assertEqual(int(Z["mult"][Z["b1"] > 0].sum()), 158)
        for k in ("(V,E)", "(V,E,Tr)", "Hol", "euler V-E+Tr"):
            self.assertGreater(d["observations"][k]["balanced"]["H(Y|O)"], 0)
        self.assertEqual(d["core_size_positive"]["3"], 105)

    def test_manifest(self):
        import hashlib
        man = json.load(open(os.path.join(ROOT, "MANIFEST.json")))
        for rel, h in man["files"].items():
            if rel.startswith("TESTS/"): continue
            self.assertEqual(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest(), h, rel)
if __name__ == "__main__": unittest.main(verbosity=1)
