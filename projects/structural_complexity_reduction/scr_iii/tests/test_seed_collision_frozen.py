import json, re, unittest
from pathlib import Path
from scr_iii.engine_common import project_root, scr_iii_root

def ints(obj):
    if isinstance(obj,int): return {obj}
    if isinstance(obj,list):
        out=set()
        for x in obj: out |= ints(x)
        return out
    if isinstance(obj,dict):
        out=set()
        for v in obj.values(): out |= ints(v)
        return out
    return set()

class TestFrozenSeedCollision(unittest.TestCase):
    def test_no_collision(self):
        root=project_root(); s3=scr_iii_root()
        new=json.loads((s3/'SCR_III_PREREG_v001'/'SEEDS_v001.json').read_text())
        newset=set()
        for x in new['audit'].values(): newset.update(x)
        for x in new['primary'].values(): newset.update(x)
        newset.update(new['null_seed_bases'].values()); newset.update([new['estimator_sample_seed'],new['trend_permutation_seed']])
        old=set()
        for p in [root/'scr_ii'/'SCR_II_PREREG_v001'/'SEEDS.json', root/'scr_ii'/'SCR_II_PREREG_v002'/'SEEDS.json', root/'SCR_I_PREREG_v003'/'config'/'scr_i_prereg_v003.json']:
            old |= ints(json.loads(p.read_text()))
        self.assertFalse(newset & old)
