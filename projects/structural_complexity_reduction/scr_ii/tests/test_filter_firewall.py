import unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from generator.route_csp_i import generate_instance, mutate_arithmetic
from filter.structural_filter import structural_signature, walk_prefix

class FirewallTests(unittest.TestCase):
    def test_arithmetic_mutation_does_not_change_structure(self):
        inst=generate_instance(222,10)
        mut=mutate_arithmetic(inst)
        self.assertEqual(structural_signature(inst), structural_signature(mut))
        for bits in ("0000000000","1111111111","0101010101","1010101010"):
            self.assertEqual(walk_prefix(inst,bits)[0:2],walk_prefix(mut,bits)[0:2])
