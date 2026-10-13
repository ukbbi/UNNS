"""Deterministic tests for ESC-I v0.1. Run: python -m unittest test_esc_i -v"""
import itertools, json, shutil, subprocess, unittest, re, os
from fractions import Fraction as Fr
import esc_i as E

def exact_orbit_period(A, x0, pmax=12):
    x = x0
    for p in range(1, pmax + 1):
        x = E.apply(A, x)
        if x == x0: return p
    return None

class T(unittest.TestCase):
    def test_exhaustive_small_integer_matrices(self):
        """Exact class vs an independent exact orbit computation + echo, over all integer A in [-2,2]^4, x0 in a small grid."""
        rng = range(-2, 3); n = 0; bad = []
        for a, b, c, d in itertools.product(rng, repeat=4):
            A = tuple(Fr(t) for t in (a, b, c, d))
            for x0 in [(Fr(1), Fr(0)), (Fr(0), Fr(1)), (Fr(1), Fr(1)), (Fr(1), Fr(-1)), (Fr(2), Fr(1)), (Fr(0), Fr(0))]:
                n += 1
                ex = E.classical(A, x0); per = exact_orbit_period(A, x0)
                # periodic <=> orbit returns exactly (independent check in Q)
                if (ex["cls"] == "periodic") != (per is not None): bad.append(("period", A, x0, ex["cls"], per))
                if ex["period"] and per != ex["period"] and not (ex["period"] in (4, 6, 3, 2, 1)): bad.append(("p", A, x0))
                if ex["period"] and per is not None and ex["period"] != per: bad.append(("p!=", A, x0, ex["period"], per))
                if per is None:
                    ec = E.echo_classify(A, x0, N=3000, tol=1e-9)
                    if ec["cls"] != ex["cls"]: bad.append(("echo", A, x0, ex["cls"], ec["cls"]))
        self.assertEqual(bad, [], bad[:5]); self.assertEqual(n, 625 * 6)

    def test_rho_vs_float_eigs(self):
        import random; r = random.Random(7)
        for _ in range(3000):
            A = tuple(Fr(r.randint(-40, 40), r.choice([1, 2, 5, 8])) for _ in range(4))
            ex = E.classical(A, (Fr(1), Fr(3)))
            rho = ex["rho"]
            if abs(rho - 1) > 1e-9: self.assertEqual(ex["rho_vs_1"], "<" if rho < 1 else ">", A)

    def test_known_cases(self):
        c = lambda A, x: E.classical(tuple(map(E.q, A)), tuple(map(E.q, x)))
        self.assertEqual(c(["0", "-1", "1", "0"], ["1", "0"])["period"], 4)
        self.assertEqual(c(["0", "-1", "1", "1"], ["1", "0"])["period"], 6)
        self.assertEqual(c(["0", "-1", "1", "-1"], ["1", "0"])["period"], 3)
        self.assertEqual(c(["3/5", "-4/5", "4/5", "3/5"], ["1", "0"])["cls"], "bounded")
        self.assertEqual(c(["1", "1", "0", "1"], ["0", "1"])["cls"], "divergent")
        self.assertEqual(c(["1", "1", "0", "1"], ["1", "0"])["cls"], "periodic")
        self.assertEqual(c(["2", "0", "0", "1/2"], ["0", "1"])["cls"], "convergent")

    def test_phase_inlet_counterexample(self):
        o = E.phase_inlet(tuple(map(Fr, (1, 1, 1, 1))), tuple(map(Fr, (1, 0, 0, -1))))
        self.assertAlmostEqual(o["rho_T"], 2.0); self.assertAlmostEqual(o["rho_UT"], 0.0)
        self.assertFalse(o["claim_rho(UT)=rho(T)_holds"]); self.assertAlmostEqual(o["rho_similar"], 2.0)

    def test_area_preserving_keeps_det(self):
        A = tuple(map(E.q, ["3/5", "-4/5", "4/5", "3/5"]))
        r = E.mulberry32(5); eps = Fr(1, 100)
        s, t = Fr(r() % 2001 - 1000, 1000) * eps, Fr(r() % 2001 - 1000, 1000) * eps
        a, b, c, d = A; b2, d2 = a * s + b, c * s + d
        Aa = (a + b2 * t, b2, c + d2 * t, d2)
        self.assertEqual(Aa[0] * Aa[3] - Aa[1] * Aa[2], 1)

    def test_periodic_is_knife_edge_but_boundedness_persists_under_area(self):
        A = tuple(map(E.q, ["0", "-1", "1", "0"])); x0 = (Fr(1), Fr(0))
        ch = E.challenge(A, x0, M=40)
        self.assertEqual(ch["eps_hold"]["generic_fine"], 0.0)       # periodic never survives generic perturbation
        self.assertEqual(ch["eps_hold"]["area_fine"], 0.0)
        self.assertGreater(ch["eps_hold"]["area_coarse"], 0.0)      # but non-escape (boundedness) does under det=1 perturbation

    def test_deterministic_report(self):
        a = json.dumps(E.run_one(E.SUITE[2], M=20)["challenge"], sort_keys=True)
        b = json.dumps(E.run_one(E.SUITE[2], M=20)["challenge"], sort_keys=True)
        self.assertEqual(a, b)

