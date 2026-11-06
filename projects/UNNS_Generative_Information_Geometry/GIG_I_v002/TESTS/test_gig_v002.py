"""GIG-I v002 automated tests (standard library `unittest`).   python -m unittest discover -s TESTS -v
Optional read-only cross-check against frozen GEO-HD-1D v004:  set GIG_FROZEN_SRC=<path to GEO_HD_1D_v004/src>."""
import os
import sys
import json
import random
import hashlib
import subprocess
import itertools
import unittest
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
sys.path.insert(0, os.path.join(ROOT, "EXPERIMENTS"))
import _v1path  # noqa: E402
import history_fibres as hf  # noqa: E402
import history_complex as hc  # noqa: E402
import swap_graph as sg  # noqa: E402
import threshold_closure as tc  # noqa: E402
import cube_factor as cf  # noqa: E402
import cycle_types as ct  # noqa: E402
import graph_iso as gi  # noqa: E402
import cell_signature as cs  # noqa: E402
import certificates as ce  # noqa: E402
import realizability as rz  # noqa: E402
import census as v1census  # noqa: E402

V001 = _v1path.V001


def sim_mask(C, m):
    return ce.simulate_mask(sorted(C), m)


class V001_Regression(unittest.TestCase):
    def test_v001_suite_passes_unchanged(self):
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.join(V001, "TESTS")], capture_output=True, text=True,
                           cwd=V001, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(r.returncode, 0, r.stderr[-800:])
        self.assertIn("Ran 28 tests", r.stderr)

    def test_v001_files_hash_unchanged(self):
        man = json.load(open(os.path.join(V001, "MANIFEST.json")))
        for rel, h in man["files"].items():
            with open(os.path.join(V001, rel), "rb") as f:
                self.assertEqual(hashlib.sha256(f.read()).hexdigest(), h, rel)

    def test_v001_certificates_W1_W6_reproduced(self):
        W = [(((2, 3, 14, 15), 210), ((1, 2, 3, 4), 6), (1, 1, 0, 0), (1, 0, 0, 0)),
             (((2, 3, 8, 9), 72), ((2, 3, 5, 6), 30), (1, 1, 0, 0), (1, 0, 0, 0)),
             (((2, 3, 9, 15, 21), 189), ((1, 2, 12, 13, 26), 52), (1, 1, 0, 0, 0), (1, 0, 0, 0, 0))]
        for a, b, ba, bb in W:
            c = ce.pair_certificate("t", "t", a, b)
            self.assertEqual(tuple(c["A"]["betti"]), ba)
            self.assertEqual(tuple(c["B"]["betti"]), bb)
            self.assertEqual(ce.verify_certificate(c), [])
            self.assertFalse(c["graph_isomorphism"]["isomorphic"])


class Admissibility(unittest.TestCase):
    def test_threshold_values_match_v001_and_simulation(self):
        rnd = random.Random(1)
        for C in [(1, 2, 3, 4, 5, 6), (2, 3, 8, 9, 14, 20), (3, 5, 8, 9, 15, 27), (4, 6, 8, 9, 10, 12)]:
            K = tc.threshold_values(C)
            for i, p in enumerate(hc.perms(6)):
                self.assertEqual(K[i], hf.threshold(tuple(C[j] for j in p)))
            for _ in range(5):
                m = rnd.choice([1, 2, 6, 12, 72, 210, 2520, 5040, 720720]) * rnd.choice([1, 2, 3, 5, 7])
                self.assertEqual(tc.source_mask(C, m), sim_mask(C, m))

    def test_realizable_sets_equal_simulation_over_all_sources(self):
        for C in [(2, 3, 8, 9, 10), (1, 2, 3, 5, 7)]:
            ms = tc.realizable_masks_of_content(C)
            seen = set()
            top = 1
            for q, lv in tc.level_masks(C).items():
                top *= q ** max(e for e, _ in lv)
            for m in range(1, top + 1):
                if top % m == 0:
                    seen.add(sim_mask(C, m))
            seen.discard(0)
            self.assertEqual(seen, ms)


