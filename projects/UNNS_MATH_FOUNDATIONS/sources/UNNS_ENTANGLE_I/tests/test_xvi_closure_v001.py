import math, unittest
from src.xvi_closure_v001 import (radial_weight,anisotropic_weight,rotation_average,iterate_closure,refinement_defect,projection_total,q_probabilities,chsh,run)

class ClosureAudit(unittest.TestCase):
    def test_radial_fixed_points_all_q(self):
        for q in (1,1.5,2,3,6):
            for p in ((1,0),(0.4,1.7)):
                self.assertAlmostEqual(rotation_average(lambda x,y:radial_weight(x,y,q),*p,256),radial_weight(*p,q),places=11)
    def test_refinement_selects_two_conditionally(self):
        self.assertAlmostEqual(refinement_defect(2),0,places=12)
        self.assertGreater(abs(refinement_defect(1)),0.1)
        self.assertGreater(abs(refinement_defect(3)),0.1)
    def test_projection_total_unique_at_pi4(self):
        self.assertAlmostEqual(projection_total(2,math.pi/4),1,places=12)
        for q in (1,1.5,3,6): self.assertGreater(abs(projection_total(q,math.pi/4)-1),0.1)
    def test_anisotropy_contraction(self):
        x,y=1.2,0.7; avg=x*x+y*y; initial=anisotropic_weight(x,y)
        for n in range(8):
            self.assertAlmostEqual(iterate_closure(anisotropic_weight,x,y,n,256),avg+2**(-n)*(initial-avg),places=11)
    def test_probabilities_no_signalling(self):
        for q in (1,1.5,2,3,6):
            for a,b in ((0,0.2),(0.33,0.8),(1,1.3)):
                p=q_probabilities(q,a,b)
                self.assertAlmostEqual(sum(p.values()),1)
                for site,sign in ((0,'+'),(0,'-'),(1,'+'),(1,'-')):
                    self.assertAlmostEqual(sum(v for k,v in p.items() if k[site]==sign),0.5)
    def test_chsh_reference(self):
        self.assertAlmostEqual(chsh(2),2*math.sqrt(2),places=12)
        self.assertGreater(chsh(3),2*math.sqrt(2))
    def test_explicit_failure_not_hidden(self):
        result=run(); self.assertEqual(result['gates']['G4'],'FAIL')
        self.assertEqual(result['gates']['G3'],'FAIL_OPEN')

if __name__=='__main__': unittest.main()
