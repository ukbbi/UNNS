import unittest
from itertools import combinations
from src.anchor_routes import Anchor, fibre
from src.joint_ops import j_join

class TestSeparation(unittest.TestCase):
    def test_all_nontrivial_fibres_upto_2000(self):
        count=0
        for m in range(1,2001):
            for r,s in combinations(fibre(m),2):
                self.assertGreater(j_join(r,s).value,m)
                self.assertEqual(j_join(r,r).value,m)
                self.assertNotEqual(j_join(s,r).value,j_join(r,r).value)
                count+=1
        self.assertGreater(count,0)
    def test_72_exact_pair_lifts(self):
        a,b,c=Anchor(18,2),Anchor(8,3),Anchor(2,6)
        self.assertEqual([j_join(a,b).value,j_join(a,c).value,j_join(b,c).value], [2592,648,288])
    def test_identity_does_not_imply_value_only_interaction(self):
        a,b,s=Anchor(4,2),Anchor(1,4),Anchor(1,4)
        self.assertEqual(a.value,b.value)
        self.assertNotEqual(j_join(a,s).value,j_join(b,s).value)

if __name__=='__main__': unittest.main()
