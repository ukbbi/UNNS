import unittest
from math import pi,sqrt
from src.models import quantum_reference,bell_local_shared_sign,independent_null
from src.benchmark import validate,run_model,build_report,corr
class BenchmarkTests(unittest.TestCase):
    def test_all_reference_distributions_normalized(self):
        for model in (quantum_reference,bell_local_shared_sign,independent_null):
            for i in range(8):
                for j in range(4):validate(model(pi*i/32,pi*j/32))
    def test_quantum_chsh(self):self.assertAlmostEqual(run_model(quantum_reference)['S'],2*sqrt(2),places=12)
    def test_local_bound(self):self.assertLessEqual(run_model(bell_local_shared_sign)['S'],2+1e-12)
    def test_independent_zero(self):self.assertAlmostEqual(run_model(independent_null)['S'],0,places=12)
    def test_no_signalling_reference(self):
        for model in (quantum_reference,bell_local_shared_sign,independent_null):
            self.assertLessEqual(run_model(model)['max_remote_setting_marginal_shift'],1e-12)
    def test_anticorrelated_same_angle(self):self.assertAlmostEqual(corr(quantum_reference(0,0)),-1)
    def test_provenance_warning(self):self.assertEqual(build_report()['status'],'REFERENCE_ONLY_NO_UNNS_DERIVATION')
if __name__=='__main__':unittest.main()
