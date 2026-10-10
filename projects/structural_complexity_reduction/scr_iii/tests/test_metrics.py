import unittest
from scr_iii.analysis.stats_v001 import clopper_pearson, spearman
class TestStats(unittest.TestCase):
    def test_cp_20_20(self):
        lo,hi=clopper_pearson(20,20)
        self.assertGreater(lo,0.83); self.assertEqual(hi,1.0)
    def test_spearman(self): self.assertAlmostEqual(spearman([1,2,3],[2,4,8]),1.0)
