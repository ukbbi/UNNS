import json, unittest
from pathlib import Path
from scr_iii.engine_common import scr_iii_root
class TestSeeds(unittest.TestCase):
    def test_unique_and_burned(self):
        s=json.loads((scr_iii_root()/"SCR_III_PREREG_v001"/"SEEDS_v001.json").read_text())
        vals=[]
        for x in s['audit'].values(): vals += x
        for x in s['primary'].values(): vals += x
        vals += list(s['null_seed_bases'].values())+[s['estimator_sample_seed'],s['trend_permutation_seed']]
        self.assertEqual(len(vals),len(set(vals)))
        self.assertFalse(set(vals)&set(s['burned_exclusions']['smoke_test']))
