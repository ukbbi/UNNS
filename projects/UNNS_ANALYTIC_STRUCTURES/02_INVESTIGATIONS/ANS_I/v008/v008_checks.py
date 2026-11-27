"""ANS-I v008 checks.  Usage: python3 -B v008_checks.py [identity|constants|count2|count3|laws]
Finite and floating-point checks; none of them is a proof."""
import sys, os, json, math, cmath, subprocess, tempfile, platform, random
from math import gcd
import numpy as np, mpmath as mp
mp.mp.dps=30
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d,indent=1))
def factor(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1;n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def divisors(n):
    d=[1]
    for p,e in factor(n).items(): d=[x*p**i for x in d for i in range(e+1)]
    return d
def mobius(n):
    f=factor(n); return 0 if any(e>1 for e in f.values()) else (-1)**len(f)
def jordan(d,s): return sum(mobius(e)*(d//e)**s for e in divisors(d))
def rho(d): return math.prod(p**((e+1)//2) for p,e in factor(d).items())
def source(word):
    E=K=1
    for N in word:
        g=gcd(E,N); K=N*K//g; E=(N+1)**2*E//g
    return K,E

# 1. the first-letter identity, exactly, on finite sets of letters
def identity():
    rows=[]; s=0.9+0.4j
    for k,M1,M in ((2,60,60),(3,14,40),(4,6,24)):
        tail=[()]
        for _ in range(k-1): tail=[w+(N,) for w in tail for N in range(1,M1+1)]
        T=[source(w) for w in tail]
        def Gtail(D,cache={}):
            key=(k,D)
            if key not in cache: cache[key]=sum(E**-s for K,E in T if K%D==0)
            return cache[key]
        for D in (1,2,3,4,6,8,9,12,18,36):
            lhs=0
            for N in range(1,M+1):
                for w in tail:
                    K,E=source((N,)+w)
                    if K%D==0: lhs+=E**-s
            rhs=0
            ds=sorted({d for K,E in T for d in divisors(K)})
            for h in divisors(D):
                n=D//h
                A={}                       # a -> its h-part
                for a in range(2,M+2):
                    t=1
                    for p in factor(h):
                        while a%(t*p)==0: t*=p
                    if gcd(a-1,D)==n: A[a]=t
                for t in sorted(set(A.values())):
                    for d in ds:
                        if gcd(d,h)!=1: continue
                        Z=sum(a**(-2*s) for a,u in A.items() if u==t and a%rho(d)==0)
                        if Z==0: continue
                        # Moebius form of Z used in the proof
                        Z2=0
                        R=math.prod(factor(h)) if h>1 else 1
                        for f in divisors(R):
                            for e in divisors(R):
                                Z2+=mobius(f)*mobius(e)*sum(a**(-2*s) for a in range(2,M+2) if a%(f*t*rho(d))==0 and (a-1)%(n*e)==0)
                        assert abs(Z-Z2)<1e-12
                        rhs+=t**(2*s)*jordan(d,s)*Gtail(h*t*t*d)*Z
            rows.append({'depth':k,'D':D,'abs_lhs':abs(lhs),'relative_error':abs(lhs-rhs)/max(abs(lhs),1e-300)})
    save('v008_identity.json',{'s':[s.real,s.imag],'rows':rows,'max_relative_error':max(r['relative_error'] for r in rows)})

# 2. constants of the depth-two expansion
def primes(n):
    v=np.ones(n+1,bool); v[:2]=False
    for i in range(2,int(n**.5)+1):
        if v[i]: v[i*i::i]=False
    return np.nonzero(v)[0].astype(float)
def H(s,P):
    x=P**-s; return math.exp(np.log1p(-(x**5+x**6)/(1+x*x)).sum())
def H_tail(s,P):
    # log of the product over p > max P, leading terms -x^5 - x^6 + x^7
    out=mp.mpf(0)
    for m,c in ((5,-1),(6,-1),(7,1),(8,1)):
        out+=c*(mp.primezeta(m*s)-float((P**(-m*s)).sum()))
    return float(mp.e**out)
def constants():
    P=primes(10**6); h=lambda s:H(s,P)*H_tail(s,P)
    Phi=lambda s: float(mp.zeta(3*s))*h(s)
    P0=Phi(0.5); e=1e-4; P1=(Phi(0.5+e)-Phi(0.5-e))/(2*e)
    # F2(1/2) = sum_d J(d) /(rho(d) d) * (psi(1) - psi(1+1/d))
    L=10**6; spf=list(range(L+1))
    for i in range(2,1001):
        if spf[i]==i:
            for j in range(i*i,L+1,i):
                if spf[j]==j: spf[j]=i
    def psi_diff(x):   # psi(1) - psi(1+x) = sum_{n>=2} (-1)^(n+1) zeta(n) x^(n-1) for |x| < 1; equals -1 at x = 1
        out=np.zeros_like(x)
        for n in range(2,60): out+=(-1)**(n+1)*float(mp.zeta(n))*x**(n-1)
        out[x==1]=-1.0
        return out
    J=np.ones(L+1); R=np.ones(L+1)
    for d in range(2,L+1):
        p=spf[d]; m=d; c=0
        while m%p==0: m//=p; c+=1
        J[d]=J[m]*(p**(c*.5)-p**((c-1)*.5)); R[d]=R[m]*p**((c+1)//2)
    d=np.arange(1,L+1,dtype=float)
    x=1/d; terms=J[1:]/(R[1:]*d)*psi_diff(x)
    F2=float(terms.sum()); F2_half=float(terms[:L//10].sum())
    g=float(mp.euler)
    r=float(mp.zeta(mp.mpf(2)/3))**2*h(1/3)
    return {'Phi(1/2)=kappa_2':P0,'Phi_prime(1/2)':P1,'F2(1/2)':F2,'F2_change_from_d<=1e5':F2-F2_half,
            'c1':P0/2,'c0':P1/2-P0+2*g*P0+F2-1,'H(1/3)':h(1/3),'coefficient_of_X^(1/3)':r}

def run(k,X):
    exe=os.path.join(tempfile.gettempdir(),'ans_depth_%d'%os.getpid())
    if not os.path.exists(exe): subprocess.run(['gcc','-O2','-o',exe,os.path.join(HERE,'depth_count.c'),'-lm'],check=True)
    return int(subprocess.run([exe,str(k),str(X)],capture_output=True,text=True,check=True).stdout)
def brute(k,X):
    def rec(E,left):
        c=0
        for N in range(1,X//E+1):
            E2=(N+1)**2*E//gcd(E,N)
            if E2<=X: c+=1 if left==1 else rec(E2,left-1)
        return c
    return rec(1,k)
def count2():
    c=constants(); agree=[run(k,X)==brute(k,X) for k,X in ((2,10**4),(2,10**5),(3,10**4),(3,10**5),(4,3*10**4))]
    rows=[]
    for e in range(6,15):
        for X in (10**e,3*10**e):
            if X>10**14: continue
            A=run(2,X); main=math.sqrt(X)*(c['c1']*math.log(X)+c['c0'])
            rows.append({'X':X,'A_2':A,'A_2-main':A-main,'(A_2-main)/X^(1/3)':(A-main)/X**(1/3),
                         'after_second_term/X^(1/4)':(A-main-c['coefficient_of_X^(1/3)']*X**(1/3))/X**.25})
    save('v008_depth2.json',{'constants':c,'independent_enumeration_agrees':agree,'rows':rows})
KAPPA={3:5.105352,4:19.11923}
def count3():
    rows={}
    for k,top in ((3,10**12),(4,10**11)):
        data=[(X,run(k,X)) for e in range(7,13) for X in (10**e,3*10**e) if X<=top]
        lead=KAPPA[k]/(2**(k-1)*math.factorial(k-1))
        # fit the k-1 lower coefficients on the largest thresholds, then compare on the others
        L=np.array([math.log(X) for X,_ in data]); y=np.array([A/math.sqrt(X) for X,A in data])-lead*L**(k-1)
        M=np.vander(L,k-1); w=np.array([X**(1/6) for X,_ in data])
        coef=np.linalg.lstsq(M*w[:,None],y*w,rcond=None)[0]
        res=y-M@coef
        extra=None
        if k==3:      # diagnostic fit with a term X^(1/3)(a log X + b); not predicted from theory
            M2=np.column_stack([L,np.ones_like(L),L*np.exp(-L/6),np.exp(-L/6)]); w2=np.exp(L/4)
            c2=np.linalg.lstsq(M2*w2[:,None],y*w2,rcond=None)[0]
            extra={'coefficients_c1_c0_a_b':c2.tolist(),'residual_times_X^(1/4)':((y-M2@c2)*w2).tolist()}
        rows[k]={'diagnostic_fit_with_second_term':extra,'leading_coefficient':lead,'fitted_lower_coefficients':coef.tolist(),
                 'rows':[{'X':X,'A_k':A,'residual/X^(-1/6)':float(res[i]*X**(1/6)),'leading_term_only_ratio':A/(lead*math.sqrt(X)*math.log(X)**(k-1))} for i,(X,A) in enumerate(data)]}
    save('v008_depth34.json',{'depths':rows})
def laws():
    s=1.5463810457225144; z=float(mp.zeta(s))
    census=json.load(open(os.path.join(HERE,'..','v007','results','v007_census.json')))['counts']
    by={r['X']:r for r in census}
    save('v008_laws.json',{'limit_mean_E_over_X':s/(s+1),'limit_share_upper_half':1-2**-s,
      'replication_limit':{j:j**-s/z for j in range(1,9)},
      'finite_values':[{'X':2*T,'P(E<=X/2) in A':by[T]['A']/by[2*T]['A'],'P(m=1) in C':by[2*T]['A']/by[2*T]['C'],
                        'P(m=2) in C':by[T]['A']/by[2*T]['C']} for T in (10**e for e in (3,4,5,6,7,8))],
      'limits':{'P(E<=X/2)':2**-s,'P(m=1)':1/z,'P(m=2)':2**-s/z}})
if __name__=='__main__':
    m=sys.argv[1]
    if m=='constants': print(json.dumps(constants(),indent=1))
    else: {'identity':identity,'count2':count2,'count3':count3,'laws':laws}[m]()
