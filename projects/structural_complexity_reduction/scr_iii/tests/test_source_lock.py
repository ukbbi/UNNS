import unittest
from scr_iii.source_lock import verify_source_lock
class TestSourceLock(unittest.TestCase):
    def test_lock(self): self.assertTrue(verify_source_lock()["pass"])
