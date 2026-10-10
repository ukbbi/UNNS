#!/usr/bin/env python3
"""Unit tests for v008 helpers and solver binary. Run: python3 scr_iii_b/solvers/test_v008.py (needs g++)."""
import sys
sys.dont_write_bytecode = True
import pathlib, subprocess, tempfile, unittest
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1] / "scr_iii_b" / "feasibility"))
import energy_windows_v006 as ew
import tie_policy_v008 as tp, diagnostics_v008 as dg, validate_v008 as v8

pe = ew.load_v005()
TMP = pathlib.Path(tempfile.mkdtemp(prefix="t8_")); BIN = TMP / "solvers"
subprocess.run(["g++", "-std=c++17", "-O2", str(v8.SRC), "-o", str(BIN)], check=True)


def real(L):
    isl = pe.source_geometry(L); pairs = pe.K_pairs(isl); inc, _ = ew.build_incidence(pe, isl, pe.vertex_positions(L))
    masks = ew.compile_masks(inc); p = TMP / ("r%d.txt" % L); v8.write_instance(p, len(isl), pairs, masks)
    return p, len(isl), pairs, masks


class T(unittest.TestCase):
    def test_policy_endpoint_and_edges(self):
        self.assertEqual(tp.classify(0.01, 0.01, 0.0), "FAIL_AT_OR_ABOVE_GAP")
        self.assertEqual(tp.classify(0.01, 0.0099, 0.0), "PRESERVED")
        self.assertTrue(tp.classify(None, 1, 0).startswith("NOT_INFORMATIVE"))
        self.assertTrue(tp.classify(0.0, 0, 1e-12).startswith("NO_PRESERVING"))

    def test_tolerance_never_removes_target(self):
        E = [0.0, 0.0, 0.01]
        self.assertTrue(tp.members_exact(E, 0.0, 0.01) <= tp.members(E, 0.0, 0.01, 1e-10))

    def test_diagnostics_empty_and_zero(self):
        self.assertIsNone(dg.delta_G([0, 1], [True, True]))
        self.assertIsNone(dg.rho_G(0.0, 1.0)); self.assertAlmostEqual(dg.rho_G(2.0, 1.0), 0.5)

    def test_solvers_agree_2x2_w0(self):
        p, n, pairs, masks = real(2); sa = sum(abs(k) for _, _, k in pairs); tau = tp.tau_abs(sa)
        outs = {s: v8.solve_ids(BIN, p, s, 0.0, tau, TMP)[0] for s in v8.SOLVERS}
        self.assertTrue(all(o == outs["b0"] for o in outs.values())); self.assertEqual(len(outs["b0"]), 2)

    def test_g_solvers_expose_false_exclusion(self):
        p, n, pairs, masks = real(2); sa = sum(abs(k) for _, _, k in pairs); tau = tp.tau_abs(sa)
        En = v8.energies(n, pairs); lv, levels, _, _ = ew.group_levels(En); W = levels[2]["E_min"] - levels[0]["E_min"]
        b0 = v8.solve_ids(BIN, p, "b0", W, tau, TMP)[0]; g2 = v8.solve_ids(BIN, p, "g2", W, tau, TMP)[0]
        self.assertEqual(len(b0) - len(g2), 16)

    def test_guard_refuses_3x3(self):
        p, n, pairs, masks = real(3)
        pr = v8.run(BIN, p, "b0", 1e-3, 1e-9)
        self.assertEqual(pr.returncode, 3); self.assertEqual(pr.stdout.strip(), "")

    def test_b1_bound_formula_matches_python_on_2x2(self):
        p, n, pairs, masks = real(2); pf = TMP / "pp.txt"; pf.write_text("0 0\n6 21\n12 1234\n")
        out = subprocess.run([str(BIN), str(p), "boundtest", str(pf)], capture_output=True, text=True).stdout.split("\n")
        lbs = [float(l.split()[2]) for l in out if l.strip()]
        self.assertAlmostEqual(lbs[2], v8.energies(n, pairs)[1234], places=12)     # m = n -> LB equals the exact energy
        self.assertLessEqual(lbs[0], min(v8.energies(n, pairs)) + 1e-12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
