import unittest
from fractions import Fraction
from src.arithmetic import D, occurrences, exponent_fibre, square_root_part
from src.select_ii import T, transport, edges, history

class ArithmeticTests(unittest.TestCase):
    def test_occurrence_72(self):
        self.assertEqual(occurrences(72), ((1, 18), (2, 16), (5, 10)))
        self.assertEqual(D(72), (2, 3, 6))
        for x in (Fraction(900), Fraction(36), Fraction(12100, 3), Fraction(1870**2, 3)):
            ps, vecs = exponent_fibre(x)
            self.assertEqual(len(vecs), len(D(x)))
            self.assertEqual(len(occurrences(x)), len(D(x)))
            for N, M in occurrences(x):
                self.assertEqual(Fraction(M*(N+1)**2, N), x)

    def test_edges_of_6(self):
        self.assertEqual([(e['N'], e['t']) for e in edges(6)], [(1,24),(2,27),(3,32),(6,49)])

    def test_all_72_edges(self):
        self.assertEqual([(e['N'], e['t'], e['g']) for e in edges(72)],
            [(1,288,6),(2,324,6),(3,384,2),(4,450,3),(6,588,2),(8,729,3),
             (9,800,2),(12,1014,1),(18,1444,2),(24,1875,1),(36,2738,1),(72,5329,1)])
        self.assertEqual([e['N'] for e in edges(72) if len(e['shared'])==0],[12,24,36,72])

    def test_factorization(self):
        for m in range(1,301):
            for e in edges(m):
                g = e['g']
                self.assertEqual(e['S'], g*e['c'])
                self.assertEqual(e['Sp'], g*(e['N']+1))
                self.assertTrue(e['gained'])
                self.assertEqual(set(D(m))<=set(D(e['t'])), e['c']==1)

    def test_histories(self):
        self.assertEqual(history(1,(1,1,2)),[1,4,16,72])
        self.assertEqual(history(1,(1,2,1)),[1,4,18,72])

if __name__=='__main__': unittest.main()
