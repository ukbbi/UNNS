"""v009: corrected constant-ratio shapes as single residue classes.
Shape (v',w',c,d,P,Q) [famE]: legal route for n iff  v'|n, w'|n+1, P | c n/v' + 1, P | d (n+1)/w' + 1 (gcd(P,Q)=1),  q=Q u/P>=2, r=Q u'/P>=2.
Hence n lies in ONE residue class  n = r0 (mod m),  m = lcm(v'P, w'P) = P v' w',  for n >= n0 (lower bounds on q,r)."""
import sys, os, math
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import famE
def crt(a1, m1, a2, m2):
    g = math.gcd(m1, m2)
    if (a2 - a1) % g: return None
    l = m1 // g * m2
    k = ((a2 - a1) // g * pow(m1 // g, -1, m2 // g)) % (m2 // g) if m2 // g > 1 else 0
    return (a1 + m1 * k) % l, l
def shape_class(sh):
    vp, wp, c, d, P, Q = sh
    if P == 1: A = (0, vp); Bc = (wp - 1, wp)                      # n=0 mod v', n=-1 mod w'
    else:
        a1 = (-pow(c, -1, P)) % P; a2 = (-pow(d, -1, P)) % P        # n/v' = a1 (P),  (n+1)/w' = a2 (P)
        A = (vp * a1, vp * P); Bc = (wp * a2 - 1, wp * P)            # n = v' a1 (v'P),  n = w' a2 -1 (w'P)
    t = crt(A[0], A[1], Bc[0], Bc[1])
    if t is None: return None
    r0, m = t
    # n0: u = c n/v'+1 >= 2P/Q and u' = d (n+1)/w' + 1 >= 2P/Q
    n0a = -(-vp * (2 * P - Q) // (Q * c)); n0b = -(-wp * (2 * P - Q) // (Q * d)) - 1
    return r0, m, max(2, n0a, n0b)
def all_classes(B, K):
    out = []
    for sh in famE.shapes(B, K):
        t = shape_class(sh)
        if t: out.append((t[0], t[1], t[2], sh))
    return out
if __name__ == "__main__":
    import random
    B = 10**6; K = int(sys.argv[1]); C = all_classes(B, K); rnd = random.Random(2)
    print("shapes", len(famE.shapes(B, K)), "classes", len(C), "with n0<=1e6:", sum(1 for c in C if c[2] <= 10**6))
    bad = 0
    for r0, m, n0, sh in rnd.sample(C, min(len(C), 300)):
        for j in range(3):
            n = max(n0, 2); n += (r0 - n) % m; n += j * m
            p = famE.route(B, n, sh); bad += p is None
            # also: n just below n0 fine either way; non-members inside the (v',w') classes handled elsewhere
    print("class members without a route:", bad)
    import statistics
    ms = sorted(c[1] for c in C if c[2] <= 10**6); print("moduli: min", ms[0], "median", ms[len(ms)//2], "max", ms[-1], " sum 1/m = %.3f" % sum(1/m for m in ms))
