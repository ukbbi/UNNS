from pathlib import Path
import json, sys
root=Path(__file__).resolve().parents[1]
try:
    c=json.loads((root/'config'/'scr_i_prereg_v003.json').read_text(encoding='utf-8'))
    assert c['preregistration_id']=='SCR_I_PREREG_v003'
    assert c['status']=='FROZEN_BEFORE_PRIMARY'
    assert c['gate_order']==['G1','G2','G3','G4']
    assert c['candidate_pool']['primary_seeds']==[2026101001,2026101002,2026101003,2026101004,2026101005]
    assert not (set(c['candidate_pool']['design_audit_seeds']) & set(c['candidate_pool']['primary_seeds']))
    b=c['basin_definition']; assert b['eps']==0.25 and b['min_neighbors']==20 and b['strict_distance'] is True
    r=c['primary_preservation_requirements']
    assert r['basin_recall']==1.0
    assert r['minimum_target_survivors_per_basin']==20
    assert r['minimum_within_basin_geometric_coverage']==0.95
    assert r['coverage_radius']==0.25
    assert r['maximum_normalized_centroid_drift']==0.125
    assert r['maximum_unclustered_target_fraction']==0.05
    assert r['signature_stratum_recall']==1.0
    required=['PREREG.md','BENCH_A.md','BASIN_ORACLE.md','DESIGN_AUDIT.md','DECISION_RULES.md','METRICS.md','GATES.md','NULLS.md','RUN_PLAN.md','SOURCE_LOCK.md','UPI_BLIND.md','V002_TRANSITION.md']
    for n in required: assert (root/n).is_file(), n
    print('SCR-I PREREG v003: PASS')
except Exception as e:
    print('SCR-I PREREG v003: FAIL:',e,file=sys.stderr); raise SystemExit(1)
