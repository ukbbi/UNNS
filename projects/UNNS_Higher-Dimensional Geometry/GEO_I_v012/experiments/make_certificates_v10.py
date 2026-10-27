#!/usr/bin/env python3
"""GEO-I v010: write certificates/C6_rank6.json (RANK6 certificates for all 215 minimal non-embedded classes of nullity 6) and C7_k2t.json (K_{2,t}, t = 2..8)."""
import os, sys, json
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'theory'))
import binary5 as B5, binary6 as B6, modular_sail as MS
from math import gcd

def cert(sig, k, claim):
    C = B5.code_masks(sig); n = len(sig); w = B6.rank3_witness(C, n)
    r, S, T, x = w
    return {'kind': 'RANK6', 'claim': claim, 'support': list(sig), 'nullity': k, 'witness': {'S': list(S), 'T': list(T), 'x': x}, 'min_rank': r, 'two_blocks': len(B6.two_blocks(C, n))}

def main():
    d = json.load(open(os.path.join(ROOT, 'output', 'data', 'v10_binary6.json')))
    c6 = [cert(m['support'], 6, 'minimal non-embedded reduced box of nullity 6 (affine class, support in the hyperplane u0.s=1); min witness rank 3') for m in d['minimal']]
    json.dump(c6, open(os.path.join(ROOT, 'certificates', 'C6_rank6.json'), 'w'))
    c7 = []
    for t in range(2, 9):
        n = 2 * t; k = t + 1; C = B6.cut_space_k2t(t)
        # reduced support of the cut space of K_{2,t}: coordinate (u,v) -> e_u + e_v in F_2^V / <1>; use basis x=bit0 dropped: vertices x,y,z_i -> coordinates (y,z_0..z_{t-1}) with x := 0
        pts = []
        for i in range(t):
            pts.append(1 << (1 + i))                     # edge x z_i  -> e_{z_i}      (x is the quotient point)
            pts.append(1 | (1 << (1 + i)))               # edge y z_i  -> e_y + e_{z_i}
        c7.append(cert(pts, k, 'cut space of K_{2,%d}: minimal non-embedded, nullity %d, min witness rank 3' % (t, k)))
    json.dump(c7, open(os.path.join(ROOT, 'certificates', 'C7_k2t.json'), 'w'))
    # BOUNDARY certificates: the zonogon cover (THEOREM G10-Z) for EVERY unit pair 5 <= d <= 40, 2 <= s <= d-2 (exact full check), plus a sample of larger pairs (cover-only check)
    cb = []
    for d in list(range(5, 41)) + [61, 100, 151, 199]:
        for s in range(2, d - 1):
            if gcd(d, s) != 1: continue
            if d > 40 and (s * 7 + d) % 11 != 0: continue
            cells = MS.general_cover(d, s)
            cb.append({'kind': 'BOUNDARY', 'claim': 'conv(F) \\ U0 = int T1 u int T2 for the hollow box (d,d), zonogon cover G10-Z', 'd': d, 's': s, 'cells': [[list(c[0]), list(c[1]), list(c[2])] for c in cells]})
    json.dump(cb, open(os.path.join(ROOT, 'certificates', 'C8_boundary.json'), 'w'))
    print(len(c6), len(c7), len(cb))

if __name__ == '__main__': main()
