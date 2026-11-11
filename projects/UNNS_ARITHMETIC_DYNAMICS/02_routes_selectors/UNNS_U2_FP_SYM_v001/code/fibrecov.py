"""Selector simulation under Definition 2.1 (R1-R5).
Input: only the current integer + finite control (class r, step i). No access to k, h, a, b.
 dispatch : eps from which of 5x^2 +-4 is a square; y=(x+L)/2; k mod 24 from (x,y) mod 24 -> class r = k mod 12.
 recover  : b from state s_i by inverting G_i(t)=p0(t)+p1(t)*A(t), A(t)=floor((isqrt(5t^2+4 eps)-t)/2), strictly increasing for t>=40.
 labels   : N_i = q0(b)+q1(b)*a with a=A(b); moves applied exactly."""
import json, sys
from fractions import Fraction
from math import isqrt
import sympy as sp
from fibparam import F
bsym=sp.symbols('b')
def coeffs(expr):
    P=sp.Poly(sp.sympify(expr),bsym)
    return [Fraction(int(c.p),int(c.q)) for c in P.all_coeffs()]
def pe(cs,t):
    v=Fraction(0)
    for c in cs: v=v*t+c
    return v
class ClassSel:
    def __init__(s,cert):
        s.eps=cert['eps']; s.steps=[tuple(t) for t in cert['searchnames']]
        s.S=[(coeffs(a),coeffs(b_)) for a,b_ in cert['states_ring']]
        s.N=[(coeffs(a),coeffs(b_)) for a,b_ in cert['labels_ring']]
    def A(s,t): return (isqrt(5*t*t+4*s.eps)-t)//2
    def G(s,i,t): p0,p1=s.S[i]; return pe(p0,t)+pe(p1,t)*s.A(t)
    def recover(s,i,state):
        lo,hi=40,max(41,state)       # G_i(t)>=t for t>=1 so b<=state
        while lo<hi:
            mid=(lo+hi)//2
            if s.G(i,mid)>=state: hi=mid
            else: lo=mid+1
        return lo if s.G(i,lo)==state else None
    def label(s,i,t):
        q0,q1=s.N[i]; v=pe(q0,t)+pe(q1,t)*s.A(t); assert v.denominator==1; return int(v)
def dispatch(x):
    """return (k mod 12, ok) from x alone."""
    for sg in (1,-1):                   # 5x^2+4 square <=> k even
        t=5*x*x+4*sg; L=isqrt(t)
        if L*L==t and (x+L)%2==0:
            y=(x+L)//2; return (x%24,y%24)
    return None
KTAB={}
for k in range(0,24): KTAB[(F[k]%24,F[k+1]%24)]=k
def run_selector(sel_by_class,x):
    key=dispatch(x)
    if key is None or key not in KTAB: return None
    r=KTAB[key]%12
    sel=sel_by_class[r]; S=x; moves=[]
    for i,(sign,lab) in enumerate(sel.steps):
        bval=sel.recover(i,S)
        if bval is None: return ("recover-fail",r,i)
        N=sel.label(i,bval)
        if sign=='+':
            if S%N: return ("illegal",r,i)
            S=S//N*(N+1)**2
        else:
            if S%((N+1)**2): return ("illegal",r,i)
            S=S*N//(N+1)**2
        moves.append((sign,N))
    return S,moves
if __name__=="__main__":
    certs=json.load(open('../reports/class_certificates.json'))
    sels={int(r):ClassSel(c) for r,c in certs.items()}
    kmax=int(sys.argv[1]) if len(sys.argv)>1 else 600
    res={r:dict(tested=0,ok=0) for r in sels}
    bad=[]
    for k in range(30,kmax):
        r=k%12
        if r not in sels: continue
        out=run_selector(sels,F[k])
        res[r]['tested']+=1
        if out is not None and out[0]==F[k+1]: res[r]['ok']+=1
        else: bad.append((k,out if out is None or isinstance(out[0],str) else "wrong-target"))
    print(res); print("failures:",bad[:10],len(bad))
    # monotonicity of G_i on integers 40..3000 (strict)
    mono=True
    for r,sel in sels.items():
        for i in range(len(sel.S)):
            prev=sel.G(i,40)
            for t in range(41,3000):
                cur=sel.G(i,t)
                if cur<=prev: mono=False;print("non-monotone",r,i,t);break
                prev=cur
    print("G_i strictly increasing on 40..2999 for all classes/states:",mono)
