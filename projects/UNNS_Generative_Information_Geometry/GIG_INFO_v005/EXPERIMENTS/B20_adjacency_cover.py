"""B20 -- finite verification of the hypotheses of the adjacency-cover theorem for pairwise-transition systems (k=6):
 (i) H~_1(Z_p;F2)=0 for each ordered pair p;
 (ii) for every set S of at most 3 ordered pairs with Z_S nonempty, Z_S is connected (H~_0=0);
 also nonemptiness criterion: Z_S nonempty iff the digraph S on the six vertices is not strongly connected (checked for all |S|<=3 trivially, and for random larger S).
Then the Mayer-Vietoris (Cech) spectral sequence of the cover {Z_p: p in B} gives H_1(Y_B;F2)=0 for EVERY set B of bad ordered pairs, i.e. beta_2(K_A)=0 for every Hamiltonian-path system."""
import itertools, json, os, random, time
from collections import Counter
import _path, adjacency as ad

def strongly_connected(S, n=6):
    adj = {i: set() for i in range(n)}; radj = {i: set() for i in range(n)}
    for x, y in S: adj[x].add(y); radj[y].add(x)
    def reach(g):
        seen = {0}; st = [0]
        while st:
            u = st.pop()
            for v in g[u]:
                if v not in seen: seen.add(v); st.append(v)
        return len(seen) == n
    return reach(adj) and reach(radj)

if __name__ == "__main__":
    t0 = time.time()
    out = {"single_pair": Counter(), "H1_single_nonzero": 0, "sizes": {}}
    # (i)
    b1 = [ad.Z_S_betti([p], 2) for p in ad.PAIRS]
    out["single_pair_betti_distinct"] = sorted(set(map(tuple, b1)))
    out["H1_single_nonzero"] = sum(1 for b in b1 if b[1] != 0)
    # (ii) canonical representatives under S6 to save time, but also report full counts
    perms = list(itertools.permutations(range(6)))
    def canon(S):
        return min(tuple(sorted((p[x], p[y]) for x, y in S)) for p in perms)
    for r in (2, 3):
        seen = {}
        total = 0; empty = 0; crit_viol = 0; disconnected = 0; nonacyclic = 0; types = Counter()
        for S in itertools.combinations(ad.PAIRS, r):
            total += 1
            c = canon(S)
            if c not in seen:
                bt = ad.Z_S_betti(c, 2)
                seen[c] = bt
            bt = seen[c]
            nonempty = bt is not None
            crit_viol += (nonempty != (not strongly_connected(S)))
            if nonempty:
                disconnected += bt[0] != 0
                nonacyclic += any(bt)
                types[tuple(bt)] += 1
            else:
                empty += 1
        out["sizes"][r] = {"sets": total, "orbit_reps": len(seen), "empty": empty, "criterion_violations": crit_viol, "disconnected": disconnected, "nonacyclic": nonacyclic, "reduced_betti_0_1_2_distribution": {str(k): v for k, v in types.items()}}
        print(r, out["sizes"][r], round(time.time() - t0), flush=True)
    # criterion on random larger S
    rng = random.Random(77); viol = 0; tested = 0; nonac = Counter()
    for _ in range(300):
        S = [p for p in ad.PAIRS if rng.random() < rng.choice([0.15, 0.3, 0.5])]
        if not S: continue
        bt = ad.Z_S_betti(S, 3); tested += 1
        viol += ((bt is not None) != (not strongly_connected(S)))
        if bt is not None: nonac[tuple(bt)] += 1
    out["criterion_random_larger"] = {"tested": tested, "violations": viol, "betti_dist": {str(k): v for k, v in nonac.items()}}
    out["single_pair"] = None
    out["seconds"] = round(time.time() - t0)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "B20_adjacency_cover.json"), "w"), indent=1)
    print(out)
