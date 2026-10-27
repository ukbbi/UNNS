"""Finite base-window certificate for the stabilization theorem (G4-C1 corrected).
For each pure lattice L(d,s) = {(i,j): j = s i mod d}, every box Q >= (d,d), Q != (d,d), with Q_i <= 3d-1 is tested for U = conv(F).
By the translation lemma (MATHEMATICS.md, Lemma S4) this settles ALL boxes Q >= (d,d) for that (d,s).
usage: stabilization_certificate.py DMIN DMAX OUT [shard nshard]"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'theory'))
from coverage import *
from math import gcd


def inv(s, d):
    for t in range(1, d + 1):
        if (s * t) % d == 1 % d: return t


def certify(d, s):
    L = Lat(d, d, d, s) if d > 1 else Lat(1, 1, 1, 1)
    bad = []; hollow = None; n = 0
    for q1 in range(d, 3 * d):
        for q2 in range(d, 3 * d):
            Q = (q1, q2)
            r = uncovered(L, Q)
            n += 1
            if Q == (d, d): hollow = (d > 1) == (len(r) > 0) if r is not None else None
            elif r: bad.append(Q)
    return {'d': d, 's': s, 'boxes': n, 'violations': bad, 'hollow_at_dd': hollow}


if __name__ == '__main__':
    dmin, dmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    sh, ns = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else (0, 1)
    with open(out, 'w') as f:
        k = 0
        for d in range(dmin, dmax + 1):
            for s in (range(1, d + 1) if d > 1 else [1]):
                if d > 1 and gcd(s, d) != 1: continue
                if d > 1 and inv(s, d) < s: continue          # (d,s) ~ (d,s^-1) by swapping the axes
                k += 1
                if k % ns != sh: continue
                t = time.time(); r = certify(d, s); r['t'] = round(time.time() - t, 1)
                f.write(json.dumps(r) + '\n'); f.flush()
