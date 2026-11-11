import json,sys,os
from fractions import Fraction
from fibparam import F
import fibsel2
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+"/sq")
def fib_samples(r,npts=26):
    C=fibsel2.CLS[r]; odd=r%2; hres=(r//2)%6
    hs=[h for h in range(12,12+6*(npts+2)) if h%6==hres][:npts]; out=[]
    for h in hs:
        k=2*h+odd; S=F[k]; st=[]
        for i,sg in enumerate(C.sign):
            N=C.label(i,F[h]); Sa=S//N*(N+1)**2 if sg=='+' else S*N//(N+1)**2
            st.append((sg,N,S,Sa)); S=Sa
        assert S==F[k+1]; out.append(dict(steps=st,x0=F[k]))
    return out
def sq_direct_samples(npts=26):
    import u2sq_selector as Q
    res={}
    for r,c in Q.CLS.items():
        out=[]
        for t in range(c['t0']+2,c['t0']+2+npts):
            n=24*t+r; S=n*n; st=[]
            for i,sg in enumerate(c['signs']):
                N=Q._label(r,i,t); Sa=S//N*(N+1)**2 if sg=='+' else S*N//(N+1)**2
                st.append((sg,N,S,Sa)); S=Sa
            assert S==(n+1)**2; out.append(dict(steps=st,x0=n*n))
        res[r]=out
    return res
def wrapper_samples(npts=26):
    """wrapper: -(n-1); successor identity of U2-001 (class c); +x.  S before/after as in the real route."""
    import u1_bnd_lib as L, sympy as sp
    res={}
    for ident in L.IDENTITIES:
        M,r=ident['M'],ident['r']; t0=[t0 for (nm,M2,r2,t0,st) in L._I if nm==ident['name']][0]
        out=[]
        for t in range(t0+2,t0+2+npts):
            m=M*t+r; n=m+1
            if m<4: continue
            st=[]; S=n*n; Sa=m; st.append(('-',m,S,Sa)); S=Sa
            for sg,e in ident['steps']:
                N=int(e.subs(L.T,t)); Sa=S//N*(N+1)**2 if sg=='+' else S*N//(N+1)**2
                st.append((sg,N,S,Sa)); S=Sa
            assert S==m+1
            Sa=S*S; st.append(('+',S,S,Sa))
            out.append(dict(steps=st,x0=n*n))
        res[ident['name']]=out
    return res
