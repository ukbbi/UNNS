"""ANS-I v006 checks.  Usage: python3 -B v006_checks.py [algebra|local|characters|sectors]
Finite checks of the proofs in PROOFS.md; none of them is a proof."""
import sys, os, json, math, cmath, random, subprocess, tempfile, platform
import numpy as np, mpmath as mp
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
SIG=1.5463810
def r(N): return (N+1)**2/N
def save(name,d):
    d['software']={'python':platform.python_version(),'numpy':np.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d,indent=1))
def spf_sieve(n):
    s=list(range(n+1))
    for i in range(2,int(n**.5)+1):
        if s[i]==i:
            for j in range(i*i,n+1,i):
                if s[j]==j: s[j]=i
    return s

# ---- the quotient of order seven
def algebra():
    L=10**6; s=spf_sieve(L+2); phi=[0]*(L+3)
    for m in range(2,L+3):
        if s[m]<m: phi[m]=(phi[s[m]]+phi[m//s[m]])%7
        elif m==2: phi[m]=2
        elif m==3: phi[m]=1
        else:
            k=m+1; t=0
            while k>1: t+=phi[s[k]]; k//=s[k]
            phi[m]=2*t%7
    cls=lambda N:(2*phi[N+1]-phi[N])%7
    bad=[p for p in range(2,L+1) if s[p]==p and cls(p)!=0]
    hist=[0]*7
    for N in range(1,L+1): hist[cls(N)]+=1
    save('v006_algebra.json',{'limit':L,'class_r1_r2_r3':[cls(1),cls(2),cls(3)],
        'primes_checked':sum(1 for p in range(2,L+1) if s[p]==p),'prime_labels_with_nonzero_class':len(bad),
        'letters_N_up_to_limit_per_class':hist})

# ---- local coupling asymptotic
def local(p,kmax,tol=1e-19):
    J=int(math.ceil(2*math.log(1/tol)/math.log(p)))+1
    q=[(1-1/p)*p**-j for j in range(1,J+1)]
    # track c-1 without cancellation: store (probability, excess = weighted - probability)
    st={0:(1.0,0.0)}; out=[0.0]
    for i in range(kmax):
        new={}
        def add(e,a,b):
            x,y=new.get(e,(0.0,0.0)); new[e]=(x+a,y+b)
        for e,(P,D) in st.items():
            add(e,P*(1-2/p),D*(1-2/p))
            for j,qj in enumerate(q,1):
                m=min(e,j); g=math.expm1(m/2*math.log(p))
                if qj*(P+D)*(1+g)<tol: continue
                add(max(e-j,0),P*qj,D*qj*(1+g)+P*qj*g)
                add(e+2*j,P*qj,D*qj)
        st=new; out.append(sum(D for P,D in st.values()))
    return out
def localcheck():
    rng=random.Random(20261127); viol=0; N=200000
    for _ in range(N):
        k=rng.randint(1,8); e=0; A=D=C=0
        for i in range(k):
            t=rng.random(); j=rng.randint(1,5)
            u,d=(0,0) if t<.3 else ((2*j,0) if t<.65 else (0,j))
            m=min(e,d); C+=m; A+=u//2; D+=d; e=u+max(e-d,0)
        viol+= 3*C>2*(A+D) or C>min(2*A,D)
    rows=[]
    for p in (11,101,1009,10007,100003):
        c=local(p,6)
        rows.append({'p':p,'(c_p-1-binom(k,2) p^-3/2) p^2':{k:(c[k]-math.comb(k,2)*p**-1.5)*p**2 for k in range(2,7)},
                     '(c_p-1-two terms) p^5/2':{k:(c[k]-math.comb(k,2)*p**-1.5-math.comb(k,3)*p**-2)*p**2.5 for k in range(2,7)}})
    # Euler products with one and with two tail terms
    ps=lambda n:[i for i,q in enumerate(spf_sieve(n)) if i>1 and q==i]
    full15=float(mp.primezeta(1.5)); full2=float(mp.primezeta(2))
    kap=[]
    for P in (2000,20000,200000):
        primes=ps(P); logs=[0.0]*7
        for p in primes:
            c=local(p,6)
            for k in range(2,7): logs[k]+=math.log1p(c[k])
        t15=full15-math.fsum(p**-1.5 for p in primes); t2=full2-math.fsum(p**-2.0 for p in primes)
        kap.append({'P':P,'one_term':{k:math.exp(logs[k]+math.comb(k,2)*t15) for k in range(2,7)},
                    'two_terms':{k:math.exp(logs[k]+math.comb(k,2)*t15+math.comb(k,3)*t2) for k in range(2,7)}})
    save('v006_local.json',{'random_sequences':N,'bound_C_violations':viol,'expansion':rows,'kappa':kap})

# ---- characters: cancellation factor and source invariance with a larger exchange set
def characters():
    R=(1,2,3); w=np.array([r(n)**-SIG for n in R]); w/=w.sum(); cl=(4,0,0)
    grid=np.linspace(0,500,500001); rows=[]
    for j in range(1,7):
        c=sum(w[i]*cmath.exp(2j*math.pi*j*cl[i]/7)*np.exp(-1j*grid*math.log(r(n))) for i,n in enumerate(R))
        a=np.abs(c); rows.append({'j':j,'abs_c_at_tau0':float(a[0]),'max_abs_c_on_grid':float(a.max()),'at_tau':float(grid[a.argmax()])})
    c0=sum(w[i]*np.exp(-1j*grid*math.log(r(n))) for i,n in enumerate(R))
    # source invariance for an exchange set containing a larger prime label
    L=10**5; s=spf_sieve(L+2); cache={}
    def fac(n):
        f=cache.get(n)
        if f is None:
            f={}; m=n
            while m>1: f[s[m]]=f.get(s[m],0)+1; m//=s[m]
            cache[n]=f
        return f
    def source(word):
        S={}; K={}
        for N in word:
            d=fac(N); u=fac(N+1)
            for p,e in d.items():
                if e-S.get(p,0)>K.get(p,0): K[p]=e-S.get(p,0)
            for p,e in u.items(): S[p]=S.get(p,0)+2*e
            for p,e in d.items(): S[p]=S.get(p,0)-e
        return K
    RR=(1,2,3,5); P=sorted({p for N in RR for p in list(fac(N))+list(fac(N+1))})
    X={p:{N:2*fac(N+1).get(p,0)-fac(N).get(p,0) for N in RR} for p in P}
    m={p:min(X[p].values()) for p in P}; dm={p:max(fac(N).get(p,0) for N in RR) for p in P}
    def good(word,J,st):
        for p in P:
            Lw=0
            for i,N in enumerate(word):
                if i>=st and (dm[p] if i in J else fac(N).get(p,0))-Lw>0: return False
                Lw+= m[p] if i in J else 2*fac(N+1).get(p,0)-fac(N).get(p,0)
        return True
    nu=np.arange(1,L+1,dtype=float); cdf=np.cumsum((nu/(nu+1)**2)**SIG); cdf/=cdf[-1]
    g=np.random.default_rng(20261127); random.seed(20261127); inv=[]
    for k in (60,200,600):
        G=chG=B=chB=0
        for _ in range(1500):
            word=[int(x)+1 for x in np.searchsorted(cdf,g.random(k))]; st=k//2
            J={i for i in range(st,k) if word[i] in RR and random.random()<.5}
            ok=good(word,J,st); K0=source(word); changed=False
            for t in range(10):
                w2=list(word)
                for i in J: w2[i]=RR[t] if t<4 else random.choice(RR)
                changed|=source(w2)!=K0
            if ok: G+=1; chG+=changed
            else: B+=1; chB+=changed
        inv.append({'k':k,'good':G,'good_with_changed_K':chG,'bad':B,'bad_with_changed_K':chB})
    save('v006_characters.json',{'sigma':SIG,'grid':'tau in [0,500], step 0.001','order_seven':rows,
        'trivial_character_max_abs_c_for_tau_ge_1':float(np.abs(c0)[grid>=1].max()),
        'exchange_set':list(RR),'primes':P,'invariance':inv})

# ---- exact sector counts
def sectors():
    exe=os.path.join(tempfile.gettempdir(),'ans_sector_%d'%os.getpid())
    subprocess.run(['gcc','-O2','-o',exe,os.path.join(HERE,'sector_count.c')],check=True)
    def brute(X):
        from math import gcd
        s=spf_sieve(X+2); memo={1:0,2:2,3:1}
        def phi(m):
            if m not in memo:
                if s[m]<m: memo[m]=(phi(s[m])+phi(m//s[m]))%7
                else: memo[m]=2*phi(m+1)%7
            return memo[m]
        c=[0]*7
        def rec(E,h):
            c[h]+=1
            for N in range(1,min(X//E,math.isqrt(X))+1):
                E2=(N+1)**2*E//gcd(E,N)
                if E2<=X: rec(E2,(h+2*phi(N+1)-phi(N))%7)
        rec(1,0); return c
    rows=[]
    for e in range(3,9):
        c=[int(x) for x in subprocess.run([exe,str(10**e)],capture_output=True,text=True,check=True).stdout.split()]
        row={'X':10**e,'counts':c,'A':sum(c),'proportions':[x/sum(c) for x in c]}
        if e<=5: row['brute_force_agrees']=brute(10**e)==c
        rows.append(row)
    os.remove(exe); save('v006_sectors.json',{'one_seventh':1/7,'rows':rows})
if __name__=='__main__':
    {'algebra':algebra,'local':localcheck,'characters':characters,'sectors':sectors}[sys.argv[1]]()
