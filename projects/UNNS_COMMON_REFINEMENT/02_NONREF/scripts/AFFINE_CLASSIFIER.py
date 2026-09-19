#!/usr/bin/env python3
"""
AFFINE_CLASSIFIER.py
Exact route-closure classifier for positive affine monoids presented
by a finite generating set in N0^d.

Criterion:
    ARD = (# atoms) - rank(gp(H))
    ARD == 0  <=>  global Riesz refinement.
"""
import argparse, json
from fractions import Fraction
from collections import deque

def addv(a,b): return tuple(x+y for x,y in zip(a,b))
def leq(a,b): return all(x<=y for x,y in zip(a,b))

def rank_q(vectors):
    if not vectors: return 0
    A=[[Fraction(x) for x in row] for row in vectors]
    m,n=len(A),len(A[0]); r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None: continue
        A[r],A[p]=A[p],A[r]
        z=A[r][c]
        A[r]=[x/z for x in A[r]]
        for i in range(m):
            if i!=r and A[i][c]:
                z=A[i][c]
                A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
        r+=1
        if r==m: break
    return r

def can_generate(target, gens):
    target=tuple(target)
    zero=tuple(0 for _ in target)
    if target==zero: return True
    q=deque([zero]); seen={zero}
    while q:
        x=q.popleft()
        for g in gens:
            y=addv(x,g)
            if y==target: return True
            if leq(y,target) and y not in seen:
                seen.add(y); q.append(y)
    return False

def atoms(gens):
    gs=sorted(set(tuple(g) for g in gens if any(g)))
    out=[]
    for i,g in enumerate(gs):
        if not can_generate(g,gs[:i]+gs[i+1:]):
            out.append(g)
    return out

def classify(gens):
    A=atoms(gens)
    r=rank_q(A)
    ard=len(A)-r
    return {
        "atoms":[list(x) for x in A],
        "rank_gp":r,
        "atom_count":len(A),
        "ARD":ard,
        "global_common_refinement":ard==0,
        "criterion":"ARD=0 iff positive affine monoid is free iff Riesz refinement holds"
    }

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument(
        "generators_json",
        help='JSON array, e.g. "[[2,0],[1,1],[0,2]]"'
    )
    ns=ap.parse_args()
    gens=json.loads(ns.generators_json)
    if not gens or any(any(int(x)<0 for x in g) for g in gens):
        raise SystemExit("This CLI version requires a nonempty generator set in N0^d.")
    print(json.dumps(classify(gens),indent=2))
