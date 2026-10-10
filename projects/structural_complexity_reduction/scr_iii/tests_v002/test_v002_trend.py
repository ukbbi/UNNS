import unittest
from scr_iii.analysis.trend_test_v002 import coverage_block_stat, blocked_permutation_coverage_trend

class TrendTest(unittest.TestCase):
    def test_positive_stat(self):
        rows=[]
        for seed in range(10):
            for c in (0.0,0.25,0.5,1.0):
                rows.append({"seed":seed,"coverage_C":c,"solution_recall":0.1+0.8*c})
        self.assertGreater(coverage_block_stat(rows),0)
        res=blocked_permutation_coverage_trend(rows,2000,12345)
        self.assertLess(res["p_one_sided"],0.02)
