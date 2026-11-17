"""v014 errata for v013 Section 1 (L4 remark) -- parity-barrier necessary condition.
Claim (PROVED): for u,w in G_C, if v_r(u) != v_r(w) (mod 2) then (r+1)^2 <= C.  Proof: an edge {kN, k(N+1)^2} changes the exponent parity exactly at the primes with odd exponent in N; so a route
between u and w contains an edge whose N has odd v_r(N), hence N >= r and the larger endpoint k(N+1)^2 >= (r+1)^2; all vertices are <= C.
v013 stated the condition for 'every prime r with odd exponent in p+1', i.e. the special case v_r(B) even; for general B it is too strong (B=11, p=43: 11 -- 44 is the N=1 edge).
Data: for B<=60, p<=1500 prime: connectivity of B and p+1 in G_{p+1} vs. the v013 condition (C1) and the corrected condition (C2)."""
import sys; sys.dont_write_bytecode = True
from primeflip import adjacency, bfs_path
from sympy import factorint, primerange
def vr(x): return {r: e % 2 for r, e in factorint(x).items()}
def run(Bmax=60, pmax=1500):
    adj = adjacency(pmax + 3); out = dict(pairs=0, C2_false_but_connected=0, C1_false_connected=0, C1_false_connected_examples=[], C2_true_not_connected=0, C2_true_connected=0, C1_true_not_connected=0)
    for p in primerange(2, pmax + 1):
        pf = vr(p + 1)
        for B in range(2, min(Bmax, p - 1) + 1):
            if p % B == 0: continue
            bf = vr(B); rs = set(pf) | set(bf); odd = {r for r in rs if pf.get(r, 0) != bf.get(r, 0)}
            C2 = all((r + 1) ** 2 <= p + 1 for r in odd); C1 = all((r + 1) ** 2 <= p + 1 for r, e in pf.items() if e)
            conn = bfs_path(adj, p + 1, B, p + 1) is not None; out["pairs"] += 1
            if conn and not C2: out["C2_false_but_connected"] += 1
            if conn and not C1: out["C1_false_connected"] += 1; 
            if conn and not C1 and len(out["C1_false_connected_examples"]) < 6: out["C1_false_connected_examples"].append((B, p))
            if C2 and conn: out["C2_true_connected"] += 1
            if C2 and not conn: out["C2_true_not_connected"] += 1
            if C1 and not conn: out["C1_true_not_connected"] += 1
    return out
if __name__ == "__main__":
    import json; r = run(); print(json.dumps(r)); json.dump(r, open("../results/ERRATA_parity.json", "w"))
