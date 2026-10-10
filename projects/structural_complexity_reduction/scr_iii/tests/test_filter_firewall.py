import copy, hashlib, json, unittest
from scr_iii.compat import install_scr_ii_path
from scr_iii.generator.route_csp_c_v001 import build_instance
install_scr_ii_path()
from generator.route_csp_i import structural_view

def dig(x): return hashlib.sha256(json.dumps(structural_view(x),sort_keys=True,separators=(',',':')).encode()).hexdigest()
class TestFirewall(unittest.TestCase):
    def test_arithmetic_mutation_invisible(self):
        a=build_instance(303030101,10,0.8,0.2,0); b=copy.deepcopy(a)
        b['checksum_target']=(b['checksum_target']+1)%b['checksum_modulus']; b['cost_min']+=17; b['cost_max']+=17; b['terminal_seal']=1-b['terminal_seal']
        for layer in b['layers']:
            for o in layer['options']:
                o['cost']+=999; o['checksum_weight']=(o['checksum_weight']+1)%b['checksum_modulus']
        self.assertEqual(dig(a),dig(b))