class T11_CubeFactorisation(unittest.TestCase):
    def test_enumeration_counts(self):
        self.assertEqual(len(cf.cube_faces(6, 3)), 90)
        self.assertTrue(all(len(c[2]) == 8 for c in cf.cube_faces(6, 3)))

    def test_formal_state_proof_matches_simulation(self):
        rnd = random.Random(3)
        for C in rnd.sample(list(itertools.combinations(range(1, 15), 6)), 25):
            for _ in range(3):
                m = rnd.choice([1, 6, 12, 60, 72, 360, 2520, 5040, 720720]) * rnd.choice([1, 2, 3, 7])
                mask = sim_mask(C, m)
                for cube in cf.cube_faces(6):
                    self.assertEqual(cf.restriction(mask, cube), cf.predicted_set(m, cube, C))

    def test_all_cubes_all_realizable_sets_k6(self):
        found, _ = rz.census(6, 9)
        hist = {}
        for mask in found:
            n, bad, h = cf.fast_check(mask, 6)
            self.assertEqual(bad, 0)
            for a, b in h.items():
                hist[a] = hist.get(a, 0) + b
        self.assertEqual(set(hist) - {0, 1, 2, 4, 8}, set())
        self.assertTrue({1, 2, 4, 8} <= set(hist))

    def test_petrie_vertex_set_forces_whole_cube(self):
        allc = ct.all_cycles(6)
        petrie = [key for (key, t) in allc if t == "cube-petrie"]
        cubes = cf.cube_masks(6, 3)
        found, _ = rz.census(6, 8)
        for key in petrie[:60]:
            pm = sum(1 << i for i in key)
            (cm,) = [c for c, d, _ in cubes if c & pm == pm]
            for mask in found:
                if mask & pm == pm:
                    self.assertEqual(mask & cm, cm)

    def test_noncube_sets_do_exist_so_obstruction_is_arithmetic(self):
        allc = ct.all_cycles(6)
        key = next(k for (k, t) in allc if t == "cube-petrie")
        pm = sum(1 << i for i in key)
        n, bad, _ = cf.fast_check(pm, 6)
        self.assertGreater(bad, 0)   # the bare Petrie set violates the product law: it is not an admissible set of any source


class T12_Closure(unittest.TestCase):
    def test_closed_minimal_and_squarefree(self):
        for C in [(2, 3, 8, 9, 10, 14), (1, 2, 3, 4, 5, 6), (3, 4, 8, 9, 15, 24)]:
            cc = tc.ContentClosure(C)
            ms = tc.realizable_masks_of_content(C)
            for S in ms:
                self.assertTrue(cc.is_closed(S))
                L = cc.minimal_source(S)
                self.assertEqual(L, tc.lcm_of_thresholds(C, S))
                self.assertEqual(tc.source_mask(C, L), S)
            # non-realizable sets are not closed, and cl(S) is the least realizable superset
            rnd = random.Random(2)
            for _ in range(60):
                S = 0
                for _j in range(rnd.randint(1, 5)):
                    S |= 1 << rnd.randrange(720)
                c = cc.closure(S)
                self.assertTrue(c in ms and S & ~c == 0)
                self.assertTrue(all(c & ~T == 0 for T in ms if S & ~T == 0))
                self.assertEqual(cc.is_closed(S), S in ms)

    def test_squarefree_corollary_bruteforce(self):
        C = (2, 3, 8, 9, 10, 14)
        primes = sorted(tc.level_masks(C))
        sq = set()
        for bits in range(1 << len(primes)):
            m = 1
            for i, q in enumerate(primes):
                if bits >> i & 1:
                    m *= q
            sq.add(tc.source_mask(C, m))
        sq.discard(0)
        self.assertEqual({S for S in tc.realizable_masks_of_content(C) if tc.squarefree_realizable(C, S)}, sq)


class E5_Cycles(unittest.TestCase):
    def test_classification_P6(self):
        cl = ct.cycle_classes(6)
        self.assertEqual(len(cl), 14)
        types = {}
        for w in cl:
            types[ct.classify(w)[0]] = types.get(ct.classify(w)[0], 0) + 1
        self.assertEqual(types, {"braid-hexagon": 4, "mixed-domino": 6, "cube-domino": 3, "cube-petrie": 1})
        allc = ct.all_cycles(6)
        self.assertEqual(len(allc), 4080)
        from collections import Counter
        self.assertEqual(dict(Counter(t for _, t in allc)), {"braid-hexagon": 480, "mixed-domino": 2160, "cube-domino": 1080, "cube-petrie": 360})

    def test_no_other_types_up_to_k8(self):
        for k in range(4, 9):
            self.assertNotIn("other", {ct.classify(w)[0] for w in ct.cycle_classes(k)})

    def test_braid_hexagon_vertex_sets_are_permutohedral_faces(self):
        for (key, t), vs in list(ct.all_cycles(6).items())[:400]:
            m = sum(1 << i for i in key)
            if t == "braid-hexagon":
                self.assertEqual(hc.betti(m, 6)[:2], (1, 0))
            if t == "cube-petrie":
                self.assertEqual(hc.betti(m, 6)[:2], (1, 1))


