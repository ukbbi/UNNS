import unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from generator.route_csp_i import generate_instance
from filter.structural_filter import walk_prefix

class GeneratorTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(generate_instance(123,8), generate_instance(123,8))

    def test_backbone_structurally_valid(self):
        inst=generate_instance(456,10)
        # Reconstruct planted bits by matching provenance hash through brute force is unnecessary;
        # instead generator contract is checked over calibration/design audits. Here test at least
        # one full structural route exists.
        found=False
        for x in range(1<<10):
            bits=f"{x:010b}"
            if walk_prefix(inst,bits)[0]:
                found=True; break
        self.assertTrue(found)
