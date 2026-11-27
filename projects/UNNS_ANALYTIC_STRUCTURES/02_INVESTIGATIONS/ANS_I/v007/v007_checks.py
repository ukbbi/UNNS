"""ANS-I v007 checks.  Usage: python3 -B v007_checks.py [census|exchange|depth]
Finite and floating-point checks; none of them is a proof."""
import sys, os, json, math, subprocess, tempfile, platform, itertools
import mpmath as mp, numpy as np
mp.mp.dps=40
HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'results')
def save(name,d):
    d['software']={'python':platform.python_version(),'numpy':np.__version__,'mpmath':mp.__version__}
    json.dump(d,open(os.path.join(OUT,name),'w'),indent=1); print(json.dumps(d,indent=1))
def B(s): # sum_{n>=2} (n-1)^s n^{-2s}, by the binomial expansion in 1/n
    return mp.nsum(lambda j:(-1)**int(j)*mp.binomial(s,int(j))*(mp.zeta(s+int(j))-1),[0,200],method='direct')
def constants():
    s=mp.findroot(lambda x:B(x)-1,mp.mpf('1.5463810'))
    lam=-mp.diff(B,s)
    return s,lam

def census():
    exe=os.path.join(tempfile.gettempdir(),'ans_census_%d'%os.getpid())
    subprocess.run(['gcc','-O2','-o',exe,os.path.join(HERE,'census.c'),'-lm'],check=True)
    rows=json.loads(subprocess.run([exe],capture_output=True,text=True,check=True).stdout); os.remove(exe)
    # independent enumeration at small thresholds
    from math import gcd, isqrt
    def brute(X):
        A=A1=C=depth=ones=0
        def rec(E,K,k,n1):
            nonlocal A,A1,C,depth,ones
            A+=1; A1+=K==1; C+=X//E; depth+=k; ones+=n1
            for N in range(1,min(X//E,isqrt(X))+1):
                g=gcd(E,N); E2=(N+1)**2*E//g
                if E2<=X: rec(E2,N*K//g,k+1,n1+(N==1))
        rec(1,1,0,0); return A,A1,C,depth/A,ones/depth
    agree=[]
    for r in rows:
        if r['X']<=100000:
            a,a1,c,d,o=brute(r['X'])
            agree.append(a==r['A'] and a1==r['N1'] and c==r['C'] and abs(d-r['mean_depth'])<1e-8 and abs(o-r['letter1_share'])<1e-8)
    s,lam=constants(); by={r['X']:r for r in rows}
    ratios=[{'T':T,'A(2T)/A(T)':by[2*T]['A']/by[T]['A'],'N1(2T)/N1(T)':by[2*T]['N1']/by[T]['N1']} for T in (10**e for e in range(3,9))]
    stats=[{'X':r['X'],'C/A':r['C']/r['A'],'max_sector_deviation':max(abs(x/r['A']-1/7) for x in r['sectors']),
            'mean_depth/logX':r['mean_depth']/math.log(r['X']),'mean_depth/mean_logQ':r['mean_depth']/r['mean_logQ'],'letter1_share':r['letter1_share'],
            'mean_logQ/logX':r['mean_logQ']/math.log(r['X']),'mean_logK/logX':(r['mean_logE']-r['mean_logQ'])/math.log(r['X'])} for r in rows]
    save('v007_census.json',{'predicted_limits':{'sigma_c':float(s),'2^sigma_c':float(mp.mpf(2)**s),'zeta(sigma_c)':float(mp.zeta(s)),
        'lambda_c':float(lam),'1/lambda_c':float(1/lam),'letter1_share':float(mp.mpf(4)**-s),'mean_logQ/logX':1,'mean_logK/logX':0},
        'independent_enumeration_agrees':agree,'ratios':ratios,'statistics':stats,'counts':rows})

# explicit exchange vectors for the order-seven quotient, letters 1,2,3
def exchange():
    s,_=constants(); a=math.log(9/8); b=math.log(4/3); cl=(4,0,0); out=[]
    L=3000
    x=np.arange(-L,L+1)
    X,Y=np.meshgrid(x,x,indexing='ij')          # delta2 = X, delta3 = Y, delta1 = -X-Y
    d=X*a+Y*b; g=(-(X+Y)*4)%7
    for eps in (0.1,0.01,0.001):
        for t in range(7):
            m=(g==t)&(d<0)&(d>-eps); size=np.abs(X)+np.abs(Y)+np.abs(X+Y); size=np.where(m,size,10**9)
            i=np.unravel_index(size.argmin(),size.shape)
            assert size[i]<10**9
            out.append({'eps':eps,'sector_shift':t,'delta':[int(-X[i]-Y[i]),int(X[i]),int(Y[i])],'d':float(d[i])})
    # multinomial ratio against exp(sigma d)
    r=[4,4.5,16/3]; pi=np.array([q**-float(s) for q in r]); pi/=pi.sum(); D=[-3,1,2]
    dd=sum(k*math.log(q) for k,q in zip(D,r)); rows=[]
    for M in (10**2,10**3,10**4,10**6):
        n=[int(round(p*M)) for p in pi]
        lr=sum(math.lgamma(v+1)-math.lgamma(v+k+1) for v,k in zip(n,D))
        rows.append({'M':M,'ratio/exp(sigma d)':math.exp(lr-float(s)*dd)})
    save('v007_exchange.json',{'vectors':out,'multinomial_test':{'delta':D,'rows':rows}})

# depth-resolved sectors: Monte Carlo of G_{chi,k}/G_k = E[chi K^-s]/E[K^-s]
def depth():
    s,_=constants(); s=float(s); L=10**6
    spf=list(range(L+2))
    for i in range(2,int((L+2)**.5)+1):
        if spf[i]==i:
            for j in range(i*i,L+2,i):
                if spf[j]==j: spf[j]=i
    phi={1:0,2:2,3:1}
    def ph(m):
        v=phi.get(m)
        if v is None:
            v=(ph(spf[m])+ph(m//spf[m]))%7 if spf[m]<m else 2*ph(m+1)%7
            phi[m]=v
        return v
    n=np.arange(1,L+1,dtype=float); c=np.cumsum((n/(n+1)**2)**s); c/=c[-1]
    g=np.random.default_rng(20261127); rows=[]
    for k in (1,2,4,6,8,12):
        T=200000; tot=np.zeros(7); sq=0.0
        W=np.searchsorted(c,g.random((T,k)))+1
        for w in W.tolist():
            E=K=1; h=0
            for N in w:
                q=math.gcd(E,N); K=N*K//q; E=(N+1)**2*E//q; h+=2*ph(N+1)-ph(N)
            v=K**-s; tot[h%7]+=v; sq+=v*v
        p=tot/tot.sum()
        rows.append({'k':k,'samples':T,'effective_samples':float(tot.sum()**2/sq),'sector_shares':[float(x) for x in p],'max_sector_deviation':float(np.abs(p-1/7).max())})
    save('v007_depth.json',{'sigma':s,'seed':20261127,'alphabet_truncation':L,'rows':rows})
if __name__=='__main__':
    {'census':census,'exchange':exchange,'depth':depth}[sys.argv[1]]()
