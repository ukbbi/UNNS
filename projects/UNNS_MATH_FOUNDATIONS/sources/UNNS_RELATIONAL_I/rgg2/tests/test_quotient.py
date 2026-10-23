import unittest
from src.anchor_routes import Anchor,fibre
from src.joint_ops import j_join, j_mul
from src.quotient import quotient_witness

class TestQuotient(unittest.TestCase):
    def test_mul_has_no_finite_witness(self):
        routes=[r for m in range(1,181) for r in fibre(m)]
        self.assertIsNone(quotient_witness(routes,j_mul))
    def test_join_has_witness(self):
        routes=[r for m in range(1,101) for r in fibre(m)]
        w=quotient_witness(routes,j_join)
        self.assertIsNotNone(w)
        self.assertNotEqual(*w['outputs'])
    def test_same_input_value_different_join_value(self):
        a,b,s=Anchor(4,2),Anchor(1,4),Anchor(1,4)
        self.assertEqual(a.value,b.value)
        self.assertEqual(j_join(a,s).value,64)
        self.assertEqual(j_join(b,s).value,16)

if __name__=='__main__': unittest.main()
