#!/usr/bin/env python3
"""GEO-I v010 G10-K: the cut space of K_{2,t} is a minimal non-embedded box of nullity t+1 for every t >= 2 (proof in MATHEMATICS.md); exact check for t <= TMAX.
Writes output/data/v10_k2t.json"""
import os, sys, json, time
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'theory'))
import binary5 as B5, binary6 as B6

def run(tmax):
    rows = []
    for t in range(2, tmax + 1):
        t0 = time.time(); n = 2 * t; C = B6.cut_space_k2t(t)
        ne = B6.non_embedded(C); mn = B6.minimal_criterion(C, n); tb = B6.two_blocks(C, n)
        w = B6.rank3_witness(C, n)
        rows.append({'t': t, 'n': n, 'nullity': t + 1, 'words': len(C), 'non_embedded': ne, 'minimal': mn, 'two_blocks': len(tb), 'predicted_two_blocks': 2 ** (t - 1),
                     'witness_rank': w[0] if w else None, 'seconds': round(time.time() - t0, 2)})
        print(rows[-1], flush=True)
    return rows

if __name__ == '__main__':
    tmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rows = run(tmax); json.dump(rows, open(os.path.join(ROOT, 'output', 'data', 'v10_k2t.json'), 'w'), indent=1)
