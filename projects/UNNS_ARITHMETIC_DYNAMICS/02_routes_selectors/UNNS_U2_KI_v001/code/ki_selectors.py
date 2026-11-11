"""U2-KI selectors: the frozen R3 controllers are NOT modified; they are imported from baseline_R3_frozen/.
Optimized variants (Fibonacci v2-KI, squares direct-KI, squares wrapper-KI) execute only certified direct-state shortcuts (KI-1)
and fall back on the baseline parameter recovery where no shortcut is certified.  Route tables, graph edges, membership test,
mod-24 dispatch and the small-index table are the baseline's, unchanged."""
import sys,os,json
from fractions import Fraction
from math import isqrt,gcd
HERE=os.path.dirname(os.path.abspath(__file__)); BASE=HERE+"/../baseline_R3_frozen"
sys.path.insert(0,BASE+"/code/sq"); sys.path.insert(0,BASE+"/code")
import fibsel2, harness as H            # frozen R3 modules (harness monkeypatches the squares decoders with counted versions)
import u2sq_selector as Q, u2_selector as U2
from fibsel2 import ACC, REJECT
class KC:                               # extra counters (never read by the selectors)
    recoveries=0; shortcuts=0; mults=0; isqrts=0; hmults=0
    @classmethod
    def reset(c): c.recoveries=0; c.shortcuts=0; c.mults=0; c.isqrts=0; c.hmults=0
    @classmethod
    def snap(c): return dict(recoveries=c.recoveries,shortcuts=c.shortcuts,sc_mults=c.mults,sc_isqrts=c.isqrts,horner_mults=c.hmults)
# ---- counting wrappers around frozen functions (behaviour unchanged)
_orig_recover=fibsel2.Class.recover
def _rec(self,i,x): KC.recoveries+=1; return _orig_recover(self,i,x)
fibsel2.Class.recover=_rec
_hor0=Q._hor
def _hor1(cs,t): KC.hmults+=max(0,len(cs)-1); return _hor0(cs,t)
Q._hor=_hor1
_sval0=U2.s_val
def _sval1(name,i,t):
    cn,cd=U2.EVAL[name][i]; KC.hmults+=max(0,len(cn)-1)+max(0,len(cd)-1); return _sval0(name,i,t)
U2.s_val=_sval1
_dec=Q._decode
def _qdec(r,i,x): KC.recoveries+=1; return _dec(r,i,x)
Q._decode=_qdec
_u2dec=U2.decode_t
def _u2d(name,i,x,t0): KC.recoveries+=1; return _u2dec(name,i,x,t0)
U2.decode_t=_u2d
# ---- shortcut tables from the KI-1 certificates
def _tab(rec):
    k=rec['kind']
    if k=='const': return ('const',int(Fraction(rec['value'])))
    if k=='affine':
        assert rec['certified']; c0,c1=Fraction(rec['c0']),Fraction(rec['c1'])
        den=c0.denominator*c1.denominator//gcd(c0.denominator,c1.denominator)
        return ('affine',int(c0*den),int(c1*den),den)
    if k=='quad':
        assert rec['certified'] and rec['rel']['11']=='0' and rec['rel']['21']=='0'
        k20,k10,k00,k01=(int(Fraction(rec['rel'][s])) for s in ('20','10','00','01'))
        sW=rec['sign_W']; assert rec['sign_A2']==1 and sW in (1,-1)
        return ('quad',k20,k10,k00,k01,sW)
    return None
def load_tables(path=None):
    d=json.load(open(path or HERE+"/../data/ki1_identities.json"))
    T={'fib':{}, 'sqd':{}, 'sqw':{}}
    for r,L in d['fibonacci'].items():
        for i,rec in enumerate(L): T['fib'][(int(r),i)]=_tab(rec)
    for r,L in d['squares_direct'].items():
        for i,rec in enumerate(L): T['sqd'][(int(r),i)]=_tab(rec)
    for nm,L in d['squares_wrapper'].items():
        for i,rec in enumerate(L): T['sqw'][(nm,i)]=_tab(rec)
    return T
TABLES=load_tables()
def shortcut(tab,S):
    """N from the current state S alone.  None if the certified form does not apply (perfect-square / divisibility guard)."""
    k=tab[0]; KC.shortcuts+=1
    if k=='const': return tab[1]
    if k=='affine':
        _,n0,n1,den=tab; KC.mults+=1; v=n0+n1*S
        return v//den if v%den==0 else None
    _,A2,A1,k00,k01,sW=tab                       # A2 N^2 + A1 N + (k00 + k01 S) = 0 ; W = 2 A2 N + A1 = sW*sqrt(Delta)
    D=A1*A1-4*A2*(k00+k01*S); KC.mults+=2; KC.isqrts+=1
    if D<0: return None
    r=isqrt(D)
    if r*r!=D: return None
    v=sW*r-A1
    return v//(2*A2) if v%(2*A2)==0 else None
