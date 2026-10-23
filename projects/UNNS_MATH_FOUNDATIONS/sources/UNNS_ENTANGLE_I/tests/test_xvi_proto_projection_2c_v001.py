import math, unittest
from src import xvi_proto_projection_2c_v001 as p
class Phase2CTest(unittest.TestCase):
    def test_lock(self): self.assertTrue(p.lock_ok())
    def test_two_cycle(self): self.assertTrue(p.recurrence_witness())
    def test_short_orbit_not_witness(self): self.assertFalse(p.recurrence_witness(2))
    def test_rotation_preserves_two_cycle(self):
        for t in (0,.4,1.3):
            self.assertAlmostEqual(sum(x*y for x,y in zip(p.projection('A',t),p.projection('B',t))),0,places=12)
    def test_q2_additivity(self):
        for t in (0,.4,1.3):
            for s in (.5,1,2): self.assertAlmostEqual(p.defect(2,t,s),0,places=12)
    def test_q1_nonadditive(self): self.assertLess(p.defect(1),-.5)
    def test_q3_nonadditive(self): self.assertGreater(p.defect(3),.8)
    def test_no_primary_pass(self): self.assertEqual(p.report()['primary_theorem'],'OPEN_NOT_DERIVED')
    def test_reject_invalid(self):
        with self.assertRaises(ValueError): p.projection('C')
        with self.assertRaises(ValueError): p.weight((1,0),0)
if __name__=='__main__': unittest.main()
