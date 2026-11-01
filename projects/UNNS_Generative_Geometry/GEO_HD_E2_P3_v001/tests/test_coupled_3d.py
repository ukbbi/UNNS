import unittest
from fractions import Fraction as Fr
import _path  # noqa
import coverage_gap as cg
import coupled_3d as c3


class Test3D(unittest.TestCase):
    def test_control_c(self):
        tr = cg.transition(Fr(2 * 110 ** 4, 3))
        self.assertEqual((tr["P"], tr["q"], tr["b"], tr["b2"]), ((2, 5, 11), (2, 2, 2), 3, 1))
        row = {"primes": list(tr["P"]), "box": list(tr["q"]), "x": str(tr["x"]), "x_next": str(tr["x2"]), "b": 3, "b_next": 1,
               "relation": "ENLARGE", "index_source": 2, "index_target": 1}
        o = c3.evaluate_3d(row)
        self.assertEqual(o["verdict"], "NOT_CONTAINED")
        self.assertTrue(o["essentiality"]["full_support"])
        self.assertTrue(o["essentiality"]["irreducible_to_faces"])
        self.assertFalse(o["both_nontrivial"])             # target lattice is Z^3: not a nontrivial-nontrivial specimen

    def test_predictor_matches_engine_on_control(self):
        tr = cg.transition(Fr(2 * 110 ** 4, 3))
        p = c3.corner_cube_predict(tr["P"], tr["q"], tr["b"], tr["b2"])
        self.assertEqual(p["verdict"], "NOT_CONTAINED")
        self.assertEqual(p["witness"], ["2/3", "2/3", "2/3"])

    def test_short_vector_screen_sound_on_control(self):
        tr = cg.transition(Fr(2 * 110 ** 4, 3))
        self.assertTrue(c3.short_vector_screen(tr["P"], tr["q"], tr["b"], tr["b2"]))

    def test_fast_predictor_equals_full_on_rectangular_rows(self):
        import planar_residual as pr
        rows, sk, _ = pr.sweep([2, 3, 5, 7, 11], 2, 40, 3, odd=True)
        n = 0
        for r in rows:
            P, q, b, b2 = tuple(r["primes"]), tuple(r["box"]), r["b"], r["b_next"]
            if not c3.rectangular_data(P, b2, q):
                continue
            f = c3.corner_cube_predict(P, q, b, b2)
            g = c3.corner_cube_predict_full(P, q, b, b2)
            self.assertEqual(f["verdict"], g["verdict"])
            if g["verdict"] != "UNAVAILABLE":
                o = c3.evaluate_3d(r)
                self.assertEqual(o["verdict"], g["verdict"])
            n += 1
        self.assertGreater(n, 5)

    def test_even_sum_family_rule(self):
        # P3-T3(h): even-sum lattice fails exactly when max(box) >= 2  (target Z^3)
        import exact_containment as ec
        from itertools import product
        E3 = lambda v: sum(v) % 2 == 0
        for q in product((1, 2), repeat=3):
            F = [v for v in product(*[range(m + 1) for m in q]) if any(v) and E3(v)]
            L = [v for v in product(*[range(-m, m + 1) for m in q]) if any(v) and E3(v)]
            G = [v for v in L if not any(w != v and all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(w, v)) for w in L)]
            Go = c3.ft.oriented(G)
            cx = c3.cg.ct0.build_complex(tuple(F), Go, 3)
            cells = [(tuple(c.base), tuple(tuple(g) for g in c.gens)) for j in cx for c in cx[j].values()]
            Fz = [v for v in product(*[range(m + 1) for m in q]) if any(v)]
            cz = c3.cg.ct0.build_complex(tuple(Fz), c3.ft.oriented([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]), 3)
            cellsz = [(tuple(c.base), tuple(tuple(g) for g in c.gens)) for j in cz for c in cz[j].values()]
            r = ec.decide_union(cells, cellsz, 3)
            self.assertEqual(r["verdict"] == "NOT_CONTAINED", max(q) >= 2, q)

    def test_max_slack(self):
        # cell with vertices (1,0,1),(0,1,1),(1,1,0),(2,1,0)... use E2-P1 cell
        r = c3.max_slack((0, 0, 2), [(0, 1, -1), (1, 0, -1)], (1, 1, 1))
        self.assertGreater(r[0], 0)
        r = c3.max_slack((1, 1, 1), [(1, 0, 0)], (1, 1, 1))
        self.assertLessEqual(r[0], 0)


if __name__ == "__main__":
    unittest.main()
