"""ANS-I v010 checks.  Usage: python3 -B v010_checks.py [exponents|zeros|identity|kloosterman|summatory]
Exact integer arithmetic where stated, otherwise floating point; none of this proves the theorems."""
import sys, os, json, platform
from math import gcd
import numpy as np, mpmath as mp
mp.mp.dps=25
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'mpmath':mp.__version__,'numpy':np.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1)
NMAX=80
def mul(a,b):
    c=[0]*(NMAX+1)
    for i,x in enumerate(a):
        if x:
            for j in range(NMAX+1-i): c[i+j]+=x*b[j]
    return c
def local():
    num=[0]*(NMAX+1); num[5]=num[6]=1; inv=[0]*(NMAX+1)
    for j in range(0,NMAX+1,2): inv[j]=(-1)**(j//2)
    h=[-x for x in mul(num,inv)]; h[0]+=1; return h
def peel(rest,n,e):                      # multiply by (1-z^n)^e
    term=[0]*(NMAX+1); b=1
    for m in range(NMAX//n+1):
        term[n*m]=(-1)**m*b; b=b*(e-m)//(m+1)
    return mul(rest,term)
def mobius(n):
    r=1;p=2
    while p*p<=n:
        if n%p==0:
            n//=p
            if n%p==0: return 0
            r=-r
        p+=1
    return -r if n>1 else r
def exponents():
    rest=local(); c={}; snap={}
    for n in range(1,NMAX+1):
        c[n]=rest[n]; rest=peel(rest,n,c[n]); assert rest[n]==0
        if n==11: snap['R_12_coefficients_z12_to_z15']=rest[12:16]
    p=[3,0,-2]                          # power sums of the roots of x^3+x+1
    for n in range(3,NMAX+1): p.append(-p[n-2]-p[n-3])
    A=lambda N: -p[N]-(3 if N%3==0 else 0)+(2*(-1)**(N//2) if N%2==0 else 0)
    mism=[n for n in range(1,NMAX+1) if n*c[n]!=sum(mobius(n//d)*A(d) for d in range(1,n+1) if n%d==0)]
    R=max(abs(x) for x in mp.polyroots([1,0,1,1],maxsteps=200,extraprec=100)); R=float(R)
    err=max(abs(n*c[n]+p[n])/(R**(n/2)) for n in range(2,NMAX+1))
    e={n:c[n]+(2 if n==2 else 0)+(1 if n==3 else 0) for n in c}
    snap.update({'c_n':c,'formula_mismatches':mism,'R':R,'max_|n c_n + p_n|/R^(n/2), 2<=n<=80':err,
      'negative_e_n_up_to_80':[n for n in e if e[n]<0],'positive_e_n_up_to_80':[n for n in e if e[n]>0],'zero_e_n':[n for n in e if e[n]==0]})
    save('v010_exponents.json',snap)
def zeros():
    rows=[]
    for j in range(1,31):
        rho=mp.zetazero(j)
        v=min(float(abs(mp.zeta(k*rho/6))) for k in range(2,13) if k!=6)
        rows.append({'zero':j,'min_|zeta(k rho/6)|, 2<=k<=12, k!=6':v})
    save('v010_zeros.json',{'rows':rows,'smallest':min(list(r.values())[1] for r in rows)})
def units(q): return [u for u in range(1,q+1) if gcd(u,q)==1]
def inv(u,q): return 1 if q==1 else pow(u,-1,q)
def rep(x,q): x%=q; return x if x else q
def identity():
    # (a) least element M0 of q|M, r|M+1 against the two closed formulas
    bad=0; n=0
    for q in range(1,61):
        for r in range(1,61):
            if gcd(q,r)>1 or (q,r)==(1,1): continue
            M0=next(M for M in range(1,q*r+1) if M%q==0 and (M+1)%r==0); n+=1
            if q<r: y=rep(inv(r%q,q) if q>1 else 1,q); bad+= M0!=r*y-1
            else:  j=rep(-inv(q%r,r),r) if r>1 else 1; bad+= M0!=q*j
    # (b) the decomposition of U(s) at s=0.8 against a direct sum with tail correction
    s=0.8; N=4*10**6
    sig=np.zeros(N+2)
    for d in range(1,N+2): sig[d::d]+=d**(-s)
    M=np.arange(1,N+1,dtype=float)
    head=float(np.sum(M**(-2*s)*sig[1:N+1]*sig[2:N+2]))
    z=lambda w: float(mp.zeta(w))
    D=z(1+s)**2/z(2+2*s); C=z(1-s)*z(1+s)/z(2); X=N+0.5
    direct=head+D*X**(1-2*s)/(2*s-1)+2*C*X**(1-3*s)/(3*s-1)
    from scipy_free import hz
    rows=[]
    for Q in (100,200,400):
        A1=0.0; T=0.0
        for q in range(1,Q+1):
            U=units(q); y=np.array([rep(inv(u%q,q),q) if q>1 else 1 for u in U],float); u=np.array(U,float)
            ym=np.array([rep(-inv(v%q,q),q) if q>1 else 1 for v in U],float)
            g=hz(3*s,1+u/q)
            T+=q**(-6*s)*float(np.dot(hz(2*s,y/q),g)+np.dot(hz(2*s,ym/q),g))
            base=hz(2*s,y/q); MM=60
            m=np.arange(1,MM+1,dtype=float)[:,None]; r=m*q+u
            diff=r**(-3*s)*(hz(2*s,(y/q-1/(q*r)).ravel()).reshape(r.shape)-base)
            tail=0.0   # remaining m>MM: first-order Taylor term
            rr=(MM+0.5)*q+u
            tail=np.sum(2*s*hz(2*s+1,y/q)/q * rr**(-3*s)/(q*(3*s)))
            A1+=q**(-3*s)*float(diff.sum()+tail)
        rows.append({'Q':Q,'decomposition':z(2*s)+A1+T})
    save('v010_identity.json',{'pairs_checked':n,'least_element_mismatches':bad,'s':s,'direct_sum_with_tail':direct,'decomposition':rows})
def kloosterman():
    from scipy_free import hz
    rows=[]
    for s in (0.32,1/3,0.36):
        h1=None
        for q in (101,211,401,809,1601,3203,6397,12007,30011,1000,2048,2310,4096,10000,27720):
            U=units(q); u=np.array(U,float)
            h=hz(3*s,1+u/q) if abs(3*s-1)>1e-9 else None
            if h is None: h=-hz_psi(1+u/q)-float(mp.euler)
            else: h=h-float(mp.zeta(3*s))
            for sign in (1,-1):
                y=np.array([rep(sign*inv(v,q),q) for v in U],float)
                f=hz(2*s,y/q); R=float(np.dot(f,h))
                rows.append({'s':s,'q':q,'sign':sign,'R_q':R,'|R_q|/q^(1/2+s)':abs(R)/q**(0.5+s),'sum_|f|/q':float(np.abs(f).sum())/q})
    J=[]
    for q in (7,12,360,1001):
        w=0.66; lhs=float(np.sum(hz(w,np.array(units(q),float)/q)))
        rhs=float(mp.zeta(w))*sum(mobius(d)*(q/d)**w for d in range(1,q+1) if q%d==0)
        J.append({'q':q,'difference':lhs-rhs})
    integ=[float(mp.quad(lambda a: a**(-w)+mp.zeta(w,1+a),[0,1])) for w in (mp.mpf('0.3'),mp.mpf('0.66'))]
    save('v010_kloosterman.json',{'rows':rows,'unit_sum_identity':J,'integral_of_hurwitz_over_(0,1)':integ,
       'largest_|R_q|/q^(1/2+s)':max(r['|R_q|/q^(1/2+s)'] for r in rows)})
def hz_psi(x):                          # digamma, for the removable point 3s=1: zeta(w,x)-zeta(w) -> -psi(x)-gamma
    x=np.array(x,float); out=np.zeros_like(x)
    for k in range(8): out-=1/(x+k)
    y=x+8; i=1/(y*y)
    return out+np.log(y)-0.5/y-i*(1/12-i*(1/120-i*(1/252-i/240)))
def summatory():
    s=1/3; z=lambda w: float(mp.zeta(w))
    D=z(1+s)**2/z(2+2*s); C=z(1-s)*z(1+s)/z(2)
    N=2*10**7; sig=np.zeros(N+2)
    for d in range(1,N+2): sig[d::d]+=d**(-s)
    cs=np.cumsum(sig[1:N+1]*sig[2:N+2]); rows=[]
    for X in (10**4,10**5,10**6,10**7,2*10**7):
        res=float(cs[X-1])-D*X
        rows.append({'X':X,'(S-DX)/X^(2/3)':res/X**(2/3),'predicted':2*C/(1-s),'remainder/X^(1/2)':(res-2*C/(1-s)*X**(1-s))/X**0.5})
    save('v010_summatory.json',{'s':s,'D':D,'rows':rows})
if __name__=='__main__':
    {'exponents':exponents,'zeros':zeros,'identity':identity,'kloosterman':kloosterman,'summatory':summatory}[sys.argv[1]]()
