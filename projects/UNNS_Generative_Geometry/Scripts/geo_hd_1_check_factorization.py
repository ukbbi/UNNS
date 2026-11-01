from sympy import factorint, divisors, gcd, ilcm
from fractions import Fraction
from itertools import product
from math import prod
def v(n,p):
    c=0
    while n%p==0:n//=p;c+=1
    return c
def s(m): return prod(p**(e//2) for p,e in factorint(m).items())
def D(m): return {d for d in divisors(s(m)) if d>=2}
# factorization identities, Cor A, Cor B, nonempty gain
n=0
for m in range(1,5001):
    for N in divisors(m):
        t=m*(N+1)**2//N; S,S2=s(m),s(t); g=gcd(S,S2)
        c=prod(p**((v(N,p)//2) if v(m,p)%2 else (v(N,p)+1)//2) for p in factorint(N))
        assert S==g*c and S2==g*(N+1) and S2*c==S*(N+1)
        assert (D(m)<=D(t))==(c==1)
        assert S2//g==N+1
        assert D(t)-D(m)
        n+=1
print("factorization, CorA, CorB, gain>0 verified on",n,"edges")
# 72 table
print([(N,72*(N+1)**2//N,gcd(6,s(72*(N+1)**2//N))) for N in divisors(72)])
# trivial lattice, enlarged boxes: coordinate-cell union vs hull witness, x=1296
from itertools import product
def covered(u,Q):  # u Fractions; is u in some unit cell (closed) whose corners are all nonzero lattice pts in box
    k=len(u); opts=[]
    for ui in u:
        if ui.denominator==1: opts.append([(int(ui),)*2])      # fixed coordinate (degenerate interval)
        else:
            f=ui.__floor__(); opts.append([(f,f+1)])
    # also integer coordinate could be free interval [ui-1,ui] or [ui,ui+1]
    opts=[]
    for ui in u:
        if ui.denominator==1:
            i=int(ui); o={(i,i)}
            if i-1>=0:o.add((i-1,i))
            if i+1<=10**9:o.add((i,i+1))
            opts.append(sorted(o))
        else:
            f=ui.__floor__(); opts.append([(f,f+1)])
    for combo in product(*opts):
        corners=product(*[set(c) for c in combo])
        if all(all(0<=x<=Q[j] for j,x in enumerate(cr)) and any(cr) for cr in corners): return True
    return False
assert s(1296)==36
print("1296 (1/2,1/2) covered in box (2,2)?",covered([Fraction(1,2)]*2,(2,2)))
print("(3/2,1/2) covered?",covered([Fraction(3,2),Fraction(1,2)],(2,2)), " (1,1/2) covered?",covered([Fraction(1),Fraction(1,2)],(2,2)))
# FIELD-I operator on 72
def C(x):
    Dx=D(x); L=ilcm(*Dx); G=0
    for d in Dx: G=gcd(G,d-1)
    return x+Fraction(L*L,G)
x=Fraction(72);orb=[x]
for _ in range(11):
    x=C(int(x)) if x.denominator==1 else None; orb.append(x)
print([int(o) for o in orb])
print("x_{n+3}=4x_n:",all(orb[i+3]==4*orb[i] for i in range(len(orb)-3)))
assert all(D(int(orb[i]))<=D(int(orb[i+1])) for i in range(len(orb)-1))
# proposed family x_k=(p1..pk)^4/3
for ps in ([2,5,11],[2,5,11,17]):
    a=prod(ps)**4; k=len(ps)
    E={d for d in divisors(s(a)) if d>=2 and (d-1)%3==0}
    claim={prod(p**e for p,e in zip(ps,al)) for al in product(range(3),repeat=k) if sum(al)%2==0 and any(al)}
    print(k,len(E),E==claim)
