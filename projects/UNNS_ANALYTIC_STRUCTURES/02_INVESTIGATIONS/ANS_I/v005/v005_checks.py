"""ANS-I v005 checks.  Usage: python3 -B v005_checks.py [continuation|constants|count]
Finite and statistical checks of the proofs in PROOFS.md; none of them is a proof."""
import sys, os, json, math, random, subprocess, shutil, tempfile, platform
from math import gcd
import numpy as np, mpmath as mp
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
R=(1,2,3)
def r(N): return (N+1)**2/N
def v(p,n):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def save(name,d):
    d['software']={'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d,indent=1))

# ---------------------------------------------------------------- continuation
SIG=1.5463810
NMAX=10**6
def sieve(n):
    s=list(range(n+1))
    for i in range(2,int(n**.5)+1):
        if s[i]==i:
            for j in range(i*i,n+1,i):
                if s[j]==j: s[j]=i
    return s
SPF=None; FC={}
def fac(n):
    f=FC.get(n)
    if f is None:
        f={}; m=n
        while m>1:
            p=SPF[m]; f[p]=f.get(p,0)+1; m//=p
        FC[n]=f
    return f
def source(word):
    """v_p(K) = max(0, max_j (v_p(N_j) - S_p(j-1)))"""
    S={}; K={}
    for N in word:
        d=fac(N); u=fac(N+1)
        for p,e in d.items():
            x=e-S.get(p,0)
            if x>K.get(p,0): K[p]=x
        for p,e in u.items(): S[p]=S.get(p,0)+2*e
        for p,e in d.items(): S[p]=S.get(p,0)-e
    return K
def source_rec(word):
    E=K=1
    for N in word:
        g=gcd(E,N); K=N*K//g; E=(N+1)**2*E//g
    return K
Xr={p:{N:2*v(p,N+1)-v(p,N) for N in R} for p in (2,3)}
m_min={p:min(Xr[p].values()) for p in (2,3)}
d_max={p:max(v(p,N) for N in R) for p in (2,3)}
def good(word,marked,start):
    for p in (2,3):
        L=0
        for j,N in enumerate(word,1):
            mk=(j-1) in marked
            if j>start:
                dem=d_max[p] if mk else v(p,N)
                if dem-L>0: return False
            L+= m_min[p] if mk else 2*v(p,N+1)-v(p,N)
    return True
def continuation():
    global SPF
    SPF=sieve(NMAX+2)
    rng=np.random.default_rng(20261127); random.seed(20261127)
    N=np.arange(1,NMAX+1,dtype=float); w=(N/(N+1)**2)**SIG; cdf=np.cumsum(w); cdf/=cdf[-1]
    draw=lambda k:[int(x)+1 for x in np.searchsorted(cdf,rng.random(k))]
    out={'sigma':SIG,'alphabet_truncation':NMAX,'seed':20261127,'m_p':m_min,'d_p':d_max}
    # 1. source formula against the recurrence
    bad=0
    for _ in range(3000):
        wd=draw(random.randint(1,25)); K=source(wd); val=1
        for p,e in K.items(): val*=p**e
        bad+= val!=source_rec(wd)
    out['source_formula_words']=3000; out['source_formula_mismatches']=bad
    # 2. invariance of K under resampling the marked letters
    res=[]
    for k,eps,eta in ((40,.5,.5),(120,.5,.5),(400,.5,.5),(400,.25,.9)):
        trials=1500; nG=0; chG=0; rsG=0; nB=0; chB=0
        for _ in range(trials):
            wd=draw(k); st=int(eps*k)
            J={i for i in range(st,k) if wd[i] in R and random.random()<eta}
            g=good(wd,J,st); K0=source(wd); changed=False
            wt=[r(n)**-SIG for n in R]
            alts=[]
            for _t in range(8):
                w2=list(wd)
                for i in J: w2[i]=random.choices(R,weights=wt)[0]
                alts.append(w2)
            for fill in R:
                w2=list(wd)
                for i in J: w2[i]=fill
                alts.append(w2)
            for w2 in alts:
                assert good(w2,J,st)==g
                if source(w2)!=K0: changed=True
            if g: nG+=1; chG+=changed
            else: nB+=1; chB+=changed
        res.append({'k':k,'eps':eps,'eta':eta,'trials':trials,'resamplings_per_trial':11,
                    'good':nG,'good_with_changed_K':chG,'bad':nB,'bad_with_changed_K':chB})
    out['resampling']=res
    # 3. modulus of c
    B=sum(r(n)**-SIG for n in R); wt=np.array([r(n)**-SIG for n in R])/B
    worst=0; rows=[]
    for tau in (0.1,1.0,5.0,20.0,100.0):
        c=sum(wt[i]*r(n)**(-1j*tau) for i,n in enumerate(R))
        idn=1-2*sum(wt[i]*wt[j]*(1-math.cos(tau*math.log(r(R[j])/r(R[i])))) for i in range(3) for j in range(i+1,3))
        worst=max(worst,abs(abs(c)**2-idn)); rows.append({'tau':tau,'abs_c':abs(c)})
    out['abs_c']=rows; out['identity_error']=worst
    # 4. Monte Carlo of |E K^-s Q^-i tau| (finite-sample values)
    mc=[]
    for tau in (1.0,5.0):
        s=SIG+1j*tau
        for k in (2,5,10,20,40):
            M=20000; tot=0; tot2=0
            for _ in range(M):
                wd=draw(k); K=source(wd)
                lk=sum(e*math.log(p) for p,e in K.items()); lq=sum(math.log(r(n)) for n in wd)
                z=np.exp(-s*lk-1j*tau*lq); tot+=z; tot2+=abs(z)
            mc.append({'tau':tau,'k':k,'samples':M,'abs_mean':abs(tot)/M,'mean_abs':tot2/M})
    out['monte_carlo']=mc
    save('v005_continuation.json',out)

# ---------------------------------------------------------------- explicit constants at sigma_c
def constants():
    mp.mp.dps=30; s=mp.mpf(SIG); M=200000
    n=np.arange(1,M+1,dtype=float); w=(n/(n+1)**2)**SIG
    B=float(w.sum()+mp.zeta(s,M+1.5))      # numerical tail estimate
    nu=w/B; eta=0.5; nuR=float(nu[:3].sum())
    out={'sigma':SIG,'B_numeric':B,'truncation':M,'eta':eta,'nu_R':nuR,'primes':{}}
    for p in (2,3):
        vp=np.zeros(M+2,dtype=np.int64); q=p
        while q<=M+1: vp[q::q]+=1; q*=p
        d=vp[1:M+1]; u=vp[2:M+2]; X=2*u-d
        mu=float((nu*X).sum()); ER=float((nu[:3]*X[:3]).sum()/nuR)
        drift1=mu-eta*nuR*(ER-m_min[p])
        best=None
        for th in np.arange(0.005,0.30,0.005):
            if th>=(SIG-1)*math.log(p): break
            phi0=float((nu*np.exp(-th*X)).sum())
            phi1=phi0+eta*float((nu[:3]*(math.exp(-th*m_min[p])-np.exp(-th*X[:3]))).sum())
            if best is None or max(phi0,phi1)<best[0]: best=(max(phi0,phi1),float(th),phi0,phi1)
        out['primes'][p]={'drift':mu,'thinned_drift':drift1,'theta':best[1],'phi0':best[2],'phi1':best[3]}
    out['note']='floating-point values over a truncated alphabet; illustration only, not certified'
    save('v005_constants.json',out)

# ---------------------------------------------------------------- depth-k counting
def primes(n):
    s=bytearray([1])*(n+1); s[:2]=b'\0\0'
    for i in range(2,int(n**.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(s[i*i::i]))
    return [i for i in range(n+1) if s[i]]
def local(p,kmax,tol=1e-17):
    """c_p(k) = E p^{(1/2) sum min(e_{i-1}, d_i)} by dynamic programming on e."""
    J=int(math.ceil(2*math.log(1/tol)/math.log(p)))+1
    q=[(1-1/p)*p**-j for j in range(1,J+1)]
    st={0:1.0}; out=[1.0]
    for i in range(kmax):
        new={}
        for e,w in st.items():
            new[e]=new.get(e,0)+w*(1-2/p)
            for j,qj in enumerate(q,1):
                x=w*qj*p**(min(e,j)/2)          # d = j
                if x>tol*1e-3: new[max(e-j,0)]=new.get(max(e-j,0),0)+x
                x=w*qj                          # u = 2j
                if x>tol*1e-3: new[e+2*j]=new.get(e+2*j,0)+x
        st=new; out.append(sum(st.values()))
    return out
def count():
    out={'kappa':{},'local_checks':{}}
    for P in (20000,200000):
        ps=primes(P); logs=[0.0]*7
        for p in ps:
            c=local(p,6)
            for k in range(1,7): logs[k]+=math.log(c[k])
        tail=float(mp.primezeta(1.5))-sum(p**-1.5 for p in ps)
        out['kappa'][P]={k:math.exp(logs[k]+math.comb(k,2)*tail) for k in range(1,7)}
    kap=out['kappa'][200000]
    # depth two against the closed product of ANS-T13
    worst=0
    for p in primes(500):
        t=1+(1-p**-.5)*sum(p**(-j/2-math.ceil(j/2)) for j in range(1,200))
        worst=max(worst,abs(local(p,2)[2]-t))
    out['local_checks']['depth2_vs_T13_max_error']=worst
    out['local_checks']['(c_p-1)p^1.5/C(k,2)']={p:[(local(p,6)[k]-1)*p**1.5/math.comb(k,2) for k in range(2,7)] for p in (101,1009,10007)}
    # DP against direct enumeration of truncated valuations at p=2,3, depth 3
    def direct(p,J=22):
        types=[(0,0,1-2/p)]+[(2*j,0,(1-1/p)*p**-j) for j in range(1,J)]+[(0,j,(1-1/p)*p**-j) for j in range(1,J)]
        tot=0
        for u1,d1,a in types:
            e1=u1
            for u2,d2,b in types:
                e2=u2+max(e1-d2,0); f2=min(e1,d2)
                tot+=a*b*sum(c*p**((f2+min(e2,d3))/2) for u3,d3,c in types)
        return tot
    out['local_checks']['dp_vs_direct_depth3']={p:[local(p,3)[3],direct(p,J)] for p,J in ((3,30),(5,24))}
    # exact counts
    exe=os.path.join(tempfile.gettempdir(),'ans_depth_count_%d'%os.getpid())
    subprocess.run(['gcc','-O2','-o',exe,os.path.join(HERE,'depth_count.c'),'-lm'],check=True)
    def brute(k,X):
        def rec(E,d):
            if d==k: return 1
            s=0
            for N in range(1,min(X//E,math.isqrt(X))+1):
                E2=(N+1)**2*E//gcd(E,N)
                if E2<=X: s+=rec(E2,d+1)
            return s
        return rec(1,0)
    run=lambda k,X:int(subprocess.run([exe,str(k),str(X)],capture_output=True,text=True,check=True).stdout)
    out['brute_force_agreement']=[[k,X,run(k,X),brute(k,X)] for X in (1000,100000,1000000) for k in (2,3,4)]
    fits={}
    for k,es in ((2,range(6,13)),(3,range(6,11)),(4,range(6,10))):
        data=[(10**e,run(k,10**e)) for e in es]
        lead=kap[k]/(2**(k-1)*math.factorial(k-1))
        L=np.array([math.log(X) for X,_ in data]); y=np.array([A/math.sqrt(X) for X,A in data])
        full=np.linalg.lstsq(np.vander(L,k),y,rcond=None)[0]
        rem=y-lead*L**(k-1)
        low=np.linalg.lstsq(np.vander(L,k-1),rem,rcond=None)[0]
        fits[k]={'counts':data,'predicted_leading':lead,'unconstrained_fit_leading':float(full[0]),
                 'ratio_A_to_leading_term':[float(a/(lead*l**(k-1))) for a,l in zip(y,L)],
                 'lower_coefficients_with_leading_fixed':[float(a) for a in low],
                 'max_fit_residual_with_leading_fixed':float(np.max(np.abs(rem-np.vander(L,k-1)@low)))}
    os.remove(exe)
    out['counting']=fits
    save('v005_counting.json',out)
if __name__=='__main__':
    {'continuation':continuation,'constants':constants,'count':count}[sys.argv[1]]()
