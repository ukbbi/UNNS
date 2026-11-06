import hashlib, json, os, random, sys, unittest
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import v2, geom, geomk, graph_direct as gd
import history_complex as hc
ROOT = _path.ROOT
RES = os.path.join(ROOT, "RESULTS")
J = lambda n: json.load(open(os.path.join(RES, n)))
F = dict(np.load(os.path.join(RES, "features_all.npz")))
pc = v2.pair_cert


class T(unittest.TestCase):
    def test_T1_against_definition_level_code(self):
        REGS = v2.census.enumerate_regimes()
        rng = random.Random(7)
        for i in rng.sample(range(len(REGS)), 25) + [int(i) for i in np.nonzero(F["beta2"] > 0)[0][:5]]:
            C, L, N, mask = REGS[i]
            A = pc.admissible_orderings(C, L)
            p = gd.profile(A)
            self.assertTrue(p["T1_identity_holds_at_every_vertex"])
            self.assertEqual((p["N"], p["E"], p["sq"], p["SB2"], p["SB22"], p["Sd2"]), tuple(int(F[k][i]) for k in ("N", "E", "sq", "SB2", "SB22", "Sd2")))
        self.assertEqual(J("F10_features.json")["T1_mismatches"], 0)

    def test_exact_identities_on_all_regimes(self):
        N, E, sq = F["N"], F["E"], F["sq"]
        self.assertTrue((F["SB2"] == N + F["Sd2"] - 4 * sq).all())
        self.assertTrue((F["Ss"] == F["Sd2"] - 2 * E).all())
        ex = N + F["Sd2"] + F["Ss2"] + F["Sq2"] + 4 * E + 2 * F["Ss"] - 8 * sq + 2 * F["Sds"] - 2 * F["Sdq"] - 2 * F["Ssq"]
        self.assertTrue((ex == F["SB22"]).all())
        self.assertTrue((F["sq"] + F["hx"] == F["f2"]).all() if "f2" in F else True)

    def test_census_unchanged(self):
        self.assertEqual(len(F["N"]), 346859)
        self.assertEqual(int((F["beta2"] > 0).sum()), 158)

    def test_minimal_signatures(self):
        a, b = J("F11_minimal_signatures.json"), J("F16_second_order_pool.json")
        self.assertIn(["N", "SB22"], [m["features"] for m in a["minimal_separating_subsets"]])
        self.assertIn(["sq", "Ss2"], b["minimal_separating_subsets"])
        self.assertEqual(a["vector_observables"]["N_hd"]["positives_in_mixed_classes"], 66)
        self.assertEqual(a["vector_observables"]["N_hd_hq"]["positives_in_mixed_classes"], 22)
        self.assertEqual(a["vector_observables"]["N_hb"]["mixed_classes"], 0)
        self.assertEqual(a["unresolved_after_radius1"], 66)
        self.assertEqual(a["unresolved_positives_still_colliding_after_adding"]["SB22"], 0)

    def test_single_scalar_resolves_the_66(self):
        r = J("F18_unresolved66.json")
        self.assertEqual((r["Ss2"]["resolved"], r["SB22"]["resolved"], r["sq"]["resolved"], r["SB2"]["resolved"]), (66, 66, 42, 42))

    def test_nontrivial(self):
        r = J("F12_nontriviality.json")["N+SB22"]
        self.assertEqual(r["real"]["positives_in_mixed"], 0)
        self.assertGreater(r["real"]["positives_in_pure_classes_size_ge2"], 100)
        self.assertGreater(r["null_positives_in_mixed_classes"]["min"], 100)

    def test_witness_certificates(self):
        W = J.__call__ and json.load(open(os.path.join(ROOT, "CERTIFICATES", "witness_2520_3780.json")))
        C = (2, 4, 5, 9, 14, 15)
        Ap, An = pc.admissible_orderings(C, 2520), pc.admissible_orderings(C, 3780)
        self.assertEqual((len(Ap), len(An)), (540, 540))
        P, Q = gd.profile(Ap), gd.profile(An)
        for k in ("N", "E", "sq", "h1", "hq", "SB2", "Sd2"):
            self.assertEqual(P[k], Q[k], k)
        self.assertNotEqual(P["h2"], Q["h2"])
        self.assertEqual((P["SB22"], Q["SB22"]), (180420, 180408))
        z = [tuple(tuple(b) for b in f) for f in W["positive"]["certificate"]["cycle"]]
        phi = [tuple(tuple(b) for b in f) for f in W["positive"]["certificate"]["cochain"]]
        self.assertEqual(pc.verify(Ap, z, phi), (True, "ok"))
        self.assertEqual(pc.verify(Ap, z[1:], phi), (False, "z not a cycle"))
        self.assertEqual(pc.betti2_by_ranks(pc.complex_of(Ap))[:2], (1, 1))
        self.assertEqual(pc.betti2_by_ranks(pc.complex_of(An))[:2], (0, 0))
        self.assertEqual(hc.betti(hc.vertex_mask(An, 6), 6)[2], 0)
        self.assertEqual(hc.betti(hc.vertex_mask(Ap, 6), 6)[2], 1)
        self.assertEqual(J("F14_sharp_witness.json")["equal_N_h1_hq"]["positive_negative_pairs"], 165)

    def test_preregistration_immutable(self):
        rec = open(os.path.join(RES, "preregistration_sha256.txt")).read().split()[0]
        self.assertEqual(hashlib.sha256(open(os.path.join(ROOT, "THEORY", "PREREGISTRATION.md"), "rb").read()).hexdigest(), rec)

    def test_heldout_resample_reproducible_and_recomputed(self):
        import H20_heldout as h
        S = h.sample(6)
        self.assertEqual([list(c) for c in S], J("H6_summary.json")["contents"])
        H6 = dict(np.load(os.path.join(RES, "H6_features.npz")))
        import source_filtration as sf
        regs = [(C, r["L"], r["N"], r["mask"]) for C in S[:5] for r in sf.regimes(C)][:60]
        f = geomk.Geom(6).features([r[3] for r in regs])
        self.assertTrue((f["SB22"] == H6["SB22"][:60]).all() and (f["N"] == H6["N"][:60]).all())
        self.assertEqual([hc.betti(r[3], 6)[2] for r in regs], H6["beta2"][:60].tolist())

    def test_heldout_outcomes_as_recorded(self):
        e = J("H21_evaluation.json")
        self.assertEqual(e["H6_alone"]["S_B (sq,Ss2)"]["mixed_classes"], 0)
        self.assertEqual(e["D_union_H6"]["S_C (Sd2,Ss2)"]["mixed_classes"], 0)
        self.assertEqual(e["D_union_H6"]["(N,h1,h2)"]["mixed_classes"], 0)
        self.assertGreater(e["H6_alone"]["S_A (N,SB22)"]["mixed_classes"], 0)   # pre-registered prediction P1 for S_A FAILED
        self.assertFalse(e["P1_confirmed"])
        self.assertTrue(e["P2_confirmed"])


if __name__ == "__main__":
    unittest.main()
