import copy, hashlib, json, unittest, sys
from pathlib import Path
SCRII=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRII))
from generator.route_csp_i_v002 import generate_instance, structural_view

def digest(i):
    return hashlib.sha256(json.dumps(structural_view(i),sort_keys=True,separators=(",",":")).encode()).hexdigest()

class V002FirewallTests(unittest.TestCase):
    def test_arithmetic_mutation_does_not_change_structural_view(self):
        inst,_,_=generate_instance(2026106302,12)
        mut=copy.deepcopy(inst)
        mut["checksum_target"]=(mut["checksum_target"]+1)%mut["checksum_modulus"]
        mut["cost_min"]+=9999; mut["cost_max"]+=9999
        mut["terminal_seal"]=1-mut["terminal_seal"]
        for layer in mut["layers"]:
            for opt in layer["options"]:
                opt["cost"]+=5000
                opt["checksum_weight"]=(opt["checksum_weight"]+1)%mut["checksum_modulus"]
        self.assertEqual(digest(inst),digest(mut))
