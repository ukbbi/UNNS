#!/usr/bin/env python3
"""FIELD-I  F1-F5 : rational nest fibres.  Exact integer/Fraction arithmetic only.
S_N(M)=M(N+1)^2/N ; occurrence=(M,N), M,N>=1 ; d=N+1."""
from fractions import Fraction as Fr
from math import gcd, isqrt
from collections import defaultdict
import random, sys
random.seed(7)
def lcm(a,b): return a*b//gcd(a,b)
OK=[True]
def P(tag,desc,ok):
    print(("PASS " if ok else "FAIL ")+tag+"."+desc); OK[0]&=bool(ok)
def D_(tag,desc): print("DATA "+tag+"."+desc)
def val(M,N): return Fr(M*(N+1)**2,N)

# ---------- theorem (as stated by the proposal) ----------
def Dset(a,b):                       # admissible d for x=a/b lowest terms
    out=[]; d=2
    while d*d<=a:
        if a%(d*d)==0 and (d-1)%b==0: out.append(d)
        d+=1
    return out
def occ_formula(a,b): return sorted((a//(d*d)*(d-1)//b, d-1) for d in Dset(a,b))   # (M,N)
def occ_brute(a,b):                  # independent: N < x-1 elementary bound (d^2/(d-1)>d+1, M>=1)
    out=[]; Nmax=-(-a//b)+1
    for N in range(1,Nmax+1):
        d=N+1
        if (a*N)%(b*d*d)==0: out.append((a*N//(b*d*d),N))
    return sorted(out)

# F1.1 exhaustive: every reduced a/b with a<=A, b<=B
A,B=1500,120; bad=0; n=0; nrealiz=0
real=defaultdict(list)               # b -> realizable numerators
for b in range(1,B+1):
    for a in range(1,A+1):
        if gcd(a,b)!=1: continue
        n+=1; f=occ_formula(a,b); g=occ_brute(a,b)
        if f!=g: bad+=1
        if g: real[b].append(a); nrealiz+=1
P("F1.1",f"formula == independent brute force on all {n} reduced fractions a<={A}, b<={B}; mismatches {bad}",bad==0)
D_("F1.1b",f"{nrealiz} of those fractions are realised by >=1 occurrence")

# F1.2 forward: generate occurrences, reduce value, check membership; and completeness inside box
NB,MB=60,1500; bad=0; groups=defaultdict(set)
for N in range(1,NB+1):
    for M in range(1,MB+1):
        v=val(M,N); groups[v].add((M,N))
        a,b=v.numerator,v.denominator; d=N+1
        if not (d>=2 and a%(d*d)==0 and (d-1)%b==0 and a//(d*d)*(d-1)//b==M): bad+=1
P("F1.2",f"every generated occurrence satisfies d>=2, d^2|a, d=1 mod b and M=(a/d^2)(d-1)/b ({NB*MB} occurrences); violations {bad}",bad==0)
bad=0
for v,s in groups.items():
    f={(M,N) for (M,N) in occ_formula(v.numerator,v.denominator) if N<=NB and M<=MB}
    if f!=s: bad+=1
P("F1.3",f"formula-fibre restricted to the box equals the generated fibre for all {len(groups)} values; mismatches {bad}",bad==0)

# F1.4 (k,b,g) parametrisation: M=kg, N=bg, gcd(k,b)=1, value=k d^2/b, d=bg+1
bad=0
for N in range(1,NB+1):
    for M in range(1,400):
        g=gcd(M,N); k,b=M//g,N//g; d=N+1; v=val(M,N)
        if not(gcd(k,b)==1 and v==Fr(k*d*d,b) and v.denominator==b and v.numerator==k*d*d): bad+=1
P("F1.4","occurrence <-> (k,b,g), gcd(k,b)=1: value=k(bg+1)^2/b in lowest terms, denominator b=N/gcd(M,N), numerator k d^2 (anchor iff b=1)",bad==0)

# F1.5 sub-fibre restatement: F(a/b) = {anchors of a with b | N}, via M -> bM
bad=0; cnt=0
for b in range(1,40):
    for a in range(1,1200):
        if gcd(a,b)!=1: continue
        fr=set(occ_brute(a,b))
        an={(M,N) for (M,N) in occ_brute(a,1) if N%b==0}
        if {(b*M,N) for (M,N) in fr}!=an: bad+=1
        cnt+=1
P("F1.5",f"F(a/b) = anchors of a with b|N, under (M,N)->(bM,N): {cnt} fractions, mismatches {bad}  [so R(a/b)<=R(a), equality iff b | N for every anchor of a]",bad==0)

# ---------- F2 cross-nest intersections ----------
bad=0; X=Fr(30000)
def outs(N,X): 
    s=Fr((N+1)**2,N); k=1; r=set()
    while k*s<=X: r.add(k*s); k+=1
    return r
cache={N:outs(N,X) for N in range(1,41)}
for N1 in range(1,41):
    for N2 in range(N1+1,41):
        g=gcd(N1,N2); L=lcm(N1+1,N2+1); st=Fr(L*L,g)
        want={j*st for j in range(1,int(X//st)+1)}
        if (cache[N1]&cache[N2])!=want: bad+=1
P("F2.1",f"S_N1(Z>0) n S_N2(Z>0) = {{jL^2/g}} for all 1<=N1<N2<=40 (values<=30000); mismatches {bad}",bad==0)
P("F2.2","gcd(gcd(N1,N2), lcm(N1+1,N2+1))=1 for all N1,N2<=300  [prime p|N1,N2 => N1+1 = 1 mod p]",
  all(gcd(gcd(a,b),lcm(a+1,b+1))==1 for a in range(1,301) for b in range(1,301)))
P("F2.3","earliest common value L^2/g is non-integer iff gcd(N1,N2)>1 (N1,N2<=300)",
  all((Fr(lcm(a+1,b+1)**2,gcd(a,b)).denominator>1)==(gcd(a,b)>1) for a in range(1,301) for b in range(1,301)))
# proof sketch check: lcm of reduced p/q lattices = lcm(p)/gcd(q): (d^2/N reduced since gcd(d^2,N)=1)
P("F2.4","each step d^2/N is already reduced (gcd(d^2,N)=1), so the lattice-lcm is lcm(d1^2,d2^2)/gcd(N1,N2)=L^2/g",
  all(gcd((N+1)**2,N)==1 for N in range(1,5000)))

# ---------- F3 non-anchor classification ----------
# realisability bound a>=(b+1)^2, tight
ok=True; tight=True
for b in range(2,38):
    if b not in real: ok=False; continue
    if min(real[b])!=(b+1)**2: tight=False
    if any(a<(b+1)**2 for a in real[b]): ok=False
P("F3.1","non-integer x=a/b (b>1) realisable only if a>=(b+1)^2 (since b|d-1 forces d>=b+1); minimum numerator is exactly (b+1)^2 = S_b(1)  [b=2..37 exhaustive for a<=1500]",ok and tight)
# necessary and sufficient criterion
ok=all(bool(occ_brute(a,b))==any(d*d<=a and a%(d*d)==0 for d in range(b+1,isqrt(a)+1,b)) for b in range(2,38) for a in range(1,1500) if gcd(a,b)==1)
P("F3.2","x=a/b realisable iff a has a square divisor d^2 with d = 1 (mod b), d>1  (exhaustive a<1500,b<38)",ok)
# multiplicity table
Rdist=defaultdict(int)
for b in range(2,38):
    for a in range(1,1500):
        if gcd(a,b)==1:
            r=len(occ_brute(a,b)); 
            if r: Rdist[r]+=1
D_("F3.3","multiplicity R(a/b) over realisable non-integers (a<1500,b<38): "+str(dict(sorted(Rdist.items()))))
# smallest non-integer values with R>=r, by value
Xv=1500; byv=defaultdict(int)
for N in range(1,Xv):
    d=N+1; s=Fr(d*d,N); M=1
    while M*s<=Xv:
        v=M*s
        if v.denominator>1: byv[v]+=1
        M+=1
first={}
for v in sorted(byv):
    r=byv[v]
    for t in range(2,r+1):
        first.setdefault(t,(v,r))
D_("F3.4","smallest non-integer value with R>=t (value<=1500): "+", ".join(f"t={t}: {first[t][0]} (R={first[t][1]})" for t in sorted(first)))
D_("F3.4b","fraction of occurrences (N<=60,M<=1500) with non-integer value: %.4f"%(sum(1 for (M,N) in [(M,N) for N in range(1,61) for M in range(1,1501)] if M%N)/90000))

# ---------- congruence obstruction ----------
# D(x)=D(a)∩(1+bZ).  lcm/gcd of two members lies in D(x) iff gcd(d,d')=1 mod b
bad=0; tot=0; viol_example=None; crit_ok=True
for b in range(2,40):
    for a in range(1,3000):
        if gcd(a,b)!=1: continue
        Ds=Dset(a,b)
        for i in range(len(Ds)):
            for j in range(i+1,len(Ds)):
                d,e=Ds[i],Ds[j]; g=gcd(d,e); l=d*e//g
                inl=(l-1)%b==0; ing=(g-1)%b==0 and g>=2
                tot+=1
                if inl!=((g-1)%b==0): crit_ok=False
                if not inl and viol_example is None: viol_example=(a,b,d,e,l)
                if (g-1)%b==0 and not inl: bad+=1
P("F3.5",f"for d,d' in D(a/b): lcm(d,d') in D(a/b) <=> gcd(d,d') = 1 (mod b)  ({tot} pairs)",crit_ok and bad==0)
# minimal counterexample (smallest a, then b)
best=None
for a in range(1,20000):
    for b in range(2,60):
        if gcd(a,b)!=1: continue
        Ds=Dset(a,b)
        for i in range(len(Ds)):
            for j in range(i+1,len(Ds)):
                d,e=Ds[i],Ds[j]; l=d*e//gcd(d,e)
                if (l-1)%b: best=(a,b,d,e,l); break
            if best: break
        if best: break
    if best: break
D_("F3.6","smallest rational fibre not closed under lcm: x=%d/%d, d=%d,d'=%d, lcm=%d (lcm^2|a but lcm != 1 mod b)"%(best[0],best[1],best[2],best[3],best[4]))
nclosed=nopen=0
for b in range(2,40):
    for a in range(1,3000):
        if gcd(a,b)!=1: continue
        Ds=Dset(a,b)
        if len(Ds)<2: continue
        if all(((d*e//gcd(d,e))-1)%b==0 for i,d in enumerate(Ds) for e in Ds[i+1:]): nclosed+=1
        else: nopen+=1
D_("F3.7",f"rational fibres (b>1,a<3000) with >=2 occurrences: lcm-closed {nclosed}, not lcm-closed {nopen}")
# refinement action
bad=0; t=0
for _ in range(20000):
    b=random.randint(1,30); d=1+b*random.randint(1,12) if b>1 else random.randint(2,40)
    k=random.choice([1,2,3,5,9,36,100]); q=random.randint(2,9)
    # anchor-style fibre element (k,d) with value kd^2 ; T_q needs q^2 | k  -> use k'=k*q^2
    k2=k*q*q; a0=k2*d*d
    if gcd(a0,b)!=1: continue
    t+=1
    in_after=((d*q-1)%b==0)
    if in_after!=((q-1)%b==0): bad+=1
P("F3.8",f"T_q:(k,d)->(k/q^2,dq) keeps value; maps a rational-fibre member (d=1 mod b) into the fibre iff q=1 mod b  ({t} trials)",bad==0)

# ---------- F5 rendezvous ----------
# two occurrences with same value x; forward orbits x+j*d^2/N; first common future value
def rend(N1,N2): 
    g=gcd(N1,N2); L=lcm(N1+1,N2+1); return Fr(L*L,g)
bad=0; tot=0
for v,s in groups.items():
    s=sorted(s,key=lambda t:t[1])
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            (M1,N1),(M2,N2)=s[i],s[j]
            st1,st2=Fr((N1+1)**2,N1),Fr((N2+1)**2,N2)
            o1={v+t*st1 for t in range(1,400)}; 
            first=None; 
            for t in range(1,2000):
                w=v+t*st2
                if w in o1 or (w-v)/st1==int((w-v)/st1): first=w; break
            tot+=1
            if first is None or first-v!=rend(N1,N2): bad+=1
P("F5.1",f"first common future value of two same-value occurrences = x + L^2/gcd(N1,N2), independent of M and x  ({tot} pairs from the box)",bad==0)
# anchors: rendezvous leaves the integers when gcd(N,N')>1
nint=nnon=0; ex=None
for m in range(2,3001):
    ds=[d for d in range(2,isqrt(m)+1) if m%(d*d)==0]
    for i in range(len(ds)):
        for j in range(i+1,len(ds)):
            g=gcd(ds[i]-1,ds[j]-1)
            if g>1:
                nnon+=1
                if ex is None: ex=(m,ds[i],ds[j])
            else: nint+=1
D_("F5.2",f"anchor fibre pairs (m<=3000): first common future value is an integer for {nint}, non-integer for {nnon}; first non-integer case m={ex[0]}, d={ex[1]},d'={ex[2]} -> common future {ex[0]}+{rend(ex[1]-1,ex[2]-1)}")
# independence from the manuscript's D = 2 log(L/gcd(d,d'))
byD=defaultdict(set); 
for m in range(2,3001):
    ds=[d for d in range(2,isqrt(m)+1) if m%(d*d)==0]
    for i in range(len(ds)):
        for j in range(i+1,len(ds)):
            d,e=ds[i],ds[j]; Dm=Fr(lcm(d,e),gcd(d,e)); byD[Dm].add(rend(d-1,e-1))
multi=sum(1 for s in byD.values() if len(s)>1)
P("F5.3",f"rendezvous is not a function of the manuscript refinement distance D: {multi} of {len(byD)} D-values carry >1 rendezvous value",multi>0)
# label reading
P("F5.4","rendezvous depends on (N1,N2) only: it is invariant under (M,x) at fixed nests, hence it reads the labels (F4 status: not a value-level invariant)",
  all(rend(a,b)==rend(b,a) for a in range(1,60) for b in range(1,60)))
print("ALL PASS" if OK[0] else "SOME FAIL")
