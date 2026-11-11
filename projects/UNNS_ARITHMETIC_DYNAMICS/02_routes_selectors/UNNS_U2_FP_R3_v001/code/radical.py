"""Exact sign of P + Q*sqrt(D) for integers P,Q and D>=0, with operation accounting."""
from math import isqrt
class Acct:
    def __init__(s): s.reset()
    def reset(s): s.mults=0; s.isqrts=0; s.comps=0; s.iters=0; s.maxbits=0
    def snap(s): return dict(mults=s.mults,isqrts=s.isqrts,comps=s.comps,iters=s.iters,maxbits=s.maxbits)
ACC=Acct()
def sgn(v): return (v>0)-(v<0)
def sign_radical(P,Q,D):
    """sign(P+Q*sqrt(D)). Squares only after the sign conditions have been checked."""
    ACC.comps+=1
    if Q==0 or D==0: return sgn(P)
    if P==0: return sgn(Q)
    if sgn(P)==sgn(Q): return sgn(P)
    # opposite signs: compare P^2 with Q^2*D
    a=P*P; b=Q*Q*D; ACC.mults+=3
    ACC.maxbits=max(ACC.maxbits,a.bit_length(),b.bit_length())
    if a>b: return sgn(P)
    if a<b: return sgn(Q)
    return 0
def horner(cs,t):
    r=0
    for c in cs: r=r*t+c
    ACC.mults+=max(0,len(cs)-1); return r
