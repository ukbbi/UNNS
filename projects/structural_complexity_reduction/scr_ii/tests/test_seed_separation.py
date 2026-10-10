import unittest, json
from pathlib import Path

class SeedTests(unittest.TestCase):
    def test_disjoint(self):
        root=Path(__file__).resolve().parents[1]/"SCR_II_PREREG_v001"
        seeds=json.loads((root/"SEEDS.json").read_text(encoding="utf-8"))
        cal=set(sum(seeds["calibration"].values(),[]))
        design=set(seeds["design_audit"])
        prim=set(sum(seeds["primary"].values(),[]))
        self.assertFalse(cal & design)
        self.assertFalse(cal & prim)
        self.assertFalse(design & prim)
        self.assertEqual(len(prim),30)
