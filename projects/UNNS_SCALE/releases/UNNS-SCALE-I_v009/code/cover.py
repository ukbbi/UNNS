"""v009: exact covering search over residue classes.  Classes (r,m): n = r mod m (valid for n >= n0).
Node (a,M) = {n = a mod M}. Covered iff some class (r,m) has m | M and r = a mod m. Otherwise refine by a prime p of m/gcd(m,M) (M -> pM).
Best-first on measure 1/M.  Uncovered measure of (frontier + dead nodes) is a RIGOROUS upper bound on the density of integers n >= n0max outside the union;
the search ends with an empty frontier and no dead node  <=>  the classes cover every integer n >= n0max (a covering certificate)."""
import sys, os, math, time, heapq
sys.dont_write_bytecode = True
from fractions import Fraction
def spf(n):
    if n % 2 == 0: return 2
    p = 3
    while p * p <= n:
        if n % p == 0: return p
        p += 2
    return n
def cover(classes, budget, log=False, max_frontier=1500000):
    cl = sorted({(r % m, m) for r, m in classes}, key=lambda t: t[1])
    heap = [(1, 0, tuple(range(len(cl))))]; dead = []; t0 = time.time(); nodes = 0; covered = Fraction(0); lastlog = t0
    while heap and time.time() - t0 < budget and len(heap) < max_frontier:
        M, a, act = heapq.heappop(heap); nodes += 1
        hit = False; best = None
        for i in act:
            r, m = cl[i]
            if M % m == 0:
                if (a - r) % m == 0: hit = True; break
            else:
                t = m // math.gcd(m, M)
                if best is None or t < best[0]: best = (t, i)
        if hit:
            covered += Fraction(1, M)
        elif best is None:
            dead.append((a, M))
        else:
            p = spf(best[0]); M2 = M * p
            for j in range(p):
                a2 = a + j * M
                act2 = tuple(k for k in act if (a2 - cl[k][0]) % math.gcd(cl[k][1], M2) == 0)
                heapq.heappush(heap, (M2, a2, act2))
        if log and time.time() - lastlog > 15:
            lastlog = time.time(); print("  nodes %d  frontier %d  dead %d  smallest-frontier-modulus %d  covered %.9f" % (nodes, len(heap), len(dead), heap[0][0] if heap else 0, float(covered)), flush=True)
    unc = 1 - covered
    return {"uncovered_upper_bound": unc, "nodes": nodes, "frontier": len(heap), "dead": dead, "finished": not heap, "seconds": time.time() - t0, "frontier_nodes": [(a, M) for M, a, _ in heap[:50]]}
if __name__ == "__main__":
    from classes import all_classes
    B = 10**6; K = int(sys.argv[1]); budget = float(sys.argv[2])
    C = [c for c in all_classes(B, K) if c[2] <= 10**6]
    print("classes", len(C), "max n0", max(c[2] for c in C), flush=True)
    out = cover([(r, m) for r, m, n0, sh in C], budget, log=True)
    print("finished:", out["finished"], "uncovered upper bound %.3e" % float(out["uncovered_upper_bound"]), "dead", len(out["dead"]), "nodes", out["nodes"], "frontier", out["frontier"])
