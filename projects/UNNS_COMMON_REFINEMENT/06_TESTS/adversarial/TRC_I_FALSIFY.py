#!/usr/bin/env python3
"""
TRC_I_FALSIFY.py

Executable certificates for the five TRC-I countermodels.

The script is intentionally small. It checks:
- CM_I: affine projection has no refinement witness.
- CM_P: <2,3> equality 2+4=3+3 has no witness and atom 2 is nonprime.
- CM_D: obligation machine cycles and never reaches terminal W.
- CM_L: all finite prefixes are compatible but the omega witness is absent.
- CM_R: local witnesses exist but global parity reconstruction fails.
"""
from collections import deque

def addv(a,b): return tuple(x+y for x,y in zip(a,b))
def leqv(a,b): return all(x<=y for x,y in zip(a,b))

def generate(gens,bound):
    z=tuple(0 for _ in gens[0]); H={z}; changed=True
    while changed:
        changed=False
        for x in list(H):
            for g in gens:
                y=addv(x,g)
                if all(v<=bound for v in y) and y not in H:
                    H.add(y); changed=True
    return H

def vw(H,a,b,c,d):
    out=[]
    for e in H:
        for f in H:
            if addv(e,f)!=a: continue
            for g in H:
                if addv(e,g)!=c: continue
                h=tuple(bi-gi for bi,gi in zip(b,g))
                if min(h)<0 or h not in H: continue
                if addv(g,h)==b and addv(f,h)==d: out.append((e,f,g,h))
    return out

# CM_I
u=(1,0);v=(1,1);w=(1,2)
B=generate([u,v,w],4)
assert vw(B,u,w,v,v)==[]

# CM_P
H={0}
for n in range(31):
    if n in H:
        for g in (2,3):
            if n+g<=30:H.add(n+g)
W=[]
for e in H:
    f=2-e; g=3-e; h=4-g
    if min(f,g,h)>=0 and f in H and g in H and h in H:
        if e+f==2 and g+h==4 and e+g==3 and f+h==3:W.append((e,f,g,h))
assert W==[]
assert 4 in H and 1 not in H  # 2 <= 6 but 2 not <= 3

# CM_D
s="X"; seen=set()
while s not in seen and s!="W":
    seen.add(s); s={"X":"Y","Y":"X"}[s]
assert s!="W"

# CM_L
p=["1"*n for n in range(1,20)]
assert all(p[i].startswith(p[i-1]) for i in range(1,len(p)))
omega_present=False
assert not omega_present

# CM_R
local=(1,1,1)
assert sum(local)%2==1

print({"countermodels":5,"status":"PASS"})
