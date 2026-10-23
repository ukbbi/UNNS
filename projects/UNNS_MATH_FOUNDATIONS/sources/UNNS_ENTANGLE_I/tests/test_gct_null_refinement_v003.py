import math
import unittest
from src.gct_null_refinement_v003 import Route, elem, pi, refine, b, b_quotient, close, witness, run

A = (1.0,0.0,0.0)
B = (0.0,1.0,0.0)

class NullRefinementAudit(unittest.TestCase):
    def test_two_structurally_distinct_routes_one_observable(self):
        x0, x1 = elem(A,0), elem(A,1)
        self.assertNotEqual(x0,x1)
        self.assertEqual(pi(x0),pi(x1))

    def test_nontrivial_period_two(self):
        x = elem(A,0)
        self.assertNotEqual(refine(x),x)
        self.assertEqual(refine(refine(x)),x)

    def test_exact_morphism_all_trajectories(self):
        for x in (elem(A,0),elem(A,1),elem(A,0)+elem(B,1)):
            self.assertTrue(close(pi(refine(x)), pi(x)))

    def test_route_additivity(self):
        x,y,z=elem(A,0),elem(B,0),elem(A,1)
        self.assertAlmostEqual(b(x+y,z), b(x,z)+b(y,z))
        self.assertAlmostEqual(b(z,x+y), b(z,x)+b(z,y))

    def test_homogeneity(self):
        x,y=elem(A,0),elem(B,0)+elem(A,0)
        self.assertAlmostEqual(b(x.scale(-2.3),y),-2.3*b(x,y))
        self.assertAlmostEqual(b(x,y.scale(2.3)),2.3*b(x,y))

    def test_rotation_covariance(self):
        x=elem(A,0)+elem(B,1)
        y=elem(B,0)+elem(A,1)
        for t in (0.1,math.pi/7,1.3,math.pi):
            self.assertAlmostEqual(b(x.rotate(t),y.rotate(t)),b(x,y),places=12)

    def test_refinement_simultaneous_invariance(self):
        x,y=elem(A,0),elem(B,0)+elem(A,1)
        self.assertAlmostEqual(b(refine(x),refine(y)),b(x,y))

    def test_aligned_anticorrelation_both_routes(self):
        self.assertEqual(b(elem(A,0),elem(A,0)),-1.)
        self.assertEqual(b(elem(A,1),elem(A,1)),-1.)

    def test_null_route_is_observationally_zero(self):
        x=elem(A,0)-elem(A,1)
        self.assertEqual(pi(x),(0.,0.,0.))

    def test_null_refinement_condition_fails(self):
        x=elem(A,0)-elem(A,1)
        y=elem(A,0)
        self.assertEqual(b(x,y),-1.)
        self.assertNotEqual(b(x,y),0.)

    def test_quotient_rule_would_remove_hidden_interaction(self):
        x=elem(A,0)-elem(A,1)
        self.assertEqual(b_quotient(pi(x),pi(elem(A,0))),0.)

    def test_baseline_and_negative_verdict(self):
        r=run()
        self.assertTrue(r['prior_baseline']['verdict_preserved'])
        self.assertEqual(r['scientific_verdict'],'NOT_ENTAILED_BY_DOCUMENTED_UNNS_AXIOMS')
        self.assertFalse(r['checks']['observable_null_gate_passes'])

if __name__=='__main__':
    unittest.main()
