"""Exact certificates for the two UNNS projection figures in manuscript v1.3."""

def T(N, x):
    assert x % N == 0
    return (x // N) * (N + 1) ** 2

def valuation(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v

def pi(n):
    return (valuation(n, 2), valuation(n, 3))

def divisors(n):
    return [d for d in range(1, n+1) if n%d==0]

def neighbors(x):
    up = {T(N, x) for N in divisors(x)}
    down = {x // (q*q) * (q-1) for q in range(2, int(x**0.5)+1) if x % (q*q) == 0}
    return up | down

assert T(2,6)==27 and T(5,30)==216
assert pi(6)==(1,1) and pi(30)==(1,1)
assert pi(27)==(0,3) and pi(216)==(3,3)
assert 6%5 != 0 and 30%5 == 0
assert T(1,1)==4 and T(5,5)==36
assert pi(1)==pi(5)==(0,0)
assert pi(4)==(2,0) and pi(36)==(2,2)
assert 4 not in neighbors(36) and not (neighbors(4)&neighbors(36))
print('PASS: exact projection vectors, branch legality, and shortcut witness')
