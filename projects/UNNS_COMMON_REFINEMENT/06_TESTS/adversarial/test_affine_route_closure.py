#!/usr/bin/env python3
from fractions import Fraction
from collections import deque

def addv(a,b): return tuple(x+y for x,y in zip(a,b))
def leq(a,b): return all(x<=y for x,y in zip(a,b))

def rank_q(vs):
    A=[[Fraction(x) for x in v] for v in vs]
    if not A:return 0
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]; z=A[r][c]
        A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]
                A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
    return r

def can_generate(t,gs):
    z=tuple(0 for _ in t); q=deque([z]); seen={z}
    while q:
        x=q.popleft()
        for g in gs:
            y=addv(x,g)
            if y==t:return True
            if leq(y,t) and y not in seen:
                seen.add(y); q.append(y)
    return False

def atoms(gs):
    gs=sorted(set(gs))
    return [g for i,g in enumerate(gs) if not can_generate(g,gs[:i]+gs[i+1:])]

cases=[
    ([(1,0),(0,1)],0),
    ([(2,0),(1,1)],0),
    ([(2,0),(1,1),(0,2)],1),
    ([(1,0),(1,1),(1,2)],1),
    ([(2,0),(1,1),(0,1)],1),
    ([(0,0,1),(1,0,1),(0,1,1),(1,1,1)],1),
    ([(1,0,0),(0,1,0),(0,0,1)],0),
]
for gs,expected in cases:
    A=atoms(gs)
    ard=len(A)-rank_q(A)
    assert ard==expected,(gs,A,ard,expected)

print({"cases":len(cases),"status":"PASS"})
