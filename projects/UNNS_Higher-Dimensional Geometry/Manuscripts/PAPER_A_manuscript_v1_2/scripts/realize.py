"""Check of Proposition 3.6 (realizability of every normalized pair (d,s)).
For each d in 2..14 and each unit s mod d we build primes b, p1, p2 exactly as in the proof
and test, by brute force on a box, that {(i,j): p1^i p2^j = 1 mod b} equals Gamma_{d,s}.
Finite check of a constructive proof; not a substitute for it."""
from math import gcd
def isprime(n):
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
def primitive_root(p):
    fac=[q for q in range(2,p) if (p-1)%q==0 and isprime(q)]
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fac): return g
def next_prime_in_class(res, mod, start=2, avoid=()):
    p = start
    while True:
        if p % mod == res % mod and isprime(p) and p not in avoid: return p
        p += 1
bad = 0; tested = 0
for d in range(2, 15):
    b = next_prime_in_class(1, d, start=d+1)
    w = primitive_root(b); h = pow(w, (b-1)//d, b)
    for s in range(1, d):
        if gcd(s, d) != 1: continue
        t = pow(s, -1, d); tau = (-t) % d
        r1, r2 = h, pow(h, tau, b)
        p1 = next_prime_in_class(r1, b, start=2, avoid=(b,))
        p2 = next_prime_in_class(r2, b, start=2, avoid=(b, p1))
        for i in range(0, 2*d+1):
            for j in range(0, 2*d+1):
                inL = (pow(p1, i, b) * pow(p2, j, b)) % b == 1
                inG = (j - s*i) % d == 0
                tested += 1
                if inL != inG: bad += 1
        # orders and D0
        assert all(pow(r, d, b) == 1 for r in (r1, r2))
print("pairs tested over d=2..14; lattice points compared:", tested, "mismatches:", bad)