class TAdm(unittest.TestCase):
    def test_rules_do_not_call_exact_classifier(self):
        import admissibility as A; A.check_rule_independence()

    def test_theorem_5_5_small(self):
        import admissibility as A
        T = tuple(Fr(1) for _ in range(4)); self.assertFalse(A.in_C(T) or A.in_Cbar(T))
        self.assertEqual(A.ar1_phase_family(T)["verdict"], "REGIME-CAN-CHANGE")
        J = (Fr(0), Fr(-2), Fr(2), Fr(0)); self.assertEqual(A.ar1_phase_family(J)["verdict"], "RHO-INVARIANT")

    def test_full_run_is_deterministic_and_rules_frozen_before_comparison(self):
        import admissibility as A, tempfile
        with tempfile.TemporaryDirectory() as d1:
            A.main(["--out", d1]); r1 = json.load(open(os.path.join(d1, "admissibility_report.json")))
            rules = open(os.path.join(d1, "admissibility_rules.md")).read()
        self.assertIn(r1["order"]["rules_sha256"], rules)
        self.assertLessEqual(r1["order"]["rules_frozen_and_hashed"], r1["order"]["predictions_hashed_before_exact_comparison"])
        self.assertEqual(r1["comparison"]["AR-1"]["AR-1a"]["DISAGREE"], 0)
        self.assertEqual(r1["comparison"]["AR-2"]["safety"]["violations"], 0)
        self.assertEqual(r1["posthoc_amendment_relquant"]["DISAGREE"], 0)
        cf = r1["confirmation_ar31"]; self.assertEqual(cf["original_disagreements_retained"], 92)
        self.assertEqual(cf["total"]["DISAGREE"], 0); self.assertEqual(cf["per_step_error_bound"]["amended_bound_violations"], 0)
        self.assertTrue(cf["necessity_of_lambda_factor_demonstrated"]); self.assertTrue(cf["matches_hash_recorded_in_earlier_run"])

class TPrd(unittest.TestCase):
    def test_prd1_rules_independent_and_no_rule_contradicted(self):
        import admissibility as A, tempfile
        A.check_rule_independence(prd=True)
        with tempfile.TemporaryDirectory() as d:
            r = A.run_prd1(d)
            self.assertIn(r["order"]["rules_sha256"], open(os.path.join(d, "prd1_rules.md")).read())
            self.assertEqual(r["nonlinear_totals"]["R"]["CONTRADICTED"], 0)
            self.assertEqual(r["nonlinear_totals"]["C"]["CONTRADICTED"], 0)
            self.assertTrue(r["success_criteria"]["recognition_passed"])
            self.assertTrue(r["success_criteria"]["linear_control_orbit_equals_matrix_recursion"])
            am = r["posthoc_comparator_amendment"]
            self.assertGreater(am["control_contradicted_first_run"], 0)  # first-run record retained
            self.assertEqual(am["control_contradicted_amended"], 0)

if __name__ == "__main__": unittest.main()
