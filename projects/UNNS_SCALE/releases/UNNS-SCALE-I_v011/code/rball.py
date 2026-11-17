"""v010: independent Python restricted balls (all vertices <= C), built on exact_lib (Pollard rho / Miller-Rabin) -- independent of ball.cpp."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor
from b2_types import moves
def rball(x, C, R=2):
    """dict vertex -> parent-chain (tuple path from x), all vertices <= C"""
    L = [{x: (x,)}]; seen = {x}
    for r in range(R):
        nxt = {}
        for v, path in L[-1].items():
            for l, N, y, fy in moves(v, factor(v)):
                if y <= C and y not in seen and y not in nxt: nxt[y] = path + (y,)
        seen |= set(nxt); L.append(nxt)
    return L
def restricted_route(x, y, C):
    """some route of length <=4 with all vertices <= C, or None (exhaustive: balls of radius 2 inside C)"""
    A = rball(x, C); Bb = rball(y, C)
    best = None
    for a in range(3):
        for b in range(3):
            for z, pa in A[a].items():
                if z in Bb[b]:
                    p = pa + Bb[b][z][::-1][1:]
                    if best is None or len(p) < len(best): best = p
    return best, sum(len(l) for l in A), sum(len(l) for l in Bb)
if __name__ == "__main__":
    B = 10**6; C = 10**12
    for n in map(int, sys.argv[1:]):
        p, sa, sb = restricted_route(B*n, B*(n+1), C); print(n, "route" if p else "NO ROUTE within [1,1e12]", sa, sb, p)
