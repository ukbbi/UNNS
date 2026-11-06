import itertools, json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "EXPERIMENTS"))
import _path
import hole_survival as H, lift as Lf, fi, cert
from pk import PK
from E30_arith import denominators
ROOT = _path.ROOT
P6, P7 = PK(6), PK(7)
z6 = P6.bits(H.Z)
f6, _ = P6.minimal_families(z6, 2)
P = P6.pz(z6)
ch = [set(Lf.filling_chain(P6, z6, P | F)) for F in f6]


def L(a, b):
    zf = Lf.lam_faces([P6.FS[g] for g in H.Z], 6) ^ Lf.first([P6.FS[g] for g in ch[a]], 6) ^ Lf.last([P6.FS[g] for g in ch[b]], 6)
    return P7.bits([P7.IDX[f] for f in zf])


class T(unittest.TestCase):
    def test_fi1_chain_identities(self):
        for a, a2, b in itertools.product(range(4), repeat=3):
            d = P6.bits(ch[a] ^ ch[a2])
            self.assertEqual(L(a, b) ^ L(a2, b), fi.embed(P6, P7, d, "first"))
            self.assertEqual(L(b, a) ^ L(b, a2), fi.embed(P6, P7, d, "last"))

    def test_fi3_bridge_first_last(self):
        # d(Lam(d)) = first(d) + last(d) for the 3-cycle d = c_0 + c_3 (LT-0 applied in P_7 to a 3-cycle)
        d = P6.bits(ch[0] ^ ch[3])
        lam = fi.embed(P6, P7, d, "lam")
        acc = 0
        for g in fi.ids_of(lam):
            for b in P7.BND[g]:
                acc ^= 1 << b
        self.assertEqual(acc, fi.embed(P6, P7, d, "first") ^ fi.embed(P6, P7, d, "last"))

    def test_inter_family_classification(self):
        for (i, j), selfb in {(0, 1): True, (0, 2): True, (1, 3): True, (2, 3): True, (0, 3): False, (1, 2): False}.items():
            e = fi.embed(P6, P7, P6.bits(ch[i] ^ ch[j]), "first")
            self.assertEqual(P7.bounds(e, P7.pz(e), 3), selfb)
        e = fi.embed(P6, P7, P6.bits(ch[0] ^ ch[3]), "first")
        self.assertTrue(P7.bounds(e, P7.pz(e) | (1 << 89), 3))
        self.assertTrue(P7.bounds(e, P7.pz(e) | (1 << 102), 3))

    def test_intra_family_basis_self_bounding(self):
        for i in (0, 1):
            for d in fi.cycle_basis(P6, P | f6[i], 3):
                e = fi.embed(P6, P7, d, "first")
                self.assertTrue(P7.bounds(e, P7.pz(e), 3))

    def test_dependence_example_full_complex(self):
        C, K = [2, 3, 8, 9, 14, 15, 20], 33600
        D = denominators(C)
        A = sum(1 << s for s in range(1, 128) if K % D[s] == 0)
        l1, l2 = L(1, 0), L(2, 0)
        self.assertTrue(P7.is_cycle(l1) and P7.is_cycle(l2))
        self.assertFalse(P7.pz(l1) & ~A or P7.pz(l2) & ~A)
        B = fi.Bounder(P7, A, 3)
        self.assertFalse(B.contains(l1))
        self.assertFalse(B.contains(l2))
        self.assertFalse(B.contains(l1 ^ l2))

    def test_role_map_correction(self):
        r = json.load(open(os.path.join(ROOT, "RESULTS", "E36_role_map_correction.json")))
        for c in r["contents"]:
            self.assertFalse(c["identity_image_has_regime"])
            self.assertEqual(c["images_with_H2_regime"], 18)

    def test_h4_certificate(self):
        c = json.load(open(os.path.join(ROOT, "CERTIFICATES", "h4_certificate_first_hit.json")))
        P8 = PK(8)
        tf = lambda f: tuple(tuple(b) for b in f)
        z = P8.bits([P8.IDX[tf(f)] for f in c["cycle"]])
        phi = [P8.IDX[tf(f)] for f in c["cochain"]]
        D = denominators(c["content"])
        K = int(c["m"])
        A = sum(1 << s for s in range(1, 256) if K % D[s] == 0)
        ok, msg = cert.verify_certificate(P8, A, 4, z, phi)
        self.assertTrue(ok, msg)
        self.assertEqual(len(phi), 6)


if __name__ == "__main__":
    unittest.main()