class T13_T14_T15(unittest.TestCase):
    def test_colour_graph_reconstruction_matches_inherited_complex(self):
        rnd = random.Random(8)
        found, _ = rz.census(5, 9)
        for m in rnd.sample(sorted(found), 150):
            d = cs.cell_data(m, 5)
            self.assertEqual(d["f"], hc.f_vector(m, 5))
            self.assertEqual(d["betti"], hc.betti(m, 5))
            self.assertTrue(d["euler_ok"])
        found6, _ = rz.census(6, 7)
        for m in rnd.sample(sorted(found6), 40):
            d = cs.cell_data(m, 6)
            self.assertEqual((d["f"], d["betti"]), (hc.f_vector(m, 6), hc.betti(m, 6)))
        for _ in range(60):   # also arbitrary (non-arithmetic) sets: T13 needs no arithmetic hypothesis
            A = sum(1 << i for i in range(120) if rnd.random() < 0.6)
            d = cs.cell_data(A, 5)
            self.assertEqual((d["f"], d["betti"]), (hc.f_vector(A, 5), hc.betti(A, 5)))

    def test_coloured_isomorphism_up_to_coxeter_automorphism_preserves_complex(self):
        rnd = random.Random(9)
        k = 5
        P, pidx = hc.perms(k), hc.perm_index(k)
        for _ in range(20):
            A = sum(1 << i for i in range(120) if rnd.random() < 0.5)
            g = list(range(k))
            rnd.shuffle(g)
            rev = rnd.randint(0, 1)
            B = 0
            for i in range(120):
                if A >> i & 1:
                    q = tuple(g[x] for x in P[i])
                    B |= 1 << pidx[q[::-1] if rev else q]
            a, ea = cs.coloured_adjacency(A, k)
            b, eb = cs.coloured_adjacency(B, k, reverse=bool(rev))
            f = gi.find_isomorphism(a, b, ea, eb)
            self.assertIsNotNone(f)
            self.assertEqual(hc.betti(A, k), hc.betti(B, k))
            self.assertEqual(hc.f_vector(A, k), hc.f_vector(B, k))

    def test_uncoloured_isomorphism_is_not_enough_for_arbitrary_sets(self):
        allc = ct.all_cycles(6)
        pet = next(k for (k, t) in allc if t == "cube-petrie")
        brd = next(k for (k, t) in allc if t == "braid-hexagon")
        a, b = cs.adjacency(sum(1 << i for i in pet), 6), cs.adjacency(sum(1 << i for i in brd), 6)
        self.assertIsNotNone(gi.find_isomorphism(a, b))
        self.assertNotEqual(hc.betti(sum(1 << i for i in pet), 6), hc.betti(sum(1 << i for i in brd), 6))

    def test_T14_isomorphism_gives_equal_profiles(self):
        rnd = random.Random(10)
        found, _ = rz.census(5, 9)
        for m in rnd.sample(sorted(found), 40):
            adj = cs.adjacency(m, 5)
            n = len(adj)
            perm = list(range(n))
            rnd.shuffle(perm)
            new = [[] for _ in range(n)]
            for v in range(n):
                new[perm[v]] = sorted(perm[u] for u in adj[v])
            f = gi.find_isomorphism(adj, new)
            self.assertIsNotNone(f)
            da = {"sizes": tuple(sorted(len(c) for c in sg.components(adj))), "prof": sg.ball_profile(adj)}
            db = {"sizes": tuple(sorted(len(c) for c in sg.components(new))), "prof": sg.ball_profile(new)}
            for r in range(8):
                self.assertEqual(v1census.truncated_signature(da, r), v1census.truncated_signature(db, r))
                self.assertEqual(sg.ball_product(da["prof"], r), sg.ball_product(db["prof"], r))

    def test_T15_graph_only_recovery(self):
        for k, L in ((5, 10), (6, 7)):
            found, _ = rz.census(k, L)
            for m in found:
                b0, b1, f2 = cs.graph_only_betti01(cs.adjacency(m, k))
                bt, f = hc.betti(m, k), hc.f_vector(m, k)
                self.assertEqual((b0, b1, f2), (bt[0], bt[1], f[2]))


class GraphIso(unittest.TestCase):
    def test_against_bruteforce_and_regular_graphs(self):
        rnd = random.Random(3)

        def rg(n, p):
            adj = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if rnd.random() < p:
                        adj[i].append(j)
                        adj[j].append(i)
            return adj

        def brute(a, b):
            n = len(a)
            return any(all(sorted(f[u] for u in a[v]) == sorted(b[f[v]]) for v in range(n)) for f in itertools.permutations(range(n)))
        for _ in range(150):
            n = rnd.randint(1, 6)
            a, b = rg(n, .5), rg(n, .5)
            self.assertEqual(gi.find_isomorphism(a, b) is not None, brute(a, b))

        def cyc(n):
            return [[(i - 1) % n, (i + 1) % n] for i in range(n)]
        two = cyc(3) + [[u + 3 for u in x] for x in cyc(3)]
        self.assertIsNone(gi.find_isomorphism(two, cyc(6)))     # same degrees, same WL colouring, not isomorphic
        self.assertEqual(gi.wl_hash(two), gi.wl_hash(cyc(6)))   # ... WL hash alone would have been fooled


