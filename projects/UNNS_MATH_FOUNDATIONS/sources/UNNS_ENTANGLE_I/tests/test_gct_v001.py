import math
import unittest

from src.gct_generator_v001 import chsh, local_joint_distribution, optimal_quantum_angles, run_gct, singlet_distribution

class GCTTests(unittest.TestCase):
    def test_local_distribution_normalized(self):
        self.assertAlmostEqual(sum(local_joint_distribution(0.1, 0.4).values()), 1.0, places=12)

    def test_singlet_distribution_normalized(self):
        self.assertAlmostEqual(sum(singlet_distribution(0.1, 0.4).values()), 1.0, places=12)

    def test_local_no_signalling_like_marginals(self):
        a = 0.2
        d1 = local_joint_distribution(a, 0.0)
        d2 = local_joint_distribution(a, 1.1)
        pa1_plus = d1[(1, 1)] + d1[(1, -1)]
        pa2_plus = d2[(1, 1)] + d2[(1, -1)]
        self.assertAlmostEqual(pa1_plus, pa2_plus, places=12)
        self.assertAlmostEqual(pa1_plus, 0.5, places=12)

    def test_local_chsh_bound(self):
        max_s = run_gct()["local_witness"]["grid_search"]["max_abs_chsh"]
        self.assertLessEqual(max_s, 2.0 + 1e-9)

    def test_quantum_comparator_hits_tsirelson(self):
        s = chsh(singlet_distribution, optimal_quantum_angles())
        self.assertAlmostEqual(abs(s), 2.0 * math.sqrt(2.0), places=12)

    def test_local_witness_below_quantum(self):
        s_local = abs(chsh(local_joint_distribution, optimal_quantum_angles()))
        s_quantum = abs(chsh(singlet_distribution, optimal_quantum_angles()))
        self.assertLessEqual(s_local, 2.0 + 1e-9)
        self.assertGreater(s_quantum, 2.0)

if __name__ == "__main__":
    unittest.main()
