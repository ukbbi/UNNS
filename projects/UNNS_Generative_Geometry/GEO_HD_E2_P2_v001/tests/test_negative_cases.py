"""Negative controls and tamper tests: corrupted stored data must be rejected by RUN_VERIFY."""
import copy, importlib.util, json, os, shutil, sys, tempfile, unittest
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
spec = importlib.util.spec_from_file_location("run_verify", os.path.join(ROOT, "RUN_VERIFY.py"))
RV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RV)


class Tamper(unittest.TestCase):
    def failing(self, rel, fn, parts):
        tmp = tempfile.mkdtemp()
        try:
            for sub in ("data", "results"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            p = os.path.join(tmp, rel)
            d = json.load(open(p, encoding="utf-8"))
            fn(d)
            json.dump(d, open(p, "w", encoding="utf-8"))
            C = RV.verify(tmp, fast=True, parts=parts)
            return [c["id"] for c in C.items if c["status"] == "FAIL"]
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_untampered_passes(self):
        tmp = tempfile.mkdtemp()
        try:
            for sub in ("data", "results"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            C = RV.verify(tmp, fast=True, parts=("spec", "family"))
            self.assertTrue(C.ok)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_wrong_G(self):
        self.assertIn("P01A", self.failing("data/P2_A.json", lambda d: d.update(G=21), ("spec",)))

    def test_drop_fibre_point(self):
        self.assertIn("P04A", self.failing("data/P2_A.json", lambda d: d["fibre"]["source"].pop(), ("spec",)))

    def test_wrong_survival(self):
        def m(d):
            d["cells"]["survival"]["1"]["preserved"] = 4
        self.assertIn("P05A", self.failing("data/P2_A.json", m, ("spec",)))

    def test_wrong_union_relation(self):
        def m(d):
            d["geometry"]["union_relation"] = "EQUAL"
        self.assertIn("P06A", self.failing("data/P2_A.json", m, ("spec",)))

    def test_wrong_betti(self):
        def m(d):
            d["geometry"]["union_topology"]["target"]["betti"] = [1, 1, 0]
        self.assertIn("P07A", self.failing("data/P2_A.json", m, ("spec",)))

    def test_family_formula_tamper(self):
        def m(d):
            d["quasi_polynomials_mod4"]["E_kept"]["0"]["c0"] = "0"
        self.assertIn("P12", self.failing("data/P2_F21.json", m, ("family",)))

    def test_family_common_graver_tamper(self):
        def m(d):
            d["direct"][5]["common_graver"].append([2, 2])
        self.assertIn("P10", self.failing("data/P2_F21.json", m, ("family",)))

    def test_corpus_relation_tamper(self):
        def m(d):
            r = [x for x in d["k2"]["rows"] if x["relation"] == "SHRINK"][0]
            r["relation"] = "ENLARGE"
        f = self.failing("data/SEARCH_CORPUS.json", m, ("corpus",))
        self.assertTrue(f)


if __name__ == "__main__":
    unittest.main()
