import json
import unittest
import sys
from pathlib import Path

SCRII = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRII))

from generator.route_csp_i_v002 import generate_instance
from solver.exact_solver import solve_scr, solve_solver_native

class V002PrimaryRunnerTests(unittest.TestCase):
    def test_cell_metrics_nonprimary(self):
        seed = 2026106401  # frozen design-audit seed, NOT primary
        inst, base, _ = generate_instance(seed, 12)
        scr = solve_scr(inst)
        native = solve_solver_native(inst)

        self.assertGreater(base["solution_count"], 1)
        density = base["solution_count"] / (1 << 12)
        self.assertGreaterEqual(density, 0.02)
        self.assertLessEqual(density, 0.04)
        self.assertEqual(native["solutions"], base["solutions"])

        recall = len(set(base["solutions"]) & set(scr["solutions"])) / len(base["solutions"])
        self.assertGreaterEqual(recall, 0.0)
        self.assertLessEqual(recall, 1.0)

    def test_primary_seed_grid_not_used_by_test(self):
        prereg = SCRII / "SCR_II_PREREG_v002"
        seeds = json.loads((prereg / "SEEDS.json").read_text(encoding="utf-8"))
        prim = set(sum(seeds["primary"].values(), []))
        self.assertNotIn(2026106401, prim)
        self.assertEqual(len(prim), 30)
