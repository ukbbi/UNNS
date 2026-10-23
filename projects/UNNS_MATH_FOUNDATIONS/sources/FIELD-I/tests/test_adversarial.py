import unittest
from fractions import Fraction
from src.fibres import occurrences, is_field
from src.nest import value
from src.intersections import common_step, is_common_output
from src.successor import next_value
from src.selection import joint_low, joint_high


class TestAdversarial(unittest.TestCase):
    def test_rational_collisions_present(self):
        F={}
        for N in range(1,12):
            for M in range(1,200):
                x=value(M,N)
                if x.denominator>1:
                    F.setdefault(x,[]).append((M,N))
        collisions={x:rs for x,rs in F.items() if len(rs)>1}
        self.assertTrue(collisions)
        for x in collisions:
            self.assertEqual(sorted(collisions[x]),sorted(o for o in occurrences(x) if o[0]<200 and o[1]<12))

    def test_field_iff_denominator_nontrivial(self):
        for N in range(1,45):
            for M in range(1,75):
                self.assertEqual(is_field(value(M,N)),M%N != 0)

    def test_nonanchor_collision_exact_example(self):
        for o in ((25,2),(18,4),(7,14)):
            self.assertEqual(value(*o),Fraction(225,2))

    def test_rational_intersection_not_prematurely_integer(self):
        self.assertTrue(is_common_output(Fraction(225,2),2,4))
        self.assertEqual(common_step(2,4),Fraction(225,2))
        self.assertFalse(is_common_output(Fraction(225,2),1,4))

    def test_future_reveals_existing_n_label_not_binary_selection(self):
        a,b=(25,2),(18,4)
        self.assertNotEqual(next_value(*a), next_value(*b))
        self.assertNotEqual(joint_low(a,b), joint_high(a,b))
