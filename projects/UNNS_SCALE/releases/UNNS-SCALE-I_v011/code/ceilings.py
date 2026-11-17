"""v011: from the stored link certificates compute, for every pair (10^6 n, 10^6 (n+1)), an UPPER bound on the connection ceiling
kappa(n) = min over all routes (any length) of the maximum vertex, and compare with the PROVED lower bound max(B(n+1), (q(n)+1)^2)."""
import sys, os, gzip, collections, json
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qn import qvec
B = 10**6
def compute(res):
    fk = {}
    for l in open(os.path.join(res, "CN1_flip_kappa.txt")):
        a, b, k = map(int, l.split()); fk[(a, b)] = k
    links = {}
    for l in open(os.path.join(res, "CN1_vertex_links.txt")):
        t = l.split(); links[int(t[0])] = t
    L = {}; cls = {}
    for m in range(1, 10**6 + 1):
        t = links.get(m)
        if t is None: L[m] = B * m; cls[m] = "direct"
        elif t[1] == "flip":
            p = int(t[2].split("=")[1]); mp = int(t[3].split("=")[1]); s = int(t[4].split("=")[1])
            L[m] = max(B * m, fk[(999 * mp, s)] * p, s * (p + 1) ** 2); cls[m] = "flip"
    for l in open(os.path.join(res, "CN2_bfs_links_R3.txt")):
        t = l.split(); m = int(t[0]); assert int(t[1]) >= 0; L[m] = max(B * m, int(t[4])); cls[m] = "bfs"
    for l in open(os.path.join(res, "CN3b_prime_links_domain.txt")):
        t = l.split(); m = int(t[0]); assert int(t[1]) >= 0; L[m] = max(B * m, 1776 * m, int(t[4])); cls[m] = "prime"
    assert len(L) == 10**6
    K = {}
    for l in gzip.open(os.path.join(res, "K_k999.txt.gz"), "rt"):
        n, k = map(int, l.split()); K[n] = k
    q = qvec(10**6 + 1); within = 0; exceed = []; ub = {}
    for n in range(1, 10**6):
        law = max(B * (n + 1), (q[n] + 1) ** 2)
        if n >= 999: u = max(L[n], L[n + 1])
        else:
            assert K[n]; u = max(B * (n + 1), K[n])
        ub[n] = u
        if u <= law: within += 1
        else: exceed.append(n)
    return {"classes": dict(collections.Counter(cls.values())), "pairs": 999999, "exact_law_proved": within, "law_not_closed": exceed,
            "max_ceiling": max(ub.values()), "law_equals_B_n1_everywhere": all(max(B*(n+1),(q[n]+1)**2) == B*(n+1) for n in range(1, 10**6))}
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
    S = compute(res); json.dump(S, open(os.path.join(res, "CN4_pair_ceilings.json"), "w")); print({k: (v if k != "law_not_closed" else len(v)) for k, v in S.items()})
