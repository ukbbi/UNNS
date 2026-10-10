import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.scr_i_v003.mechanism import generate_pool
from src.scr_i_v003.gates import audit
from src.scr_i_v003.target_oracle import labels
from src.scr_i_v003.basins import preservation,passes_frozen_requirements
class T(unittest.TestCase):
 def test_design_seed_small(self):
  p=generate_pool(2500,2026100701);t=labels(p);a,_=audit(p);s=[r['scr_pass'] for r in a];tm=[];sm=[]
  for m,x,y in zip(p,t,s):
   if x:tm.append(m);sm.append(y)
  q=preservation(tm,sm);self.assertGreaterEqual(q['basin_count'],1);self.assertEqual(q['basin_recall'],1.0)
 def test_primary_seed_separation(self):
  self.assertTrue(set([2026100701,2026100702,2026100703,2026100704,2026100705]).isdisjoint([2026101001,2026101002,2026101003,2026101004,2026101005]))
if __name__=='__main__':unittest.main()
