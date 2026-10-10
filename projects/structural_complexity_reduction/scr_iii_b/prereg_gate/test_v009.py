#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v009 -- fast unit tests (run: python3 scr_iii_b/prereg_gate/test_v009.py).  Public 1x1/2x2 and synthetic inputs only."""
import sys
sys.dont_write_bytecode = True
import json, pathlib, random, subprocess, tempfile, unittest
HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(PROJECT / "scr_iii_b" / "feasibility"))
import energy_windows_v006 as ew
import tolerance_v009 as tol, seeds_v009 as sd, cost_audit_v009 as ca

TMP = pathlib.Path(tempfile.mkdtemp(prefix="v009t_"))
for src, name in (("prereg_gate_v009.cpp", "pg"), ("e2_v009.cpp", "e2")):
    r = subprocess.run(["g++", "-std=c++17", "-O2", str(HERE / src), "-o", str(TMP / name)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
PE = ew.load_v005()


def inst(L):
    isl = PE.source_geometry(L); pairs = PE.K_pairs(isl); masks = ew.compile_masks(ew.build_incidence(PE, isl, PE.vertex_positions(L))[0])
    p = TMP / ("r%d.txt" % L)
    p.write_text("\n".join(["%d %d" % (len(isl), len(pairs))] + ["%d %d %.17g" % t for t in pairs] + [str(len(masks))] + ["%d %d" % m for m in masks]) + "\n")
    return p, len(isl), pairs


def energies(n, pairs):
    return [sum((-k if ((s >> i) ^ (s >> j)) & 1 else k) for i, j, k in pairs) for s in range(1 << n)]


def run(*a):
    return subprocess.run([str(x) for x in a], capture_output=True, text=True)


class T(unittest.TestCase):
    def test_preservation_table(self):
        self.assertEqual(tol.preservation(1.0, 0.5, 0.1)[0], "PASS")
        self.assertEqual(tol.preservation(1.0, 0.9, 0.1)[0], "FAIL")
        self.assertEqual(tol.preservation(0.0, 0.0, 0.1)[0], "FAIL")
        self.assertIn("EMPTY_EXCLUDED_SET_NOT_INFORMATIVE", tol.preservation(None, 0.2, 0.1, empty_excluded=True)[2])

    def test_hierarchy_ordering(self):
        self.assertTrue(tol.hierarchy(0.17, 276)["ordering_ok"])

    def test_seed_derivation_matches_v006(self):
        v6 = sd.load_v006_nulls(PROJECT / "scr_iii_b" / "feasibility")
        for fam in sd.FAMILIES.values():
            for i in range(20):
                self.assertEqual(sd.rng_for(fam, i).random(), v6.rng_for(fam, i).random())

    def test_solvers_agree_2x2_and_e2_exact(self):
        p, n, pairs = inst(2); En = energies(n, pairs); E0 = min(En); Q = sum(abs(k) for _, _, k in pairs); tau = 1e-9 * Q
        for W in (0.0, 0.3 * (max(En) - E0)):
            ref = {i for i, e in enumerate(En) if e <= E0 + W + tau}
            for mode in ("b0", "b1", "e2"):
                out = TMP / "d.txt"; r = run(TMP / ("e2" if mode == "e2" else "pg"), p, mode, repr(W), repr(tau), "--e0", repr(E0), "--dump", out)
                self.assertEqual(r.returncode, 0, r.stderr); self.assertEqual({int(x) for x in out.read_text().split()}, ref)

    def test_wrong_reference_rejected(self):
        p, n, pairs = inst(2); E0 = min(energies(n, pairs)); tau = 1e-9 * sum(abs(k) for _, _, k in pairs)
        self.assertEqual(run(TMP / "pg", p, "b0", "0", repr(tau), "--e0", repr(E0 + 100 * tau)).returncode, 4)
        self.assertEqual(run(TMP / "pg", p, "b0", "0", repr(tau)).returncode, 2)

    def test_guard_refuses_3x3_w_positive(self):
        p, n, pairs = inst(3); E0 = -0.09184041396072776
        r = run(TMP / "pg", p, "b0", "0.001", "1e-10", "--e0", repr(E0))
        self.assertEqual(r.returncode, 3); self.assertEqual(r.stdout.strip(), ""); self.assertIn("REFUSED", r.stderr)
        self.assertEqual(run(TMP / "pg", p, "nullgap", "0", "1e-10", "--e0", repr(E0)).returncode, 3)

    def test_decision_rule(self):
        base = [1.0] * 15; fast = [0.4] * 15
        self.assertEqual(ca.hc_decision(ca.hc_intervals(base, fast), 1.2, True, True), "CHARGED_GAIN_PASS")
        self.assertEqual(ca.hc_decision(ca.hc_intervals(base, fast), 1.2, False, True), "NOT_ELIGIBLE_COMPLETE_TASK_NOT_CERTIFIED")

    def test_balanced_schedule(self):
        sch = ca.schedule(["a", "b", "c", "d", "e"], 15)
        for pos in range(5):
            self.assertEqual(len({sum(1 for r in sch if r[pos] == s) for s in "abcde"}), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
