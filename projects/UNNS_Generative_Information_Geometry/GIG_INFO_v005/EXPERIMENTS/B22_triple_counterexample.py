"""B22 -- certified minimal-ish counterexample showing the pair-adjacency theorem is sharp: a 3-adjacency system (admissible iff every consecutive triple is allowed) with beta_2(K)=1.
Greedy minimisation of the set of forbidden triples (pre-specified deterministic order), certificate z/phi verified by definition-level code (v002 pair_cert.verify)."""
import itertools, json, os, random
import _path, v2
import history_complex as hc
import B21_locality_boundary as B21

PERMS = hc.perms(6)
T3 = list(itertools.permutations(range(6), 3))

def b2(allowed):
    m = B21.triple_mask(allowed)
    return (hc.betti(m, 6)[2] if 0 < m < (1 << 720) - 1 else -1), m

if __name__ == "__main__":
    rng = random.Random(20261125)
    # reproduce first positive found by the B21 sampling stream, then minimise
    found = None
    for it in range(40000):
        dens = rng.choice([0.5, 0.65, 0.8, 0.9, 0.95])
        allowed = set(t for t in T3 if rng.random() < dens)
        m = B21.triple_mask(allowed)
        if m == 0 or m == (1 << 720) - 1: continue
        if hc.betti(m, 6)[2] > 0:
            found = allowed; break
    # fresh stream to recount positives
    cnt = 0; tot = 0
    rng2 = random.Random(20261126)
    for it in range(20000):
        dens = rng2.choice([0.5, 0.65, 0.8, 0.9, 0.95])
        al = set(t for t in T3 if rng2.random() < dens)
        m = B21.triple_mask(al)
        if m == 0 or m == (1 << 720) - 1: continue
        tot += 1; cnt += hc.betti(m, 6)[2] > 0
    bad = sorted(set(T3) - found)
    # greedy: try re-allowing each forbidden triple; keep if beta2 stays >0
    changed = True
    while changed:
        changed = False
        for t in list(bad):
            trial = found | {t}
            v, m = b2(trial)
            if v > 0:
                found = trial; bad.remove(t); changed = True
    v, m = b2(found)
    A = [PERMS[i] for i in range(720) if m >> i & 1]
    pc = v2.pair_cert
    by = pc.complex_of(A)
    zi, pi = pc.find_certificate(by)
    z = [by[2][i] for i in zi]; phi = [by[2][i] for i in pi]
    rec = {"forbidden_triples": [list(t) for t in bad], "n_forbidden_triples": len(bad), "N": len(A), "betti_hc_engine": list(hc.betti(m, 6)),
           "beta2_rank_route": pc.betti2_by_ranks(by)[0], "beta2_column_route": pc.betti2_by_ranks(by)[1], "mask_hex": hex(m),
           "certificate": {"cycle_2faces": len(z), "cochain_2faces": len(phi), "verified": pc.verify(A, z, phi), "cycle": [[list(b) for b in f] for f in z], "cochain": [[list(b) for b in f] for f in phi]},
           "pair_adjacency_only": False, "recount_random_3adjacency": {"tested": tot, "beta2_positive": cnt}}
    # is it truly not a pair-adjacency system?  (pair-adjacency masks have beta2=0 by the theorem; check that the mask is not Hamiltonian-path of any digraph)
    import adjacency as ad
    allowed_pairs = set()
    for p in A:
        for j in range(5): allowed_pairs.add((p[j], p[j + 1]))
    rec["is_pair_adjacency_system"] = (ad.hamiltonian_mask(allowed_pairs) == m)
    json.dump(rec, open(os.path.join(_path.ROOT, "CERTIFICATES", "counterexample_triple_adjacency_beta2.json"), "w"))
    print({k: v for k, v in rec.items() if k != "certificate"}, rec["certificate"]["verified"])
