#!/usr/bin/env python3
"""GEO-I v011: write certificates/C9_partition.json (PARTITION, every minimal class of nullity 3..6 = 231) and C10_capcover.json (CAPCOVER, one-sided boxes d<=16)."""
import os, sys, json
from math import gcd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); sys.path.insert(0, os.path.join(ROOT, 'theory'))
import circuit_partitions as CP, cap_cells as K
D = os.path.join(ROOT, 'output', 'data'); certs = []
for k in (3, 4, 5, 6):
    for i, r in enumerate(json.load(open(os.path.join(D, 'v10_binary%d.json' % k)))['minimal']):
        certs.append(CP.two_block_certificate(r['support'], k, 'k%d_class%d' % (k, i)))
json.dump(certs, open(os.path.join(ROOT, 'certificates', 'C9_partition.json'), 'w'))
cc = []
for d in range(5, 17):
    for s in range(2, d - 1):
        if gcd(s, d) != 1: continue
        for u in range(1, d):
            cells, M, g = K.proof_cells_onesided(d, s, u)
            cc.append({'type': 'CAPCOVER', 'd': d, 's': s, 'u': u, 'cells': [[c[0][0], c[0][1], c[1][0], c[1][1], c[2][0], c[2][1]] for c in cells]})
json.dump(cc, open(os.path.join(ROOT, 'certificates', 'C10_capcover.json'), 'w'))
print(len(certs), 'PARTITION', len(cc), 'CAPCOVER')
