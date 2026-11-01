"""Tests for GEO-HD-1B / E2-P1.  Run:  python -m unittest discover -s tests -v   (from the package root)

Unit tests of the builder, the full independent audit (fast mode), and TAMPER tests: stored data is
mutated in a temporary copy and the audit must fail."""
import copy
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import unittest
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import fibre_transport as ft  # noqa: E402
import cell_transport as ct  # noqa: E402

spec = importlib.util.spec_from_file_location("run_verify", os.path.join(ROOT, "RUN_VERIFY.py"))
RV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RV)

X0 = Fraction(110 ** 4, 3)


class TestArithmetic(unittest.TestCase):
    def test_orbit(self):
        o = ft.orbit(X0, 3)
        self.assertEqual([str(r["x"]) for r in o[:3]], ["146410000/3", "292820000/3", "146410000"])
        self.assertEqual([len(r["D"]) for r in o[:3]], [13, 13, 26])
        self.assertEqual([o[n]["G"] for n in range(3)], [3, 3, 1])
        self.assertEqual(o[0]["L"], 12100)

    def test_occurrences(self):
        for x in (X0, 2 * X0, Fraction(110 ** 4)):
            for N, M in ft.occurrences(x):
                self.assertEqual(Fraction(M * (N + 1) ** 2, N), x)

    def test_graver_sets(self):
        G0 = ft.region_graver((2, 5, 11), 3, (2, 2, 2))
        G2 = ft.region_graver((2, 5, 11), 1, (2, 2, 2))
        self.assertEqual(len(G0), 18)
        self.assertEqual(set(G2), {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)})
        self.assertFalse(set(G0) & set(G2))

    def test_lattice_group_order_criterion(self):
        # Theorem/Lemma E2-2 on the specimen and on a EQUAL case
        from importlib import import_module
        b = import_module("build_e2")
        self.assertEqual(b.predicted_relation((2, 5, 11), 3, 1), "ENLARGE")
        self.assertEqual(b.predicted_relation((5, 17, 29), 3, 12), "EQUAL")
        self.assertEqual(b.group_order((2, 5, 11), 3), 2)


class TestComplexes(unittest.TestCase):
    def setUp(self):
        self.F0 = ft.fibre(X0)
        self.G0 = ft.oriented(ft.region_graver((2, 5, 11), 3, (2, 2, 2)))
        self.cx0 = ct.build_complex(self.F0, self.G0, 3)
        x2 = Fraction(110 ** 4)
        self.cx2 = ct.build_complex(ft.fibre(x2), ft.oriented(ft.region_graver((2, 5, 11), 1, (2, 2, 2))), 3)

    def test_f_vectors_and_betti(self):
        self.assertEqual(ct.f_vector(self.cx0), [13, 45, 36, 3])
        self.assertEqual(ct.f_vector(self.cx2), [26, 51, 33, 7])
        self.assertEqual(ct.betti_complex(self.cx0), [1, 6, 6, 0])
        self.assertEqual(ct.betti_complex(self.cx2), [1, 0, 0, 0])
        self.assertTrue(ct.check_boundary_squared(self.cx0) and ct.check_boundary_squared(self.cx2))

    def test_survival(self):
        s = ct.abstract_survival(self.cx0, self.cx2)
        self.assertEqual([s[j]["preserved"] for j in range(4)], [13, 0, 0, 0])
        self.assertEqual([s[j]["lost"] for j in range(4)], [0, 45, 36, 3])

    def test_hnf_index(self):
        self.assertEqual(ct.hnf_index(self.F0, 3), 2)
        self.assertEqual(ct.hnf_index(ft.fibre(Fraction(110 ** 4)), 3), 1)


class TestAudit(unittest.TestCase):
    def test_fast_audit_passes(self):
        C = RV.verify(ROOT, fast=True, parts=("orbit", "fibres", "cells", "geometry", "baselines", "family"))
        self.assertTrue(C.ok, [c for c in C.items if c["status"] == "FAIL"])


class TestTamper(unittest.TestCase):
    """The audit must reject corrupted data."""

    def mutated(self, rel, fn):
        tmp = tempfile.mkdtemp()
        for sub in ("data", "results"):
            shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
        path = os.path.join(tmp, rel)
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        fn(d)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=1, sort_keys=True)
        return tmp

    def failing(self, rel, fn, parts):
        tmp = self.mutated(rel, fn)
        try:
            C = RV.verify(tmp, fast=True, parts=parts)
            return [c["id"] for c in C.items if c["status"] == "FAIL"]
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_drop_fibre_point(self):
        f = self.failing("data/E2_FIBRES.json", lambda d: d["stages"][0]["fibre"].pop(), ("orbit", "fibres"))
        self.assertIn("C02", f)

    def test_wrong_orbit_G(self):
        def m(d):
            d["steps"][2]["G"] = 3
        self.assertIn("C01", self.failing("data/E2_ORBIT.json", m, ("orbit",)))

    def test_drop_cell(self):
        def m(d):
            d["stage0"]["cells"]["2"].pop()
        self.assertIn("C06", self.failing("data/E2_CELLS.json", m, ("orbit", "fibres", "cells")))

    def test_wrong_betti(self):
        def m(d):
            d["topology"]["K_abs_stage0"]["betti_Q"] = [1, 6, 7, 0]
        self.assertIn("C08", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "fibres", "cells")))

    def test_wrong_union_betti(self):
        def m(d):
            d["geometry"]["stage0"]["U_betti_b0_b1_b2_b3"] = [1, 0, 17, 0]
        self.assertIn("C13", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "fibres", "cells", "geometry")))

    def test_flip_embedded(self):
        def m(d):
            d["geometry"]["stage0"]["embedded"] = True
        self.assertIn("C15", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "fibres", "cells", "geometry")))

    def test_wrong_geometric_status(self):
        def m(d):
            d["geometry"]["source_cells_vs_U2"]["3"] = {"CONTAINED": 3, "PARTIAL": 0}
        self.assertIn("C16", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "fibres", "cells", "geometry")))

    def test_bad_witness(self):
        def m(d):
            d["geometry"]["partial_cells"][0]["witness_point_in_cell_with_all_coordinates_lt_1"] = ["1", "1", "1"]
        self.assertIn("C17", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "fibres", "cells", "geometry")))

    def test_theorem1_row_tamper(self):
        def m(d):
            d["theorem1_check_rows_containing_2"]["all_match"] = False
        self.assertIn("C23", self.failing("results/E2_TRANSPORT.json", m, ("orbit", "family")))


if __name__ == "__main__":
    unittest.main()
