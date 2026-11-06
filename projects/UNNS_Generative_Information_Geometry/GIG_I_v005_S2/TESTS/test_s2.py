import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import atlas as A
import hole_survival as H
import cell_boundary as cb
import threshold_closure as tc
import E23_families as E23
ROOT = _path.ROOT


class T(unittest.TestCase):
    def test_dualisation_reproduces_stage1(self):
        zb = sum(1 << g for g in H.Z)
        fams, st = A.minimal_families(zb)
        got = sorted(sorted(s for s in range(64) if f >> s & 1) for f in fams)
        self.assertEqual(got, sorted(json.load(open(os.path.join(_path._vpath.V005, "RESULTS", "E19_bounding_lattice.json")))["minimal_bounding_families"]))
        self.assertEqual(st["q"], 20)

    def test_dualisation_vs_brute_force_small_q(self):
        classes = json.load(open(os.path.join(ROOT, "CERTIFICATES", "atlas_v2_classes.json")))
        done = 0
        for c in classes:
            zb = int(c["cycle_bits"])
            P = A.pz(zb)
            U = [s for s in range(1, 64) if not P >> s & 1]
            if len(U) > 14:
                continue
            fams = sorted(int(f) for f in c["families"])
            true = [sum(1 << U[i] for i in range(len(U)) if S >> i & 1) for S in range(1 << len(U))]
            tr = [S for S in true if A.bounds(zb, P | S)]
            mins = sorted(S for S in tr if not any(T != S and T & S == T for T in tr))
            self.assertEqual(mins, fams)
            done += 1
            if done == 2:
                break
        self.assertEqual(done, 2)

    def test_all_158_regime_certificates(self):
        certs = json.load(open(os.path.join(ROOT, "CERTIFICATES", "regime_certificates.json")))
        self.assertEqual(len(certs), 158)
        nb = 0
        for r in certs:
            cx = cb.Complex(tc.source_mask(tuple(r["content"]), r["L"]), 6)
            self.assertEqual(cx.betti()[2], r["beta2"])
            L2 = cx.dims[2]
            pos = {g: j for j, g in enumerate(L2)}
            for b in r["basis"]:
                z = sum(1 << pos[g] for g in b["z_faces"])
                phi = sum(1 << pos[g] for g in b["phi_faces"])
                v = cb.verify_cocycle(cx, 2, z, phi)
                self.assertTrue(v["z_is_cycle"] and v["phi_of_z"] == 1 and v["phi_kills_all_boundaries"])
                nb += 1
        self.assertEqual(nb, 160)

    def test_coverage_numbers(self):
        o = json.load(open(os.path.join(ROOT, "RESULTS", "E27_assignment.json")))
        self.assertEqual((o["regimes"], o["covered"], o["regimes_106_unexplained"], o["of_which_covered"]), (158, 158, 106, 106))
        self.assertEqual(o["v2_classes"], 32)

    def test_atlas_soundness_on_sample(self):
        import E24_atlas_coverage as E24
        regimes, classes = E24.law_classes()
        for r in regimes[:30]:
            cx = cb.Complex(tc.source_mask(tuple(r["content"]), r["L"]), 6)
            Af = E23.adm_family(tuple(r["content"]), r["L"])
            self.assertTrue(E24.predict(classes, Af))
            self.assertGreater(cx.betti()[2], 0)

    def test_heldout_records(self):
        e = json.load(open(os.path.join(ROOT, "RESULTS", "E24_atlas_coverage.json")))["heldout"]
        self.assertEqual(e["n_false_positive"], 0)
        e2 = json.load(open(os.path.join(ROOT, "RESULTS", "E25_refine.json")))
        self.assertEqual(e2["fresh_heldout_v2"]["n_false_positive"], 0)
        self.assertEqual(e2["fresh_heldout_v1"]["n_false_positive"], 0)


if __name__ == "__main__":
    unittest.main()
