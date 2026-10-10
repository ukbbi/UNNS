import unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from generator.route_csp_i import generate_instance
from solver.exact_solver import solve_baseline, solve_solver_native

class SolverTests(unittest.TestCase):
    def test_native_control_exact(self):
        inst=generate_instance(789,10)
        b=solve_baseline(inst)
        c=solve_solver_native(inst)
        self.assertEqual(b["solutions"],c["solutions"])
        self.assertGreaterEqual(b["solution_count"],1)
