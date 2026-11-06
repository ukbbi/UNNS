"""B21 -- (a) direct confirmation of the pair-adjacency theorem on random bad-pair sets (reduced Betti of Y_B, beta_2(K) via history_complex);
          (b) where the theorem stops: random 3-adjacency systems (admissible iff every consecutive TRIPLE of events is allowed)."""
import itertools, json, os, random, time
import numpy as np
import _path, adjacency as ad, forbidden as fb
import history_complex as hc

def triple_mask(allowed3):
    m = 0
    for i, p in enumerate(hc.perms(6)):
        if all((p[j], p[j + 1], p[j + 2]) in allowed3 for j in range(4)):
            m |= 1 << i
    return m

if __name__ == "__main__":
    t0 = time.time(); rng = random.Random(20261125); out = {}
    # (a)
    n = 0; b2pos = 0; y1pos = 0; mism = 0
    for _ in range(300):
        B = set(p for p in ad.PAIRS if rng.random() < rng.choice([0.05, 0.1, 0.2, 0.3, 0.45]))
        m = ad.hamiltonian_mask(set(ad.PAIRS) - B)
        if m == 0 or m == (1 << 720) - 1: continue
        yb = fb.reduced_betti(ad.Y_from_adjacency(B), 2); b = hc.betti(m, 6)
        n += 1; y1pos += yb[1] > 0; b2pos += b[2] > 0; mism += (yb[1] != b[2])
    out["pair_adjacency_random"] = {"tested": n, "Y_H1_positive": int(y1pos), "beta2_K_positive": int(b2pos), "duality_mismatch": int(mism)}
    print(out, flush=True)
    # (b)
    T3 = list(itertools.permutations(range(6), 3))
    tested = 0; pos = []; b1pos = 0
    for it in range(40000):
        dens = rng.choice([0.5, 0.65, 0.8, 0.9, 0.95])
        allowed = set(t for t in T3 if rng.random() < dens)
        m = triple_mask(allowed)
        if m == 0 or m == (1 << 720) - 1: continue
        b = hc.betti(m, 6); tested += 1; b1pos += b[1] > 0
        if b[2] > 0 and len(pos) < 5:
            pos.append({"beta": list(b), "N": m.bit_count(), "bad_triples": sorted(set(T3) - allowed)[:40], "n_bad": len(T3) - len(allowed), "mask_hex": hex(m)})
    out["triple_adjacency_random"] = {"tested": tested, "beta1_positive": int(b1pos), "beta2_positive_found": len(pos), "examples": pos}
    out["seconds"] = round(time.time() - t0)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "B21_locality_boundary.json"), "w"), indent=1)
    print({k: (v if k != "triple_adjacency_random" else {kk: vv for kk, vv in v.items() if kk != "examples"}) for k, v in out.items()})
