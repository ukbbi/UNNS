"""UNNS-U2-RN core: exact integer factorization with certification flags, complete neighbourhoods, degree.
Edge grammar: {kN, k(N+1)^2}. Forward nbr of x per divisor d|x: x(d+1)^2/d. Inverse nbr per q>=2, q^2|x: x(q-1)/q^2.
All arithmetic is exact integer arithmetic; no floats."""
import random
from collections import Counter
CNT=Counter()
MR_BASES=(2,3,5,7,11,13,17,19,23,29,31,37,41)
MR_BOUND=3317044064679887385961981   # deterministic for n < this with the 13 bases (Sorenson-Webster 2015)
_SP=[p for p in range(2,2000) if all(p%q for q in range(2,int(p**.5)+1))]
def is_prime(n):
    """returns (is_prime, certified).  certified=True iff the answer is a proof (deterministic MR range or trial division)."""
    if n<2: return False,True
    for p in _SP[:12]:
        if n==p: return True,True
        if n%p==0: return False,True
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in MR_BASES:
        if a%n==0: continue
        CNT['mr_modexp']+=1
        x=pow(a,d,n)
        if x in(1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False,True        # a composite witness is always a proof
    return True,(n<MR_BOUND)
def _gcd(a,b):
    while b: a,b=b,a%b
    return a
def _rho(n,seed=1):
    if n%2==0: return 2
    c=seed
    while True:
        x=y=2;d=1
        while d==1:
            CNT['rho_iter']+=1
            x=(x*x+c)%n;y=(y*y+c)%n;y=(y*y+c)%n
            d=_gcd(abs(x-y),n)
        if d!=n: return d
        c+=1
_FC={}
def factor(n):
    """returns ({prime:exp}, certified). certified iff every prime factor is certified prime and the product equals n."""
    if n in _FC: return _FC[n]
    CNT['factor_calls']+=1
    m=n;f=Counter();cert=True
    for p in _SP:
        if p*p>m: break
        while m%p==0: f[p]+=1;m//=p
    if m>1:
        st=[m]
        while st:
            t=st.pop()
            if t==1: continue
            if t<_SP[-1]**2 or True:
                pr,c=is_prime(t)
                if pr: f[t]+=1;cert=cert and c;continue
            d=_rho(t);st+= [d,t//d]
    r=(dict(f),cert); _FC[n]=r
    prod=1
    for p,e in r[0].items(): prod*=p**e
    assert prod==n
    return r
def tau(f):
    r=1
    for e in f.values(): r*=e+1
    return r
def degree_from_fact(f):
    """deg = prod(e+1) + prod(floor(e/2)+1) - 1  (forward + inverse neighbours)"""
    a=1;b=1
    for e in f.values(): a*=e+1;b*=e//2+1
    return a+b-1
def merge(*fs):
    r=Counter()
    for f in fs:
        for p,e in f.items(): r[p]+=e
    return dict(r)
def divisors_f(f):
    ds=[(1,{})]
    for p,e in f.items():
        new=[]
        pk=1
        for k in range(e+1):
            for d,ex in ds:
                ex2=dict(ex)
                if k: ex2[p]=k
                new.append((d*pk,ex2))
            pk*=p
        ds=new
    return ds
def neighbours(x):
    """complete neighbourhood.  returns dict(F=[(d,y,fy)...] ascending, I=[(q,y,fy)...] descending by y, cert=bool).
    fy = factorization of y composed from factorizations of the pieces (no refactoring of y)."""
    f,cert=factor(x)
    F=[];I=[]
    for d,ex in divisors_f(f):
        fd=factor(d+1); cert=cert and fd[1]
        rest={p:e-ex.get(p,0) for p,e in f.items() if e-ex.get(p,0)>0}      # x/d
        F.append((d,x*(d+1)**2//d,merge(rest,{p:2*e for p,e in fd[0].items()})))
    F.sort()
    # q>=2, q^2|x
    qs=[(1,{})]
    for p,e in f.items():
        new=[]
        for k in range(e//2+1):
            for q,ex in qs:
                ex2=dict(ex)
                if k: ex2[p]=k
                new.append((q*p**k,ex2))
        qs=new
    for q,ex in qs:
        if q==1: continue
        fq=factor(q-1); cert=cert and fq[1]
        rest={p:e-2*ex.get(p,0) for p,e in f.items() if e-2*ex.get(p,0)>0}  # x/q^2
        I.append((q,x*(q-1)//(q*q),merge(rest,fq[0])))
    I.sort(key=lambda t:-t[1])
    CNT['neighbours_enum']+=len(F)+len(I)
    return dict(F=F,I=I,cert=cert,fx=f)
def deg(x): return degree_from_fact(factor(x)[0])
