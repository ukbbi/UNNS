import unittest
from fractions import Fraction
from src.nest import value, index_number, integer_index, next_occurrence, next_integer_occurrence, is_anchor


class TestNest(unittest.TestCase):
    def test_formula(self):
        for M in range(1, 61):
            for N in range(1, 41):
                self.assertEqual(value(M, N), M * N + Fraction(M, N) + 2 * M)

    def test_index_18(self):
        self.assertEqual(index_number(18), Fraction(361, 18))
        self.assertEqual(integer_index(18), 361)
        self.assertEqual([value(M, 18) for M in (18, 36, 54)], [361, 722, 1083])

    def test_increment(self):
        for N in range(1, 41):
            for M in range(1, 41):
                self.assertEqual(value(M+1, N) - value(M, N), index_number(N))

    def test_anchor(self):
        for M in range(1, 41):
            for N in range(1, 41):
                self.assertEqual(is_anchor(M, N), value(M, N).denominator == 1)

    def test_integer_progression(self):
        for N in range(1, 35):
            M = N * 4
            self.assertEqual(next_integer_occurrence(M, N), (M + N, N))
            self.assertEqual(value(M + N, N) - value(M, N), integer_index(N))

    def test_invalid_inputs(self):
        for M, N in [(0, 1), (1, 0), (-1, 3), (3, -1), (True, 1), (1, 1.5)]:
            with self.assertRaises(ValueError): value(M, N)
        with self.assertRaises(ValueError): next_integer_occurrence(1, 2)
        with self.assertRaises(ValueError): next_occurrence(1, 1, -1)