# ================= Fibonacci
def fib_route_baseline(x):
    ACC.reset(); KC.reset(); S,mv,st=fibsel2.route(x); return S,mv,st,dict(ACC.snap(),**KC.snap())
def fib_route_ki(x):
    ACC.reset(); KC.reset()
    if x in fibsel2.SMALL:
        S,mv,st=fibsel2.route(x); return S,mv,st,dict(ACC.snap(),**KC.snap())
    m=fibsel2.membership(x)
    if m is None: return None,[],REJECT,dict(ACC.snap(),**KC.snap())
    L,sg=m; y=(x+L)//2; key=(x%24,y%24)
    if key not in fibsel2.KTAB: return None,[],REJECT,dict(ACC.snap(),**KC.snap())
    r=fibsel2.KTAB[key]%12; C=fibsel2.CLS[r]; S=x; mv=[]
    for i,sgn_ in enumerate(C.sign):
        tab=TABLES['fib'][(r,i)]; N=None
        if tab is not None:
            N=shortcut(tab,S)
            if N is None: return None,mv,"shortcut-failed",dict(ACC.snap(),**KC.snap())
        else:
            t=C.recover(i,S)
            if t is None: return None,mv,"recovery-failed",dict(ACC.snap(),**KC.snap())
            N=C.label(i,t)
            if N is None: return None,mv,"label-failed",dict(ACC.snap(),**KC.snap())
        if sgn_=='+':
            if S%N: return None,mv,"illegal",dict(ACC.snap(),**KC.snap())
            S=S//N*(N+1)**2
        else:
            if S%((N+1)**2): return None,mv,"illegal",dict(ACC.snap(),**KC.snap())
            S=S*N//(N+1)**2
        mv.append((sgn_,N))
    return S,mv,"route",dict(ACC.snap(),**KC.snap())
# ================= squares, direct (85 control states): baseline sigma_direct with shortcuts for states ("c",r,i), i>=1
def sigma_direct_ki(x,q):
    if q==Q.READY or q[0]=="S": return Q.sigma_direct(x,q)           # READY / special table: unchanged (no recovery occurs there)
    _,r,i=q; tab=TABLES['sqd'][(r,i)]
    if tab is None: return Q.sigma_direct(x,q)
    s=Q.CLS[r]["signs"][i]; N=shortcut(tab,x)
    if N is None: raise ArithmeticError("shortcut guard failed")
    return (s,N,("c",r,i+1) if i+1<len(Q.CLS[r]["signs"]) else Q.READY)
# ================= squares wrapper (45 control states): -(n-1); U2-001 successor with shortcuts; +x
def u2_sigma_ki(x,q):
    if q==U2.READY:
        if x==1 or x==3: return U2.sigma(x,q)
        c=U2.class_of(x); tab=TABLES['sqw'].get((c,1))
        if tab is None: return U2.sigma(x,q)
        N=shortcut(tab,x)
        if N is None: raise ArithmeticError("shortcut guard failed")
        return (U2.SIGN[c][0],N,(c,1) if len(U2.SIGN[c])>1 else U2.READY)
    c,i=q
    if c in("S1","S3"): return U2.sigma(x,q)
    tab=TABLES['sqw'].get((c,i+1))
    if tab is None: return U2.sigma(x,q)
    N=shortcut(tab,x)
    if N is None: raise ArithmeticError("shortcut guard failed")
    nxt=(c,i+1) if i+1<len(U2.SIGN[c]) else U2.READY
    return (U2.SIGN[c][i],N,nxt)
def sigma_wrap_ki(x,q):
    if q==Q.SQ_READY or q==Q.SQ_FINISH: return Q.sigma_wrap(x,q)
    _,oq=q; s,N,nq=u2_sigma_ki(x,oq)
    return (s,N,Q.SQ_FINISH if nq==U2.READY else ("SUB",nq))
def _run_sq(sig,ready,x):
    H.C2.reset(); KC.reset(); n=isqrt(x)
    if n*n!=x or n<1: return None,[],REJECT,dict(iters=0,evals=0,**KC.snap()),[]
    S=x;q=ready;mv=[];way=[x]
    while True:
        sg,N,q=sig(S,q); S=H.apply(S,sg,N); mv.append((sg,N)); way.append(S)
        if q==ready: break
    return S,mv,"route",dict(iters=H.C2.iters,evals=H.C2.evals,**KC.snap()),way
def sqd_baseline(x): return _run_sq(Q.sigma_direct,Q.READY,x)
def sqd_ki(x): return _run_sq(sigma_direct_ki,Q.READY,x)
def sqw_baseline(x): return _run_sq(Q.sigma_wrap,Q.SQ_READY,x)
def sqw_ki(x): return _run_sq(sigma_wrap_ki,Q.SQ_READY,x)