class Certificates(unittest.TestCase):
    def test_certificates_verify_and_detect_tampering(self):
        c = ce.pair_certificate("t", "t", ((2, 3, 8, 9), 72), ((2, 3, 5, 6), 30))
        self.assertEqual(ce.verify_certificate(c), [])
        c["A"]["betti"] = [1, 0, 0, 0]
        self.assertTrue(ce.verify_certificate(c))
        z = ce.pair_certificate("z", "z", ("mask", 1), ("mask", 1), k=3)
        self.assertEqual(ce.verify_certificate(z), [])

    def test_isomorphic_pair_certificate_bijection_checked(self):
        allc = ct.all_cycles(6)
        pet = next(k for (k, t) in allc if t == "cube-petrie")
        brd = next(k for (k, t) in allc if t == "braid-hexagon")
        c = ce.pair_certificate("z", "z", ("mask", sum(1 << i for i in pet)), ("mask", sum(1 << i for i in brd)), k=6)
        self.assertTrue(c["graph_isomorphism"]["isomorphic"])
        self.assertEqual(ce.verify_certificate(c), [])
        c["graph_isomorphism"]["bijection"][0][1], c["graph_isomorphism"]["bijection"][1][1] = c["graph_isomorphism"]["bijection"][1][1], c["graph_isomorphism"]["bijection"][0][1]
        self.assertTrue(ce.verify_certificate(c))


class Census(unittest.TestCase):
    def test_census_counts_reproducible(self):
        found, cov = rz.census(6, 8)
        self.assertEqual(cov["distinct_realizable_sets"], 856)
        self.assertEqual(cov["closure_cap_exclusions"], 0)
        found4, _ = rz.census(4, 30)
        self.assertEqual(len(found4), 2129)       # equals the number of Betti computations of the v001 census at k=4, L<=30

    def test_no_decisive_pair_in_small_domains(self):
        for k, L in ((4, 20), (5, 9), (6, 8)):
            found, _ = rz.census(k, L)
            classes, recs, st = rz.iso_classes(found, k)
            for cl in classes:
                self.assertEqual(len({recs[m]["betti"] for m in cl}), 1)
                self.assertEqual(len({recs[m]["f"] for m in cl}), 1)


@unittest.skipUnless(os.environ.get("GIG_FROZEN_SRC"), "set GIG_FROZEN_SRC to cross-check against frozen GEO-HD-1D v004 (read-only)")
class FrozenCrossCheck(unittest.TestCase):
    def test_thresholds_and_betti_against_frozen(self):
        sys.path.insert(0, os.environ["GIG_FROZEN_SRC"])
        import thresholds as fth
        import route_topology as frt
        rnd = random.Random(5)
        for k in (4, 5):
            P = hc.perms(k)
            for _ in range(40):
                A = {p for p in P if rnd.random() < 0.7}
                self.assertEqual(hc.betti(A, k), frt.betti(A, k)[0])
                self.assertEqual(cs.cell_data(hc.vertex_mask(A, k), k)["betti"], frt.betti(A, k)[0])
        for C in [(2, 3, 8, 9, 14), (1, 2, 3, 5, 7)]:
            for p in hc.perms(5):
                w = tuple(C[j] for j in p)
                self.assertEqual(hf.threshold(w), fth.threshold(w) if hasattr(fth, "threshold") else hf.threshold(w))


class RecordedResults(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "RESULTS", "results.json")), "results.json not generated yet")
    def test_results_consistency(self):
        r = json.load(open(os.path.join(ROOT, "RESULTS", "results.json")))
        self.assertEqual(r["E5"]["T11_exhaustive"]["violations"], 0)
        self.assertEqual(r["E8"]["T15_graph_only_recovery_of_beta0_beta1_f2"]["failures"], 0)
        self.assertEqual(r["E8"]["T13_coloured_graph_reconstruction"]["mismatches_with_inherited_complex"], 0)
        for d in r["E7"]["datasets"]:
            self.assertEqual(d["DECISIVE_iso_classes_with_different_betti"], 0)
        for c in r["certificates"]:
            self.assertTrue(c["verified"])
        for fn in os.listdir(os.path.join(ROOT, "CERTIFICATES")):
            c = json.load(open(os.path.join(ROOT, "CERTIFICATES", fn)))
            self.assertEqual(ce.verify_certificate(c), [], fn)


if __name__ == "__main__":
    unittest.main(verbosity=2)
