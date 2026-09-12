#!/usr/bin/env python3
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np
import pandas as pd


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()


def load_cfg(root):
    return json.loads((root/'05_METHODS/drive_torus_config_v002.json').read_text(encoding='utf-8'))


def make_features(x, freqs):
    cols=[np.ones_like(x,dtype=float)]
    for f in freqs:
        ph=2*np.pi*f*x
        cols.append(np.cos(ph)); cols.append(np.sin(ph))
    return np.column_stack(cols)


def ridge_fit(X,y,alpha):
    a=X.T@X
    reg=np.eye(a.shape[0])*alpha
    reg[0,0]=0.0
    return np.linalg.solve(a+reg,X.T@y)


def blocked_cv_r2(x,y,freqs,k,alpha):
    n=len(x)
    bounds=np.linspace(0,n,k+1,dtype=int)
    fold=[]
    for i in range(k):
        test=np.zeros(n,dtype=bool)
        test[bounds[i]:bounds[i+1]]=True
        train=~test
        beta=ridge_fit(make_features(x[train],freqs),y[train],alpha)
        pred=make_features(x[test],freqs)@beta
        ss=float(np.sum((y[test]-np.mean(y[test]))**2))
        r2=float(1-np.sum((y[test]-pred)**2)/(ss+1e-30))
        fold.append(r2)
    return float(np.mean(fold)),float(np.std(fold,ddof=0)),fold


def basis(depth,ratio):
    # Minimal complete first-order basis on a d-fold cover of the two source clocks.
    # Axis terms: L/d, R/d. Mixed terms: |R-L|/d and (R+L)/d.
    axis=[1.0/depth,ratio/depth]
    mixed=[abs(ratio-1.0)/depth,(ratio+1.0)/depth]
    return axis,mixed


def eval_depth(x,y,depth,cfg,ratio=None):
    ratio=float(cfg['source_ratio'] if ratio is None else ratio)
    axis,mixed=basis(depth,ratio)
    ar2,asd,afolds=blocked_cv_r2(x,y,axis,cfg['cv_folds'],cfg['ridge_alpha'])
    fr2,fsd,ffolds=blocked_cv_r2(x,y,axis+mixed,cfg['cv_folds'],cfg['ridge_alpha'])
    return {
        'depth':int(depth),
        'axis_freqs_cycles_per_source_time':[float(v) for v in axis],
        'mixed_freqs_cycles_per_source_time':[float(v) for v in mixed],
        'axis_r2_cv':ar2,'axis_r2_cv_sd':asd,
        'full_r2_cv':fr2,'full_r2_cv_sd':fsd,
        'mixed_interaction_gain':float(fr2-ar2),
        'axis_fold_r2':[float(v) for v in afolds],
        'full_fold_r2':[float(v) for v in ffolds]
    }


def load_record(root,corpus_row):
    p=root/corpus_row['file']
    df=pd.read_csv(p)
    if 'time' not in df.columns or 'S' not in df.columns:
        raise ValueError(f'Expected time,S in {p}')
    x=df['time'].to_numpy(float); y=df['S'].to_numpy(float)
    ok=np.isfinite(x)&np.isfinite(y)
    return x[ok],y[ok]


