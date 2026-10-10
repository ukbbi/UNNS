import unittest
from scr_iii.source_lock_v002 import verify_source_lock_v002, verify_design_freeze_v002

class FreezeTest(unittest.TestCase):
    def test_source_lock(self):
        self.assertTrue(verify_source_lock_v002()["pass"])
    def test_design_freeze(self):
        self.assertTrue(verify_design_freeze_v002()["pass"])
