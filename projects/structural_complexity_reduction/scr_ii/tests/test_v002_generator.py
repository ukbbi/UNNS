import json, unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from generator.route_csp_i_v002 import generate_instance

class V002GeneratorTests(unittest.TestCase):
    def test_deterministic_and_in_band(self):
        a,b1,_=generate_instance(2026106101,8)
        c,b2,_=generate_instance(2026106101,8)
        self.assertEqual(a,c)
        self.assertEqual(b1["solutions"],b2["solutions"])
        density=b1["solution_count"]/(1<<8)
        self.assertGreaterEqual(density,0.02)
        self.assertLessEqual(density,0.04)

    def test_nontrivial_multiplicity(self):
        _,b,_=generate_instance(2026106301,12)
        self.assertGreater(b["solution_count"],1)
