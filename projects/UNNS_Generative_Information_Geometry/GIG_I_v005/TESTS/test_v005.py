import json, os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "EXPERIMENTS"))
import _path
import filling as F
import hole_survival as H

ROOT = _path.ROOT
FAM = json.load(open(os.path.join(ROOT, "RESULTS", "E19_bounding_lattice.json")))["minimal_bounding_families"]
mask = lambda fam: sum(1 << F.BIT[s] for s in fam)


class T(unittest.TestCase):
    def test_extra_sets(self):
        self.assertEqual(len(F.EXTRA), 20)
        self.assertEqual(len(F.FACES3), 540)

    def test_minimal_families_are_minimal_bounding(self):
        self.assertEqual(len(FAM), 4)
        for f in FAM:
            S = mask(f)
            self.assertTrue(F.bounds(S))
            for s in f:
                self.assertFalse(F.bounds(S & ~(1 << F.BIT[s])), (f, s))

    def test_gate_sets_are_inside_families(self):
        gs = H.gate_sets()
        self.assertTrue(set(gs[0]) <= set(FAM[0]))
        self.assertTrue(all(set(gs[1]) <= set(f) for f in FAM[1:2]))
        self.assertTrue(all(set(gs[3]) <= set(f) for f in FAM[2:]))

    def test_gate0_necessity_and_sufficient_filling_absent_for_1_3(self):
        self.assertTrue(F.bounds(1 << F.BIT[21]))
        self.assertFalse(F.bounds(mask([34, 38])))
        self.assertFalse(F.bounds(mask([8, 24, 40, 56])))

    def test_ps1_is_corollary(self):
        # every minimal family contains a complete gate set, so 'all gates closed' excludes every family
        gs = H.gate_sets()
        for f in FAM:
            self.assertTrue(any(set(g) <= set(f) for g in gs.values()))

    def test_counterexamples(self):
        import E20_gate_counterexamples as E
        for a in (1, 3):
            d = json.load(open(os.path.join(ROOT, "CERTIFICATES", "gate%d_counterexample.json" % a)))
            v = E.verify(d["labels"], d["m"])
            self.assertTrue(v["z_present"] and not v["z_bounds"] and v["phi_verified"])
            self.assertEqual(sorted(d["labels"]), d["labels"])
            self.assertEqual(len(set(d["labels"])), 6)
            gs = H.gate_sets()[a]
            from math import lcm
            import block_factor as bf
            D = bf.denominators(d["labels"])
            self.assertTrue(all(d["m"] % D[I] == 0 for I in gs))      # the gate is OPEN
            self.assertTrue(d["m"] % D[21] != 0)

    def test_exact_criterion_matches_engine_on_sample(self):
        from itertools import combinations
        from math import lcm
        import block_factor as bf
        n = 0
        for lab in list(combinations(range(2, 11), 6))[:40]:
            D = bf.denominators(list(lab))
            Kz = lcm(*[D[I] for I in H.PZ])
            for m in (Kz, 2 * Kz, 6 * Kz, 30 * Kz):
                A = sum(1 << F.BIT[I] for I in F.EXTRA if m % D[I] == 0)
                if H.survives_gates(list(lab), m):
                    self.assertFalse(F.bounds(A))   # PS-1 sufficient direction
                n += 1
        self.assertGreater(n, 100)


if __name__ == "__main__":
    unittest.main()
