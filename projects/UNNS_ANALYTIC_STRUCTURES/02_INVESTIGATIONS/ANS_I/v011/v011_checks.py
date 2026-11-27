"""ANS-I v011 checks.  Usage: python3 -B v011_checks.py [grammar|exponents|local|decomposition|shifted|counts]
Exact integer or rational arithmetic where stated, otherwise floating point; none of this proves the theorems."""
import sys, os, json, math, platform
from fractions import Fraction
from math import gcd
import numpy as np, mpmath as mp
from hurwitz_np import hz
mp.mp.dps=25
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'mpmath':mp.__version__,'numpy':np.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d)[:3000])
def factor(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
# ---- exponents (T45f) ----
def exponents(N=3000):
    p=[3,0,-2]
    for n in range(3,N+1): p.append(-p[n-2]-p[n-3])
    A=[0]+[-p[m]-(3 if m%3==0 else 0)+(2*(-1)**(m//2) if m%2==0 else 0) for m in range(1,N+1)]
    mu=[0]*(N+1); mu[1]=1
    for i in range(1,N+1):
        for j in range(2*i,N+1,i): mu[j]-=mu[i]
    S=[0]*(N+1)
    for d in range(1,N+1):
        for n in range(d,N+1,d): S[n]+=mu[n//d]*A[d]
    assert all(S[n]%n==0 for n in range(1,N+1))
    e={n:S[n]//n+(2 if n==2 else 0)+(1 if n==3 else 0) for n in range(1,N+1)}
    R=max(abs(x) for x in mp.polyroots([1,0,1,1],maxsteps=200,extraprec=100))
    Y=[float(mp.mpf(n*e[n])/(2*R**n)) for n in range(1,N+1)]
    rows=[]
    for M in (300,1000,3000):
        y=np.array(Y[:M])
        rows.append({'N':M,'share |e_n|>R^n/n':float(np.mean(np.abs(y)>0.5)),'share positive':float(np.mean(y>0.5)),'share negative':float(np.mean(y<-0.5)),
          'empirical CDF at -0.5,0,0.5':[float(np.mean(y<=t)) for t in (-0.5,0,0.5)]})
    save('v011_exponents.json',{'rows':rows,'arcsine CDF at -0.5,0,0.5':[1/3,0.5,2/3],
       'quoted_values':{n:e[n] for n in (24,27,32,42,44,47,54,66,69,80)}})
# ---- grammar weights ----
def J(p,v,s): return 1 if v==0 else p**(v*s)-p**((v-1)*s)
def Phi_p(p,v,s): return sum(J(p,i,s)*p**(-2*s*((i+1)//2)) for i in range(v+1))
def Phi_closed(v,z): return 1+(1-z)*(v//2+((v+1)//2)*z)
def Lm(mu_,z): return Phi_closed(mu_,z)+(z**3/(1+z*z) if mu_%2==0 else z*z*(1-z+z*z)/(1+z*z))
def L0(z): return (1+z*z+z**3)/(1+z*z)
def Lb(beta,z): return 1+z-z**(2*beta+1)/(1+z*z)
def w1p(p,mu_,s): z=p**(-s); return Lm(mu_,z)/L0(z)
def w2p(p,beta,s): z=p**(-s); return 1.0 if beta==0 else Lb(beta,z)/L0(z)
def local(T=120):
    out=[]
    for p,s in ((2,0.9),(3,0.8),(5,1.1),(2,1.4)):
        z=p**(-s); worst=0
        for mu_ in range(0,7):     # sum_j (Phi(p^{mu+j})-Phi(p^{mu+j-1})) p^{-2js}, first term Phi(p^mu)
            t=Phi_p(p,mu_,s)+sum((Phi_p(p,mu_+j,s)-Phi_p(p,mu_+j-1,s))*z**(2*j) for j in range(1,T))
            worst=max(worst,abs(t-Lm(mu_,z)),abs(Phi_p(p,mu_,s)-Phi_closed(mu_,z)))
        for beta in range(0,7):
            phi=lambda j: p**(s*min(j,2*beta))*Phi_p(p,j-min(j,2*beta),s)
            t=1+sum((phi(j)-phi(j-1))*z**(2*j) for j in range(1,T))
            worst=max(worst,abs(t-Lb(beta,z)))
        out.append({'p':p,'s':s,'largest_error':worst})
    sym=[]
    for z in (Fraction(1,2),Fraction(2,7)):
        sym.append(bool(Lm(1,z)/L0(z)==Lb(1,z)/L0(z)==(1+z+z*z)/(1+z*z+z**3) and Lm(0,z)==L0(z)==Lb(0,z)))
    save('v011_local.json',{'closed_forms':out,'exact_rational_identities_at_test_points':sym})
# ---- decomposition ----
def tables(N,s):
    w1=np.ones(N+2); w2=np.ones(N+2)
    comp=np.zeros(N+2,bool)
    for p in range(2,N+2):
        if comp[p]: continue
        comp[p*p::p]=True
        q=p; v=1; prev1=np.float64(1); 
        while q<=N+1:
            # multiples of p^v receive the ratio w(p^v)/w(p^(v-1))
            a=w1p(p,v,s); b=w1p(p,v-1,s) if v>1 else 1.0; w1[q::q]*=a/b
            a=w2p(p,v,s); b=w2p(p,v-1,s) if v>1 else 1.0; w2[q::q]*=a/b
            q*=p; v+=1
    return w1,w2
def Phi(n,s):
    r=1.0
    for p,v in factor(n).items(): r*=Phi_p(p,v,s)
    return r
def decomposition():
    s=1.5; res={'s':s}
    # (a) sum over the first letter
    bad=0
    for K in (1,2,12,45,64,360,1001):
        a=np.arange(2,2*10**6+1,dtype=np.int64); g=np.gcd(a*a,K).astype(float)
        direct=float(np.sum(a.astype(float)**(-2*s)*g**s)); formula=float(mp.zeta(2*s))*Phi(K,s)-1
        tail=K**s*(2*10**6)**(1-2*s)/(2*s-1)
        bad=max(bad,max(0,abs(direct-formula)-tail))
    res['first_letter_identity_excess_over_tail_bound']=bad
    # (b) sum over the last letter: Euler product w1(M) w2(M+1)
    P=1.0
    sieve=np.ones(200000,bool); sieve[:2]=False
    for p in range(2,448):
        if sieve[p]: sieve[p*p::p]=False
    for p in np.nonzero(sieve)[0]: P*=L0(float(p)**(-s))
    P*=1.0
    rows=[]
    N=10**6; Nn=np.arange(1,N+1,dtype=np.int64)
    w1,w2=tables(60,s)
    for M in (1,2,3,4,7,8,12,15,24,35,48):
        b=M+1
        g=np.gcd(Nn,b*b); 
        # exact f(N)=(N,b^2)^s Phi(M N/(N,b^2)) on a smaller range
        n2=40000; f=np.array([float(g[i])**s*Phi(M*int(Nn[i])//int(g[i]),s) for i in range(n2)])
        direct=float(np.sum((Nn[:n2]+1.0)**(-2*s)*f))
        # Lambda = Moebius transform of f, f(0 shift) 
        K=4000; Lam=f[:K].copy()
        for k in range(1,K+1):
            for m in range(2*k,K+1,k): Lam[m-1]-=Lam[k-1]
        k=np.arange(1,K+1,dtype=float)
        R=float(np.sum(Lam*k**(-2*s)*(hz(2*s,1+1/k)-float(mp.zeta(2*s)))))
        main=float(mp.zeta(2*s))*P*w1[M]*w2[b]
        rows.append({'M':M,'direct':direct,'zeta*P*w1*w2 + remainder':main+R,'difference':direct-main-R})
    res['last_letter']=rows
    save('v011_decomposition.json',res)
# ---- shifted convolution at s=1/3 ----
def local_series(z):
    """closed forms at s = 1/3, z = p^(-1/3): returns D_p, E1_p, E2_p, H_p"""
    y=z**3; x=z**2; ce=z**3/(1+z*z); co=z*z*(1-z+z*z)/(1+z*z); L=L0(z)
    def W1(t):
        base=t/(1-t)+(1-z)*(t*t+z*t)/((1-t)*(1-t*t))
        return 1+(base+ce*t*t/(1-t*t)+co*t/(1-t*t))/L
    def W2(t): return 1+((1+z)*t/(1-t)-z/(1+z*z)*(z*z*t)/(1-z*z*t))/L
    D=(1-y)*W1(y)+(1-y)*W2(y)-1
    c=1-z*z
    E1=(1-y)*(1-x)*W1(x)+c*((1-y)*W2(y)-1)
    E2=(1-y)*(1-x)*W2(x)+c*((1-y)*W1(y)-1)
    H=1-(z**5+z**6)/(1+z*z)
    return D,E1,E2,H
def primes(P):
    sieve=np.ones(P+1,bool); sieve[:2]=False
    for p in range(2,int(P**.5)+1):
        if sieve[p]: sieve[p*p::p]=False
    return [int(p) for p in np.nonzero(sieve)[0]]
def eulerE(P,order=26):
    """Euler products over p <= P times the tail from the power series of the logarithm and the prime zeta function"""
    mp.mp.dps=30
    ps=primes(P); partial=[mp.mpf(1)]*4
    zs=[mp.mpf(p)**(-mp.mpf(1)/3) for p in ps]
    for z in zs:
        for i,v in enumerate(local_series(z)): partial[i]*=v
    out=[]; lowest=[]
    pw={}
    for i in range(4):
        co=mp.taylor(lambda z: mp.log(local_series(z)[i]),0,order)
        assert all(abs(c)<mp.mpf('1e-12') for c in co[:4]); lowest.append(next(k for k,c in enumerate(co) if abs(c)>1e-12))
        tail=0
        for k in range(4,order+1):
            if k not in pw: pw[k]=mp.primezeta(mp.mpf(k)/3)-mp.fsum(mp.mpf(p)**(-mp.mpf(k)/3) for p in ps)
            tail+=co[k]*pw[k]
        out.append(partial[i]*mp.exp(tail))
    return [float(v) for v in out],lowest
def closed_vs_series():
    z=0.55; p=z**-3; s=1/3; J_=200
    a=[1.0]+[w1p(p,j,s) for j in range(1,J_)]; b=[1.0]+[w2p(p,j,s) for j in range(1,J_)]
    y=1/p; x=p**(s-1)
    ser=lambda w,t: sum(v*t**j for j,v in enumerate(w))
    D=(1-y)*(ser(a,y)+ser(b,y))-1
    E1=(1-y)*(1-x)*ser(a,x)+(1-z*z)*((1-y)*ser(b,y)-1)
    return [abs(D-local_series(z)[0]),abs(E1-local_series(z)[1])]
def shifted():
    s=1/3; out={'s':s,'closed_form_vs_series_error':closed_vs_series()}
    vals=[]
    for P in (500,2000):
        (D,E1,E2,H),low=eulerE(P); vals.append({'P':P,'D':D,'E1':E1,'E2':E2,'H(1/3)':H,'lowest_order_in_z_of_log_local_factor':low})
    out['euler_products']=vals
    D,E1,E2,H=[vals[-1][k] for k in ('D','E1','E2','H(1/3)')]
    C=float(mp.zeta(mp.mpf(2)/3))*(E1+E2)
    N=2*10**7; w1,w2=tables(N,s); cs=np.cumsum(w1[1:N+1]*w2[2:N+2])
    out['predicted_coefficient_of_X^(2/3)']=C/(1-s)
    out['rows']=[{'X':X,'(S-DX)/X^(2/3)':float(cs[X-1]-D*X)/X**(2/3),'(S-DX-predicted)/X^(1/2)':float(cs[X-1]-D*X-C/(1-s)*X**(1-s))/X**0.5} for X in (10**4,10**5,10**6,3*10**6,10**7,2*10**7)]
    out['residue_of_V_conjectured']=C/3
    out['predicted_a_in_A3']=float(mp.zeta(mp.mpf(2)/3))**2*H*C/3
    save('v011_shifted.json',out)
def counts():
    sh=json.load(open(os.path.join(OUT,'v011_shifted.json'))); a=sh['predicted_a_in_A3']
    d=json.load(open(os.path.join(HERE,'..','v008','results','v008_depth34.json')))['depths']['3']
    X=np.array([r['X'] for r in d['rows']],float); A=np.array([r['A_k'] for r in d['rows']],float); L=np.log(X)
    y=A/np.sqrt(X)-d['leading_coefficient']*L**2; out={'predicted_a':a,'fits':[]}
    for first in (0,2,4):
        x_,L_,y_=X[first:],L[first:],y[first:]; w=x_**0.25
        for fixed in (False,True):
            cols=[L_,np.ones_like(L_),x_**(-1/6)] + ([] if fixed else [L_*x_**(-1/6)])
            M=np.column_stack(cols); t=y_-(a*L_*x_**(-1/6) if fixed else 0)
            c=np.linalg.lstsq(M*w[:,None],t*w,rcond=None)[0]; res=(t-M@c)*w
            out['fits'].append({'from_X':float(x_[0]),'a':a if fixed else float(c[3]),'a_fixed':fixed,'rms_residual_X^(1/4)':float(np.sqrt(np.mean(res**2)))})
    save('v011_counts.json',out)
# ---- the grammar itself ----
def source_E(word):
    E=1
    for N in word: E=(N+1)**2*E//gcd(E,N)
    return E
def grammar():
    out={}
    L=60; bad=0
    for a in range(2,L+2):
        for M in range(1,L+1):
            for N in range(1,L+1):
                g1=gcd(N,(M+1)**2); g2=gcd(M*N//g1,a*a)
                if source_E((a-1,M,N))*g1*g2!=(a*(M+1)*(N+1))**2: bad+=1
    out['formula_(1)']={'words_checked':L**3,'failures':bad,'arithmetic':'exact integers'}
    # G_3 at s=2: words from the grammar against zeta(2s) * sum_{M,N} - G_2, all letters up to T
    s=2.0; rows=[]
    z=float(mp.zeta(2*s)); cache={}
    def Ph(K):
        if K not in cache: cache[K]=Phi(K,s)
        return cache[K]
    for T in (40,80,160):
        n=np.arange(1,T+1,dtype=np.int64); direct=0.0
        for a1 in range(1,T+1):
            E1=(a1+1)**2
            E2=(n+1)**2*E1//np.gcd(E1,n)
            for E in E2.tolist():
                E3=(n+1)**2*E//np.gcd(E,n)
                direct+=float(np.sum(E3.astype(float)**-s))
        S=0.0; G2=0.0
        for M in range(1,T+1):
            b=M+1
            for N in range(1,T+1):
                g=gcd(N,b*b); w=((b*(N+1))**(-2*s))
                S+=w*g**s*Ph(M*N//g); G2+=w*g**s
        rows.append({'T':T,'G_3 from words':direct,'zeta(2s)*S - G_2':z*S-G2,'difference':direct-(z*S-G2)})
    out['G_3_at_s=2']=rows
    # control for the residue recipe: weights sigma_{-s} must give E_p=(1-p^(-1-3s))/(1-p^(-1-s))
    worst=0; s=1/3
    for p in (2,3,7,101):
        zz=p**(-s); y=1/p; x=p**(s-1)
        W=lambda t: 1/(1-t)+zz*t/((1-t)*(1-zz*t))
        Ep=(1-y)*(1-x)*W(x)+(1-zz*zz)*((1-y)*W(y)-1)
        worst=max(worst,abs(Ep-(1-p**(-1-3*s))/(1-p**(-1-s))))
    out['control_sigma_weights_largest_error']=worst
    save('v011_grammar.json',out)
if __name__=='__main__':
    {'grammar':grammar,'exponents':exponents,'local':local,'decomposition':decomposition,'shifted':shifted,'counts':counts}[sys.argv[1]]()
