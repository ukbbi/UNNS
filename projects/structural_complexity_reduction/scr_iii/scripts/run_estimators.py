from __future__ import annotations
import json
from collections import defaultdict
from scr_iii.engine_common import scr_iii_root, read_json_gz, safe_write_json
from scr_iii.analysis.estimators_v001 import sample_prefixes, solve_sampled_subtrees, mae
from scr_iii.analysis.stats_v001 import spearman


def main():
    s3=scr_iii_root(); p=s3/'output'/'primary'/'PRIMARY_RESULT_v001.json'
    if not p.exists(): print('Estimators blocked: primary incomplete.'); return 2
    primary=json.loads(p.read_text()); seeds=json.loads((s3/'SCR_III_PREREG_v001'/'SEEDS_v001.json').read_text())
    out=s3/'output'/'estimators'; out.mkdir(parents=True,exist_ok=True)
    cal={d:set(seeds['primary'][f'depth_{d}'][:5]) for d in (14,16,18)}
    hold={d:set(seeds['primary'][f'depth_{d}'][5:]) for d in (14,16,18)}
    groups=defaultdict(list)
    for r in primary['main_cells']: groups[(int(r['depth']),float(r['sigma']),float(r['q']))].append(r)
    e1=[]
    for key,rows in sorted(groups.items()):
        d,sig,q=key; cr=[r for r in rows if int(r['seed']) in cal[d]]; hr=[r for r in rows if int(r['seed']) in hold[d]]
        if not cr or not hr: continue
        pred_r=sum(r['solution_recall'] for r in cr)/len(cr); pred_e=sum(r['excess_inclusion_EI'] for r in cr if r['excess_inclusion_EI'] is not None)/max(1,sum(r['excess_inclusion_EI'] is not None for r in cr))
        obs_r=sum(r['solution_recall'] for r in hr)/len(hr); evals=[r['excess_inclusion_EI'] for r in hr if r['excess_inclusion_EI'] is not None]; obs_e=sum(evals)/len(evals) if evals else None
        e1.append({"depth":d,"sigma":sig,"q":q,"pred_recall":pred_r,"obs_recall":obs_r,"pred_EI":pred_e,"obs_EI":obs_e})
    e1_mae=mae([(r['pred_recall'],r['obs_recall']) for r in e1]); e1_sp=spearman([r['pred_recall'] for r in e1],[r['obs_recall'] for r in e1])
    e1_pass=e1_mae is not None and e1_mae<=0.10 and e1_sp is not None and e1_sp>=0.80
    e2=[]; est_seed=int(seeds['estimator_sample_seed'])
    for i,r in enumerate(primary['main_cells'],1):
        d=int(r['depth']);
        if int(r['seed']) not in hold[d]: continue
        inst=read_json_gz(s3/r['instance_path']); prefixes=sample_prefixes(inst,8,6,est_seed); pred=solve_sampled_subtrees(inst,prefixes)
        e2.append({"cell_id":r['cell_id'],"pred_recall":pred['recall_hat'],"obs_recall":r['solution_recall'],"pred_EI":pred['EI_hat'],"obs_EI":r['excess_inclusion_EI'],"C_E2_seconds":pred['seconds'],"C_E2_over_Tbaseline":pred['seconds']/r['seconds_baseline'] if r['seconds_baseline']>0 else None,"sample":pred})
        if len(e2)%25==0: print('E2',len(e2))
    pairs=[(x['pred_recall'],x['obs_recall']) for x in e2 if x['pred_recall'] is not None]
    e2_mae=mae(pairs); e2_sp=spearman([x[0] for x in pairs],[x[1] for x in pairs]) if len(pairs)>=2 else None
    e2_pass=e2_mae is not None and e2_mae<=0.10 and e2_sp is not None and e2_sp>=0.80
    result={"engine":"SCR_III_ENGINE_v001","status":"COMPLETE","H4_pass":e1_pass and e2_pass,"E1":{"pass":e1_pass,"MAE":e1_mae,"Spearman":e1_sp,"conditions":e1},"E2":{"pass":e2_pass,"MAE":e2_mae,"Spearman":e2_sp,"cells":e2}}
    safe_write_json(out/'ESTIMATOR_RESULT_v001.json',result); print('ESTIMATORS COMPLETE H4=',result['H4_pass']); return 0
if __name__=='__main__': raise SystemExit(main())
