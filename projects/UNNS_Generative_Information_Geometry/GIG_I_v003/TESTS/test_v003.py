"""GIG-I v003 automated tests (standard library `unittest`).   python -m unittest discover -s TESTS -v
Optional read-only cross-check against frozen GEO-HD-1D v004:  set GIG_FROZEN_SRC=<path to GEO_HD_1D_v004/src>."""
import hashlib
import json
import math
import os
import random
import subprocess
import sys
import unittest
from fractions import Fraction
from itertools import combinations

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
sys.path.insert(0, os.path.join(ROOT, "EXPERIMENTS"))
import _v2path  # noqa: E402
import history_complex as hc  # noqa: E402
import threshold_closure as tc  # noqa: E402
import cell_signature as cs  # noqa: E402
import block_factor as bf  # noqa: E402
import face_threshold as ft  # noqa: E402
import cell_boundary as cb  # noqa: E402
import source_filtration as sf  # noqa: E402
import cell_recognition as cr  # noqa: E402
import boundary_info as bi  # noqa: E402

V001, V002 = _v2path.V001, _v2path.V002
A_ANCH = ((2, 3, 4, 5, 8, 9), 288)
B_ANCH = ((2, 3, 6, 7, 8, 9), 432)


def check_manifest(root):
    man = json.load(open(os.path.join(root, "MANIFEST.json")))
    for rel, h in man["files"].items():
        with open(os.path.join(root, rel), "rb") as f:
            assert hashlib.sha256(f.read()).hexdigest() == h, rel


class Frozen_Regression(unittest.TestCase):
    def test_v001_files_hash_unchanged(self):
        check_manifest(V001)

    def test_v002_files_hash_unchanged(self):
        check_manifest(V002)

    def test_v002_parent_hash_of_v001_manifest(self):
        man = json.load(open(os.path.join(V002, "MANIFEST.json")))
        h = hashlib.sha256(open(os.path.join(V001, "MANIFEST.json"), "rb").read()).hexdigest()
        self.assertEqual(man["parent"]["MANIFEST.json_sha256"], h)

    def test_v001_and_v002_suites_pass_unchanged(self):
        if os.environ.get("GIG_SKIP_HEAVY"):
            self.skipTest("GIG_SKIP_HEAVY set")
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "GIG_SKIP_HEAVY": "1"}
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.join(V001, "TESTS")], capture_output=True, text=True, cwd=V001, env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-600:])
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", os.path.join(V002, "TESTS")], capture_output=True, text=True, cwd=V002, env=env)
        self.assertEqual(r.returncode, 0, r.stderr[-600:])


class LemmaF_T16_T17(unittest.TestCase):
    def test_lemma_F_all_arrangements(self):
        rnd = random.Random(1)
        for _ in range(12):
            C = tuple(sorted(rnd.sample(range(1, 15), 5)))
            K = tc.threshold_values(C)
            D = bf.denominators(C)
            for i, p in enumerate(hc.perms(5)):
                self.assertEqual(bf.threshold_via_D(C, p, D), K[i])

    def test_feasible_family_chains_equal_simulation(self):
        rnd = random.Random(2)
        for _ in range(8):
            C = tuple(sorted(rnd.sample(range(1, 13), 5)))
            for m in (1, 12, 36, 60, 144, 720, 1260):
                self.assertEqual(bf.admissible_mask_via_chains(C, m), tc.source_mask(C, m))

    def test_T16_product_law_all_faces(self):
        rnd = random.Random(3)
        k = 5
        faces = ft.faces(k)
        for _ in range(6):
            C = tuple(sorted(rnd.sample(range(1, 16), k)))
            for m in (rnd.choice([6, 12, 24, 36, 72, 360, 840]) for _ in range(4)):
                mask = tc.source_mask(C, m)
                for f, d, _ in faces:
                    self.assertEqual(bf.predicted_vertices(C, m, f), bf.actual_vertices(mask, f, k))

    def test_T17_closed_form_vs_vertex_lcm(self):
        rnd = random.Random(4)
        for _ in range(5):
            C = tuple(sorted(rnd.sample(range(1, 14), 6)))
            K = tc.threshold_values(C)
            D = bf.denominators(C)
            for f, d, _ in ft.faces(6):
                self.assertEqual(ft.threshold_by_vertices(C, f, K), ft.threshold_closed_form(C, f, D))

    def test_P6_three_face_grammar(self):
        g = ft.grammar(6, 3)
        self.assertEqual({ft.TYPE_NAME[t]: v["count"] for t, v in g.items()}, {"cube": 90, "hexagonal prism": 360, "truncated octahedron": 90})
        self.assertEqual(sum(v["count"] for v in g.values()), 540)

    def test_face_presence_matches_complex(self):
        C, m = A_ANCH
        mask = tc.source_mask(C, m)
        D = bf.denominators(C)
        fs, vm, dim, _ = hc._complex_data(6)
        for i, f in enumerate(fs):
            self.assertEqual(vm[i] & ~mask == 0, ft.face_present(C, m, f))


