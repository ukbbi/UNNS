"""Predeclared recognizers (applied after generation; no feedback to the selector)."""
from fractions import Fraction
from math import isqrt
import sys,os
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE+"/../frozen_KI/baseline_R3_frozen/code")
import u1_bnd_lib as L
def bm(seq):
    """Berlekamp-Massey over Q: minimal linear recurrence (coefficients c_1..c_r with a_n = sum c_i a_{n-i})"""
    s=[Fraction(v) for v in seq]; C=[Fraction(1)]; B=[Fraction(1)]; Lc=0; m=1; b=Fraction(1)
    for n in range(len(s)):
        d=s[n]+sum(C[i]*s[n-i] for i in range(1,Lc+1))
        if d==0: m+=1; continue
        T=C[:]; coef=d/b
        C=C+[Fraction(0)]*(len(B)+m-len(C))
        for i in range(len(B)): C[i+m]-=coef*B[i]
        if 2*Lc<=n: Lc=n+1-Lc; B=T; b=d; m=1
        else: m+=1
    C=C[:Lc+1]+[Fraction(0)]*max(0,Lc+1-len(C))
    return Lc,[-c for c in C[1:Lc+1]]
def linrec(seq,rmax=4,minlen=22):
    """(order, coefficients) if a recurrence of order r<=rmax with n>=4r+6 explains the whole sequence, else None"""
    if len(seq)<minlen: return None
    r,c=bm(seq)
    if r==0 or r>rmax or len(seq)<4*r+6: return None
    for n in range(r,len(seq)):
        if sum(c[i]*seq[n-1-i] for i in range(r))!=seq[n]: return None
    return r,[str(x) for x in c]
def _is_sq(v): return isqrt(v)**2==v
def _icbrt(v):
    r=round(v**(1/3)) if v<10**15 else int(round(float(v)**(1/3)))
    for c in (r-1,r,r+1):
        if c>=0 and c**3==v: return c
    return None
def idx_squares(v): r=isqrt(v); return r if r*r==v else None
def idx_cubes(v): return _icbrt(v)
def idx_tri(v):
    d=8*v+1; r=isqrt(d); return (r-1)//2 if r*r==d else None
def idx_pow(b):
    def f(v):
        k=0
        while v%b==0: v//=b; k+=1
        return k if v==1 else None
    return f
_FIB=[0,1]
while _FIB[-1]<10**40: _FIB.append(_FIB[-1]+_FIB[-2])
_FIBI={f:i for i,f in enumerate(_FIB) if i>=2}
def idx_fib(v): return _FIBI.get(v)
_FAC=[1]
for k in range(1,30): _FAC.append(_FAC[-1]*k)
_FACI={f:i for i,f in enumerate(_FAC) if i>=1}
def idx_fact(v): return _FACI.get(v)
def idx_nat(v): return v
FAMILIES={"naturals":idx_nat,"squares":idx_squares,"cubes":idx_cubes,"triangular":idx_tri,"powers_of_2":idx_pow(2),"powers_of_3":idx_pow(3),"fibonacci":idx_fib,"factorials":idx_fact}
def is_prime(v): return v>1 and L._is_prime(v)
def next_prime(v):
    v+=1
    while not is_prime(v): v+=1
    return v
def family_hits(seq):
    """for each family: subset (>=8 distinct terms, all in family) and consecutive (8 successive terms are consecutive family members, increasing)"""
    out={}
    dist=sorted(set(seq))
    for nm,f in FAMILIES.items():
        ix=[f(v) for v in seq]
        sub=(len(dist)>=8 and all(f(v) is not None for v in dist))
        cons=False
        for i in range(len(seq)-7):
            w=ix[i:i+8]
            if None not in w and all(w[j+1]==w[j]+1 for j in range(7)): cons=True;break
        if sub or cons: out[nm]=dict(subset=sub,consecutive=cons)
    # primes
    if len(dist)>=8 and all(is_prime(v) for v in dist): out.setdefault("primes",{})["subset"]=True
    for i in range(len(seq)-7):
        if is_prime(seq[i]) and all(next_prime(seq[i+j])==seq[i+j+1] for j in range(7)): out.setdefault("primes",{})["consecutive"]=True;break
    return out
def records(seq):
    r=[seq[0]]
    for v in seq[1:]:
        if v>r[-1]: r.append(v)
    return r
def analyse(res):
    """classification of one orbit: sequences V (vertex sequence) and R (records)"""
    seq=res["seq"]; out=dict(status=res["status"],length=len(seq),max=max(seq),distinct=len(set(seq)))
    if res["status"]=="cyclic": out["pre"]=res["pre"]; out["period"]=res["period"]
    V=seq; R=records(seq); out["records"]=len(R)
    for nm,S in (("V",V),("R",R)):
        S2=S if nm=="R" else (S[:res["pre"]] if res["status"]=="cyclic" else S)   # for V: the pre-periodic part only; the cycle itself is classified as cyclic
        S2=S2[:60]                                   # analysis window: first 60 terms (amendment A1, before the first complete run)
        lr=linrec(S2,minlen=22 if nm=="V" else 10)
        out["linrec_"+nm]=lr
        out["fam_"+nm]=family_hits(S2) if len(S2)>=8 else {}
    return out
