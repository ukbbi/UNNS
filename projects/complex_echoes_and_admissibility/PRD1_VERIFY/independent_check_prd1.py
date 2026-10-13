"""Independent PRD-1 arithmetic and rule check. No imports from ESC-I."""
from fractions import Fraction as F
import random, json, hashlib
from pathlib import Path
r=random.Random(20261014)
opts=[F(0),F(1,8),F(1,4),F(1,2),F(1),F(2),F(4)]
def choose():return r.choice([-1,1])*r.choice(opts)
def round_even(q):
 n,d=q.numerator,q.denominator; a,b=divmod(abs(n),d)
 z=a+(b*2>d or (b*2==d and a%2==1)); return (1 if n>=0 else -1)*z
def project(kind,par,y):
 u,w=y
 if kind=='DZ':return (F(0) if abs(u)<par else u,w)
 if kind=='CLIP':return (max(-par,min(par,u)),max(-par,min(par,w)))
 if kind=='LAT':return (round_even(u/par)*par,round_even(w/par)*par)
 if kind=='GATE':return (F(0) if abs(u)<=abs(w) else u,w)
 if kind=='LINP':return (F(0),par*u+w)
 if kind=='LINQ':return (u+par*w,F(0))
def prediction(kind,p,L,M,u,w):
 a,b=abs(L),abs(M)
 if kind=='DZ':
  if a*abs(u)>=p:return 'DIV',None
  if M*w==0:return 'ZERO',None
  return ('DEC' if b<1 else 'BOUND' if b==1 else 'DIV'),(abs(w) if b==1 else None)
 if kind=='CLIP':return 'BOUND',p
 if kind=='GATE':
  if a*abs(u)>b*abs(w):return 'DIV',None
  return ('DEC' if b<1 else 'BOUND' if b==1 else 'DIV'),(abs(w) if b==1 else None)
 if kind=='LAT':
  if abs(u)>p/(2*(a-1)) or (b>1 and abs(w)>p/(2*(b-1))):return 'DIV',None
  if a*abs(u)<p/2 and b*abs(w)<p/2:return 'ZERO',None
  if a*abs(u)<p/2 and b<=1:return 'BOUND',b*abs(w)+p/2
  return 'ABSTAIN',None
 if kind in ('LINP','LINQ'):return 'LIN',None
 raise ValueError(kind)
def check(kind,p,L,M,u,w,pred,B):
 z=(u,w); seen=set(); n0=max(abs(u),abs(w)); maxn=0; hit0=False; cycle=False; escape=False; bound_bad=False
 for j in range(201):
  if z==(0,0):hit0=True
  if z in seen:cycle=True
  seen.add(z)
  if j>0 and B is not None and max(map(abs,z))>B:bound_bad=True
  if j>0 and max(map(abs,z))>10**6*max(F(1),n0): escape=True
  if j<200:z=project(kind,p,(L*z[0],M*z[1]))
 if pred=='ZERO' and not hit0:return False,'collapse-not-observed'
 if pred=='DIV' and (hit0 or cycle):return False,'divergence-contradicted'
 if pred=='BOUND' and (bound_bad or escape):return False,'bound-violated'
 if pred=='DEC' and escape:return False,'decay-contradicted'
 return True,'ok'
counts={}; contradictions=[]; unproven=[]; linear_mismatches=0
for kind in ['DZ','CLIP','LAT','GATE','LINP','LINQ']:
 ks={'cases':0,'claimed':0,'abstained':0,'contradictions':0,'linear_control':0}; counts[kind]=ks
 for i in range(400):
  a=F(r.randint(5,20),4); L=a*r.choice([-1,1]); b=r.choice([F(0),F(1,4),F(1,2),F(3,4),F(7,8),F(1),F(5,4),F(3,2),F(2)])
  if b>=a:b=F(1,2)
  M=b*r.choice([-1,1]);u=choose() or F(1,8); w=choose()
  p=r.choice({'DZ':[F(1,4),F(1,2),F(1),F(2)],'CLIP':[F(1),F(2),F(4)],'LAT':[F(1,4),F(1,2),F(1)],'GATE':[F(0)],'LINP':[F(1,2),F(2)],'LINQ':[F(1,2),F(2)]}[kind]); ks['cases']+=1
  pred,B=prediction(kind,p,L,M,u,w)
  if pred=='ABSTAIN':ks['abstained']+=1;continue
  if pred=='LIN':
   ks['linear_control']+=1
   x=(u,w); y=x
   for j in range(12):
    y=project(kind,p,(L*y[0],M*y[1]))
    if kind=='LINP':
     first=p*L*u+M*w
     expected=(F(0),first*M**j)
    else:
     first=L*u+p*M*w
     expected=(first*L**j,F(0))
    if y!=expected:linear_mismatches+=1;break
   continue
  ks['claimed']+=1; ok,why=check(kind,p,L,M,u,w,pred,B)
  if not ok:ks['contradictions']+=1;contradictions.append([kind,str(L),str(M),str(u),str(w),str(p),pred,why])
  # independent analytical foundations: the claims are derived directly from threshold/rounding dynamics
  # Numerical trajectories used only as a falsification layer, not to establish the theorem.
report={'checker':'independent_check_prd1','independent_seed':20261014,'uses_original_rule_source':False,'cases':sum(x['cases'] for x in counts.values()),'counts':counts,'contradictions':contradictions[:25],'linear_mismatches':linear_mismatches,'notes':['Exact rational trajectories for 200 steps; not a proof of infinity.','Separate elementary symbolic arguments verify domain-restricted closed-form rules.','Comparator scoring issue assessed separately.']}
p=Path(__file__).resolve().parent/'RUN_RESULT.json';p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));
if contradictions or linear_mismatches: raise SystemExit(1)
