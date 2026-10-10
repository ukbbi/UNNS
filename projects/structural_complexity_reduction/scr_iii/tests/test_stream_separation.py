import unittest
from scr_iii.generator.route_csp_c_v001 import build_instance
class TestStreams(unittest.TestCase):
    def test_q_changes_arithmetic_not_unmasked_structure(self):
        a=build_instance(303030101,10,0.8,0.0,0)
        b=build_instance(303030101,10,0.8,0.3,0)
        self.assertEqual(a['coupling_metadata']['mirror_u'],b['coupling_metadata']['mirror_u'])
        self.assertEqual(a['coupling_metadata']['mask_permutation'],b['coupling_metadata']['mask_permutation'])
        self.assertTrue(set(a['coupling_metadata']['mask_layers']).issubset(set(b['coupling_metadata']['mask_layers'])))
