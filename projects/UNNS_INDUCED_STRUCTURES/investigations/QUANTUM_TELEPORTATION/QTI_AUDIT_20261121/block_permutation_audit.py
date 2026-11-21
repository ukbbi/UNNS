import csv, json
from pathlib import Path
import sys
import numpy as np
root=(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'QUANTUM_TELEPORTATION')/'results'
files=['iPsiM_156p45_tot','iPsiP_156p45_tot','iPsiM_156p95_tot']
rng=np.random.default_rng(20261121)
B=1400
res={}
for fn in files:
 rows=list(csv.DictReader(open(root/(fn+'_gaps.csv'))))
 # Blocks of 128 consecutive gap records; excluded records break adjacency
 blocks=[]
 for off in range(0,len(rows),128):
  arr=[int(r['max_square_root_divisor']) if r['included']=='yes' else -1 for r in rows[off:off+128]]
  # split at invalid gaps
  run=[]
  for v in arr+[-1]:
   if v == -1:
    if len(run)>=2: blocks.append(np.array(run,dtype=np.int64))
    run=[]
   else: run.append(v)
 obs=sum(int(np.count_nonzero(np.gcd(a[:-1],a[1:])>1)) for a in blocks)
 obs_b=sum(int(np.count_nonzero((a[:-1]>1)&(a[1:]>1))) for a in blocks)
 vals=np.empty(B,dtype=np.int64); valb=np.empty(B,dtype=np.int64)
 for b in range(B):
  c=0;d=0
  for a in blocks:
   aa=a[rng.permutation(len(a))]
   c+=np.count_nonzero(np.gcd(aa[:-1],aa[1:])>1)
   d+=np.count_nonzero((aa[:-1]>1)&(aa[1:]>1))
  vals[b]=c; valb[b]=d
 def summarize(obs, vv):
  avg=float(vv.mean()); sd=float(vv.std(ddof=1))
  z=(obs-avg)/sd
  p=(1+int(np.count_nonzero(abs(vv-avg)>=abs(obs-avg))))/(len(vv)+1)
  return dict(obs=int(obs),null_mean=round(avg,3),null_sd=round(sd,3),z=round(z,3),p_two_sided_empirical=round(p,4))
 res[fn]=dict(n_blocks=len(blocks),n_adj_pairs=sum(len(a)-1 for a in blocks),shared_nest=summarize(obs,vals),both_nonempty=summarize(obs_b,valb))
 print(fn,res[fn],flush=True)
with open(Path(__file__).resolve().parent/'block_permutation_audit.json','w') as f: json.dump(res,f,indent=2)
