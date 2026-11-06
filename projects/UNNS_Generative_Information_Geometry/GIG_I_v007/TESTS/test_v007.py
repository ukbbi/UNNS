import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import jmap
from pk import PK
from E30_arith import denominators
ROOT = _path.ROOT
P5, P6, P7 = PK(5), PK(6), PK(7)
am = lambda D, m, n: sum(1 << s for s in range(1, n) if m % D[s] == 0)


class T(unittest.TestCase):
    def test_first_last_chain_maps(self):
        for Pk, Pk1 in ((P5, P6), (P6, P7)):
            for g, f in enumerate(Pk.FS):
                for kind in ("first", "last"):
                    m = (lambda x: ((Pk.k,),) + x) if kind == "first" else (lambda x: x + ((Pk.k,),))
                    lhs = 0
                    for b in Pk1.BND[Pk1.IDX[m(f)]]:
                        lhs ^= 1 << b
                    rhs = 0
                    for b in Pk.BND[g]:
                        rhs ^= 1 << Pk1.IDX[m(Pk.FS[b])]
                    self.assertEqual(lhs, rhs)

    def test_rho_chain_map_and_left_inverse(self):
        r = 6
        def rho(g):
            f = P7.FS[g]
            if (r,) in f:
                h = tuple(b for b in f if b != (r,))
                return P6.IDX[h] if h else None
        for g in range(len(P7.FS)):
            lhs = 0
            for b in P7.BND[g]:
                x = rho(b)
                if x is not None:
                    lhs ^= 1 << x
            x = rho(g)
            rhs = 0
            if x is not None:
                for b in P6.BND[x]:
                    rhs ^= 1 << b
            self.assertEqual(lhs, rhs)
        for f in range(len(P6.FS)):
            self.assertEqual(rho(P7.IDX[((r,),) + P6.FS[f]]), f)

    def test_witness_r_fill_one(self):
        for C, K in (([2, 3, 8, 9, 14, 15, 20], 33600), ([3, 8, 9, 14, 15, 20, 21], 793800)):
            r = jmap.J_rank(P6, P7, am(denominators(C), K, 128), 3)
            self.assertEqual((r["dim_V"], r["r_fill"], r["beta_facet"]), (37, 1, 1))

    def test_census_file_consistent(self):
        e = json.load(open(os.path.join(ROOT, "RESULTS", "E44_sandwich_and_second_lift.json")))
        self.assertTrue(e["sandwich_valid"])
        self.assertEqual(e["sandwich_(lower,r_fill,beta)_hist"], {"(0, 0, 0)": 298, "(1, 1, 1)": 12})
        self.assertTrue(all(x["first"]["r_fill"] == 0 and x["last"]["r_fill"] == 0 for x in e["second_lift"]))

    def test_E42_matches(self):
        e = json.load(open(os.path.join(ROOT, "RESULTS", "E42_facet_theorem.json")))
        self.assertEqual(e["violations_of_r<=beta_facet"], 0)
        self.assertEqual(e["instances"], 310)


if __name__ == "__main__":
    unittest.main()
