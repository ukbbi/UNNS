# B2-T2/T9 on all SELECT-II edges m --N--> m(N+1)^2/N, N | m, 1<=m<=3000  (exact, stdlib)
import sys, json; sys.path.insert(0,'.')
from eng3 import factor, divisors, Dset
def sig(m):
    s=1
    for p,e in factor(m).items(): s*=p**(e//2)
    return s
ne=bad=strict=dchg=incl_ok=incl_fail=0; first_fail=None
for m in range(1,3001):
    fm=factor(m) if m>1 else {}
    for N in (divisors(fm) if m>1 else [1]):
        m2=m*(N+1)**2//N; ne+=1
        s1,s2=sig(m),sig(m2)
        c=1
        for p,n_ in factor(N).items() if N>1 else []:
            v=fm.get(p,0); l=n_//2 if v%2==1 else (n_+1)//2; c*=p**l
        if s2*c!=s1*(N+1): bad+=1
        if s2>s1: strict+=1
        D1=set(Dset(m)) if m>1 else set(); D2=set(Dset(m2))
        if D1!=D2: dchg+=1
        if D1<=D2: incl_ok+=1
        else:
            incl_fail+=1
            if first_fail is None: first_fail=(m,N,m2,sorted(D1),sorted(D2))
R={'edges':ne,'bad_transport':bad,'sigma_strictly_increasing':strict,'D_changes':dchg,'inclusion_holds':incl_ok,'inclusion_fails':incl_fail,'first_failure':first_fail}
print(R); json.dump(R,open('../results/c9_b2.json','w'),default=str)
