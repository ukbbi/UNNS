import csv,json,hashlib
from pathlib import Path
import sys
from sympy import factorint
root=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'QUANTUM_TELEPORTATION'
files=['iPsiM_156p45_tot','iPsiP_156p45_tot','iPsiM_156p95_tot']
results=json.load(open(root/'results/results.json'))
agg={}; total=0
for fn in files:
 rows=list(csv.DictReader(open(root/'results'/f'{fn}_gaps.csv')))
 n=0; meanR=0; positive=0;maxr=0; mismatch=0; raw_4=True
 for r in rows:
  if r['included']!='yes': continue
  x=int(r['inferred_counter_gap']); raw=int(r['raw_gap']);f=factorint(x)
  R=1;q=1
  for p,e in f.items(): R*=e//2+1; q*=int(p)**(e//2)
  R-=1
  if R!=int(r['UNNS_R']) or q!=int(r['max_square_root_divisor']): mismatch+=1
  n+=1; meanR+=R; positive+=(R>0);maxr=max(maxr,R);raw_4 &= (raw%4==0)
 rj=results['files'][fn+'.pt'];
 assert mismatch==0 and n==rj['gaps_analyzed'] and meanR/n ==rj['counter_R_mean'] and abs(positive/n-rj['counter_R_positive_rate'])<1e-15
 agg[fn]=dict(gaps=n,rate=positive/n,meanR=meanR/n,maxR=maxr,all_raw_div4=raw_4,independent_mismatch=mismatch)
 total+=n
X=3000
count=[1]*(X+1);count[0]=0
for src in range(1,X+1):
 for N in range(1,src+1):
  if src%N==0:
   y=(src//N)*(N+1)**2
   if y<=X: count[y]+=count[src]
# independent incoming recurrence using square divisor d, backwards induction
h=[0]*(X+1)
for x in range(1,X+1):
 h[x]=1+sum(h[x//(m*m)*(m-1)] for m in range(2,int(x**.5)+1) if x%(m*m)==0)
assert all(count[i]==h[i] for i in range(1,X+1))
agg['cross_stream_n']=total
agg['independent_history_dp_checked']=X
agg['archived_named_checks']=len(json.load(open(root/'QTI-I_v001/results/qti_v001_results.json')))
with open(Path(__file__).resolve().parent/'independent_audit.json','w') as f: json.dump(agg,f,indent=2)
print(json.dumps(agg,indent=2))
