import unittest
from scr_iii.generator.route_csp_c_v001 import build_instance
from scr_iii.nulls.controls_v001 import build_n4
from scr_iii.compat import install_scr_ii_path
install_scr_ii_path()
from solver.exact_solver import solve_baseline, solve_scr
class TestControls(unittest.TestCase):
    def test_z0(self):
        z=build_instance(303030101,10,1.0,0.0,0)
        self.assertEqual(solve_baseline(z)['solutions'],solve_scr(z)['solutions'])
        self.assertEqual(solve_scr(z)['leaves_checked'],1<<10)
    def test_n4_target_differs(self):
        a=build_instance(303030101,10,0.8,0.3,0)
        n=build_n4(a)
        self.assertTrue(n['coupling_metadata']['anti_coupled'])
        self.assertNotEqual((a['checksum_target'],a['cost_min'],a['terminal_seal']),(n['checksum_target'],n['cost_min'],n['terminal_seal']))
