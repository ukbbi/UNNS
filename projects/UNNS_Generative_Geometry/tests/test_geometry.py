import unittest
from fractions import Fraction
from src.arithmetic import D, exponent_fibre
from src.cells import coordinate_cell_union_contains, coordinate_hull_contains, rational_rank
from src.parity import parity_benchmark, graver_basis

class GeometryTests(unittest.TestCase):
    def test_trivial_hull_gap(self):
        for k in (2,3,4,5):
            Q=(2,)*k
            witness=(Fraction(1,2),Fraction(1,2))+(Fraction(0),)*(k-2)
            self.assertTrue(coordinate_hull_contains(witness,Q))
            self.assertFalse(coordinate_cell_union_contains(witness,Q))
        self.assertFalse(coordinate_cell_union_contains((Fraction(1,2),Fraction(1,2)),(2,2)))
        self.assertTrue(coordinate_cell_union_contains((Fraction(3,2),Fraction(1,2)),(2,2)))
        self.assertTrue(coordinate_cell_union_contains((Fraction(1),Fraction(1,2)),(2,2)))

    def test_parity_3_4(self):
        for primes, count in [((2,5,11),13),((2,5,11,17),40)]:
            x, pts = parity_benchmark(primes)
            self.assertEqual(len(pts),count)
            self.assertEqual(len(D(x)), count)
            self.assertTrue(all(sum(p)%2==0 and any(p) for p in pts))
            self.assertEqual(len(graver_basis(len(primes))), 2*len(primes)**2)
            self.assertEqual(len(graver_basis(len(primes), oriented=True)), len(primes)**2)

    def test_rank(self):
        self.assertEqual(rational_rank(((2,0,0),(0,2,0))),2)
        self.assertEqual(rational_rank(((1,1,0),(2,2,0))),1)

if __name__=='__main__': unittest.main()
