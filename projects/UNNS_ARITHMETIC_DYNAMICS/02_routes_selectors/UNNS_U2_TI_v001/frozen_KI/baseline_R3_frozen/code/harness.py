"""Uniform runners with accounting for: Fibonacci v2, squares direct (85-state, polynomial recovery), squares wrapper (45-state)."""
import sys,os
from math import isqrt
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))+"/sq")
import fibsel2
from fibsel2 import ACC, REJECT
import u2sq_selector as Q, u2_selector as U2
class C2:  # counters for squares selectors
    iters=0; evals=0
    @classmethod
    def reset(c): c.iters=0; c.evals=0
def _decode_counted(r,i,x):
    c=Q.CLS[r]; lo=c["t0"]; hi=lo+1
    def ev(t): C2.evals+=1; return Q._hor(c["states"][i],t)
    while ev(hi)<x: hi*=2; C2.iters+=1
    while lo<hi:
        C2.iters+=1; mid=(lo+hi)//2
        if ev(mid)<x: lo=mid+1
        else: hi=mid
    return lo if ev(lo)==x else None
Q._decode=_decode_counted
def _u2_decode_counted(name,i,x,t0):
    lo,hi=t0,max(t0+1,1)
    def ev(t): C2.evals+=1; return U2.s_val(name,i,t)
    while ev(hi)<x: hi*=2; C2.iters+=1
    while lo<hi:
        C2.iters+=1; mid=(lo+hi)//2
        if ev(mid)<x: lo=mid+1
        else: hi=mid
    return lo if ev(lo)==x else None
U2.decode_t=_u2_decode_counted
def apply(S,sg,N):
    if sg=='+':
        assert S%N==0; return S//N*(N+1)**2
    assert S%((N+1)**2)==0; return S*N//(N+1)**2
def fib_run(x):
    ACC.reset(); S,mv,st=fibsel2.route(x); return S,mv,st,dict(ACC.snap())
def sq_direct_run(x):
    C2.reset(); n=isqrt(x)
    if n*n!=x or n<1: return None,[],REJECT,dict(iters=0,evals=0)
    S=x;q=Q.READY;mv=[]
    while True:
        sg,N,q=Q.sigma_direct(S,q); S=apply(S,sg,N); mv.append((sg,N))
        if q==Q.READY: break
    return S,mv,"route",dict(iters=C2.iters,evals=C2.evals)
def sq_wrap_run(x):
    C2.reset(); n=isqrt(x)
    if n*n!=x or n<1: return None,[],REJECT,dict(iters=0,evals=0)
    S=x;q=Q.SQ_READY;mv=[];first=True
    while True:
        sg,N,q=Q.sigma_wrap(S,q); S=apply(S,sg,N); mv.append((sg,N))
        if q==Q.SQ_READY: break
    return S,mv,"route",dict(iters=C2.iters,evals=C2.evals)
