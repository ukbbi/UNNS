import unittest
from scr_iii.generator.route_csp_c_v001 import generate_family
class TestFamilyPairing(unittest.TestCase):
    def test_common_attempt(self):
        fam=generate_family(303030101,10,[0.0,0.1,0.2,0.3],[0.8,0.9])
        self.assertEqual(fam['status'],'ACCEPTED')
        attempts={x['attempt'] for x in fam['instances'].values()}
        self.assertEqual(len(attempts),1)
        self.assertTrue(all(x['q0_v002_arithmetic_identity'] for x in fam['attempt_log']))
