import unittest, json
from pathlib import Path

class V002SeedTests(unittest.TestCase):
    def test_separation(self):
        root=Path(__file__).resolve().parents[1]/"SCR_II_PREREG_v002"
        s=json.loads((root/"SEEDS.json").read_text(encoding="utf-8"))
        cal=set(sum(s["calibration"].values(),[]))
        des=set(s["design_audit"])
        prim=set(sum(s["primary"].values(),[]))
        self.assertFalse(cal&des)
        self.assertFalse(cal&prim)
        self.assertFalse(des&prim)
        self.assertEqual(len(prim),30)
