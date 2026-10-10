import unittest
from pathlib import Path

class V002PrimaryFreezeTests(unittest.TestCase):
    def test_no_primary_result_bundled(self):
        scrii = Path(__file__).resolve().parents[1]
        self.assertFalse((scrii / "output" / "v002_primary" / "PRIMARY_RESULT_v002.json").exists())
