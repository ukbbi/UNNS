from __future__ import annotations
from pathlib import Path
import json
from .mechanism import generate_pool
from .gates import audit
from .target_oracle import labels
from .basins import preservation, passes_frozen_requirements

DESIGN_SEEDS=[2026100701,2026100702,2026100703,2026100704,2026100705]
EXPECTED={
  2026100701:(5252,775),2026100702:(5294,791),2026100703:(5297,806),2026100704:(5243,809),2026100705:(5271,813)
}

def run(root:Path)->dict:
    rows=[]; all_ok=True
    for seed in DESIGN_SEEDS:
        pool=generate_pool(10000,seed); target=labels(pool); gates,_=audit(pool); scr=[bool(r['scr_pass']) for r in gates]
        tc=sum(target); sc=sum(scr); exp=EXPECTED[seed]; adapter_match=(tc,sc)==exp
        target_mechs=[]; target_surv=[]
        for m,t,s in zip(pool,target,scr):
            if t: target_mechs.append(m); target_surv.append(s)
        p=preservation(target_mechs,target_surv); preserve=passes_frozen_requirements(p)
        cand_recall=sum(target_surv)/len(target_surv) if target_surv else None
        row={'seed':seed,'target_count':tc,'expected_target_count':exp[0],'survivors':sc,'expected_survivors':exp[1],'adapter_match':adapter_match,'candidate_target_recall':cand_recall,**p,'preservation_pass':preserve}
        rows.append(row); all_ok=all_ok and adapter_match and preserve
    rec={'ok':all_ok,'audit':'SCR-I v003 design preservation','primary_seeds_inspected':False,'design_seeds':DESIGN_SEEDS,'rows':rows}
    out=root/'output'/'v003_phase1'; out.mkdir(parents=True,exist_ok=True)
    (out/'DESIGN_PRESERVATION_AUDIT.json').write_text(json.dumps(rec,indent=2,allow_nan=False),encoding='utf-8')
    if all_ok:(out/'DESIGN_PRESERVATION_AUDIT_PASS.json').write_text(json.dumps(rec,indent=2,allow_nan=False),encoding='utf-8')
    return rec
