#!/usr/bin/env python3
"""GEO-I v010 Programme C (adversarial, different family): cut spaces of random connected graphs.  For each graph with 1 in its cut space (bipartite) or not, shorten greedily
(edge contraction) to a minimal non-embedded box and test W2 (a double two-circuit decomposition => rank-3 collision, theory/binary6.py rank3_witness).
python3 experiments/graphic_attack.py NVERT NSAMPLES SEED   -> output/data/v10_graphic_attack.json (one record per call appended)"""
import os, sys, json, random, itertools
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'theory'))
import binary5 as B5, binary6 as B6

def cut_space(nv, edges):
    ws = set()
    for U in range(1 << (nv - 1)):
        m = 0
        for i, (u, v) in enumerate(edges):
            if ((U >> u) & 1) ^ ((U >> v) & 1): m |= 1 << i
        ws.add(m)
    return sorted(ws)

def shorten_to_minimal(C, n):
    """repeat: delete a coordinate (shortening) keeping non-embeddedness.  Returns the minimal code, its length, and the number of deletions.  Coordinates with all-zero column are dropped."""
    cur, ln = C, n
    while True:
        for i in range(ln):
            D = B5.delete(cur, i)
            if len(D) < len(cur) and B6.non_embedded(D): cur = D; break
        else: return cur, ln
        # drop coordinate i physically is unnecessary: B5.delete keeps length semantics (coordinate becomes identically zero); count live coordinates below
        # keep ln unchanged; liveness measured by the support union
def live(C):
    u = 0
    for c in C: u |= c
    return bin(u).count('1')

def run(nv, nsamples, seed):
    rng = random.Random(seed); rec = {'nv': nv, 'samples': 0, 'nonembedded': 0, 'minimal_checked': 0, 'with_W2': 0, 'without_W2': [], 'ranks': {}, 'nullities': {}}
    for _ in range(nsamples):
        p = rng.choice((0.35, 0.5, 0.7))
        edges = [(u, v) for u, v in itertools.combinations(range(nv), 2) if rng.random() < p]
        if len(edges) < nv or len(edges) > 18: continue
        C = cut_space(nv, edges); n = len(edges); rec['samples'] += 1
        if not B6.non_embedded(C): continue
        rec['nonembedded'] += 1
        M, ln = shorten_to_minimal(C, n)
        liveidx = [i for i in range(ln) if any((c >> i) & 1 for c in M)]
        if not all(not B6.non_embedded(B5.delete(M, i)) for i in liveidx): continue
        rec['minimal_checked'] += 1; k = len(M).bit_length() - 1
        rec['nullities'][str(k)] = rec['nullities'].get(str(k), 0) + 1
        w = B6.rank3_witness(M, ln)
        if w is None: rec['without_W2'].append({'edges': edges, 'code_size': len(M)})
        else: rec['with_W2'] += 1; rec['ranks'][str(w[0])] = rec['ranks'].get(str(w[0]), 0) + 1
    return rec

if __name__ == '__main__':
    nv, ns, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    r = run(nv, ns, seed); print(json.dumps(r)[:600])
    p = os.path.join(ROOT, 'output', 'data', 'v10_graphic_attack.json'); old = json.load(open(p)) if os.path.exists(p) else []
    old.append(r); json.dump(old, open(p, 'w'), indent=1)
