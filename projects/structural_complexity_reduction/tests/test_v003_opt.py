import sys,unittest,tempfile,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.scr_i_v003.mechanism import generate_pool
from src.scr_i_v003.gates import audit
from src.scr_i_v003.target_oracle import labels
from src.scr_i_v003.basins import preservation,prepare_preservation_baseline,preservation_from_baseline
from src.scr_i_v003.nulls import rate_matched_random,rate_matched_random_cached

class OptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pool=generate_pool(2500,2026100701)
        cls.target=labels(cls.pool)
        cls.audit,_=audit(cls.pool)
        cls.smask=[bool(r['scr_pass']) for r in cls.audit]
        cls.tm=[m for m,t in zip(cls.pool,cls.target) if t]
        cls.ts=[s for s,t in zip(cls.smask,cls.target) if t]
        cls.base=prepare_preservation_baseline(cls.tm)

    def test_cached_scr_preservation_identical(self):
        a=preservation(self.tm,self.ts)
        b=preservation_from_baseline(self.base,self.ts)
        for k in ('baseline_target_count','basin_count','basin_recall','min_target_survivors_per_basin','min_basin_geometric_coverage','max_basin_centroid_drift','unclustered_target_fraction','signature_strata_count','signature_stratum_recall'):
            self.assertEqual(a[k],b[k],k)

    def test_cached_null_identical(self):
        n1=sum(self.smask)
        for rep in (0,1,7):
            a=rate_matched_random(self.pool,self.target,n1,2026100701,rep)
            b=rate_matched_random_cached(self.pool,self.target,n1,2026100701,rep,self.base)
            for k in ('n_survivors','candidate_target_recall','basin_count','basin_recall','min_target_survivors_per_basin','min_basin_geometric_coverage','max_basin_centroid_drift','unclustered_target_fraction','signature_strata_count','signature_stratum_recall'):
                self.assertEqual(a[k],b[k],(rep,k))

if __name__=='__main__': unittest.main()
