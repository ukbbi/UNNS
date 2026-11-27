"""Oracle straight from the definition: walk forward from every source along legal moves."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ancestry_engine import ancestry_census, unpack
from grammar_controls import grammars


def brute(X, pairs):
    H = [[0] for _ in range(X + 1)]
    def add(n, k):
        while len(H[n]) <= k:
            H[n].append(0)
        H[n][k] += 1
    for source in range(1, X + 1):
        stack = [(source, 0)]
        while stack:
            x, k = stack.pop()
            add(x, k)
            for p, q in pairs:
                if x % q == 0 and x // q * p <= X:
                    stack.append((x // q * p, k + 1))
    return H


class FromDefinition(unittest.TestCase):
    def check(self, name, X):
        pairs = grammars(X)[name][1]
        B = brute(X, pairs)
        H = ancestry_census(X, pairs)
        for n in range(1, X + 1):
            self.assertEqual(unpack(H[n]), B[n], (name, n))

    def test_nesting(self):
        self.check("selected_nesting", 3000)

    def test_cubic(self):
        self.check("cubic_nesting", 3000)

    def test_integer(self):
        self.check("integer_scaling", 400)

    def test_consuming(self):
        self.check("consuming_3/2_9/4", 3000)

    def test_finite(self):
        self.check("finite_2_3", 1500)


if __name__ == "__main__":
    unittest.main()
