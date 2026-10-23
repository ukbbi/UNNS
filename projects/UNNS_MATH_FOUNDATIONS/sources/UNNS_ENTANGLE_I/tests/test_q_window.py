import math,sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from q_window import ANGLES, probs, correl, chsh, raw_weight

class TestPhase0(unittest.TestCase):
 def test_probabilities(self):
  for q in [0.1,1,1.5,2,3,6,20]:
   for a,b in [(0,.13),(.43,.27),(0,math.pi/4)]:
    p=probs(q,a,b)
    self.assertAlmostEqual(float(p.sum()),1.,places=12)
    self.assertTrue(np.all(p >= 0))
 def test_no_signalling(self):
  for q in [0.3,1,1.5,2,3,6,10]:
   for a in [.1,.3,.5]:
    for b in [.2,.45,1.]:
     p=probs(q,a,b)
     np.testing.assert_allclose(p.sum(axis=0), [.5,.5],atol=1e-14)
     np.testing.assert_allclose(p.sum(axis=1), [.5,.5],atol=1e-14)
 def test_born(self):self.assertAlmostEqual(chsh(2,*ANGLES),2*math.sqrt(2),places=12)
 def test_weight_q2(self):
  for d in np.linspace(0,math.pi/2,61):self.assertAlmostEqual(raw_weight(2,d),1.,places=12)
 def test_weight_non2(self):
  for q in [1,1.5,3,6]:self.assertGreater(abs(raw_weight(q,0)-raw_weight(q,math.pi/4)),1e-4)
 def test_fixed_q_table(self):
  for q in [1,1.5,2,3,6]:
   expected=4*(1-math.tan(math.pi/8)**q)/(1+math.tan(math.pi/8)**q)
   self.assertAlmostEqual(chsh(q,*ANGLES),expected,places=12)
 def test_strictly_positive_q(self):
  with self.assertRaises(ValueError):probs(0,0,1)

if __name__=='__main__':unittest.main()
