from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.scr_i_v003.design_audit import run
r=run(ROOT)
print('V003 DESIGN-PRESERVATION AUDIT:', 'PASS' if r['ok'] else 'FAIL')
for x in r['rows']:
    print({k:x[k] for k in ['seed','target_count','survivors','adapter_match','candidate_target_recall','basin_count','basin_recall','min_target_survivors_per_basin','min_basin_geometric_coverage','max_basin_centroid_drift','signature_stratum_recall','preservation_pass']})
raise SystemExit(0 if r['ok'] else 1)
