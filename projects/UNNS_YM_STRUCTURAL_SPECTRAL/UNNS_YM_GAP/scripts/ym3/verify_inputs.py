#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, hashlib, sys
ROOT=Path(__file__).resolve().parents[2]
DU=0.10383
PS=[0.5,1,2,4,8]
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def read(path):
 with open(path,newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def slug(s): return 'b'+s.replace('.','')
def pslug(p): return 'p05' if p==0.5 else f'p{int(p)}'
checks=[]
def ck(name,ok,detail=''): checks.append({'check':name,'pass':bool(ok),'detail':detail})
ck('CORR-I SHA256',sha(ROOT/'chambers/corr_i/corr_i_v012.html')=='f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2')
ck('PREREG SHA256',sha(ROOT/'docs/PREREG_YM3.md')=='d36a47fe047577d13264188abbec30ed5b20da5eae964727d2a23f7f7febf61d')
ck('INPUT MATRIX SHA256',sha(ROOT/'docs/YM3_INPUT_MATRIX.csv')=='c9b1266f1b59805d80cea477696ef9f63953277e93ebb441109400acda950bbe')
mat=read(ROOT/'docs/YM3_INPUT_MATRIX.csv')
# Every common input obeys the frozen equation.
for r in mat:
 s=slug(r['beta']); q=float(r['aM_0pp'])/float(r['a_sqrtsigma']); rr=read(ROOT/f'data/derived/corr_i/ym3/common/{s}.csv')
 err=max(abs(float(x['corr'])-math.exp(-q*float(x['t']))) for x in rr)
 ck(f'{s} common formula',len(rr)==11 and err<5e-14,f'max_abs_diff={err:.3e}')
# beta 6.50 massive sample identity.
new=read(ROOT/'data/derived/corr_i/ym3/common/b65000.csv'); old=read(ROOT/'data/derived/corr_i/at20_0pp_b650_control/corr.csv')
maxdc=max(abs(float(a['corr'])-float(b['corr'])) for a,b in zip(new,old))
ck('beta6.50 common sampled C matches frozen YM-2 massive control',len(new)==len(old)==11 and maxdc<5e-14,f'max_abs_diff={maxdc:.3e}')
# fixed gamma references must reproduce the frozen YM-2 samples after unit transformation.
fixed=read(ROOT/'data/derived/corr_i/ym3/fixed_gapless/fixed_all.csv')
oldmap={
 'p05':ROOT/'data/derived/corr_i/gapless_family/p05.csv',
 'p1':ROOT/'data/derived/corr_i/gapless_control/corr.csv',
 'p2':ROOT/'data/derived/corr_i/gapless_family/p2.csv',
 'p4':ROOT/'data/derived/corr_i/gapless_family/p4.csv',
 'p8':ROOT/'data/derived/corr_i/gapless_family/p8.csv'}
for k,path in oldmap.items():
 old=read(path); col='fixed_'+k
 # old family files use corr or channel-specific value column; find numeric non-time column.
 if 'corr' in old[0]: vals=[float(x['corr']) for x in old]
 else:
  keys=[x for x in old[0].keys() if x.lower() not in ('t','time','channel')]
  vals=[float(x[keys[0]]) for x in old]
 err=max(abs(float(a[col])-b) for a,b in zip(fixed,vals))
 ck(f'fixed {k} reproduces YM-2 samples',len(fixed)==len(vals)==11 and err<5e-14,f'max_abs_diff={err:.3e}')
# beta 6.50 matched panel equals fixed panel (same preregistered anchor).
m650=read(ROOT/'data/derived/corr_i/ym3/matched_gapless/b65000.csv')
for p in PS:
 k=pslug(p); err=max(abs(float(a[f'b65000_{k}'])-float(b[f'fixed_{k}'])) for a,b in zip(m650,fixed))
 ck(f'beta6.50 matched {k} equals fixed reference',err<5e-14,f'max_abs_diff={err:.3e}')
status='PASS' if all(x['pass'] for x in checks) else 'FAIL'
out={'status':status,'scientific_batch_run':False,'checks':checks}
path=ROOT/'output/ym3/checksum/input_verify.json'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2)); sys.exit(0 if status=='PASS' else 1)
