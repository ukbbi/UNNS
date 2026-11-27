import os, sys, unittest
from math import gcd, log
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ancestry_engine import ancestry_census, unpack
from endpoint_engine import endpoint_census
from prime_dynamics import least_source, step, factor, lindley
from dirichlet import zeta, hurwitz, B_bracket, kappa_local


def E(w):
    K, a, b = least_source(w)
    return K * a // b


class Statements(unittest.TestCase):
    def test_tree(self):
        self.assertEqual([E(w) for w in [(1,), (2,), (1, 1), (1, 2), (2, 1), (2, 2)]],
                         [4, 9, 16, 18, 36, 81])

    def test_prime_example(self):
        self.assertEqual(step(factor(12), 2), factor(54))
        self.assertEqual(step(factor(36), 2), factor(9 * 36 // 2))
        self.assertNotIn(12, endpoint_census(100000))

    def test_closed_form_example(self):
        w = (7, 2, 5, 3, 3, 8)
        for p in (2, 3, 7):
            self.assertEqual(lindley(w, p), factor(E(w)).get(p, 0))

    def test_not_multiplicative(self):
        H = ancestry_census(40)
        self.assertEqual([sum(unpack(H[n])) for n in (4, 9, 36)], [2, 2, 6])
        self.assertEqual([unpack(H[n])[1] for n in (4, 9, 36)], [1, 1, 3])

    def test_B2(self):
        lo, hi = B_bracket(1.999999)
        exact = zeta(2.0) - 2 * zeta(3.0) + zeta(4.0)
        self.assertAlmostEqual(exact, 0.3231434942, places=9)
        self.assertLess(abs(lo - exact), 1e-5)

    def test_zeta_values(self):
        from math import pi
        self.assertAlmostEqual(zeta(2.0), pi ** 2 / 6, places=13)
        self.assertAlmostEqual(zeta(4.0), pi ** 4 / 90, places=13)
        self.assertAlmostEqual(hurwitz(2.0, 2.0), pi ** 2 / 6 - 1, places=13)

    def test_kappa_factor_equals_transfer_expectation(self):
        for p in (2, 3, 5, 13):
            P = lambda i: (1 - 1 / p) * p ** (-i)
            T = int(40 / log(p, 2)) + 5
            val = sum(P(u) * P(d) * p ** (min(2 * u, d) / 2) for u in range(T) for d in range(2 * T))
            self.assertAlmostEqual(val, kappa_local(p), places=9)


if __name__ == "__main__":
    unittest.main()
