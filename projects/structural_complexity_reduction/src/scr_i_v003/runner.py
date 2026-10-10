from __future__ import annotations
import csv,json,platform,statistics,subprocess,sys,time
from pathlib import Path
from .mechanism import generate_pool
from .gates import audit as gate_audit, timed_chain_count
from .target_oracle import labels as target_labels, TARGET_WORK_UNITS_PER_CANDIDATE
from .basins import prepare_preservation_baseline, preservation_from_baseline, passes_frozen_requirements
from .nulls import rate_matched_random_cached
from .metrics import median,cell_verdict
from .source_lock_v003 import verify as source_verify
from .safe_io import safe_dump
ENGINE='SCR_I_ENGINE_v003'; PREREG='SCR_I_PREREG_v003'; OPT='SCR_I_V003_OPT_v001'
SEEDS=[2026101001,2026101002,2026101003,2026101004,2026101005]; SIZES=[2500,10000,40000]


def dump(p,o):
    safe_dump(p,o)

def marker_ok(p):
    try:return p.is_file() and bool(json.loads(p.read_text(encoding='utf-8')).get('ok'))
    except:return False

def validate(root):
    p=subprocess.run([sys.executable,str(root/PREREG/'scripts'/'validate_prereg.py')],cwd=str(root/PREREG),capture_output=True,text=True);return p.returncode==0,p.stdout+p.stderr

def preflight(root):
    s=source_verify(root); okp,log=validate(root); d=root/'output'/'v003_phase1'/'DESIGN_PRESERVATION_AUDIT_PASS.json'
    return {'source_lock_ok':s.get('ok',False),'prereg_ok':okp,'design_preservation_audit_ok':marker_ok(d),'source_lock':s,'prereg_log':log,'ok':bool(s.get('ok')) and okp and marker_ok(d)}

def target_and_baseline(pool,scrmask):
    target=target_labels(pool); tm=[];sm=[]
    for m,t,s in zip(pool,target,scrmask):
        if t: tm.append(m); sm.append(bool(s))
    baseline=prepare_preservation_baseline(tm)
    p=preservation_from_baseline(baseline,sm,include_details=False)
    p['candidate_target_recall']=(sum(sm)/len(sm)) if sm else None
    return target,baseline,p

def time_base(pool):
    t=time.perf_counter();target_labels(pool);return time.perf_counter()-t

def time_scr(pool):
    t0=time.perf_counter(); surv=[];q=0
    for m in pool:
        ok,_,n=timed_chain_count(m);q+=n
        if ok:surv.append(m)
    t1=time.perf_counter();target_labels(surv);t2=time.perf_counter();return t2-t0,t1-t0,t2-t1,len(surv),q

def checkpoint_default():
    return {'engine':ENGINE,'preregistration':PREREG,'optimization':OPT,'version':1,'completed_cells':[],
            'records':[],'nullrows':[],'timing':[],'gate_summary':[],'active':None}

def load_checkpoint(path:Path):
    if not path.exists(): return checkpoint_default()
    try:c=json.loads(path.read_text(encoding='utf-8'))
    except Exception: raise RuntimeError(f'Cannot read v003 checkpoint: {path}')
    if c.get('engine')!=ENGINE or c.get('preregistration')!=PREREG:
        raise RuntimeError('Checkpoint belongs to a different engine/preregistration; move or delete it before running')
    c.setdefault('optimization',OPT); c.setdefault('completed_cells',[]); c.setdefault('records',[]); c.setdefault('nullrows',[]); c.setdefault('timing',[]); c.setdefault('gate_summary',[]); c.setdefault('active',None)
    return c

def save_checkpoint(path:Path,c:dict): dump(path,c)

