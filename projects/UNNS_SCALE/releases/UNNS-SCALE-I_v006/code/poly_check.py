"""Independent (sympy-free) exact verification of residue-class path identities.
A polynomial is a list of ints, highest degree first.  An identity (B, M, r, steps) with steps=[(dir, N(t) coefficients)]
claims: for every integer t >= t0 the integers  B(Mt+r) -> ... -> B(Mt+r+1)  form a path of the SELECT-II graph.
Checked here:  (i) exact polynomial division identities (forward: N | S, backward: (N+1)^2 | S) in Z[t];
              (ii) final polynomial = B(M t + r + 1);  (iii) positivity of all labels / cofactors for t >= t0 (Cauchy bound + finite check);
              (iv) numerical replay with plain integers for many t."""
from fractions import Fraction

def trim(p):
    i = 0
    while i < len(p) - 1 and p[i] == 0: i += 1
    return p[i:]

def padd(a, b):
    n = max(len(a), len(b)); a = [0] * (n - len(a)) + a; b = [0] * (n - len(b)) + b
    return trim([x + y for x, y in zip(a, b)])

def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): r[i + j] += x * y
    return trim(r)

def pdivexact(a, b):
    """exact division in Z[t]; returns quotient or None"""
    a = list(a); b = trim(list(b))
    if len(a) < len(b): return None if any(a) else [0]
    q = []
    while len(a) >= len(b):
        c = Fraction(a[0], b[0])
        if c.denominator != 1: return None
        c = int(c); q.append(c)
        for i in range(len(b)): a[i] -= c * b[i]
        a.pop(0)
        if not a: break
    if any(a): return None
    return trim(q) if q else [0]

def peval(p, t):
    v = 0
    for c in p: v = v * t + c
    return v

def positive_from(p):
    """least t0>=0 such that p(t)>=1 for ALL integers t>=t0, or None"""
    p = trim(p)
    if len(p) == 1: return 0 if p[0] >= 1 else None
    if p[0] <= 0: return None
    H = 1 + max(abs(c) for c in p[1:]) // p[0] + 1          # Cauchy bound: p(t)>0 for t>=H, integer valued => >=1
    bad = [x for x in range(0, H + 1) if peval(p, x) < 1]
    return (max(bad) + 1) if bad else 0

def verify_identity(B, M, r, steps, t_samples=60):
    S = trim([B * M, B * r]); target = trim([B * M, B * (r + 1)]); t0 = 0; polys = [S]
    for dr, N in steps:
        N = trim(list(N))
        if dr == '+':
            Q = pdivexact(S, N)
            if Q is None: return False, "forward label does not divide"
            S = pmul(Q, pmul(padd(N, [1]), padd(N, [1])))
            labs = [N, Q]
        else:
            q = padd(N, [1]); Q = pdivexact(S, pmul(q, q))
            if Q is None: return False, "backward square does not divide"
            S = pmul(Q, N)
            labs = [N, Q, q]
        for g in labs:
            z = positive_from(g)
            if z is None: return False, "label/cofactor not eventually positive"
            t0 = max(t0, z)
        polys.append(S)
    if S != target: return False, "endpoint mismatch"
    for P_ in polys:
        z = positive_from(P_)
        if z is None: return False, "state not eventually positive"
        t0 = max(t0, z)
    # numerical replay
    for t in list(range(t0, t0 + t_samples)) + [t0 + 10**6 + 17, t0 + 10**9 + 3]:
        x = peval(polys[0], t)
        for dr, N in steps:
            Nv = peval(trim(list(N)), t)
            if dr == '+':
                assert Nv >= 1 and x % Nv == 0; x = x // Nv * (Nv + 1) ** 2
            else:
                q = Nv + 1; assert q >= 2 and x % (q * q) == 0; x = x // (q * q) * Nv
        assert x == peval(target, t)
    return True, t0
