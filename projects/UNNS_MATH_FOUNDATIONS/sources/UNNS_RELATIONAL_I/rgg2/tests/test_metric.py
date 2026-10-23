import unittest
from itertools import product, combinations
from math import isclose, log
from src.anchor_routes import Anchor, fibre
from src.relational_metric import lift_ratio, distance, weighted_l1, verify_lift

class TestMetric(unittest.TestCase):
    def test_formula_from_72(self):
        a,b,c=Anchor(18,2),Anchor(8,3),Anchor(2,6)
        self.assertEqual((lift_ratio(a,b),lift_ratio(a,c),lift_ratio(b,c)),(36,9,4))
    def test_exact_lift_across_1200(self):
        for m in range(1,1201):
            for a,b in combinations(fibre(m),2):
                self.assertTrue(verify_lift(a,b))
    def test_metric_axioms_on_finite_fibres(self):
        for m in range(1,601):
            F=fibre(m)
            if len(F)<2: continue
            for a in F:
                self.assertEqual(distance(a,a),0.0)
                for b in F:
                    self.assertAlmostEqual(distance(a,b),distance(b,a))
                    self.assertTrue(isclose(distance(a,b),weighted_l1(a,b),abs_tol=1e-11))
                    if a!=b: self.assertGreater(distance(a,b),0)
                    for c in F:
                        self.assertLessEqual(distance(a,c),distance(a,b)+distance(b,c)+1e-10)
    def test_reject_cross_fibre(self):
        with self.assertRaises(ValueError): distance(Anchor(1,2),Anchor(1,3))
        with self.assertRaises(ValueError): lift_ratio(Anchor(1,2),Anchor(1,3))

if __name__=='__main__': unittest.main()