def perturb_cases(x,y,cfg):
    yield 'BASE',x,y
    for f in cfg['robustness']['downsample_factors']:
        yield f'DOWNSAMPLE_{f}',x[::int(f)],y[::int(f)]
    for frac in cfg['robustness']['prefix_fractions']:
        n=max(100,int(round(len(x)*float(frac))))
        yield f'PREFIX_{frac:.2f}',x[:n],y[:n]
    for sig in cfg['robustness']['noise_sigma_fractions']:
        rng=np.random.default_rng(cfg['seed'])
        yn=y+rng.normal(0,float(sig)*(np.std(y)+1e-30),size=len(y))
        yield f'NOISE_{sig:.3f}SD',x,yn


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='.')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    cfg=load_cfg(root)
    corpus=pd.read_csv(root/'04_CORPUS/CORPUS_v001.csv')
    corpus=corpus.set_index('id',drop=False)
    out=root/'08_OUTPUTS/DRIVE_TORUS_v002'
    details=out/'RECORD_DETAILS'
    details.mkdir(parents=True,exist_ok=True)

    results=[]; cover_rows=[]; robust_rows=[]
    for rid in cfg['scope_ids']:
        row=corpus.loc[rid]
        if row['status']!='INGESTED':
            raise RuntimeError(f'{rid} is not INGESTED')
        x,y=load_record(root,row)
        scans=[eval_depth(x,y,d,cfg) for d in cfg['cover_depths']]
        for s in scans:
            cover_rows.append({'id':rid,'role':row['role'],'regime':row['regime'],**{k:v for k,v in s.items() if not isinstance(v,list)}})
        ordered=sorted(scans,key=lambda z:z['full_r2_cv'],reverse=True)
        best=ordered[0]; second=ordered[1]
        result={
            'id':rid,'role':row['role'],'regime':row['regime'],'N':int(rid.split('N')[-1]),
            'n':int(len(y)),'source_ratio':float(cfg['source_ratio']),
            'source_time_start':float(x[0]),'source_time_end':float(x[-1]),
            'best_cover_depth':int(best['depth']),
            'best_full_r2_cv':float(best['full_r2_cv']),
            'best_axis_r2_cv':float(best['axis_r2_cv']),
            'mixed_interaction_gain':float(best['mixed_interaction_gain']),
            'cover_depth_margin':float(best['full_r2_cv']-second['full_r2_cv']),
            'coupling_mean_S':float(np.mean(y)),
            'coupling_median_S':float(np.median(y)),
            'coupling_std_S':float(np.std(y)),
            'coupling_final_S':float(y[-1])
        }
        results.append(result)
        recdetail={'summary':result,'cover_scan':scans}
        (details/f'{rid}.json').write_text(json.dumps(recdetail,indent=2),encoding='utf-8')

        # Robustness is intentionally evaluated at the automatically selected cover depth,
        # without re-selecting depth under each perturbation.
        dstar=best['depth']
        for label,xp,yp in perturb_cases(x,y,cfg):
            ev=eval_depth(xp,yp,dstar,cfg)
            robust_rows.append({
                'id':rid,'role':row['role'],'case':label,'fixed_depth':int(dstar),'n':int(len(yp)),
                'axis_r2_cv':ev['axis_r2_cv'],'full_r2_cv':ev['full_r2_cv'],
                'mixed_interaction_gain':ev['mixed_interaction_gain'],
                'mean_S':float(np.mean(yp))
            })

    rdf=pd.DataFrame(results)
    cdf=pd.DataFrame(cover_rows)
    bdf=pd.DataFrame(robust_rows)
    rdf.to_csv(out/'DRIVE_TORUS_RESULTS.csv',index=False)
    cdf.to_csv(out/'COVER_SCAN.csv',index=False)
    bdf.to_csv(out/'ROBUSTNESS_RESULTS.csv',index=False)
    (out/'DRIVE_TORUS_RESULTS.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    (out/'COVER_SCAN.json').write_text(json.dumps(cover_rows,indent=2),encoding='utf-8')
    (out/'ROBUSTNESS_RESULTS.json').write_text(json.dumps(robust_rows,indent=2),encoding='utf-8')

    audit={
        'version':cfg['version'],'status':'PASS_DIAGNOSTIC_ONLY','records':len(results),
        'scope':'Luo Fig.3 entanglement time-domain records only',
        'classification_thresholds':0,'verdicts_emitted':0,
        'c003_loaded':False,'zhu_holdout_loaded':False,'moon_loaded':False,
        'm_or_f_records_loaded':False,
        'source_ratio_used':cfg['source_ratio'],'cover_depths_scanned':cfg['cover_depths'],
        'basis_order':cfg['basis_order'],'cv_folds':cfg['cv_folds'],
        'results_sha256':sha256(out/'DRIVE_TORUS_RESULTS.csv'),
        'cover_scan_sha256':sha256(out/'COVER_SCAN.csv'),
        'robustness_sha256':sha256(out/'ROBUSTNESS_RESULTS.csv')
    }
    (out/'DRIVE_TORUS_AUDIT.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
    print(json.dumps(audit,indent=2))

if __name__=='__main__':
    main()
