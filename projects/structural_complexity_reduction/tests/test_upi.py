import math
import unittest

from src.diagnostics.upi import compute_upi


class TestUPI(unittest.TestCase):
    def test_safe(self):
        r = compute_upi(D=2, R=0, M=1, S=2)
        self.assertEqual(r.value, 0)
        self.assertEqual(r.band, "SAFE")

    def test_high_risk(self):
        r = compute_upi(D=10, R=0.5, M=0.5, S=1)
        self.assertGreater(r.value, 3)
        self.assertEqual(r.band, "HIGH_RISK")

    def test_zero_denominator(self):
        r = compute_upi(D=1, R=1, M=0, S=0)
        self.assertTrue(math.isinf(r.value))


if __name__ == "__main__":
    unittest.main()
