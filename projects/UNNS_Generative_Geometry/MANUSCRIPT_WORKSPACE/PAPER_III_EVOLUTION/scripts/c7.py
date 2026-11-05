import sys, json; sys.path.insert(0,'.')
from eng3 import *
R={}
# B-T10 plateau: 1369/9
o=orbit(Fr(1369,9),160); ap=None
n=0
D0=Dset(o[0]); 
while n<len(o) and Dset(o[n])==D0 and n<len(o)-1: n+=1
R['BT10']={'plateau_len':n,'delta':str(o[1]-o[0]),'x140':str(o[140]) ,'x140_is_4_37sq':o[140]==4*37**2,'D0':D0}
print(R['BT10'])
# B2-T6 rigid set & C^3 = 4x
bad=0; cnt=0
for sg in range(2,61,2):
    for t in (1,2,3):
        x=Fr(sg*sg*t); o3=orbit(x,3)
        cnt+=1; bad+= (o3[3]!=4*x)
R['BT12_rigid']={'checked':cnt,'bad':bad}
# t-trajectory: t -> sqf(t+1); find rigid set {1,2,3} by brute force on t<=300 : entry time
def sqf_split(n):
    u=1; t=1
    for p,e in factor(n).items(): u*=p**(e//2); t*=p**(e%2)
    return u,t
rig=[t for t in range(1,300) if all(True for _ in [0])]
# periodic cycles of t-map
cyc=set()
for t0 in range(1,2000):
    seen=[]; t=t0
    for _ in range(100):
        t=sqf_split(t+1)[1]
    c=[t]; u=sqf_split(t+1)[1]
    while u!=t: c.append(u); u=sqf_split(u+1)[1]
    cyc.add(tuple(sorted(c)))
R['B2T6_cycles']=sorted(cyc)
print('t-cycles',R['B2T6_cycles'])
# B2-T2 transport and T9 strictness on all edges m<=3000
def sig(m):
    s=1
    for p,e in factor(m).items(): s*=p**(e//2)
    return s
bad=0; strict=0; incl_fail=0; ne=0
for m in range(2,3001):
    for N in divisors(factor(m)):
        if N<1: continue
        m2=m*(N+1)**2//N; ne+=1
        s1,s2=sig(m),sig(m2)
        # formula: sigma' = sigma*(N+1)/c, c=prod p^{l_p}
        c=1
        for p,n_ in factor(N).items():
            v=factor(m).get(p,0); l=n_//2 if v%2==1 else (n_+1)//2; c*=p**l
        if s1*(N+1)%c!=0 or s2*c!=s1*(N+1): bad+=1
        if s2>s1: strict+=1
        if s1>1 and not set(Dset(m))<=set(Dset(m2)) and Dset(m): incl_fail+=1
R['B2T2T9']={'edges':ne,'bad_transport':bad,'sigma_strictly_increasing':strict,'inclusion_fail_edges':incl_fail}
print(R['B2T2T9'])
# B2-T12 family
fam=[]
for a in (2,3,4,5):
    N=2**a-1
    if any(e>1 for e in factor(N).values()): continue
    for s in (2,4,6,8,10):
        x=Fr(N*s*s); y=Fr((2**a*s)**2); cur=x; k=0
        while cur!=y and k<200 and cur<y: cur=C(cur); k+=1
        fam.append({'a':a,'s':s,'k':k,'ok':cur==y and y==x*Fr((N+1)**2,N)})
R['B2T12']={'rows':fam,'all_ok':all(f['ok'] for f in fam)}
print('T12',[ (f['a'],f['s'],f['k']) for f in fam][:12],R['B2T12']['all_ok'])
# phase shifted correspondence ell=11: C^{8-g}(2g S^2/11)=R(2) x
S=2**2*3**3*5**4; ok=[]
for g in range(1,5):
    x=Fr(2*g*S*S,11); y=orbit(x,8-g)[8-g]; ok.append(y==Fr(9,2)*x)
R['phase_shift']=ok; print('phase',ok)
# G=11 |F_k|=2k+7 and L=S
def tD(S,m): return sorted(d for d in divisors(factor(S)) if d>=2 and d%m==1%m)
S11=lambda k: 2**2*3**(3+k)*5**4
R['F11']=all(len(tD(S11(k),11))==2*k+7 for k in range(0,40))
# ell=5,S=36 step 3->4 unchanged betti
o=orbit(Fr(36*36,5),5); R['l5_S36']=[(Dset(o[n]),bettiD(Dset(o[n])) if Dset(o[n]) else None) for n in (3,4)]
print(R['l5_S36'])
json.dump(R,open('../results/c7.json','w'),default=str)
