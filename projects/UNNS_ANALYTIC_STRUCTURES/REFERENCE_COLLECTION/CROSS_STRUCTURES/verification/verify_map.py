#!/usr/bin/env python3
"""Finite exact checks for Cross-Structural Research Map v001. Standard library only.
Checks test the stated identities on finite ranges; they are not proofs."""
import itertools, math, random
from functools import lru_cache
from fractions import Fraction

def r(N): return Fraction((N+1)**2, N)
@lru_cache(None)
def KE(w):
    K, E = 1, 1
    for N in w:
        d = math.gcd(E, N); K, E = K*N//d, E*(N+1)**2//d
    return K, E
@lru_cache(None)
def W(k, x):
    """all words of length k ending at x (direct backward enumeration, no use of E)"""
    if k == 0: return ((),)
    out = []
    for d in range(2, math.isqrt(x)+1):
        if x % (d*d) == 0:
            out += [w+(d-1,) for w in W(k-1, x*(d-1)//(d*d))]
    return tuple(out)
def admissible(src, w):
    x = src
    for N in w:
        if x % N: return None
        x = x//N*(N+1)**2
    return x
def sqfree(n): return all(n % (p*p) for p in range(2, math.isqrt(n)+1))
def report(name, count): print(f"PASS  {name}: {count} cases")

X = 20000
# 0. fibre = divisibility down-set of the thresholds
A = {k: {} for k in (1, 2, 3)}
n = 0
for k in A:
    words = {w for x in range(1, X+1) for w in W(k, x)}
    for w in words:
        E = KE(w)[1]; A[k].setdefault(E, set()).add(w)
    for x in range(1, X+1):
        lhs = set(W(k, x)); rhs = {w for E, s in A[k].items() if x % E == 0 for w in s}
        assert lhs == rhs; n += 1
report("W_k(x) = {w : E(w) | x}", n)
# 1. composition law
random.seed(1); n = 0
for _ in range(20000):
    u = tuple(random.randint(1, 30) for _ in range(random.randint(0, 5)))
    v = tuple(random.randint(1, 30) for _ in range(random.randint(0, 5)))
    (a, b), (c, e) = KE(u), KE(v); d = math.gcd(b, c)
    assert KE(u+v) == (a*c//d, b*e//d)
    assert Fraction(KE(u+v)[1], KE(u+v)[0]) == Fraction(b, a)*Fraction(e, c)
    K, E = KE(u+v); assert admissible(K, u+v) == E
    n += 1
report("composition law for (K,E)", n)
# 2. shared-history kernel and r-fold coefficient identity
n = 0
for k in (1, 2, 3):
    H = [0]+[len(W(k, x)) for x in range(1, X+1)]
    for _ in range(20000):
        xs = [random.randint(1, X//1) for _ in range(random.choice((2, 3)))]
        g = math.gcd(*xs); s = set(W(k, xs[0]))
        for x in xs[1:]: s &= set(W(k, x))
        assert len(s) == H[g]; n += 1
    for x in (36*k, 72, 144, 3600, 14400):
        for y in (72, 288, 900, 14400):
            assert len(set(W(k, x)) & set(W(k, y))) == sum(len(s) for E, s in A[k].items() if x % E == 0 and y % E == 0); n += 1
report("C_k(x1..xr) = H_k(gcd) = sum over common thresholds", n)
# 3. GCD-matrix determinant and rank
def bareiss(M):
    M = [row[:] for row in M]; m = len(M); prev = 1; sign = 1; rank = 0; col = 0
    while rank < m and col < m:
        p = next((i for i in range(rank, m) if M[i][col]), None)
        if p is None: col += 1; continue
        if p != rank: M[p], M[rank] = M[rank], M[p]; sign = -sign
        for i in range(rank+1, m):
            for j in range(col+1, m):
                M[i][j] = (M[i][j]*M[rank][col]-M[i][col]*M[rank][j])//prev
            M[i][col] = 0
        prev = M[rank][col]; rank += 1; col += 1
    det = sign*M[m-1][m-1] if rank == m else 0
    return det, rank
n = 0
for k in (0, 1, 2):
    for m in range(1, 101):
        a = lambda j: (1 if j == 1 else 0) if k == 0 else len(A[k].get(j, ()))
        M = [[len(W(k, math.gcd(i, j))) for j in range(1, m+1)] for i in range(1, m+1)]
        det, rank = bareiss(M)
        assert det == math.prod(a(j) for j in range(1, m+1))
        assert rank == sum(1 for j in range(1, m+1) if a(j)); n += 1
report("determinant = product of a_k(m), rank = number of m with a_k(m)>0", n)
# 4. complete histories (squarefree source)
n = 0
for k in (1, 2, 3):
    for t in range(1, X+1):
        direct = 0
        for w in W(k, t):
            src = Fraction(t)
            for N in w: src /= r(N)
            assert src.denominator == 1 and admissible(src.numerator, w) == t
            direct += sqfree(src.numerator)
        formula = 0
        for w in W(k, t):
            K, E = KE(w); m = t//E
            formula += sqfree(K) and sqfree(m) and math.gcd(m, K) == 1
        assert direct == formula; n += 1
report("complete-history coefficient identity", n)
comp72 = []
for k in range(1, 6):
    for w in W(k, 72):
        src = Fraction(72)
        for N in w: src /= r(N)
        if sqfree(src.numerator): comp72.append((int(src), w))
assert sorted(comp72) == [(1, (1,1,2)), (1, (1,2,1)), (3, (3,2)), (10, (5,))]; report("four complete histories of 72 (GIG-T4)", 4)

# 5. history complexes on distinct-letter words: faces of the permutohedron = ordered block partitions
def blocks(letters):
    if not letters: yield (); return
    s = sorted(letters)
    for m in range(1, len(s)+1):
        for first in itertools.combinations(s, m):
            for rest in blocks([a for a in s if a not in first]):
                yield (first,)+rest
def verts(cell):
    for parts in itertools.product(*[itertools.permutations(b) for b in cell]):
        yield tuple(itertools.chain(*parts))
def dim(c): return sum(len(b)-1 for b in c)
def complex_at(content, x):
    Q = math.prod(r(N) for N in content); y = Fraction(x)/Q
    if y.denominator != 1: return []
    return [c for c in blocks(list(content)) if all(admissible(y.numerator, v) is not None for v in verts(c))]
def rank2(rows):
    basis = {}; rk = 0
    for v in rows:
        while v:
            h = v.bit_length()-1
            if h in basis: v ^= basis[h]
            else: basis[h] = v; rk += 1; break
    return rk
def faces(c):
    for i, b in enumerate(c):
        for m in range(1, len(b)):
            for f in itertools.combinations(b, m):
                yield c[:i]+(f, tuple(a for a in b if a not in f))+c[i+1:]
def betti(cells):
    by = {}
    for c in cells: by.setdefault(dim(c), []).append(c)
    top = max(by, default=-1); rk = {}
    for d in range(1, top+1):
        ix = {c: i for i, c in enumerate(by[d-1])}
        rows = []
        for c in by.get(d, []):
            v = 0
            for f in faces(c): v ^= 1 << ix[f]
            rows.append(v)
        rk[d] = rank2(rows)
    return [len(by.get(d, []))-rk.get(d, 0)-rk.get(d+1, 0) for d in range(top+1)]
def threshold(c): return math.lcm(*[KE(v)[1] for v in verts(c)])
n = 0
for content in [(1,2,3), (1,3,8), (2,3,8), (1,2,5), (2,3,14,15), (1,2,3,4)]:
    allc = list(blocks(list(content))); th = {c: threshold(c) for c in allc}
    L = math.lcm(*th.values()); Q = math.prod(r(N) for N in content)
    pts = {t*m for t in th.values() for m in (1, 2, 7, 11)} | {L}
    for x in pts:
        got = set(complex_at(content, x)); assert got == {c for c in allc if x % th[c] == 0}
        b = betti(list(got)); assert sum((-1)**i*v for i, v in enumerate(b)) == sum((-1)**dim(c) for c in got); n += 1
report("cell present iff threshold divides x; Euler characteristic", n)
C = (2,3,14,15); t = 210*math.prod(r(N) for N in C); assert t == 1382400
b = betti(complex_at(C, int(t))); assert b[:2] == [1, 1] and not any(b[2:])
L = math.lcm(*[threshold(c) for c in blocks(list(C))]); n = 0
for m in range(1, 400):
    if math.gcd(m, L) == 1: assert betti(complex_at(C, int(t)*m))[:2] == [1, 1]; n += 1
report(f"content (2,3,14,15) at 1382400 has beta1=1, unchanged by coprime multipliers (L={L})", n)

# 6. constants in the mean-log-endpoint bounds
g = 0.5772156649015329
def Ein(t, M=2000):
    h = 1/M; f = lambda u: t if u == 0 else (1-math.exp(-t*u))/u
    return h/3*(f(0)+f(1)+sum((4 if i % 2 else 2)*f(i*h) for i in range(1, M)))
c0 = 1.107910
lo = max(((math.log(c0)-g+Ein(i/100))/(i/100), i/100) for i in range(1, 5001))
hi = min(((g-Ein(-i/100)-math.log(c0))/(i/100), i/100) for i in range(1, 1001))
print(f"lower constant {lo[0]:.6f} at tau={lo[1]}; upper constant {hi[0]:.6f} at tau={hi[1]}")