class Chain_Complex_And_Anchors(unittest.TestCase):
    def test_boundary_squared_and_anchor_betti(self):
        for C, m in (A_ANCH, B_ANCH):
            cx = cb.Complex(tc.source_mask(C, m), 6)
            self.assertEqual(cx.check_boundary_squared(), 0)
            self.assertEqual(cx.betti(), (1, 0, 1, 0, 0, 0))
            self.assertEqual(bi.invariants(cx.f(), cx.ranks())["beta2"], 1)

    def test_anchor_certificates(self):
        import E10_h2
        for name, (C, m, n) in E10_h2.ANCHORS.items():
            r = E10_h2.anchor(name, C, m, n, write=False)
            self.assertEqual(r["arrangements"], n)
            self.assertTrue(r["z"]["is_cycle"])
            self.assertTrue(r["phi"]["kills_all_3cell_boundaries"])
            self.assertEqual(r["phi"]["phi_of_z"], 1)
            self.assertEqual(len(r["obstructed_3faces_of_P6"]), 6)
            self.assertEqual(sorted(o["K_F_over_gcd_with_source"] for o in r["obstructed_3faces_of_P6"]), sorted([2, 2, 3, 3, 5, 5] if name == "A" else [2, 2, 3, 3, 7, 7]))
            self.assertFalse(any(o["present_in_anchor_complex"] for o in r["obstructed_3faces_of_P6"]))

    def test_anchor_arithmetic_predicate(self):
        for (C, s), P in ((A_ANCH, 30), (B_ANCH, 42)):
            am = tc.source_mask(C, s)
            for m in range(1, 6000):
                self.assertEqual(tc.source_mask(C, m) == am, m % s == 0 and math.gcd(m // s, P) == 1)

    def test_filtration_events_anchor_A(self):
        C, s = A_ANCH
        regs = sf.regimes(C)
        cov = sf.hasse(regs)
        self.assertEqual((len(regs), len(cov)), (55, 115))
        cache = {}
        for i, j in cov:
            ev = sf.transition(C, regs[i], regs[j], cache)
            self.assertTrue(ev["accounting_identity_holds"] and ev["inclusion_holds"])
        h2 = [sf.transition(C, regs[i], regs[j], cache) for i, j in cov]
        self.assertTrue(any(e["delta_betti"][2] == 1 for e in h2) and any(e["delta_betti"][2] == -1 for e in h2))

    def test_birth_vector_rule(self):
        C = (2, 3, 4, 5, 8, 9)
        cc = tc.ContentClosure(C)
        D = bf.denominators(C)
        for f, d, _ in ft.faces(6)[:200]:
            K = ft.threshold_closed_form(C, f, D)
            b = sf.face_birth(C, f, cc)
            for q, e in b.items():
                v = 0
                x = K
                while x % q == 0:
                    x //= q
                    v += 1
                self.assertEqual(v, e)


class Recognition(unittest.TestCase):
    def test_T20b_full_Pk_soundness_k_le_6(self):
        for k in (4, 5, 6):
            full = (1 << math.factorial(k)) - 1
            host = cr.Host(cs.adjacency(full, k))
            for bl in cr.face_types(k, 3):
                raw, conv, exp = cr.rooted_check(k, bl, host)
                self.assertEqual(conv, exp, (k, bl))

    def test_T20c_graph_complex_equals_true_complex(self):
        rnd = random.Random(7)
        for k, L, n in ((4, 20, 40), (5, 12, 40)):
            ms = set()
            for C in combinations(range(1, L + 1), k):
                ms |= tc.realizable_masks_of_content(C)
            for mask in rnd.sample(sorted(ms), min(n, len(ms))):
                g = cr.graph_complex(cs.adjacency(mask, k), k)
                cx = cb.Complex(mask, k)
                self.assertEqual((g["f"], g["ranks"], g["betti"]), (cx.f(), cx.ranks(), cx.betti()))

    def test_T20c_anchors_exact_poset(self):
        import _recovery as R
        for C, m in (A_ANCH, B_ANCH):
            r = R.check((tc.source_mask(C, m), 6))
            self.assertTrue(r["poset_match"] and r["numbers_match"])

    def test_Z1_negative_control(self):
        import E12_recovery as E
        z = E.z1_control()
        self.assertTrue(z["identical_graph_derived_output"])
        self.assertEqual(z["reconstruction_fails_for"], ["A_petrie"])

    def test_T19_difference_identity(self):
        # beta2 = f2 - rank d2 - rank d3 for random arrangement sets
        rnd = random.Random(9)
        P = hc.perms(5)
        for _ in range(25):
            A = {p for p in P if rnd.random() < 0.6}
            if not A:
                continue
            cx = cb.Complex(hc.vertex_mask(A, 5), 5)
            inv = bi.invariants(cx.f(), cx.ranks())
            self.assertEqual(inv["beta2"], cx.betti()[2])


class T12_Erratum(unittest.TestCase):
    def test_empty_intersection_example(self):
        C = (2, 3)
        a2, a3, a1 = (set(tc_perms(C, m)) for m in (2, 3, 1))
        self.assertEqual(a2, {(2, 3)})
        self.assertEqual(a3, {(3, 2)})
        self.assertEqual(a2 & a3, a1)
        self.assertEqual(a1, set())


def tc_perms(C, m):
    mask = tc.source_mask(C, m)
    P = hc.perms(len(C))
    return [tuple(C[r] for r in P[i]) for i in range(len(P)) if mask >> i & 1]


class BoundaryInfo(unittest.TestCase):
    def test_entropy_and_A3(self):
        self.assertAlmostEqual(bi.entropy({"a": 1, "b": 1}), 1.0)
        self.assertEqual(bi.A3([5, 5, 5]), 0.0)
        self.assertAlmostEqual(bi.A3([1, 2, 2, 3, 4]), 2.0)
        self.assertEqual(bi.cond_entropy([(0, 1), (0, 1), (1, 2)]), 0.0)


@unittest.skipUnless(os.environ.get("GIG_FROZEN_SRC"), "set GIG_FROZEN_SRC to cross-check against frozen GEO-HD-1D v004 (read-only)")
class FrozenCrossCheck(unittest.TestCase):
    def test_betti_against_frozen(self):
        sys.path.insert(0, os.environ["GIG_FROZEN_SRC"])
        import route_topology as frt
        rnd = random.Random(5)
        for k in (4, 5):
            P = hc.perms(k)
            for _ in range(40):
                A = {p for p in P if rnd.random() < 0.7}
                self.assertEqual(cb.Complex(hc.vertex_mask(A, k), k).betti(), tuple(frt.betti(A, k)[0]))


class RecordedResults(unittest.TestCase):
    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, "RESULTS", "results.json")), "results.json not generated yet")
    def test_results_consistency(self):
        r = json.load(open(os.path.join(ROOT, "RESULTS", "results.json")))
        self.assertTrue(r["E9"]["P6_3face_reproduced"])
        self.assertEqual(r["E9"]["T16_block_factorization"]["violations"], 0)
        self.assertEqual(r["E9"]["T17_closed_form_vs_vertex_lcm"]["violations"], 0)
        self.assertEqual(r["E9"]["LemmaF_feasible_family"]["violations"], 0)
        for d in r["E12"]["domains"]:
            self.assertEqual(d["failures"], 0)
        self.assertTrue(r["E12"]["T20b_full_permutohedron_soundness"]["all_exact"])
        for name, a in r["E11"]["anchors"].items():
            self.assertTrue(a["accounting_and_inclusion_hold_on_every_cover"])
            self.assertTrue(a["z_fate"]["all_filling_chains_verified"])


if __name__ == "__main__":
    unittest.main()
