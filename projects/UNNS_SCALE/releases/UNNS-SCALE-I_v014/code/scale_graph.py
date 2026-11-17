"""v014: distances d_{G_B}(B, A) for all A in G_B (BFS), used in the scale-transfer bound tau^B_n(C) <= 2 d_{G_B}(B,A) + tau^A_n(C)  (C >= B(n+1))."""
import sys; sys.dont_write_bytecode = True
from sympy import divisors, factorint
from indep_check import nbrs
def ball(B, depth):
    dist = {B: 0}; fr = [B]
    for d in range(1, depth + 1):
        nx = []
        for v in fr:
            for w in nbrs(v):
                if w <= B and w not in dist: dist[w] = d; nx.append(w)
        fr = nx
    return dist
if __name__ == "__main__":
    import collections
    D = ball(10**6, int(sys.argv[1]) if len(sys.argv) > 1 else 4); print(collections.Counter(D.values()))
