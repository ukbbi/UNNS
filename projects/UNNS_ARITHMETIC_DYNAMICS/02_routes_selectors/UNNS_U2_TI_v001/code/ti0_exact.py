"""TI-0: exact-arithmetic gate.  (1) static float audit of the executed selector code and of every U2-001 label expression;
(2) a new float-trapped exact implementation of the U2-001 successor selector and of the squares wrapper (baseline logic and KI shortcuts);
(3) identical-transition comparison on the KI test domain and on an extended domain up to 10^60."""
import sys,os,ast,inspect,random
HERE=os.path.dirname(os.path.abspath(__file__)); FROZ=HERE+"/../frozen_KI"
sys.path.insert(0,FROZ+"/code"); sys.path.insert(0,FROZ+"/baseline_R3_frozen/code"); sys.path.insert(0,FROZ+"/baseline_R3_frozen/code/sq")
import sympy as sp
from fractions import Fraction
from math import isqrt
import u1_bnd_lib as L, u2_selector as U2, u2sq_selector as Q
import ki_selectors as KS
T=L.T
# ---------------------------------------------------------------- (1) static audit
def ast_float_scan(path):
    tree=ast.parse(open(path).read()); hits=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Div): hits.append(("true-division",node.lineno))
        if isinstance(node,ast.Constant) and isinstance(node.value,float): hits.append(("float-literal",node.lineno))
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=="float": hits.append(("float()",node.lineno))
        if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name) and node.value.id=="math" and node.attr in("sqrt","pow","log","exp","floor","ceil"): hits.append(("math."+node.attr,node.lineno))
    return hits
def label_audit():
    out=[]
    for ident in L.IDENTITIES:
        for i,(sg,e) in enumerate(ident['steps']):
            if e.free_symbols:
                P=sp.Poly(e,T); integer_coeffs=all(c.q==1 for c in P.all_coeffs()); src=sp.printing.lambdarepr.lambdarepr(e)
            else: integer_coeffs=(sp.Integer(e).q==1); src=str(e)
            out.append(dict(identity=ident['name'],step=i,integer_coeffs=integer_coeffs,has_division=("/" in src),has_dot=("." in src)))
    return out
# ---------------------------------------------------------------- (2) exact implementation
class FloatTrap(Exception): pass
def _chk(v):
    if isinstance(v,float): raise FloatTrap(v)
    return v
EXLAB={}
for ident in L.IDENTITIES:
    nm=ident['name']; EXLAB[nm]=[]
    for sg,e in ident['steps']:
        cs=[int(c) for c in sp.Poly(e,T).all_coeffs()] if e.free_symbols else [int(e)]
        EXLAB[nm].append(cs)
def exact_label(nm,i,t):
    r=0
    for c in EXLAB[nm][i]: r=r*t+c
    return _chk(r)
def u2x_sigma(x,q):
    """U2-001 successor selector with exact labels (same control logic as the frozen selector; only the label evaluation differs)."""
    if q==U2.READY:
        if x==1: return ("+",1,("S1",1))
        if x==3: return ("+",3,("S3",1))
        c=U2.class_of(x); t=U2.decode_t(c,0,x,U2.T0[c])
        return (U2.SIGN[c][0],exact_label(c,0,t),(c,1) if len(U2.SIGN[c])>1 else U2.READY)
    c,i=q
    if c in("S1","S3"): return U2.sigma(x,q)           # explicit integer table; no label evaluation
    t=U2.decode_t(c,i,x,U2.T0[c]); nxt=(c,i+1) if i+1<len(U2.SIGN[c]) else U2.READY
    return (U2.SIGN[c][i],exact_label(c,i,t),nxt)
def u2x_sigma_ki(x,q):
    """as u2x_sigma, but with the certified KI-1 shortcuts at steps where one exists"""
    if q==U2.READY:
        if x==1 or x==3: return u2x_sigma(x,q)
        c=U2.class_of(x); tab=KS.TABLES['sqw'].get((c,1))
        if tab is None: return u2x_sigma(x,q)
        N=KS.shortcut(tab,x)
        if N is None: raise ArithmeticError("guard")
        return (U2.SIGN[c][0],N,(c,1) if len(U2.SIGN[c])>1 else U2.READY)
    c,i=q
    if c in("S1","S3"): return U2.sigma(x,q)
    tab=KS.TABLES['sqw'].get((c,i+1))
    if tab is None: return u2x_sigma(x,q)
    N=KS.shortcut(tab,x)
    if N is None: raise ArithmeticError("guard")
    return (U2.SIGN[c][i],N,(c,i+1) if i+1<len(U2.SIGN[c]) else U2.READY)
def _wrap(sig):
    def f(x,q):
        if q==Q.SQ_READY or q==Q.SQ_FINISH: return Q.sigma_wrap(x,q)
        _,oq=q; s,N,nq=sig(x,oq); return (s,N,Q.SQ_FINISH if nq==U2.READY else ("SUB",nq))
    return f
sigma_wrap_exact=_wrap(u2x_sigma); sigma_wrap_ki_exact=_wrap(u2x_sigma_ki)
def run(sig,x):
    n=isqrt(x); S=x; q=Q.SQ_READY; mv=[]
    while True:
        sg,N,q=sig(S,q)
        if sg=='+':
            if S%N: raise ArithmeticError("illegal +")
            S=S//N*(N+1)**2
        else:
            if S%((N+1)**2): raise ArithmeticError("illegal -")
            S=S*N//(N+1)**2
        mv.append((sg,N))
        if q==Q.SQ_READY: break
    return S,mv
