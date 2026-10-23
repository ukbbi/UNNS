import unittest
from fractions import Fraction
from math import gcd, lcm
from src.intersections import common_step, common_integer_step, is_common_output, is_output_of, first_common_occurrences
from src.nest import value


class TestIntersections(unittest.TestCase):
    def test_2_and_4(self):
        self.assertEqual(common_step(2, 4), Fraction(225, 2))
        self.assertEqual(first_common_occurrences(2, 4), (Fraction(225, 2), 25, 18))

    def test_1_and_2(self):
        self.assertEqual(first_common_occurrences(1, 2), (Fraction(36), 9, 8))

    def test_common_step_is_output(self):
        for n in range(1, 24):
            for q in range(1, 24):
                first, M, Mp = first_common_occurrences(n, q)
                self.assertGreaterEqual(M, 1)
                self.assertGreaterEqual(Mp, 1)
                self.assertEqual(value(M, n), first)
                self.assertEqual(value(Mp, q), first)
                self.assertEqual(common_integer_step(n, q), lcm(n+1, q+1)**2)
                self.assertEqual(gcd(common_integer_step(n, q), gcd(n,q)), 1)

    def test_progression_against_independent_enumeration(self):
        # Enumerate each nest sequence in its native modulus coordinate.
        for n in range(1, 16):
            for q in range(n + 1, 16):
                A = {value(M,n) for M in range(1, 1201)}
                B = {value(M,q) for M in range(1, 1201)}
                step = common_step(n, q)
                for x in (A & B):
                    self.assertEqual((x/step).denominator, 1)
                for j in range(1, 4):
                    x = j * step
                    self.assertTrue(is_common_output(x, n, q))

    def test_membership_criterion_independent(self):
        for n in range(1, 17):
            for q in range(1, 17):
                step = common_step(n,q)
                for x in [Fraction(a,b) for a in (9,16,25,36,72,100,225,441,500) for b in (1,2,3,4,5)]:
                    self.assertEqual(is_common_output(x,n,q), x>0 and (x/step).denominator == 1)

    def test_integral_progression(self):
        for n in range(1, 17):
            for q in range(n+1, 17):
                step = common_integer_step(n,q)
                self.assertTrue(is_common_output(step,n,q))
                self.assertTrue(is_common_output(step*2,n,q))

    def test_bad_inputs(self):
        with self.assertRaises(ValueError): common_step(0, 2)
        with self.assertRaises(ValueError): is_output_of(10, 0)
