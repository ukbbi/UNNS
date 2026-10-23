import hashlib, math, unittest
from pathlib import Path
from src.measure_rep_phase3_v001 import verify_lock,contextual_counterexample,frame2,frame3_raw,generate
class Phase3Tests(unittest.TestCase):
    def test_baseline_lock(self): self.assertTrue(verify_lock())
    def test_two_contexts_normalized(self):
        self.assertTrue(all(abs(sum(c.values())-1)<1e-12 for c in contextual_counterexample().values()))
    def test_shared_event_contextuality(self): self.assertNotEqual(contextual_counterexample()['C']['e'],contextual_counterexample()['D']['e'])
    def test_2d_orthogonal_pair_sum(self):
        for theta in [0,0.13,0.7,2.11]: self.assertAlmostEqual(frame2(theta)+frame2(theta+math.pi/2),1)
    def test_2d_harmonic_nonborn(self):
        # f(0)=0.75, f(pi/3)=0.75, f(pi/6)=0.25;
        # a 2x2 Born quadratic fixed by three such orientations cannot match all 6theta oscillations.
        self.assertAlmostEqual(frame2(0),frame2(math.pi/3))
        self.assertAlmostEqual(frame2(math.pi/6),0.25)
    def test_q2_three_dimensional_frame(self): self.assertAlmostEqual(frame3_raw(2,(1/math.sqrt(3),)*3),1)
    def test_q1_noninvariant(self): self.assertGreater(frame3_raw(1,(1/math.sqrt(3),)*3),1)
    def test_q3_noninvariant(self): self.assertLess(frame3_raw(3,(1/math.sqrt(3),)*3),1)
    def test_no_false_theorem_pass(self): self.assertEqual(generate()['gates']['R5'],'BLOCKED_NOT_DERIVED')
if __name__=='__main__': unittest.main()
