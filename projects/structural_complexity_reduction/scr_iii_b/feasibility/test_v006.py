#!/usr/bin/env python3
"""Unit tests for the v006 feasibility modules. Run: python3 scr_iii_b/feasibility/test_v006.py"""
import sys
sys.dont_write_bytecode = True
import pathlib, unittest
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import energy_windows_v006 as ew
import grammar_nulls_v006 as gn

pe = ew.load_v005()


def patch(L):
    isl, pairs, vpos = ew.build_patch(pe, L)
    inc, roles = ew.build_incidence(pe, isl, vpos)
    return isl, pairs, vpos, inc, roles, len(isl)


class T(unittest.TestCase):
    def test_grammar_counts(self):
        for L, g in ((1, 6), (2, 82)):
            isl, pairs, vpos, inc, roles, n = patch(L)
            self.assertEqual(sum(ew.grammar_set(n, ew.compile_masks(inc))), g)

    def test_grammar_equals_geometric_rule_and_typing(self):
        isl, pairs, vpos, inc, roles, n = patch(2)
        surv = ew.grammar_set(n, ew.compile_masks(inc))
        for s in range(0, 1 << n, 7):
            st = pe.decode(s, n)
            self.assertEqual(surv[s], pe.ice_ok_geometric(st, isl, vpos))
            self.assertEqual(surv[s], all(t in (1, 2) for t in ew.vertex_types(s, inc, roles)))

    def test_incidence_arity_and_islands(self):
        for L in (1, 2, 3):
            isl, pairs, vpos, inc, roles, n = patch(L) if L < 3 else (pe.source_geometry(3), None, pe.vertex_positions(3), None, None, 24)
            if inc is None:
                inc, _ = ew.build_incidence(pe, isl, vpos)
            self.assertTrue(all(len(e) == 4 and len({i for i, _ in e}) == 4 for e in inc))

    def test_levels_and_windows(self):
        isl, pairs, vpos, inc, roles, n = patch(1)
        En = [pe.energy_norm(pe.decode(s, n), pairs) for s in range(1 << n)]
        lv, levels, gap, sc = ew.group_levels(En)
        self.assertEqual(sum(len(l["members"]) for l in levels), 1 << n)
        self.assertEqual(len(levels[0]["members"]), 2)
        surv = ew.grammar_set(n, ew.compile_masks(inc))
        fns = [ew.window_metrics(n, lv, len(levels), surv, k)["false_exclusions"] for k in range(len(levels))]
        self.assertEqual(fns[0], 0); self.assertEqual(fns[1], 0); self.assertGreater(fns[2], 0)
        self.assertEqual(fns, sorted(fns))

    def test_constructive_equals_bruteforce(self):
        for L in (1, 2):
            isl, pairs, vpos, inc, roles, n = patch(L)
            S, nodes = ew.constructive_enumerate(inc, n)
            surv = ew.grammar_set(n, ew.compile_masks(inc))
            self.assertEqual(S, {s for s in range(1 << n) if surv[s]})
            self.assertLess(nodes, (1 << (n + 1)))

    def test_null_controls(self):
        isl, pairs, vpos, inc, roles, n = patch(2)
        real = gn.survivors(n, inc)
        self.assertEqual(gn.survivors(n, gn.unchanged_control(inc)), real)
        self.assertNotEqual(gn.survivors(n, gn.perturbed_control(inc)), real)

    def test_swap_preserves_degrees_and_arity(self):
        isl, pairs, vpos, inc, roles, n = patch(2)
        prof = gn.degree_profile(inc)
        for idx in range(20):
            nb, att, rej = gn.swap_null(inc, gn.rng_for("t", idx))
            self.assertEqual(gn.degree_profile(nb), prof)
            self.assertTrue(gn.valid_structure(nb, inc)[0])

    def test_seed_determinism(self):
        isl, pairs, vpos, inc, roles, n = patch(2)
        a, _ = gn.generate("DEGREE_PRESERVING_SWAP", inc, n, 5)
        b, _ = gn.generate("DEGREE_PRESERVING_SWAP", inc, n, 5)
        self.assertEqual([x["inc"] for x in a], [x["inc"] for x in b])

    def test_1x1_has_no_degree_preserving_rewiring(self):
        isl, pairs, vpos, inc, roles, n = patch(1)
        nulls, log = gn.generate("DEGREE_PRESERVING_SWAP", inc, n, 3, max_tries=10)
        self.assertEqual(len(nulls), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
