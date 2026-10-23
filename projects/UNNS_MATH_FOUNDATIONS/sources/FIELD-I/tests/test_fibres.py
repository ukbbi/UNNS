import unittest
from fractions import Fraction
from src.fibres import occurrences, admissible_d, multiplicity, brute_occurrences, is_field
from src.nest import value


class TestFibres(unittest.TestCase):
    def test_integer_72(self):
        self.assertEqual(occurrences(72), [(18, 1), (16, 2), (10, 5)])
        self.assertEqual(multiplicity(72), 3)

    def test_rational_225_over_2(self):
        x = Fraction(225, 2)
        self.assertEqual(admissible_d(x), [3, 5, 15])
        self.assertEqual(occurrences(x), [(25, 2), (18, 4), (7, 14)])
        self.assertEqual(multiplicity(x), 3)
        self.assertTrue(is_field(x))

    def test_no_output_for_squarefree_integer(self):
        for x in [1, 2, 3, 5, 6, 10, 30, 210]:
            self.assertEqual(occurrences(x), [])

    def test_rational_numerator_squarefree_empty(self):
        for x in [Fraction(3, 2), Fraction(10, 3), Fraction(17, 9)]:
            self.assertEqual(occurrences(x), [])

    def test_reconstruction(self):
        for M in range(1, 100):
            for N in range(1, 32):
                self.assertIn((M, N), occurrences(value(M, N)))

    def test_independent_full_fibre_enumeration(self):
        # Ensure formula is complete, not merely consistent for the generating pair.
        keys = {value(M, N) for N in range(1, 21) for M in range(1, 91)}
        for x in keys:
            self.assertEqual(
                [p for p in occurrences(x) if p[0] <= 90 and p[1] <= 20],
                brute_occurrences(x, 90, 20))

    def test_fraction_reductions(self):
        self.assertEqual(occurrences(Fraction(450, 4)), occurrences(Fraction(225, 2)))
        self.assertEqual(occurrences(Fraction(72, 1)), occurrences(72))

    def test_denominator_congruences(self):
        for x in [value(M, N) for N in range(1, 35) for M in range(1, 60)]:
            for M, N in occurrences(x):
                self.assertEqual((N % x.denominator), 0)
                self.assertEqual((x.numerator % (N + 1) ** 2), 0)

    def test_invalid_values(self):
        for x in [0, -1, Fraction(-3, 2)]:
            with self.assertRaises(ValueError): occurrences(x)
        with self.assertRaises(TypeError): occurrences(0.5)
