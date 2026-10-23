import unittest
from src.anchor_routes import Anchor
from src.joint_ops import j_gcd,j_mixed,j_blind,j_join,j_mul

class TestAdversarial(unittest.TestCase):
    def test_gcd_partial_domain(self):
        self.assertIsNone(j_gcd(Anchor(2,2),Anchor(3,3)))
        self.assertEqual(j_gcd(Anchor(6,4),Anchor(9,6)),Anchor(3,2))
    def test_mixed_partial_domain(self):
        self.assertIsNone(j_mixed(Anchor(2,2),Anchor(3,3)))
        self.assertEqual(j_mixed(Anchor(6,4),Anchor(9,6)),Anchor(18,2))
    def test_join_vs_mul_not_same_rule(self):
        a=Anchor(3,2)
        self.assertEqual(j_join(a,a),a)
        self.assertNotEqual(j_mul(a,a),a)
    def test_blind_is_not_an_explanation_of_join(self):
        r,s=Anchor(4,2),Anchor(1,4)
        self.assertTrue(j_mul(r,s) in j_blind(r,s))
        self.assertNotIn(j_join(r,s),j_blind(r,s))
    def test_blind_output_set_never_singleton_on_anchor_inputs(self):
        for k in range(1,6):
            for d in range(2,7):
                self.assertGreater(len(j_blind(Anchor(k,d), Anchor(1,2))),1)

if __name__=='__main__': unittest.main()
