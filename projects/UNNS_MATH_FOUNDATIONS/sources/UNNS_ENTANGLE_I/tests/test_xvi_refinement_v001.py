import hashlib,unittest
from pathlib import Path
from src.xvi_refinement_v001 import defect, report

ROOT=Path(__file__).resolve().parents[1]
class Phase2Audit(unittest.TestCase):
    def test_baseline_lock(self): self.assertTrue(report(ROOT)['phase1_integrity_pass'])
    def test_not_canonical(self): self.assertFalse(report(ROOT)['canonical_operator_evaluated'])
    def test_q2_zero(self):
        for x,y in [(1,1),(2,3),(.1,.8)]: self.assertAlmostEqual(defect(2,x,y),0,places=12)
    def test_q1_counterexample(self): self.assertLess(defect(1,1,1),0)
    def test_q3_counterexample(self): self.assertGreater(defect(3,1,1),0)
    def test_invalid_power(self):
        with self.assertRaises(ValueError): defect(0,1,1)
if __name__=='__main__': unittest.main()