def set_progress(path:Path,**kw):
    state={'engine':ENGINE,'optimization':OPT,'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**kw}
    dump(path,state)

def key(seed,size): return f'{seed}:{size}'

def _remove_incomplete_cell_rows(c,seed,size):
    if key(seed,size) in set(c['completed_cells']): return
    c['timing']=[r for r in c['timing'] if not (r.get('seed')==seed and r.get('pool_size')==size)]
    # Null rows are intentionally retained: deterministic completed replicates are resumable.

def _existing_null_reps(c,seed,size):
    return {int(r['replicate']) for r in c['nullrows'] if r.get('seed')==seed and r.get('pool_size')==size}

def _write_outputs(out:Path,c:dict,final:bool=False):
    records=c['records']; nullrows=c['nullrows']; timing=c['timing']; gate_summary=c['gate_summary']
    if final: dump(out/'PRIMARY_RESULT_v003.json',records)
    for name,rows,cols in [
      ('null_results_v003.csv',nullrows,['seed','pool_size','replicate','n_survivors','basin_recall','min_basin_geometric_coverage','max_basin_centroid_drift','signature_stratum_recall','candidate_target_recall']),
      ('timing_trials_v003.csv',timing,['seed','pool_size','repeat','arm','seconds','filter_seconds','downstream_seconds']),
      ('gate_audit_v003.csv',gate_summary,['seed','n','survivors','rejected','timed_gate_evals','first_G1','first_G2','first_G3','first_G4'])]:
        with (out/name).open('w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows({k:r.get(k,'') for k in cols} for r in rows)

def run(root:Path):
    out=root/'output'; result=out/'PRIMARY_RESULT_v003.json'; checkpoint=out/'checkpoints'/'SCR_I_A_v003_checkpoint.json'; progress=out/'RUN_PROGRESS_v003.json'
    if (result.with_suffix(result.suffix+'.sha256')).exists():raise RuntimeError('v003 primary result is frozen; refusing overwrite')
    if result.exists() and not checkpoint.exists(): raise RuntimeError('PRIMARY_RESULT_v003.json already exists without an active checkpoint; archive/freeze it before another run')
    pf=preflight(root);dump(out/'PRE_FLIGHT_v003.json',pf)
    if not pf['ok']:raise RuntimeError('v003 preflight failed; see output/PRE_FLIGHT_v003.json')
    c=load_checkpoint(checkpoint); save_checkpoint(checkpoint,c)
    completed=set(c['completed_cells']); total_cells=len(SEEDS)*len(SIZES)
    set_progress(progress,status='RUNNING',phase='preflight',completed_cells=len(completed),total_cells=total_cells,message='v003 optimized primary run starting/resuming')
    for si,seed in enumerate(SEEDS):
        seed_done=all(key(seed,s) in completed for s in SIZES)
        if seed_done:
            print(f'[v003 seed {seed}] all cells already checkpointed; skipping',flush=True); continue
        print(f'[v003 seed {seed}] generating 40000 candidates',flush=True)
        set_progress(progress,status='RUNNING',phase='generate_pool',seed=seed,completed_cells=len(completed),total_cells=total_cells)
        pool=generate_pool(40000,seed); aud,asum=gate_audit(pool); passmask=[bool(r['scr_pass']) for r in aud]
        if not any(r.get('seed')==seed for r in c['gate_summary']):
            c['gate_summary'].append({'seed':seed,'n':asum['n'],'survivors':asum['survivors'],'rejected':asum['rejected'],'timed_gate_evals':asum['timed_gate_evals'],**{f'first_{g}':asum['first_reject'][g] for g in ('G1','G2','G3','G4')}})
            save_checkpoint(checkpoint,c)
        for size in SIZES:
            ck=key(seed,size)
            if ck in completed:
                print(f'  [size {size}] checkpoint complete; skipping',flush=True); continue
            cell_index=SEEDS.index(seed)*len(SIZES)+SIZES.index(size)+1
            print(f'  [cell {cell_index}/{total_cells}] seed={seed} size={size}: preparing cached target-basin geometry',flush=True)
            c['active']={'seed':seed,'pool_size':size,'stage':'baseline_geometry'}; save_checkpoint(checkpoint,c)
            set_progress(progress,status='RUNNING',phase='baseline_geometry',seed=seed,pool_size=size,cell=cell_index,total_cells=total_cells,completed_cells=len(completed))
            sub=pool[:size];smask=passmask[:size];target,baseline,p=target_and_baseline(sub,smask);n1=sum(smask);rcan=1-n1/size;presok=passes_frozen_requirements(p)
            qgate=sum(int(aud[i]['timed_gate_evals']) for i in range(size));cbase=size*TARGET_WORK_UNITS_PER_CANDIDATE;cscr=qgate+n1*TARGET_WORK_UNITS_PER_CANDIDATE;gops=cbase/cscr if cscr else None
            _remove_incomplete_cell_rows(c,seed,size)
            print(f'    targets={sum(target)} survivors={n1} basins={p["basin_count"]}; running timing trials',flush=True)
            set_progress(progress,status='RUNNING',phase='timing',seed=seed,pool_size=size,cell=cell_index,total_cells=total_cells,completed_cells=len(completed),target_count=sum(target),survivors=n1,basin_count=p['basin_count'])
            time_base(sub);time_scr(sub);bt=[];st=[];ft=[];dt=[]
            order=('baseline','scr') if si%2==0 else ('scr','baseline')
            for rep in range(5):
                for arm in order:
                    if arm=='baseline':x=time_base(sub);bt.append(x);c['timing'].append({'seed':seed,'pool_size':size,'repeat':rep+1,'arm':'baseline','seconds':x})
                    else:tt,tf,td,_,_=time_scr(sub);st.append(tt);ft.append(tf);dt.append(td);c['timing'].append({'seed':seed,'pool_size':size,'repeat':rep+1,'arm':'scr','seconds':tt,'filter_seconds':tf,'downstream_seconds':td})
            save_checkpoint(checkpoint,c)
            gtime=median(bt)/median(st) if median(st)>0 else None
            row={'engine':ENGINE,'preregistration':PREREG,'optimization':OPT,'benchmark':'SCR-I-A','pool_size':size,'seed':seed,'n0':size,'n1':n1,'target_count_base':sum(target),'candidate_target_recall':p['candidate_target_recall'],'r_candidate':rcan,'r_eval':rcan,'g_time':gtime,'g_ops':gops,'t_base_median':median(bt),'t_scr_median':median(st),'t_filter_median':median(ft),'t_downstream_scr_median':median(dt),**{k:p[k] for k in ['basin_count','basin_recall','min_target_survivors_per_basin','min_basin_geometric_coverage','max_basin_centroid_drift','unclustered_target_fraction','signature_strata_count','signature_stratum_recall']}}
            row['verdict']=cell_verdict(row['target_count_base'],presok,rcan)
            reps=100 if size==10000 else 30; existing=_existing_null_reps(c,seed,size)
            print(f'    nulls: {len(existing)}/{reps} already checkpointed; cached baseline geometry will be reused',flush=True)
            for ri in range(reps):
                if ri in existing: continue
                nr=rate_matched_random_cached(sub,target,n1,seed,ri,baseline);c['nullrows'].append({'seed':seed,'pool_size':size,'replicate':ri,'n_survivors':n1,'basin_recall':nr['basin_recall'],'min_basin_geometric_coverage':nr['min_basin_geometric_coverage'],'max_basin_centroid_drift':nr['max_basin_centroid_drift'],'signature_stratum_recall':nr['signature_stratum_recall'],'candidate_target_recall':nr['candidate_target_recall']})
                done_null=sum(1 for r in c['nullrows'] if r.get('seed')==seed and r.get('pool_size')==size)
                c['active']={'seed':seed,'pool_size':size,'stage':'nulls','null_done':done_null,'null_total':reps}
                save_checkpoint(checkpoint,c)
                set_progress(progress,status='RUNNING',phase='nulls',seed=seed,pool_size=size,cell=cell_index,total_cells=total_cells,completed_cells=len(completed),null_done=done_null,null_total=reps,target_count=sum(target),survivors=n1,basin_count=p['basin_count'])
                if done_null==1 or done_null%10==0 or done_null==reps: print(f'      null {done_null}/{reps}',flush=True)
            c['records']=[r for r in c['records'] if not (r.get('seed')==seed and r.get('pool_size')==size)];c['records'].append(row)
            c['completed_cells'].append(ck);completed.add(ck);c['active']=None;save_checkpoint(checkpoint,c);_write_outputs(out,c,final=False)
            print(f'    COMPLETE verdict={row["verdict"]} reduction={row["r_candidate"]:.4f} basin_recall={row["basin_recall"]}',flush=True)
            set_progress(progress,status='RUNNING',phase='cell_complete',seed=seed,pool_size=size,cell=cell_index,total_cells=total_cells,completed_cells=len(completed),last_verdict=row['verdict'])
    _write_outputs(out,c,final=True)
    dump(out/'RUN_ENVIRONMENT_v003.json',{'engine':ENGINE,'preregistration':PREREG,'optimization':OPT,'python':sys.version,'platform':platform.platform(),'timestamp_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'primary_seeds':SEEDS,'pool_sizes':SIZES,'resume_checkpoint':str(checkpoint.relative_to(root))})
    records=c['records']; verdicts=sorted(set(r['verdict'] for r in records));lines=['# SCR-I-A v003 primary summary','',f'- Engine: {ENGINE}',f'- Optimization: {OPT} (implementation-only cache + resume)',f'- Cells: {len(records)}',f'- Verdicts: {", ".join(verdicts)}',f'- Minimum basin recall: {min(r["basin_recall"] for r in records if r["basin_recall"] is not None)}',f'- Minimum basin coverage: {min(r["min_basin_geometric_coverage"] for r in records if r["min_basin_geometric_coverage"] is not None)}',f'- Maximum centroid drift: {max(r["max_basin_centroid_drift"] for r in records if r["max_basin_centroid_drift"] is not None)}',f'- Median candidate reduction: {statistics.median(r["r_candidate"] for r in records)}','']
    (out/'SUMMARY_v003.md').write_text('\n'.join(lines),encoding='utf-8')
    set_progress(progress,status='COMPLETE',phase='complete',completed_cells=len(completed),total_cells=total_cells,message='SCR-I-A v003 optimized primary run complete')
    completed_cp=checkpoint.with_name('SCR_I_A_v003_checkpoint.completed.json')
    if completed_cp.exists(): completed_cp.unlink()
    checkpoint.replace(completed_cp)
    return records
