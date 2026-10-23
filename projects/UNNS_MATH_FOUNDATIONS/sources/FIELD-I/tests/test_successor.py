import unittest
from fractions import Fraction
from src.nest import value, index_number
from src.successor import next_value, next_integer_value, reconstruct_consecutive, reconstruct_integer_neighbors, next_options


class TestSuccessor(unittest.TestCase):
    def test_seventy_two(self):
        self.assertEqual([next_value(*occ) for occ in [(18,1),(16,2),(10,5)]],
                         [Fraction(76), Fraction(153,2), Fraction(396,5)])
        self.assertEqual([next_integer_value(*occ) for occ in [(18,1),(16,2),(10,5)]], [76,81,108])

    def test_reverse_chart(self):
        for M in range(1, 151):
            for N in range(1, 81):
                x = value(M,N)
                self.assertEqual(reconstruct_consecutive(x, next_value(M,N)), (M,N))

    def test_reverse_integer_chart(self):
        for N in range(1, 45):
            for k in range(1, 18):
                M = N*k
                x = int(value(M,N))
                self.assertEqual(reconstruct_integer_neighbors(x,next_integer_value(M,N)),(M,N))

    def test_noninteger_fibre_successors(self):
        vals = next_options(Fraction(225,2))
        self.assertEqual(len(vals),3)
        self.assertEqual(len({y for _, y in vals}),3)

    def test_invalid_differences(self):
        for x, y in [(72,72),(72,73),(72,74),(72,75),(72,77),(Fraction(225,2),Fraction(227,2))]:
            with self.assertRaises(ValueError): reconstruct_consecutive(x,y)
        with self.assertRaises(ValueError): reconstruct_integer_neighbors(72,78)

    def test_increment_strictness(self):
        for n in range(1,500):
            self.assertLess(index_number(n),index_number(n+1))
