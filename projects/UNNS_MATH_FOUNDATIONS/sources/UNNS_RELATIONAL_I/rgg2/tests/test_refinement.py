import unittest
from src.anchor_routes import Anchor
from src.joint_ops import j_join
from src.refinement import t,simultaneous_covariance

class TestRefinement(unittest.TestCase):
    def test_partial_domain(self):
        self.assertIsNone(t(2,Anchor(1,2)))
        self.assertEqual(t(2,Anchor(4,2)),Anchor(1,4))
    def test_value_preservation(self):
        for k in range(1,55):
            for d in range(2,12):
                for q in (2,3):
                    r=Anchor(k,d); rr=t(q,r)
                    if rr is not None:self.assertEqual(rr.value,r.value)
    def test_joint_covariance(self):
        for k in (4,8,12,16,36):
            for kk in (4,12,36):
                for d in (2,3,5):
                    for dd in (2,4,7):
                        self.assertTrue(simultaneous_covariance(2,Anchor(k,d),Anchor(kk,dd)))
    def test_independent_value_change(self):
        r,s=Anchor(4,2),Anchor(1,4)
        self.assertNotEqual(j_join(r,s).value,j_join(t(2,r),s).value)
        self.assertEqual(j_join(t(2,r),s).value,16)

if __name__=='__main__': unittest.main()
