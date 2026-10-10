from __future__ import annotations
import json
from collections import defaultdict
from scr_iii.engine_v002_common import output_root_v002, scr_iii_root, load_seeds_v002, accepted_seed_order
from scr_iii.engine_common import read_json_gz, safe_write_json
from scr_iii.analysis.estimators_v001 import sample_prefixes, solve_sampled_subtrees, mae
from scr_iii.analysis.stats_v001 import spearman


def main():
    root=output_root_v002(); p=root/"primary"/"PRIMARY_RESULT_v002.json"
    if not p.exists(): print("v002 estimators blocked: primary incomplete."); return 2
    primary=json.loads(p.read_text(encoding="utf-8")); seeds=load_seeds_v002(); out=root/"estimators"; out.mkdir(parents=True,exist_ok=True)
    cal={}; hold={}
    for d in (14,16,18):
        acc=accepted_seed_order(primary,d); cal[d]=set(acc[:5]); hold[d]=set(acc[5:])
    groups=defaultdict(list)
    for r in primary["main_cells"]: groups[(int(r["depth"]),float(r["sigma"]),float(r["q"]))].append(r)
    e1=[]
    for key,rows in sorted(groups.items()):
        d,sig,q=key; cr=[r for r in rows if int(r["seed"]) in cal[d]]; hr=[r for r in rows if int(r["seed"]) in hold[d]]
        if not cr or not hr: continue
        pred_r=sum(r["solution_recall"] for r in cr)/len(cr); ce=[r["excess_inclusion_EI"] for r in cr if r["excess_inclusion_EI"] is not None]; pred_e=sum(ce)/len(ce) if ce else None
        obs_r=sum(r["solution_recall"] for r in hr)/len(hr); he=[r["excess_inclusion_EI"] for r in hr if r["excess_inclusion_EI"] is not None]; obs_e=sum(he)/len(he) if he else None
        e1.append({"depth":d,"sigma":sig,"q":q,"pred_recall":pred_r,"obs_recall":obs_r,"pred_EI":pred_e,"obs_EI":obs_e,"cal_n":len(cr),"hold_n":len(hr)})
    e1_mae=mae([(r["pred_recall"],r["obs_recall"]) for r in e1]); e1_sp=spearman([r["pred_recall"] for r in e1],[r["obs_recall"] for r in e1]) if len(e1)>=2 else None
    e1_pass=e1_mae is not None and e1_mae<=0.10 and e1_sp is not None and e1_sp>=0.80
    e2=[]; est_seed=int(seeds["analysis_rng"]["estimator_sample_seed"])
    for r in primary["main_cells"]:
        d=int(r["depth"])
        if int(r["seed"]) not in hold[d]: continue
        inst=read_json_gz(scr_iii_root()/r["instance_path"]); prefixes=sample_prefixes(inst,8,6,est_seed); pred=solve_sampled_subtrees(inst,prefixes)
        e2.append({"cell_id":r["cell_id"],"pred_recall":pred["recall_hat"],"obs_recall":r["solution_recall"],"pred_EI":pred["EI_hat"],"obs_EI":r["excess_inclusion_EI"],"C_E2_seconds":pred["seconds"],"C_E2_over_Tbaseline":pred["seconds"]/r["seconds_baseline"] if r["seconds_baseline"]>0 else None,"sample":pred})
        if len(e2)%25==0: print("v002 E2",len(e2))
    pairs=[(x["pred_recall"],x["obs_recall"]) for x in e2 if x["pred_recall"] is not None]
    e2_mae=mae(pairs); e2_sp=spearman([x[0] for x in pairs],[x[1] for x in pairs]) if len(pairs)>=2 else None
    e2_pass=e2_mae is not None and e2_mae<=0.10 and e2_sp is not None and e2_sp>=0.80
    result={"engine":"SCR_III_ENGINE_v002","status":"COMPLETE","H4_pass":e1_pass and e2_pass,"calibration_seeds":{str(d):sorted(cal[d]) for d in cal},"E1":{"pass":e1_pass,"MAE":e1_mae,"Spearman":e1_sp,"conditions":e1},"E2":{"pass":e2_pass,"MAE":e2_mae,"Spearman":e2_sp,"cells":e2}}
    safe_write_json(out/"ESTIMATOR_RESULT_v002.json",result); print("v002 ESTIMATORS COMPLETE H4=",result["H4_pass"]); return 0

if __name__=="__main__": raise SystemExit(main())
