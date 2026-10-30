"""Exact reproduction of the worked example of Section 18 (integers and Fractions only).
Worked-example check, not a proof of any universal statement."""
from fractions import Fraction as Fr
from itertools import product
def occurrences(a,b):
    out=[]; k=2
    while k*k<=a:
        if a%(k*k)==0 and (k-1)%b==0: out.append((k,k-1,(a//k**2)*((k-1)//b)))
        k+=1
    return out
def expo(k):
    i=j=0
    while k%5==0: k//=5; i+=1
    while k%3==0: k//=3; j+=1
    assert k==1; return (i,j)
X={'x0':(5**10*3**10,11),'x1':(5**12*3**10,11)}
for nm,(a,b) in X.items():
    occ=occurrences(a,b)
    for k,N,M in occ: assert Fr(M*(N+1)**2,N)==Fr(a,b)
    print(nm,len(occ),sorted((expo(k),k,N,M) for k,N,M in occ))
d,s=5,2
Gam=lambda i,j:(j-s*i)%d==0
F0={(i,j) for i,j in product(range(6),range(6)) if Gam(i,j) and (i,j)!=(0,0)}
F1={(i,j) for i,j in product(range(7),range(6)) if Gam(i,j) and (i,j)!=(0,0)}
assert F0=={expo(k) for k,_,_ in occurrences(*X['x0'])}
assert F1=={expo(k) for k,_,_ in occurrences(*X['x1'])}
def area(P): return Fr(abs(sum(P[i][0]*P[(i+1)%len(P)][1]-P[(i+1)%len(P)][0]*P[i][1] for i in range(len(P)))),2)
assert area([(0,5),(1,2),(3,1),(5,0),(5,5)])==Fr(35,2)
assert area([(0,5),(1,2),(3,1),(5,0),(6,2),(5,5)])==20
cells=[((0,5),(1,2),(3,1),(2,4)),((1,2),(2,4),(4,3),(3,1)),((1,2),(2,4),(5,5),(4,3)),((2,4),(3,1),(5,0),(4,3))]
for c in cells:
    assert area(c)==5 and all(p in F0 for p in c)
def inside(P,pt):  # closed convex polygon, any orientation
    sg=[ (P[(i+1)%len(P)][0]-P[i][0])*(pt[1]-P[i][1])-(P[(i+1)%len(P)][1]-P[i][1])*(pt[0]-P[i][0]) for i in range(len(P))]
    return all(v>=0 for v in sg) or all(v<=0 for v in sg)
T1=[(0,5),(2,4),(5,5)]; T2=[(5,0),(4,3),(5,5)]
cen=lambda T:(Fr(sum(p[0] for p in T),3),Fr(sum(p[1] for p in T),3))
for T in (T1,T2):
    assert area(T)==Fr(5,2)
    c=cen(T); assert not any(inside(P,c) for P in cells); print('centroid',c,'in no cell')
fill=[((5,0),(4,3),(5,5),(6,2)),((1,2),(6,2),(5,5),(0,5)),((4,3),(5,0),(6,2),(5,5))]
assert all(p in F1 for P in fill for p in P)
# covering of H1 by the old cells, the three further cells and the L-cell, tested on a fine rational grid
H1=[(0,5),(1,2),(3,1),(5,0),(6,2),(5,5)]
Lc=((6,2),(5,5),(0,5),(1,2))
allc=cells+list(fill)+[Lc]
bad=0; n=0
for X_ in range(0,6*60+1):
    for Y_ in range(0,5*60+1):
        pt=(Fr(X_,60),Fr(Y_,60))
        if inside(H1,pt):
            n+=1
            if not any(inside(P,pt) for P in allc): bad+=1
print('grid points in H1',n,'uncovered',bad)
# D9 identity
assert Fr(1,9)*5+Fr(5,9)*8==5 and Fr(1,3)*5+Fr(5,9)*6==5 and Fr(1,9)+Fr(1,3)+Fr(5,9)==1
print('PASS')
