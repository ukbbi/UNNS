import math
import unittest
from src.xvi_proto_measure_2b_v001 import orbit,proto_closed,projection,weight,defect,verify_baselines,build_report

class Phase2BAudit(unittest.TestCase):
    def test_period_two_is_nontrivial(self): self.assertEqual(orbit(6),('A','B','A','B','A','B'))
    def test_proto_closed(self): self.assertTrue(proto_closed())
    def test_invalid_witness(self):
        with self.assertRaises(ValueError): proto_closed(2)
    def test_weights_constant_all_q(self):
        for q in (1,1.5,2,3,6): self.assertEqual(weight(projection('A'),q),weight(projection('B'),q))
    def test_q2_additivity(self): self.assertAlmostEqual(defect(2),0,places=12)
    def test_q1_q3_counterexamples(self):
        self.assertLess(defect(1),0)
        self.assertGreater(defect(3),0)
    def test_exact_q_formula(self):
        for q in (1,1.5,2,3,6): self.assertAlmostEqual(defect(q),2**(q/2)-2,places=12)
    def test_lock_integrity(self): self.assertTrue(all(x['pass'] for x in verify_baselines().values()))
    def test_unproved_theorem_flagged(self):
        r=build_report();self.assertFalse(r['canonical_operator_evaluated']);self.assertEqual(r['primary_theorem'],'OPEN_B3_NOT_DERIVED')
if __name__=='__main__': unittest.main()
