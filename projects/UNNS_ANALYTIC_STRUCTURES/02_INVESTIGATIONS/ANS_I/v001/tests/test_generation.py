import os, sys, unittest
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generative_record import nest, replay, records, orbit_histories, prime_word
from prime_dynamics import least_source, factor
from endpoint_engine import endpoint_census, unpack


class Generation(unittest.TestCase):
    def test_records_replay(self):
        for w, K, Q, E in records(20000):
            self.assertEqual(replay(K, w)[-1], E)
            self.assertEqual(Q * K, E)
            self.assertEqual(least_source(w)[0], K)

    def test_least_source_by_trial(self):
        def legal(x, w):
            try:
                replay(x, w)
                return True
            except ValueError:
                return False
        for w, K, Q, E in records(3000):
            self.assertEqual(next(x for x in range(1, K + 1) if legal(x, w)), K)

    def test_prime_coordinates_of_a_transition(self):
        v = lambda n, p: factor(n).get(p, 0)
        for x in range(1, 400):
            for N in range(1, 30):
                if x % N == 0:
                    y = nest(x, N)
                    for p in (2, 3, 5, 7, 11, 13):
                        self.assertEqual(v(y, p), v(x, p) + 2 * v(N + 1, p) - v(N, p))

    def test_records_aggregate_to_census(self):
        a = {}
        for w, K, Q, E in records(20000):
            a[E] = a.get(E, 0) + (1 << (40 * len(w)))
        self.assertEqual(a, endpoint_census(20000))

    def test_actual_histories_factor_through_records(self):
        """histories (x,w) ending at y  <->  records with E | y and x = (y/E) K."""
        X = 1500
        direct = sorted((x, y, w) for x in range(1, X + 1)
                        for w, y in orbit_histories(x, X))
        built = sorted((m * K, m * E, w) for w, K, Q, E in records(X)
                       for m in range(1, X // E + 1))
        self.assertEqual(direct, built)

    def test_source_one_is_K_equal_one(self):
        X = 100000
        self.assertEqual(sorted(orbit_histories(1, X)),
                         sorted((w, E) for w, K, Q, E in records(X) if K == 1))

    def test_prime_words(self):
        memo = {}
        for p in range(2, 200):
            if factor(p) == {p: 1}:
                self.assertEqual(replay(1, prime_word(p, memo))[-1] % p, 0)


if __name__ == "__main__":
    unittest.main()
