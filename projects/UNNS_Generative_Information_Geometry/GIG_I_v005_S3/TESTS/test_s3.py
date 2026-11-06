import json, os, random, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import lift as Lf
from pk import PK, verify_family_certificate
ROOT = _path.ROOT
P6, P7 = PK(6), PK(7)
LP = json.load(open(os.path.join(ROOT, "CERTIFICATES", "lift_pairs.json")))


def bd7(ids):
    acc = set()
    for g in ids:
        for b in P7.BND[g]:
            acc ^= {b}
    return acc


class T(unittest.TestCase):
    def test_boundary_lemma_all_faces_of_P6(self):
        # d Ins_i(f) summed over i  =  Ins(d f) + first(f) + last(f)   (mod 2) for EVERY face f of P_6 of dimension >= 1
        for g, f in enumerate(P6.FS):
            if P6.DIM[g] < 1:
                continue
            lhs = set()
            for i in range(len(f)):
                lhs ^= bd7([P7.IDX[Lf.ins(f, i, 6)]])
            rhs = set()
            for b in P6.BND[g]:
                for i in range(len(P6.FS[b])):
                    rhs ^= {P7.IDX[Lf.ins(P6.FS[b], i, 6)]}
            rhs ^= {P7.IDX[((6,),) + f], P7.IDX[f + ((6,),)]}
            self.assertEqual(lhs, rhs)

    def test_all_pairs_are_cycles_with_phi_one(self):
        import hole_survival as H
        phi3 = P7.bits([P7.IDX[Lf.ins(P6.FS[g], 0, 6)] for g in H.PHI])
        self.assertEqual(len(LP["pairs"]), 16)
        for p in LP["pairs"]:
            z = P7.bits(p["z3_faces"])
            self.assertTrue(P7.is_cycle(z))
            self.assertEqual(bin(z & phi3).count("1") & 1, 1)
        self.assertEqual(len(P7.obstructed(phi3, 3)), 6)

    def test_diagonal_lifts_are_boundaries(self):
        import hole_survival as H
        z6 = P6.bits(H.Z)
        fams, _ = P6.minimal_families(z6, 2)
        P = P6.pz(z6)
        for a in range(4):
            c = Lf.filling_chain(P6, z6, P | fams[a])
            cf = [P6.FS[g] for g in c]
            d4 = set()
            for f in cf:
                for i in range(len(f)):
                    d4 ^= {P7.IDX[Lf.ins(f, i, 6)]}
            z3 = set(next(p for p in LP["pairs"] if p["a"] == a and p["b"] == a)["z3_faces"])
            self.assertEqual(bd7(d4), z3)
            for g in d4:                       # every 4-face of Lam(c) has its prefix sets inside P_{z3}
                self.assertEqual(P7.PM[g] & ~P7.pz(P7.bits(z3)), 0)

    def test_completeness_certificates(self):
        for p in [q for q in LP["pairs"] if not q["diagonal"]][:3]:
            z = P7.bits(p["z3_faces"])
            fams = [sum(1 << s for s in f) for f in p["families"]]
            mf = [sum(1 << s for s in f) for f in p["maximal_false_sets"]]
            ok, msg = verify_family_certificate(P7, z, 3, fams, mf)
            self.assertTrue(ok, msg)

    def test_h3_certificates(self):
        E = json.load(open(os.path.join(ROOT, "RESULTS", "E28_h3_certificates.json")))
        for k in ("H3-1", "H3-2", "H3-3", "H3-4"):
            r = E[k]
            self.assertTrue(r["z3_is_cycle_in_P7"] and r["phi3_of_z3"] == 1 and len(r["obstructed_4faces_of_P7"]) == 6)
            rc = r["regime_complex"]
            self.assertEqual((rc["betti"][3], rc["phi_of_z"], rc["z_is_cycle"], rc["phi_kills_all_boundaries"]), (1, 1, True, True))
            self.assertTrue(r["lifted_pair"]["z3cert_plus_lift_is_boundary"])

    def test_regime_verification_record(self):
        E = json.load(open(os.path.join(ROOT, "RESULTS", "E31_verify_regimes_L30.json")))
        self.assertEqual((E["positives"], E["positives_ok"], E["negatives"], E["negatives_ok"], E["failures"]), (214, 214, 100, 100, []))

    def test_census_sample_reproducible(self):
        import E30_arithmetic_census as E30
        R = json.load(open(os.path.join(ROOT, "RESULTS", "E30_arithmetic_census_L30.json")))
        pat = {"%d%d" % (p["a"], p["b"]): p for p in E30.PAIRS}
        for r in R["records"][:12]:
            D = E30.denominators(r["content"])
            for name, K in r["patterns"]:
                ok, K2 = E30.exists(D, pat[name]["Pset"], pat[name]["fam_masks"])
                self.assertTrue(ok)
                self.assertEqual(str(K2), K)

    def test_all_classes_lift(self):
        E = json.load(open(os.path.join(ROOT, "RESULTS", "E32_lift_all_classes.json")))["summary"]
        self.assertEqual((E["classes"], E["offdiag_pairs"], E["offdiag_nondegenerate"], E["diagonal_always_degenerate"]), (32, 554, 554, True))


if __name__ == "__main__":
    unittest.main()
