#!/usr/bin/env python3
"""Small exact checks for examples in the Intrinsic--Selected synthesis.
No external packages required. Does not replace the source manuscripts' proofs.
"""
import math


def divisor_list(n):
    result=[]
    for d in range(1,math.isqrt(n)+1):
        if n%d==0:
            result.append(d)
            if d*d!=n: result.append(n//d)
    return sorted(result)


def neighbours(x):
    up={x//N*(N+1)**2 for N in divisor_list(x)}
    down={x//q**2*(q-1) for q in range(2,math.isqrt(x)+1) if x%(q*q)==0}
    return up|down


def edge(a,b):
    small,large=sorted((a,b))
    return any(small//N*(N+1)**2 == large for N in divisor_list(small))

route=[1,4,16,100,9,2]
assert all(edge(a,b) for a,b in zip(route,route[1:]))
for m in range(1,201):
    assert all(edge(m*a,m*b) for a,b in zip(route,route[1:]))
assert neighbours(1)=={4}
assert neighbours(4)=={1,16,18,25}
assert neighbours(2)=={8,9}
assert neighbours(8)=={2,32,36,50,81}
assert neighbours(9)=={2,36,48,100}
B21={1}|neighbours(1)|neighbours(4)
B22={2}|neighbours(2)|neighbours(8)|neighbours(9)
assert B21.isdisjoint(B22)
assert B21=={1,4,16,18,25}
assert B22=={2,8,9,32,36,48,50,81,100}

x=8
D=[N for N in divisor_list(x) if N>=2]
vertices={x,4*x}
edges={tuple(sorted((x,4*x)))}
for N in D:
    y=x//N*(N+1)**2
    vertices |= {y,4*y}
    for a,b in ((x,y),(y,4*y),(4*y,4*x)):
        assert edge(a,b)
        edges.add(tuple(sorted((a,b))))
assert len(D)==3 and len(vertices)==8 and len(edges)==10
assert len(edges)-len(vertices)+1==3
assert sorted(vertices)==[8,32,36,50,81,144,200,324]

assert len(divisor_list(64))==7
lam=2;m=6
assert lam**3-lam**2+lam==m
assert (2**3-2**2+2)==6
print('PASS: exact five-edge doubling route; scaling n=1..200; disjoint balls; F(8) structure; F(64) cubic.')
