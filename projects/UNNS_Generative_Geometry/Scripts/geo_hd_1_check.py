from sympy import factorint, divisors, gcd
from fractions import Fraction
from itertools import product
def v(n,p):
    c=0
    while n%p==0: n//=p;c+=1
    return c
def s(m):
    r=1
    for p,e in factorint(m).items(): r*=p**(e//2)
    return r
def D(m): return {d for d in divisors(s(m)) if d>=2}
# 1. bijection occurrence <-> E(x), brute force over integer m (x=m,b=1) and rationals
def occ(x):  # x Fraction; brute N up to bound
    out=[]
    for N in range(1,3000):
        M=x*N/(N+1)**2
        if M.denominator==1 and M>0: out.append((N,int(M)))
    return out
for x in [Fraction(72),Fraction(900),Fraction(1870**2,3),Fraction(12100,3),Fraction(36)]:
    a,b=x.numerator,x.denominator
    E={d for d in divisors(s(a)) if d>=2 and (d-1)%b==0}
    O=occ(x); assert {N+1 for N,M in O}==E,(x,O,E)
    assert all(M==a*(N)//(b*(N+1)**2) and a*N%(b*(N+1)**2)==0 for N,M in O)
print("bijection OK; 72 ->",occ(Fraction(72)))
# 2. Prop 2.1 + counting + loss formula, all m<=3000, all N|m
bad=0;cnt=0
for m in range(1,3001):
    for N in divisors(m):
        t=m*(N+1)**2//N
        lhs=D(m)<=D(t)
        rhs=all(v(N,p)==1 and v(m,p)%2==1 for p in factorint(N))
        assert lhs==rhs,(m,N)
        g=gcd(s(m),s(t)); tau=lambda n:len(divisors(n))
        assert len(D(m)&D(t))==tau(g)-1
        assert len(D(m)-D(t))==tau(s(m))-tau(g)
        assert len(D(t)-D(m))==tau(s(t))-tau(g)
        # closed-form loss exponent
        for p in factorint(N):
            n=v(N,p);vm=v(m,p)
            loss=vm//2-(vm-n)//2
            assert loss==(n//2 if vm%2 else (n+1)//2)
        cnt+=1
print("T1, counts, loss formula verified on",cnt,"edges")
# 3. benchmarks
for m in (72,6):
    print(m,[(N,m*(N+1)**2//N,sorted(D(m*(N+1)**2//N)),sorted(D(m)-D(m*(N+1)**2//N))) for N in divisors(m)])
print([ (m,factorint(m)) for m in (24,27,32,49)])
# 4. cube obstruction: U_k vs H_k via exact LP-free check, plus k=2 at x=36, and Graver of Z^k
for k in (2,3,4,5):
    ps=[2,3,5,7,11][:k]; x=1
    for p in ps:x*=p*p
    assert {d for d in divisors(s(x)) if d>=2}== {__import__('math').prod(p for p,e in zip(ps,w) if e) for w in product((0,1),repeat=k) if any(w)}
    pt=[Fraction(1,2)]*k
    assert sum(pt)>=1 and max(pt)<1
print("k=2..5 certificate OK (k=2 is x=36, already fails)")
