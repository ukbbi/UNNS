"""v012: readers for the exact frontier files (tau_exact output) and ladder files (ladder output); q(n) helper."""
import sys; sys.dont_write_bytecode = True
from sympy import factorint
def read_frontier(path):
    """-> {n: ([(l,H),...], flag)} flag '*' = reached floor B(n+1); '~' stalled above; 'inf' unreachable inside Cmax"""
    out = {}
    for line in open(path):
        r = line.split()
        if not r: continue
        out[int(r[0])] = ([tuple(map(int, x.split(":"))) for x in r[1:] if ":" in x], r[-1])
    return out
def read_ladder(*paths):
    """-> {(n,W): int distance | ('>',r,capped) lower bound | 'below'}"""
    out = {}
    for p in paths:
        for line in open(p):
            n, W, v = line.split()
            if v == "below": out[(int(n), int(W))] = "below"
            elif v.startswith(">"):
                import re; m = re.match(r">(\d+)(cap)?", v); out[(int(n), int(W))] = (">", int(m.group(1)), bool(m.group(2)))
            else: out[(int(n), int(W))] = int(v)
    return out
_q = {}
def qn(n):
    """largest prime with odd exponent in n(n+1) (1 if none)"""
    if n not in _q:
        f = factorint(n); g = factorint(n + 1)
        odd = [p for p, e in list(f.items()) + list(g.items()) if e % 2]
        _q[n] = max(odd) if odd else 1
    return _q[n]
