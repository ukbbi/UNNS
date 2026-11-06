"""GIG-I v001 automated tests (standard library `unittest`).  Run:  python -m unittest discover -s TESTS -v
Optional read-only cross-check against the frozen GEO-HD-1D v004 sources:  set GIG_FROZEN_SRC=<path to GEO_HD_1D_v004/src>."""
import os, sys, json, random, unittest
from fractions import Fraction
from decimal import Decimal
from math import comb, log2, floor, log
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
sys.path.insert(0, os.path.join(ROOT, "EXPERIMENTS"))
import history_fibres as hf
import swap_graph as sg
import information as inf
import history_complex as hc
import census as cs

TOL = Decimal(10) ** -40
REFERENCE = [4, 100, 3601, 194864, 14177856, 1258011667]


def fibre_graph(histories):
    H = sorted(histories)
    return H, sg.swap_graph(H)


class T1_ReverseEdges(unittest.TestCase):
    def test_reverse_edge_characterisation_bruteforce(self):
        for t in range(2, 2500):
            brute = set()
            for m in range(1, t // 4 + 1):
                for N in range(1, m + 1):
                    if m % N == 0 and m // N * (N + 1) ** 2 == t:
                        brute.add((N, m))
            self.assertEqual(brute, set(hf.reverse_edges(t)), t)
            for N, m in hf.reverse_edges(t):
                self.assertEqual((N + 1) ** 2 * (t // (N + 1) ** 2), t)        # (N+1)^2 | t
                self.assertEqual(m, N * t // (N + 1) ** 2)
                self.assertGreaterEqual(t, 4 * m)                               # T_N(m)/m = N+2+1/N >= 4

    def test_ratio_identity(self):
        for N in range(1, 200):
            self.assertEqual(hf.R(N), N + 2 + Fraction(1, N))
            self.assertGreaterEqual(hf.R(N), 4)

    def test_edge_count_formula(self):
        # number of reverse edges = tau(s(t)) - 1, s(t) = prod p^floor(v_p/2)
        for t in range(2, 4000):
            tau = 1
            for p, e in hf.factor(t):
                tau *= e // 2 + 1
            self.assertEqual(len(hf.reverse_edges(t)), tau - 1)

    def test_history_length_bound(self):
        for r in (1, 2, 3):
            t = 72 ** r
            for m0, labs in hf.complete_histories(t):
                self.assertTrue(hf.is_admissible(m0, labs) and hf.endpoint(m0, labs) == t and hf.is_squarefree(m0))
                self.assertLessEqual(4 ** len(labs) * m0, t)


class T2_Counts(unittest.TestCase):
    def test_histories_of_72(self):
        self.assertEqual(set(hf.complete_histories(72)), {(1, (1, 1, 2)), (1, (1, 2, 1)), (3, (3, 2)), (10, (5,))})

    def test_reference_sequence_and_enumeration(self):
        self.assertEqual([hf.count_complete(72 ** r) for r in range(1, 7)], REFERENCE)
        for r in (1, 2, 3):
            self.assertEqual(sum(1 for _ in hf.complete_histories(72 ** r)), REFERENCE[r - 1])

    def test_lower_bound_family(self):
        import E2_growth
        for r in range(1, 6):
            fam = E2_growth.binomial_family(r)
            self.assertEqual(len(set(fam)), comb(2 * r, r))
            self.assertTrue(all(hf.is_admissible(*h) and hf.endpoint(*h) == 72 ** r for h in fam))
        for r in range(1, 8):
            self.assertGreaterEqual(hf.count_complete(72 ** r), comb(2 * r, r))

    def test_fixed_source_dp_matches_enumeration(self):
        for m0, t in ((4, 65536), (72, 194400), (1, 72 ** 2)):
            self.assertEqual(hf.count_fixed_source(m0, t), sum(1 for _ in hf.fixed_source_histories(m0, t)))


class T3_Information(unittest.TestCase):
    def test_E1_decomposition(self):
        import E1_72
        r = E1_72.run()
        self.assertEqual(r["swap_class_sizes"], [1, 1, 2])
        self.assertEqual(Decimal(r["A_bits"]), 2)
        self.assertEqual(Decimal(r["H(C|T)"]), Decimal("1.5"))
        self.assertEqual(Decimal(r["H(W|C,T)"]), Decimal("0.5"))
        self.assertEqual(Decimal(r["H(W|T)"]), 2)
        self.assertEqual(Decimal(r["H(M|T)"]), Decimal("1.5"))
        self.assertTrue(Decimal(r["nonuniform_example"]["H"]) < 2)

    def test_hartley_shannon_bounds(self):
        rnd = random.Random(1)
        for _ in range(60):
            n = rnd.randint(1, 9)
            w = [rnd.randint(1, 7) for _ in range(n)]
            p = [Fraction(x, sum(w)) for x in w]
            self.assertLessEqual(inf.shannon(p), inf.hartley(n) + TOL)
            self.assertGreaterEqual(inf.shannon(p), 0)
        for n in range(1, 40):
            self.assertLess(abs(inf.shannon([Fraction(1, n)] * n) - inf.hartley(n)), TOL)
        # arbitrarily small entropy with a large fibre
        p = [Fraction(1000, 1003)] + [Fraction(1, 1003)] * 3
        self.assertLess(inf.shannon(p), Decimal("0.05"))

    def test_chain_rule_identity(self):
        rnd = random.Random(2)
        for _ in range(40):
            pieces = {i: [rnd.randint(1, 6) for _ in range(rnd.randint(1, 4))] for i in range(rnd.randint(1, 5))}
            c = inf.uniform_chain(pieces)
            self.assertLess(abs(c["H(P|T)"] + c["H(C|P,T)"] + c["H(W|C,T)"] - c["A"]), TOL)

    def test_class_entropy_vs_component_count(self):
        rnd = random.Random(3)
        for _ in range(60):
            sizes = [rnd.randint(1, 9) for _ in range(rnd.randint(1, 6))]
            self.assertLessEqual(inf.class_entropy(sizes), inf.log2_dec(len(sizes)) + TOL)
        for k in range(1, 8):
            self.assertLess(abs(inf.class_entropy([5] * k) - inf.log2_dec(k)), TOL)
        self.assertLess(inf.class_entropy([1, 1, 100]), inf.log2_dec(3) - Decimal("0.5"))

    def test_E3(self):
        import E3_content
        r = E3_content.run()
        self.assertTrue(r["multiplier_identity_R1^7=R2^2*R3^4"])
        self.assertEqual(r["N"], 18)
        self.assertEqual(r["admissible_orderings_from_4"], {"1^7": 1, "2^2 3^4": 3})
        self.assertEqual(r["admissible_orderings_from_1"]["2^2 3^4"], 0)
        self.assertEqual({k: v["n_histories"] for k, v in r["pieces_by_content"].items()},
                         {"1|1|1|1|1|1|1": 1, "1|3|4|5|15": 10, "2|2|3|3|3|3": 3, "2|3|6|7|7": 4})
        tot = Decimal(r["content_entropy_H(Q|T)"]) + Decimal(r["class_entropy_given_content_H(C|Q,T)"]) + Decimal(r["ordering_entropy_H(W|C,T)"])
        self.assertLess(abs(tot - Decimal(r["A_bits"])), Decimal("1e-9"))


class T4_Profile(unittest.TestCase):
    FIBRES = [("complete", 72), ("complete", 72 ** 2), ("complete", 3600), ("fixed", (4, 65536)), ("fixed", (72, 194400))]

    def fibres(self):
        for kind, a in self.FIBRES:
            yield (hf.complete_histories(a) if kind == "complete" else hf.fixed_source_histories(*a))

    def test_profile_properties(self):
        for hs in self.fibres():
            H, adj = fibre_graph(hs)
            prof = sg.ball_profile(adj)
            N = len(H)
            D = sg.max_component_diameter(adj)
            sizes = [len(c) for c in sg.components(adj)]
            I = inf.information_profile(prof, D + 3)
            self.assertEqual(I[0], 0)
            for r in range(D + 3):
                self.assertGreaterEqual(I[r + 1] + TOL, I[r])
            for r in range(D):
                self.assertGreater(I[r + 1], I[r] + Decimal("1e-30"))           # strict until the maximal diameter
            for r in range(D, D + 3):
                self.assertLess(abs(I[r] - inf.within_class_entropy(sizes)), TOL)
            if D > 0:
                self.assertLess(I[D - 1], inf.within_class_entropy(sizes) - Decimal("1e-30"))
            # I_r = log2(P_r)/N and integer product identity
            for r in range(D + 1):
                self.assertAlmostEqual(float(I[r]), log2(sg.ball_product(prof, r)) / N, places=9)

    def test_jensen_and_cycle_law(self):
        for hs in self.fibres():
            H, adj = fibre_graph(hs)
            prof = sg.ball_profile(adj)
            N, E = len(H), sum(len(a) for a in adj) // 2
            b0 = len(sg.components(adj))
            I1 = inf.information_profile(prof, 1)[1] if sg.max_component_diameter(adj) >= 1 else Decimal(0)
            bound = inf.log2_dec(Fraction(N + 2 * E, N))
            self.assertLessEqual(I1, bound + TOL)
            b1G = E - N + b0
            self.assertEqual(b1G >= 0, True)
            if I1 >= inf.log2_dec(3) - TOL:
                self.assertGreaterEqual(b1G, 1)
        # synthetic: cycle C_n attains equality and I_1 = log2 3; path has I_1 < log2 3
        n = 9
        cyc = [[(i - 1) % n, (i + 1) % n] for i in range(n)]
        path = [[j for j in (i - 1, i + 1) if 0 <= j < n] for i in range(n)]
        self.assertLess(abs(inf.information_profile(sg.ball_profile(cyc), 1)[1] - inf.log2_dec(3)), TOL)
        self.assertLess(inf.information_profile(sg.ball_profile(path), 1)[1], inf.log2_dec(3))

    def test_additivity_over_pieces(self):
        H, adj = fibre_graph(hf.complete_histories(3600))
        prof = sg.ball_profile(adj)
        D = sg.max_component_diameter(adj)
        whole = inf.information_profile(prof, D)
        pieces = hf.classify(H)
        N = len(H)
        acc = [Decimal(0)] * (D + 1)
        for key, hs in pieces.items():
            sub = sg.swap_graph(hs)
            p2 = sg.ball_profile(sub)
            for r in range(D + 1):
                acc[r] += Decimal(len(hs)) / Decimal(N) * (inf.log2_dec(sg.ball_product(p2, r)) / Decimal(len(hs)))
        for r in range(D + 1):
            self.assertLess(abs(acc[r] - whole[r]), TOL)

    def test_swap_preserves_source_content_endpoint(self):
        for hs in self.fibres():
            for h in list(hs)[:200]:
                for g in sg.legal_swap_neighbours(h):
                    self.assertEqual((g[0], hf.content(g[1]), hf.endpoint(*g)), (h[0], hf.content(h[1]), hf.endpoint(*h)))


class T5_Topology(unittest.TestCase):
    def test_inherited_examples(self):
        a = hc.admissible_arrangements((2, 3, 8, 9), 72)
        self.assertEqual((len(a), hc.betti(a, 4), hc.betti(a, 4, True)), (16, (1, 1, 0, 0), (1, 1, 0, 0)))
        b = hc.admissible_arrangements((2, 3, 8, 9, 14), 1008)
        self.assertEqual((len(b), hc.betti(b, 5), hc.betti(b, 5, True)), (96, (1, 0, 1, 0, 0), (1, 19, 0, 0, 0)))

    def test_full_permutohedron(self):
        for k, fv in ((3, (6, 6, 1)), (4, (24, 36, 14, 1)), (5, (120, 240, 150, 30, 1))):
            P = hc.perms(k)
            self.assertEqual(hc.f_vector(set(P), k), fv)
            self.assertEqual(hc.betti(set(P), k), (1,) + (0,) * (k - 1))

    def test_euler_and_radius2_formula_random_sets(self):
        rnd = random.Random(7)
        for k, trials in ((4, 150), (5, 60)):
            P = hc.perms(k)
            for _ in range(trials):
                A = {p for p in P if rnd.random() < rnd.choice((0.3, 0.5, 0.8))}
                if not A:
                    continue
                self.assertEqual(hc.euler_characteristic(A, k), sum((-1) ** i * b for i, b in enumerate(hc.betti(A, k))))
                order, adj = hc.induced_adjacency(A, k)
                ok, maxc, tri = sg.ball2_check(adj)
                self.assertTrue(ok and maxc <= 2 and tri)

    def test_square_count_from_fine_radius2_data(self):
        rnd = random.Random(21)
        for k, trials in ((4, 120), (5, 50)):
            P = hc.perms(k)
            for _ in range(trials):
                A = {p for p in P if rnd.random() < rnd.choice((0.4, 0.6, 0.85))}
                if len(A) < 2:
                    continue
                order, adj = hc.induced_adjacency(A, k)
                prof = sg.ball_profile(adj)
                N, E = len(adj), sum(len(a) for a in adj) // 2
                num = N + 2 * E + sum(len(a) * (len(a) - 1) for a in adj) - sum(sg.ball_size(p, 2) for p in prof)
                self.assertEqual(num % 4, 0)
                self.assertEqual(num // 4, hc.square_hexagon_counts(A, k)[0])

    def test_four_cycles_are_square_faces(self):
        for k in (4, 5):
            P = hc.perms(k)
            order, adj = hc.induced_adjacency(set(P), k)
            c4 = 0
            for v in range(len(adj)):
                cnt = {}
                for x in adj[v]:
                    for z in adj[x]:
                        if z != v:
                            cnt[z] = cnt.get(z, 0) + 1
                c4 += sum(1 for c in cnt.values() if c == 2)
            self.assertEqual(c4 // 4, hc.square_hexagon_counts(set(P), k)[0])

    def test_threshold_law_equals_simulation(self):
        rnd = random.Random(11)
        for _ in range(3000):
            m0 = rnd.choice([1, 2, 6, 12, 72, 210, 1008, 3600, 5040])
            w = tuple(rnd.randint(1, 15) for _ in range(rnd.randint(1, 6)))
            self.assertEqual(hf.is_admissible(m0, w), m0 % hf.threshold(w) == 0)

    def test_complete_history_loop(self):
        s = hc.admissible_arrangements((2, 3, 14, 15), 210)
        self.assertTrue(hf.is_squarefree(210))
        self.assertEqual(hc.betti(s, 4), (1, 1, 0, 0))
        t = hf_end((2, 3, 14, 15), 210)
        H = list(hf.complete_histories(t))
        self.assertEqual(len(H), 15842)
        self.assertIn((210, (2, 3, 14, 15)), {(h[0], tuple(sorted(h[1]))) for h in H})

    def test_certificates(self):
        import E4_topology as e4
        expected = {"W1-loop-entropy": 1, "W2-loop-entropy-inherited": 1, "W3-void-radius1": 2, "W4-loop-radius1": 2,
                    "W5-loop-radius2": 3, "W6-loop-radius2-complete-history": 3}
        got = {c["id"]: c for c in e4.section_C()}
        self.assertEqual(set(got), set(expected))
        for cid, rsep in expected.items():
            c = got[cid]
            self.assertTrue(c["topologies_differ"] and c["same_N"] and c["same_class_sizes"] and c["same_H_C_and_H_W_given_C"], cid)
            self.assertEqual(c["separating_radius"], rsep, cid)
            self.assertTrue(c["A"]["euler_equals_alternating_betti"] and c["B"]["euler_equals_alternating_betti"])
            self.assertTrue(c["A"]["threshold_law_agrees_with_simulation"] and c["B"]["threshold_law_agrees_with_simulation"])
        for cid in ("W5-loop-radius2", "W6-loop-radius2-complete-history"):
            self.assertTrue(got[cid]["same_N_E_squares"] and got[cid]["same_fine_signature_r_le_2"] and not got[cid]["same_fine_signature_r_le_3"])
        self.assertTrue(got["W3-void-radius1"]["same_fine_signature_r_le_1"] and got["W3-void-radius1"]["same_I_1"])
        self.assertTrue(got["W6-loop-radius2-complete-history"]["A"]["source_squarefree"])
        self.assertTrue(got["W1-loop-entropy"]["A"]["source_squarefree"] and got["W1-loop-entropy"]["B"]["source_squarefree"])

    def test_small_census_invariants(self):
        found, skipped = cs.realizable_masks(4, 18, 30000)
        self.assertEqual(skipped, 0)
        datas = [cs.mask_data(m, 4) for m in found]
        table = {(r["r"], r["kind"]): r["ambiguous_groups"] for r in cs.detection_table(datas, 3)}
        self.assertGreater(table[(0, "scalar")], 0)          # entropy-level data is ambiguous
        self.assertEqual(table[(1, "fine")], 0)              # k=4: radius 1 already separates (finite-exact, this bound)
        self.assertTrue(any(d["betti"] == (1, 1, 0, 0) for d in datas))


def hf_end(content, m0):
    t = Fraction(m0)
    for N in content:
        t *= hf.R(N)
    return int(t)


@unittest.skipUnless(os.environ.get("GIG_FROZEN_SRC"), "set GIG_FROZEN_SRC to cross-check against frozen GEO-HD-1D v004 (read-only)")
class T6_CrossCheckFrozen(unittest.TestCase):
    def test_against_frozen(self):
        sys.path.insert(0, os.environ["GIG_FROZEN_SRC"])
        import select_history as fs, route_topology as frt, thresholds as fth
        for t in list(range(2, 400)) + [72, 144, 1296, 3600, 5184, 72 ** 2]:
            self.assertEqual(sorted(hf.complete_histories(t)), sorted(fs.complete_histories(t)))
            self.assertEqual(sorted(hf.reverse_edges(t)), sorted(fs.predecessors(t)))
        rnd = random.Random(5)
        for k in (4, 5):
            P = hc.perms(k)
            for _ in range(40):
                A = {p for p in P if rnd.random() < 0.7}
                self.assertEqual(hc.betti(A, k), frt.betti(A, k)[0])
                self.assertEqual(hc.betti(A, k, True), frt.betti(A, k, True)[0])


class T7_RecordedResults(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "RESULTS", "results.json")), "results.json not generated yet")
    def test_results_json_matches_recomputation(self):
        r = json.load(open(os.path.join(ROOT, "RESULTS", "results.json")))
        self.assertEqual([x["count"] for x in r["E2"]["rows"][:6]], REFERENCE)
        self.assertEqual(r["E1"]["swap_class_sizes"], [1, 1, 2])
        self.assertEqual(r["E4"]["B_complete_history_loop"]["fibre_size"], 15842)
        self.assertTrue(all(c["topologies_differ"] for c in r["E4"]["C_certificates"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
