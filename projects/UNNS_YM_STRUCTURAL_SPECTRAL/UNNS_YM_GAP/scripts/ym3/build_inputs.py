#!/usr/bin/env python3
from pathlib import Path
import csv, json, math

DU=0.10383
PS=[0.5,1,2,4,8]
ROOT=Path(__file__).resolve().parents[2]
MATRIX=ROOT/'docs'/'YM3_INPUT_MATRIX.csv'
BASE=ROOT/'data'/'derived'/'corr_i'/'ym3'

def slug(s): return 'b'+s.replace('.','')
def pslug(p): return 'p05' if p==0.5 else f'p{int(p)}'
def fmt(x): return format(x,'.15g')
def write(path,header,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f,lineterminator='\n'); w.writerow(header); w.writerows(rows)
def write_json(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

with open(MATRIX,newline='',encoding='utf-8') as f:
    src=list(csv.DictReader(f))
levels=[]
for i,r in enumerate(src,1):
    b=r['beta']; asig=float(r['a_sqrtsigma']); am=float(r['aM_0pp']); q=am/asig
    levels.append({'level':i,'beta':b,'a_sqrtsigma':asig,'aM_0pp':am,'q':q,'evidence':'B+C' if b=='6.5000' else 'C'})

for sub in ['common','native','fixed_gapless','matched_gapless']:
    (BASE/sub).mkdir(parents=True,exist_ok=True)
write_json(BASE/'backbone.json',{
    'project':'UNNS_YM_GAP','stage':'YM-3A','preregistration':'YM3-PREREG v0.1.0',
    'status':'INPUTS_BUILT_PRE_SCIENTIFIC_BATCH','du':DU,'points':11,'u_max':10*DU,'levels':levels
})

u=[j*DU for j in range(11)]
# Common-grid massive controls.
write(BASE/'common'/'massive_all.csv',['t']+[f"{slug(x['beta'])}_C" for x in levels],
      [[fmt(t)]+[fmt(math.exp(-x['q']*t)) for x in levels] for t in u])
for x in levels:
    ch=f"{slug(x['beta'])}_C"
    write(BASE/'common'/f"{slug(x['beta'])}.csv",['t','corr','channel'],[[fmt(t),fmt(math.exp(-x['q']*t)),ch] for t in u])
    write_json(BASE/'common'/f"{slug(x['beta'])}.json",{
        **x,'evidence_class':'C','representation':'common_physical_grid','coordinate':'u=t*sqrt(sigma)',
        'du':DU,'points':11,'formula':'C(u)=exp[-q*u]','q_definition':'aM_0pp/a_sqrtsigma',
        'source':'AT20 published fitted 0++ mass; exact mass-anchored exponential control',
        'not_measured_correlator':True
    })
# Native massive diagnostics.
write(BASE/'native'/'massive_all.csv',['t']+[f"{slug(x['beta'])}_C_native" for x in levels],
      [[str(n)]+[fmt(math.exp(-x['aM_0pp']*n)) for x in levels] for n in range(11)])
for x in levels:
    ch=f"{slug(x['beta'])}_C_native"
    write(BASE/'native'/f"{slug(x['beta'])}.csv",['t','corr','channel'],[[str(n),fmt(math.exp(-x['aM_0pp']*n)),ch] for n in range(11)])
# Fixed YM-2 Gamma references, unit-transform only.
q650=levels[-1]['q']
fixed_rows=[]
for t in u:
    row=[fmt(t)]
    for p in PS:
        theta=(math.exp(q650*DU/p)-1.0)/DU
        row.append(fmt((1+theta*t)**(-p)))
    fixed_rows.append(row)
write(BASE/'fixed_gapless'/'fixed_all.csv',['t']+[f'fixed_{pslug(p)}' for p in PS],fixed_rows)
write_json(BASE/'fixed_gapless'/'metadata.json',{
    'evidence':'synthetic positive-spectral gapless controls','role':'frozen YM-2 primary fixed references',
    'coordinate':'u=t*sqrt(sigma)','du':DU,'p':PS,'anchor_beta':'6.5000','anchor_q':q650,
    'formula':'C_p(u)=(1+theta_p*u)^(-p); theta_p=(exp(q650*du/p)-1)/du',
    'unit_transform_only':True,'retuned':False
})
# Matched 8x5 Gamma panel.
channels=[]; params=[]
for x in levels:
    for p in PS:
        theta=(math.exp(x['q']*DU/p)-1.0)/DU; ch=f"{slug(x['beta'])}_{pslug(p)}"
        channels.append((ch,p,theta)); params.append([x['beta'],fmt(x['q']),fmt(p),fmt(theta),ch])
write(BASE/'matched_gapless'/'params.csv',['beta','q','p','theta','channel'],params)
write(BASE/'matched_gapless'/'matched_all.csv',['t']+[x[0] for x in channels],
      [[fmt(t)]+[fmt((1+theta*t)**(-p)) for ch,p,theta in channels] for t in u])
for x in levels:
    cols=[(p,(math.exp(x['q']*DU/p)-1.0)/DU) for p in PS]
    write(BASE/'matched_gapless'/f"{slug(x['beta'])}.csv",['t']+[f"{slug(x['beta'])}_{pslug(p)}" for p,_ in cols],
          [[fmt(t)]+[fmt((1+theta*t)**(-p)) for p,theta in cols] for t in u])
print('YM-3A inputs built. Full scientific CORR-I batch has not been run.')
