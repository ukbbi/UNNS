"""ANS-I v012 checks.  Usage: python3 -B v012_checks.py [algebra|representation|margins|lemma|remainder|shifted|leading]
Exact where stated, otherwise floating point.  Finite checks; none of them proves a theorem."""
import sys, os, json, math, platform, random
from fractions import Fraction as Fr
from math import gcd
import numpy as np, mpmath as mp, sympy as sp
mp.mp.dps=30
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__,'sympy':sp.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d)[:2500])
def factor(n):
    f={};p=2
    while p*p<=n:
        while n%p==0: f[p]=f.get(p,0)+1; n//=p
        p+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def primes(P):
    s=np.ones(P+1,bool); s[:2]=False
    for p in range(2,int(P**.5)+1):
        if s[p]: s[p*p::p]=False
    return [int(p) for p in np.nonzero(s)[0]]
# ---------- local data ----------
def Pz(z): return 1+z*z+z**3
def A_(z): return z*(1-z*z)/Pz(z)
def B_(z): return (1-z)*(1+z**3)/Pz(z)
def W1(t,z): return (1+A_(z)*t+(B_(z)-1)*t*t)/((1-t)*(1-t*t))
def W2(t,z): return (1+A_(z)*t/(1-z*z*t))/(1-t)
def WPhi(t,z): return (1+(z-z*z)*t-z*t*t)/((1-t)*(1-t*t))
def Phi_pp(v,z): return 1+(1-z)*(v//2+((v+1)//2)*z)
# ---------- algebra: T46g, residue identity, expansions ----------
def algebra():
    out={}
    z,t=sp.symbols('z t')
    L0=Pz(z)/(1+z*z)
    c=lambda mu: z**3/(1+z*z) if mu%2==0 else z*z*(1-z+z*z)/(1+z*z)
    w1=lambda j: 1 if j==0 else (Phi_pp(j,z)+c(j))/L0
    w2=lambda j: 1 if j==0 else (1+z-z**(2*j+1)/(1+z*z))/L0
    zero=lambda e: sp.cancel(sp.together(e))==0
    out['T46g_differences_j<=8']=all(zero(w1(j)-w1(j-1)-(A_(z) if j%2 else B_(z))) and zero(w2(j)-w2(j-1)-A_(z)*z**(2*j-2)) for j in range(1,9))
    N=9
    ser=lambda e: sp.series(e,t,0,N).removeO()
    out['T46g_generating_functions']=all(zero(ser(W1(t,z)).coeff(t,j)-w1(j)) and zero(ser(W2(t,z)).coeff(t,j)-w2(j)) for j in range(N))
    Q=lambda x: (1-z*x)*(1+A_(z)*x+(B_(z)-1)*x*x)/(1-x*x)          # q1
    R2=lambda x: (1-z*x)*(1+A_(z)*x/(1-z*z*x))                     # r2
    y=z**3; x=z**2
    E1=(1-y)*(1-x)*W1(x,z)+(1-z*z)*((1-y)*W2(y,z)-1)
    E2=(1-y)*(1-x)*W2(x,z)+(1-z*z)*((1-y)*W1(y,z)-1)
    fromB=1+(1-x)*((1-y)*W2(y,z)-1)+(Q(x)-1)
    fromA=1+(1-x)*((1-y)*W1(y,z)-1)+(R2(x)-1)
    out['residue_local_factor_equals_E1']=zero(E1-fromB); out['residue_local_factor_equals_E2']=zero(E2-fromA)
    out['E1p_series']=str(sp.series(E1,z,0,6)); out['E2p_series']=str(sp.series(E2,z,0,6))
    out['lowest_terms']={'q1(p^j)':[str(sp.series(sp.series(Q(t),t,0,6).removeO().coeff(t,j),z,0,8)) for j in range(1,6)],
                         'r2(p^j)':[str(sp.series(sp.series(R2(t),t,0,6).removeO().coeff(t,j),z,0,10)) for j in range(1,6)]}
    sig=lambda u: 1/((1-u)*(1-z*u))
    Eu=(1-y)*(1-x)*sig(x)+(1-z*z)*((1-y)*sig(y)-1)
    out['control_model_U_gives_(1-p^-2)/(1-p^-4/3)']=zero(Eu-(1-z**6)/(1-z**4))
    PhiS=sp.series(WPhi(t,z),t,0,8).removeO()
    out['Phi_generating_function_j<=7']=all(zero(PhiS.coeff(t,j)-Phi_pp(j,z)) for j in range(8))
    out['T46h_residual_factor']=str(sp.expand((1-z**3)*(1+z**3-z**4-z**5)))
    out['T46h_factorisation_of_Q']=str(sp.factor(1+z**3-z**4-z**5))
    save('v012_algebra.json',out)
# ---------- exact representation of alpha ----------
def representation():
    bad=0; n=0
    for u in range(1,121):
        for v in range(1,121):
            if gcd(u,v)!=1: continue
            M0=next(M for M in range(1,u*v+2) if M%u==0 and (M+1)%v==0); n+=1
            assert M0<=u*v
            al=Fr(M0+1,u*v)
            if v>=2:                      # alpha = j/u with j = inverse of v mod u, 1<=j<=u
                j=pow(v,-1,u) if u>1 else 1
                if j==0: j=u
                bad+=al!=Fr(j,u)
            j=(-pow(u,-1,v))%v if v>1 else 1
            if j==0: j=v
            bad+=al!=Fr(j,v)+Fr(1,u*v)
    save('v012_representation.json',{'coprime_pairs_u,v<=120':n,'failures':bad,'arithmetic':'exact'})
# ---------- exponent margins on the strip ----------
def margins():
    d=Fr(1,1500); rows=[]
    for s in (Fr(1,3)-d,Fr(1,3),Fr(1,3)+d):
        t=Fr(1,48); q=Fr(4,3); h=Fr(1,2)
        c={}
        # (name, value, bound): condition value < bound
        c['S1 F-moment p']=((-2*s+t)*q-1,-1); c['S1 F-moment p^2']=(2*((s+t)*q-1),-1)
        c['S1 G-moment p']=((-2*s+t)*4-1,-1); c['S1 G-moment p^2']=(8*t-2,-1)
        c['S1 total']=(1-3*s-t/9,0)
        c['S2 a,b']=(-(2*s-24*max(0,Fr(1,3)-s)),-h)
        for side in ('A','B'):
            long_=(-3*s+Fr(1,2)-s-3*s/4,-1)
            c[side+' term1 inner']=long_
            if side=='A':
                c['A term1 a']=(Fr(1,2)-4*s,-h); c['A term1 b']=(-3*s,-h)
                c['A term2 a']=(-4*s,-h); c['A term2 b']=(-2*s,-h)
            else:
                c['B term1 a']=(-3*s,-h); c['B term1 b']=(Fr(1,2)-4*s,-h)
                c['B term2 a']=(-2*s,-h); c['B term2 b']=(-4*s,-h)
            c[side+' term2 inner']=(-7*s/2,-1)
        e=3*d
        c['P_A a']=(-1+4*e,-h); c['P_A b']=(-2*s+4*e,-h); c['P_A inner']=(-s-1+e,-1)
        c['P_B a']=(-2*s+4*e,-h); c['P_B b']=(-1+4*e,-h); c['P_B inner']=(-s-1+e,-1)
        c['D_B ii a']=(-2*s,-h); c['D_B ii inner']=(-3*s-1-s/2,-1)
        c['R: theta<sigma']=(1-Fr(5,2)*s if s<Fr(1,3) else Fr(1,2)-s, s)
        rows.append({'sigma':str(s),'all_hold':all(v<b for v,b in c.values()),'values':{k:[float(v),float(b)] for k,(v,b) in c.items()}})
    save('v012_margins.json',{'delta':str(d),'rows':rows,'note':'strict inequalities used in the proofs, evaluated in exact fractions; epsilon powers omitted'})
# ---------- sanity check of the counting lemma ----------
def lemma():
    random.seed(12); s=1/3; rows=[]; worst=0
    zeta=lambda x: np.array([float(mp.zeta(2*s,float(a))) for a in x])
    for u in (97,360,1009,2048,3001,5000):
        F=np.zeros(u+1); units=[j for j in range(1,u+1) if gcd(j,u)==1]; F[units]=zeta(np.array(units)/u); avg=F[units].mean()
        for b in (1,7,101):
            if gcd(b,u)!=1: continue
            for N in (int(u**.5)+1,u//3+2,u,4*u,int(u**1.6)):
                S=0.0; best=0.0
                for n in range(N+1,2*N+1):
                    if gcd(n,u)!=1: continue
                    j=pow(b*n,-1,u) or u
                    S+=F[j]-avg; best=max(best,abs(S))
                bound=u**(.5-s)*N**(2*s)+(b*N)**(2*s)
                worst=max(worst,best/bound); rows.append({'u':u,'b':b,'N':N,'sup|Delta|/bound_without_epsilon':best/bound})
    save('v012_lemma.json',{'largest_ratio':worst,'rows':rows})
# ---------- remainder: fixed N mean values and residue ----------
def euler(local,P=2000,order=30,start=4):
    """product over primes of local(z), z = p^(-s0); local is given with s0"""
    f,s0=local; ps=primes(P); prod=mp.mpf(1)
    for p in ps: prod*=f(mp.mpf(p)**(-s0))
    co=mp.taylor(lambda z: mp.log(f(z)),0,order)
    assert all(abs(c)<mp.mpf('1e-12') for c in co[:start])
    tail=0
    for k in range(start,order+1):
        if abs(co[k])>0: tail+=co[k]*(mp.primezeta(k*s0)-mp.fsum(mp.mpf(p)**(-k*s0) for p in ps))
    return prod*mp.exp(tail)
def sieve(N,f):
    """multiplicative function with f(p,v) on 1..N+1"""
    w=np.ones(N+2); comp=np.zeros(N+2,bool)
    for p in range(2,N+2):
        if comp[p]: continue
        comp[p*p::p]=True
        q=p; v=1; prev=1.0
        while q<=N+1:
            cur=f(p,v); w[q::q]*=cur/prev; prev=cur; q*=p; v+=1
    return w
def lam(p,v,s=1/3):
    z=p**(-s); r=(v+1)//2
    H=lambda i: p**(s*min(v,2*i))*Phi_pp(v-min(v,2*i),z)
    hat=H(0)+sum((H(j)-H(j-1))/(p**(j-1)*(p-1)) for j in range(1,r+1))
    t=p**(-2*s); mu_=1; acc=0.0
    while t**mu_>1e-17: acc+=t**mu_*Phi_pp(mu_+v,z); mu_+=1
    return (hat+acc)/WPhi(t,z)
def remainder():
    s=mp.mpf(1)/3
    B=euler((lambda z:(1-z**3)*(1+z**3-z**4-z**5),s))
    Mean=euler((lambda z:(1-z**3)*WPhi(z**3,z),s))
    Cphi=float(mp.zeta(2*s)*mp.zeta(4*s)*B)/3          # residue of D_Phi at 1/3
    s=1/3; X=10**7
    Ph=sieve(X,lambda p,v:Phi_pp(v,p**(-s)))
    M=np.arange(1,X+1); rows=[]
    for N in (1,2,3,4,6,8,9,12,36):
        f=Ph[1:X+1].copy(); mean=float(Mean)
        for p,v in factor(N).items():
            z=p**(-s)
            mu_=np.zeros(X,np.int64); be=np.zeros(X,np.int64); q=p
            while q<=X+1:
                mu_[q-1::q]+=1; be[q-2::q]+=1; q*=p
            tab=np.array([[p**(s*min(v,2*b))*Phi_pp(m+v-min(v,2*b),z)/Phi_pp(m,z) for b in range(be.max()+1)] for m in range(mu_.max()+1)])
            f*=tab[mu_,be]
            # local factor of the mean value
            r=(v+1)//2; H=lambda i: p**(s*min(v,2*i))*Phi_pp(v-min(v,2*i),z)
            hat=H(0)+sum((H(j)-H(j-1))/(p**(j-1)*(p-1)) for j in range(1,r+1))
            y=1/p; mean*=(hat+sum(y**m*Phi_pp(m+v,z) for m in range(1,200)))/WPhi(y,z)
        cs=np.cumsum(f)
        lN=math.prod(lam(p,v) for p,v in factor(N).items())
        pred=4.5*Cphi*lN
        rows.append({'N':N,'lambda':lN,'predicted_coefficient':pred,
           'observed':{str(x):float(cs[x-1]-mean*x)/x**(2/3) for x in (10**4,10**5,10**6,10**7)}})
    T=10**6
    L=sieve(T,lam)
    n=np.arange(1,T+1,dtype=float); terms=((n+1)**(-2/3)-n**(-2/3))*L[1:T+1]; cs=np.cumsum(terms)
    save('v012_remainder.json',{'residue_of_D_Phi_at_1/3':Cphi,'residue_of_R_1_at_1/3':-Cphi,'fixed_N':rows,
        'residue_of_R_at_1/3_partial_sums':{str(x):Cphi*float(cs[x-1]) for x in (10**3,10**4,10**5,10**6)}})
# ---------- shifted series: the general residue formula on a second weight pair ----------
def shifted():
    s=mp.mpf(1)/3
    sg=lambda t,z: 1/((1-t)*(1-z*t))
    V1=lambda t,z: sg(t,z)/(1-t*t)                    # (sigma * squares)
    def loc(kind):
        def f(z):
            y=z**3; x=z**2
            D=(1-y)*(V1(y,z)+sg(y,z))-1
            E1=(1-y)*(1-x)*V1(x,z)+(1-z*z)*((1-y)*sg(y,z)-1)
            E2=(1-y)*(1-x)*sg(x,z)+(1-z*z)*((1-y)*V1(y,z)-1)
            return (D,E1,E2)[kind]
        return f
    D,E1,E2=[float(euler((loc(i),s),start=3)) for i in range(3)]
    coef=1.5*float(mp.zeta(2*s))*(E1+E2)
    s=1/3; X=2*10**7
    a=sieve(X,lambda p,v: sum((p**(-s))**i*((v-i)//2+1) for i in range(v+1)))
    b=sieve(X,lambda p,v: sum((p**(-s))**i for i in range(v+1)))
    cs=np.cumsum(a[1:X+1]*b[2:X+2])
    save('v012_shifted.json',{'weights':'(sigma_{-1/3} * indicator of squares)(M) and sigma_{-1/3}(M+1)','D':D,'E1':E1,'E2':E2,
        'predicted_coefficient_of_X^(2/3)':coef,'rows':{str(x):float(cs[x-1]-D*x)/x**(2/3) for x in (10**4,10**5,10**6,10**7,2*10**7)}})
# ---------- leading terms ----------
def leading():
    def D(z):
        y=z*z; return (1-y)*(W1(y,z)+W2(y,z))-1
    s=mp.mpf(1)/2
    Dh=euler((D,s),start=3); H=euler((lambda z: 1-(z**5+z**6)/(1+z*z),s),start=5)
    sh=json.load(open(os.path.join(HERE,'..','v011','results','v011_shifted.json')))
    z23=float(mp.zeta(mp.mpf(2)/3)); H13=sh['euler_products'][-1]['H(1/3)']; rV=sh['residue_of_V_conjectured']
    kappa=float(Dh*mp.zeta(1.5)*H)
    save('v012_leading.json',{'D(1/2)*zeta(3/2)*H(1/2)':kappa,'kappa_3_recorded_in_v006':5.105352,
      'coefficient_of_(s-1/3)^-2_in_G_3':z23**2*H13*rV/3,'residue_of_V_at_1/3':rV,'coefficient_of_X^(1/3)logX_formal':z23**2*H13*rV})
if __name__=='__main__':
    {'algebra':algebra,'representation':representation,'margins':margins,'lemma':lemma,'remainder':remainder,'shifted':shifted,'leading':leading}[sys.argv[1]]()
