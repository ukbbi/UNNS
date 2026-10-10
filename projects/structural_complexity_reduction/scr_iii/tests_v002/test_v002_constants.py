import unittest
from scr_iii.engine_v002_common import Q_LEVELS_V002,SIGMA_LEVELS_V002,MAX_ATTEMPTS_V002,N_DOSE_MIN_V002,N_ACC_MIN_V002,AUDIT_DEPTH_V002,PRIMARY_DEPTHS_V002

class ConstantsTest(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(Q_LEVELS_V002,(0.0,0.1,0.2,0.3,0.4))
        self.assertEqual(SIGMA_LEVELS_V002,(0.8,0.9))
        self.assertEqual(MAX_ATTEMPTS_V002,64)
        self.assertEqual(N_DOSE_MIN_V002,6)
        self.assertEqual(N_ACC_MIN_V002,21)
        self.assertEqual(AUDIT_DEPTH_V002,14)
        self.assertEqual(PRIMARY_DEPTHS_V002,(14,16,18))
