import sys,unittest,random,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'models'))
from physical_energy import patch,pair_coupling,couplings,energy,ice_ok,enumerate_patch
class Checks(unittest.TestCase):
 def test_spin_counts(self):
  for L in (1,2,3):
   e,v=patch(L);self.assertEqual(len(e),2*L*(L+1));self.assertEqual(len(v),L*L)
 def test_coupling_symmetric(self):
  e,_=patch(2)
  for a in range(len(e)):
   for b in range(a+1,len(e)):
    self.assertAlmostEqual(pair_coupling(e[a],e[b]),pair_coupling(e[b],e[a]),places=12)
 def test_flip_delta(self):
  e,_=patch(2);p=couplings(e);rng=random.Random(17)
  for _ in range(100):
   s=[rng.choice([-1,1]) for _ in e];i=rng.randrange(len(s));field=sum(k*s[j] if a==i else k*s[a] for a,j,k in p if i in (a,j));old=energy(s,p);expected=2*s[i]*field;s[i]*=-1
   self.assertAlmostEqual(energy(s,p)-old,expected,places=11)
 def test_enumeration(self):
  for L in (1,2):
   r=enumerate_patch(L);self.assertEqual(r['states'],2**r['N']);self.assertGreater(r['ice_states'],0)
if __name__=='__main__': unittest.main()
