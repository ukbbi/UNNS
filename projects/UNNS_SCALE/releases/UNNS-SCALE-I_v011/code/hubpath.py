"""v011: independent explicit path (all vertices <= C) between a vertex and the hub vertex 1 by bidirectional BFS in Python (exact_lib)."""
import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exact_lib import factor
from b2_types import moves
def expand(layer, seen, par, C):
    nxt = {}
    for v in layer:
        for l, N, y, fy in moves(v, factor(v)):
            if y <= C and y not in seen and y not in nxt: nxt[y] = v
    for y, v in nxt.items(): seen.add(y); par[y] = v
    return list(nxt)
def route(a, b, C, rmax=7, cap=400000):
    """bidirectional BFS; returns explicit vertex path a..b with all vertices <= C, or None"""
    pa = {a: None}; pb = {b: None}; sa = {a}; sb = {b}; la = [a]; lb = [b]
    for r in range(rmax):
        if len(sa) <= len(sb): la = expand(la, sa, pa, C)
        else: lb = expand(lb, sb, pb, C)
        meet = sa & sb
        if meet:
            z = next(iter(meet)); p1 = []; v = z
            while v is not None: p1.append(v); v = pa[v]
            p2 = []; v = pb[z]
            while v is not None: p2.append(v); v = pb[v]
            return p1[::-1] + p2
        if len(sa) + len(sb) > cap: return None
    return None
if __name__ == "__main__":
    C = int(float(sys.argv[1])); a, b = int(sys.argv[2]), int(sys.argv[3]); p = route(a, b, C); print(len(p) - 1 if p else None, p)
