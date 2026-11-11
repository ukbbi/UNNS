"""Closed forms proved in the manuscript (RN-1)."""
from rn_core import factor
def spf(x): return min(factor(x)[0]) if x>1 else None
def sqpart(x):
    """x = a^2 b with b squarefree; returns (a,b)"""
    a=1
    for p,e in factor(x)[0].items(): a*=p**(e//2)
    return a,x//(a*a)
def minq(x):
    """smallest q>=2 with q^2|x = smallest prime p with p^2|x, or None"""
    ps=[p for p,e in factor(x)[0].items() if e>=2]
    return min(ps) if ps else None
def maxF(x): return (x+1)**2
def minF(x): return 4*x
def secmaxF(x):
    if x==1: return None
    p=spf(x); return (x+p)**2//p
def secminF(x):
    if x==1: return None
    p=spf(x); return x*(p+1)**2//p
def maxI(x):
    p=minq(x); return None if p is None else x*(p-1)//(p*p)
def minI(x):
    a,b=sqpart(x); return None if a==1 else b*(a-1)       # sigma(x)=b(a-1)
def minAll(x):
    y=minI(x); return 4*x if y is None else y
CLOSED={("F","top",1):maxF,("A","top",1):maxF,("F","bottom",1):minF,("F","top",2):secmaxF,("A","top",2):secmaxF,
        ("F","bottom",2):secminF,("I","top",1):maxI,("I","bottom",1):minI,("A","bottom",1):minAll}
def orbit(fn,x0,T,ESC):
    seq=[x0];x=x0
    while len(seq)<=T:
        y=fn(x)
        if y is None: return seq,"stuck"
        seq.append(y);x=y
        if x>ESC: return seq,"escape"
        if len(seq)>3 and y in seq[:-1]:      # exact-state map: any repeat is a cycle
            return seq,"cyclic"
    return seq,"horizon"
