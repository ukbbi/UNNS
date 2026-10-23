import unittest
from src.anchor_routes import Anchor, fibre, from_occurrence
from src.joint_ops import j_join, j_mul

class TestJoin(unittest.TestCase):
    def test_anchor_occurrence_roundtrip(self):
        for k in range(1,11):
            for d in range(2,11):
                r=Anchor(k,d)
                self.assertEqual(from_occurrence(*r.occurrence),r)
                self.assertEqual(r.value, r.occurrence[0]*(r.occurrence[1]+1)**2//r.occurrence[1])
    def test_fibre72(self):
        self.assertEqual(set(fibre(72)),{Anchor(18,2),Anchor(8,3),Anchor(2,6)})
    def test_semilattice_laws(self):
        A=[Anchor(k,d) for k in range(1,7) for d in range(2,7)]
        for a in A:
            self.assertEqual(j_join(a,a),a)
            for b in A:
                self.assertEqual(j_join(a,b),j_join(b,a))
                for c in A[:6]:
                    self.assertEqual(j_join(j_join(a,b),c),j_join(a,j_join(b,c)))
    def test_value_homomorphism_only_for_multiplication(self):
        a,b=Anchor(4,2),Anchor(1,4)
        self.assertEqual(a.value,b.value)
        self.assertEqual(j_mul(a,b).value,a.value*b.value)
        self.assertNotEqual(j_join(a,b).value,a.value)

if __name__=='__main__': unittest.main()
