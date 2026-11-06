import json, os, random, sys, unittest, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import nerve, adjacency as ad, forbidden as fb
import history_complex as hc
ROOT = _path.ROOT
RES = os.path.join(ROOT, "RESULTS")
def J(n):
    with open(os.path.join(RES, n)) as f: return json.load(f)

class T(unittest.TestCase):
    def test_nerve_model_fresh_pairs(self):
        for C, mp, mn in (((2, 3, 4, 5, 8, 15), 480, 800), ((2, 4, 5, 9, 14, 15), 2520, 3780)):
            mP, mN = nerve.arithmetic_mask(C, mp), nerve.arithmetic_mask(C, mn)
            for m, want in ((mP, 1), (mN, 0)):
                self.assertEqual(hc.betti(m, 6)[2], want)
                self.assertTrue(nerve.is_prefix_defined(m))
                self.assertEqual(nerve.y_betti(m, 1), nerve.nerve_betti(nerve.dead_sets(m), 1))
                self.assertEqual(nerve.y_betti(m, 1)[1], want)

    def test_nerve_model_census(self):
        r = J("A20_nerve_model.json")
        self.assertEqual((r["tested"], r["prefix_defined"], r["model_agrees_b0_b1"]), (1290, 1290, 1290))
        self.assertEqual(r["by_kind"]["positive_D"]["b1_pos"], 158); self.assertEqual(r["by_kind"]["positive_H6"]["b1_pos"], 132); self.assertEqual(r["by_kind"]["negative_D"]["b1_pos"], 0)

    def test_lemma_L1_fresh(self):
        import A25_star_intersection_lemma as A
        rng = random.Random(11)
        for _ in range(150):
            Tt = rng.sample(nerve.SUBS, rng.choice([1, 2, 3, 4]))
            Q = A.Q_of(Tt)
            if Q: self.assertTrue(A.acyclic(Q))
        r = J("A25_star_intersection_lemma.json")
        self.assertEqual((r["nonempty_not_acyclic"], r["tested"]), (0, 5953)); self.assertGreater(r["hard_case_tested"], 100)

    def test_motif_census(self):
        r = J("A21_motifs.json")
        self.assertEqual(r["positives"]["counts"]["with_nonbounding_hollow_triangle"], 288)
        self.assertEqual(r["negatives"]["counts"]["with_nonbounding_hollow_triangle"], 0)
        self.assertEqual(r["negatives"]["counts"]["with_hollow_triangle"], 707)
        c = J("A23_cone_criterion.json")
        self.assertEqual(len(c["positives"]["exceptional_positives_without_hollow_triangle_nonbounding"]), 2)
        self.assertTrue(all(e["shortest_nonbounding_cycle_len"] == 4 for e in c["positives"]["exceptional_positives_without_hollow_triangle_nonbounding"]))
        self.assertEqual(c["positives"]["counts"]["bounding|uncone"], 6); self.assertEqual(c["negatives"]["counts"]["bounding|uncone"], 105)

    def test_cocycle_certificates_fresh(self):
        C, mp = (2, 4, 5, 9, 14, 15), 2520
        D = nerve.dead_sets(nerve.arithmetic_mask(C, mp))
        import A21_motifs as M
        B = nerve.Bounder(D)
        nb = [t for t in M.hollow_triangles(D) if not B.bounds(t)]
        self.assertEqual(len(nb), 4)
        cert = nerve.cocycle_certificate(D, list(nb[0]))
        self.assertTrue(nerve.check_cocycle(cert[0], D, list(nb[0])))
        # tamper: flipping an edge must break the cocycle property
        bad = set(cert[0]) ^ {cert[1][0]}
        self.assertFalse(nerve.check_cocycle(sorted(bad), D, list(nb[0])))
        r = J("A26_cocycle_certificates.json"); self.assertEqual(r["counts"], {"systems": 290, "certified": 290})

    def test_pair_anatomy_numbers(self):
        r = J("A22_pair_anatomy.json")
        a, b = r["INFO v003 witness"], r["INFO v002 pair"]
        self.assertEqual((a["|D|"], b["|D|"]), ([5, 5], [11, 7]))
        self.assertEqual((a["nerve_betti"], b["nerve_betti"]), ([[0, 1], [0, 0]], [[0, 1], [0, 0]]))
        self.assertEqual(a["nonbounding_hollow"], [4, 0])
        self.assertEqual(sorted(a["dead_only_in_positive"]), ["{4,9,15}", "{9,15}"])

    def test_adjacency_description_fresh(self):
        rng = random.Random(4)
        for _ in range(10):
            Bd = set(p for p in ad.PAIRS if rng.random() < rng.choice([0.1, 0.3]))
            m = ad.hamiltonian_mask(set(ad.PAIRS) - Bd)
            if m in (0, (1 << 720) - 1): continue
            s1, s2 = fb.y_simplices(m, 6), ad.Y_from_adjacency(Bd)
            self.assertEqual({d: set(v) for d, v in s1.items()}, {d: set(v) for d, v in s2.items()})
            self.assertEqual(hc.betti(m, 6)[2], 0)

    def test_pairwise_theorem_hypotheses(self):
        r = J("B20_adjacency_cover.json")
        self.assertEqual(r["H1_single_nonzero"], 0); self.assertEqual(r["single_pair_betti_distinct"], [[0, 0, 0]])
        self.assertEqual((r["sizes"]["2"]["sets"], r["sizes"]["2"]["empty"], r["sizes"]["2"]["disconnected"]), (435, 0, 0))
        self.assertEqual((r["sizes"]["3"]["sets"], r["sizes"]["3"]["empty"]), (4060, 0))
        self.assertEqual((r["sizes"]["2"]["criterion_violations"], r["sizes"]["3"]["criterion_violations"], r["criterion_random_larger"]["violations"]), (0, 0, 0))
        fresh = [ad.Z_S_betti([p], 2) for p in ad.PAIRS[:6]]
        self.assertTrue(all(b == [0, 0, 0] for b in fresh))

    def test_symbolic_theorem_data(self):
        r = J("B24_symbolic_theorem_check.json")
        self.assertEqual((r["distinct_masks"], r["beta2_max"], r["direct_Y_sample"]["H1_of_Y_nonzero"]), (665, 0, 0))
        r2 = J("B21_locality_boundary.json")["pair_adjacency_random"]
        self.assertEqual((r2["Y_H1_positive"], r2["beta2_K_positive"], r2["duality_mismatch"]), (0, 0, 0))

    def test_triple_adjacency_counterexample(self):
        c = json.load(open(os.path.join(ROOT, "CERTIFICATES", "counterexample_triple_adjacency_beta2.json")))
        self.assertEqual(c["forbidden_triples"], [[1, 2, 0], [5, 4, 3]])
        self.assertEqual(c["betti_hc_engine"], [1, 2, 5, 0, 0, 0]); self.assertEqual((c["beta2_rank_route"], c["beta2_column_route"]), (5, 5))
        self.assertTrue(c["certificate"]["verified"][0]); self.assertFalse(c["is_pair_adjacency_system"])
        import v2, B21_locality_boundary as B
        T3 = list(itertools.permutations(range(6), 3))
        m = B.triple_mask(set(T3) - {(1, 2, 0), (5, 4, 3)})
        self.assertEqual(hex(m), c["mask_hex"]); self.assertEqual(hc.betti(m, 6)[2], 5)
        A = [hc.perms(6)[i] for i in range(720) if m >> i & 1]
        z = [tuple(tuple(b) for b in f) for f in c["certificate"]["cycle"]]; phi = [tuple(tuple(b) for b in f) for f in c["certificate"]["cochain"]]
        self.assertTrue(v2.pair_cert.verify(A, z, phi)[0])
        self.assertFalse(v2.pair_cert.verify(A, z[:-1], phi)[0])
        mech = J("B23_two_triple_mechanism.json")
        self.assertEqual(mech["reduced_betti_intersection"][0], 5); self.assertEqual(mech["reduced_betti_union"][1], 5)

    def test_manifest(self):
        import hashlib
        man = json.load(open(os.path.join(ROOT, "MANIFEST.json")))
        for rel, h in man["files"].items():
            if rel.startswith("TESTS/"): continue
            self.assertEqual(hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest(), h, rel)

if __name__ == "__main__":
    unittest.main(verbosity=1)
