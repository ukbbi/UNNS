import json, unittest
from scr_iii.engine_common import scr_iii_root
from scr_iii.generator.route_csp_c_v001 import build_instance
class TestSchema(unittest.TestCase):
    def test_instance_schema(self):
        try: import jsonschema
        except Exception as e: self.skipTest('jsonschema unavailable')
        schema=json.loads((scr_iii_root()/"SCR_III_PREREG_v001"/"schema"/"route_csp_c_v001.schema.json").read_text())
        jsonschema.validate(build_instance(303030101,10,0.8,0.2,0),schema)
