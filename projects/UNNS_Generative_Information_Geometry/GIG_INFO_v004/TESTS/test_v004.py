import hashlib, json, os, random, sys, unittest
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import v2, sym, ent2, forbidden as fb, graph_direct as gd
import history_complex as hc
ROOT = _path.ROOT
RES = os.path.join(ROOT, "RESULTS")


def J(n):
    with open(os.path.join(RES, n)) as f:
        return json.load(f)


class T(unittest.TestCase):
    def test_entropy_engine_toy(self):
        p = ent2.profile([0, 0, 0, 1], [1, 1, 2, 2], "balanced")
        self.assertAlmostEqual(float(p["H(Y|O)"]), 2 / 3 * 0.8112781244591328, places=12)
        self.assertEqual(p["H(Y)"][:5], "1.000")

    def test_alexander_duality_fresh(self):
        rng = random.Random(3)
        for _ in range(12):
            dens = rng.choice([0.6, 0.85, 0.95])
            m = sum(1 << b for b in range(720) if rng.random() < dens)
            if m in (0, (1 << 720) - 1):
                continue
            b = hc.betti(m, 6)
            yb = fb.reduced_betti(fb.y_simplices(m, 6), 4)
            self.assertEqual([b[0] - 1] + list(b[1:4]), [yb[3], yb[2], yb[1], yb[0]])
            self.assertEqual(b[2], yb[1])
        r = J("A10_alexander_duality.json")
        self.assertEqual((r["tested"], r["mismatches"], r["beta2_equals_H1_of_Y"]), (700, 0, 700))

    def test_information_numbers(self):
        b = J("B10_information_profiles.json")
        self.assertEqual(b["D"]["balanced"]["none"]["H(Y)"][:6], "1.0000")
        self.assertAlmostEqual(float(b["D"]["natural"]["none"]["H(Y)"]), 0.005713350154290559, places=12)
        for dom in ("D", "D_union_H6"):
            for mode in ("natural", "balanced"):
                self.assertEqual(float(b[dom][mode]["(N,h1,Q,S2)"]["H(Y|O)"]), 0.0)
                self.assertGreater(float(b[dom][mode]["N"]["H(Y|O)"]), 0.0)
        self.assertAlmostEqual(float(b["D_union_H6"]["balanced"]["N"]["H(Y|O)"]), 0.45521, places=4)

    def test_out_of_sample_is_much_weaker_than_plug_in(self):
        o = J("B11_out_of_sample.json")
        for t, v in o.items():
            self.assertLess(v["exact_signature_lookup_with_backoff"]["information_recovered_bits"], 0)
            for k, x in v["gradient_boosting"].items():
                self.assertLess(x["information_recovered_bits"], 0.7)
                self.assertGreater(x["AUC"], 0.8)

    def test_seven_hard_positives(self):
        a = J("A11_seven_hard_positives.json")
        self.assertEqual((a["D"]["(N,h1,Sds)"]["hidden_positives"], a["D"]["(Q,Sds)"]["hidden_positives"], a["D"]["(Q,S2)"]["hidden_positives"]), (7, 10, 0))
        self.assertEqual(a["D_union_H6"]["(Q,S2)"]["hidden_positives"], 0)
        self.assertEqual(len(a["seven_detail_D"]), 7)
        self.assertTrue(all(x["S2_differs_from_all_partners"] for x in a["seven_detail_D"]))

    def test_counterexample_independent(self):
        c = J("../CERTIFICATES/counterexample_PF_N_h1_Q_S2.json") if False else json.load(open(os.path.join(ROOT, "CERTIFICATES", "counterexample_PF_N_h1_Q_S2.json")))
        P = [hc.perms(6)[i] for i in range(720) if int(c["positive"]["mask_hex"], 16) >> i & 1]
        Nn = [hc.perms(6)[i] for i in range(720) if int(c["negative"]["mask_hex"], 16) >> i & 1]
        pp, pn = gd.profile(P), gd.profile(Nn)
        for k in ("N", "h1", "sq", "Ss2", "Sds", "SB22", "hq"):
            self.assertEqual(pp[k], pn[k], k)
        self.assertNotEqual(pp["h2"], pn["h2"])
        pcx = v2.pair_cert
        self.assertEqual(pcx.betti2_by_ranks(pcx.complex_of(P))[:2], (1, 1))
        self.assertEqual(pcx.betti2_by_ranks(pcx.complex_of(Nn))[:2], (0, 0))
        z = [tuple(tuple(b) for b in f) for f in c["positive"]["certificate"]["cycle"]]
        phi = [tuple(tuple(b) for b in f) for f in c["positive"]["certificate"]["cochain"]]
        self.assertEqual(pcx.verify(P, z, phi), (True, "ok"))
        self.assertFalse(c["positive_mask_is_arithmetic_census_regime"] or c["negative_mask_is_arithmetic_census_regime"])
        self.assertTrue(c["positive_is_prefix_family_system"] and c["negative_is_prefix_family_system"])

    def test_scope_hierarchy(self):
        s, a = J("A12_scope_hierarchy.json"), J("A15_stronger_signatures.json")
        self.assertGreater(a["PF"]["(N,h1,Q,S2)"]["mixed_classes"], 0)
        self.assertGreater(s["PF"]["(Q,S2)"]["mixed_classes"], 0)
        for t in ("PF", "VS"):
            self.assertEqual(a[t]["(N,h1,h2)"]["mixed_classes"], 0)
        self.assertEqual(s["TF"]["positives"], 0)
        k = J("A13_collision_concordance.json")
        self.assertEqual(k["AR (census u H6)"]["(Q,S2)"]["partner_positive_rate"], 1.0)
        self.assertLess(k["PF"]["(Q,S2)"]["partner_positive_rate"], 1.0)

    def test_symbolic_primary_recomputed(self):
        cats = tuple("SSSRRN")
        sysd = sym.all_systems(cats)
        self.assertEqual(sum(len(v) for v in sysd.values()), 198)
        self.assertEqual(len(sysd), 71)
        b = [hc.betti(m, 6) for m in sysd]
        self.assertEqual(sum(1 for x in b if x[2] > 0), 0)
        self.assertEqual(sum(1 for x in b if x[1] > 0), 9)
        self.assertTrue(all(sum(x[2:]) == 0 for x in b))

    def test_symbolic_extensions_recorded(self):
        for n, (mk, p1) in {"C12_summary.json": (55296, 1843), "C13_stress_summary.json": (508680, 11547)}.items():
            s = J(n)
            self.assertEqual((s["distinct_masks"], s["positives_beta2"], s["positives_beta1"]), (mk, 0, p1))
        z = np.load(os.path.join(RES, "SYM6_stress_features.npz"))["beta"]
        self.assertEqual(int((z[:, 2:] > 0).sum()), 0)
        c = J("C15_prereg_evaluation.json")
        self.assertIn("UNTESTABLE", c["T1"])

    def test_beta1_transfer(self):
        c = J("C14_beta1_transfer.json")
        for t, v in c.items():
            self.assertEqual(v["(N,h1,h2)"]["mixed_classes"], 0)
            self.assertEqual(v["(N,h1,Q,S2)"]["mixed_classes"], 0)
            self.assertGreater(v["N"]["mixed_classes"], 0)

    def test_preregistration_immutable(self):
        rec = open(os.path.join(RES, "preregistration_sha256.txt")).read().split()[0]
        with open(os.path.join(ROOT, "THEORY", "PREREGISTRATION.md"), "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), rec)


if __name__ == "__main__":
    unittest.main()
