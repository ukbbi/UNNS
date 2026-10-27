"""G6-C1 / E1b: COMPLETE base-window certification beyond d=21.  By the v004 translation lemma S4 the base window [d,3d-1]^2 (minus (d,d)) decides
U=conv(F) for ALL boxes Q>=(d,d), Q!=(d,d).  For every unit class (d,s), s<=t=s^-1 (transposition symmetry; s=t: Q1<=Q2) every window box is certified:
  max(Q)>=2d : proof-cell cover (theory/modular_layers.py), else generic v005 fallback;   small boxes: theory/small_boxes.py (family test, generic fallback).
A box that cannot be certified is recorded 'unresolved' (never PASS).  usage: window_full.py DMIN DMAX OUT.jsonl SHARD NSHARD"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
import modular_layers as ML, small_boxes as SB, coverage as C
from lattice_model import Lat
inv = lambda s, d: next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def run(d, s):
    t0 = time.time(); sym = inv(s, d) == s; L = None
    row = {'d': d, 's': s, 't': inv(s, d), 'boxes': 0, 'via_proof_cells': 0, 'via_family': 0, 'via_generic': 0, 'unresolved': []}
    for q1 in range(d, 3 * d):
        for q2 in range(d, 3 * d):
            if (q1, q2) == (d, d) or (sym and q2 < q1): continue
            Q = (q1, q2); row['boxes'] += 1
            if max(Q) >= 2 * d:
                r = ML.verify_box(d, s, Q)
                if r['ok'] is True: row['via_proof_cells'] += 1; continue
            else:
                r = SB.certify_box(d, s, Q, fallback=False)
                if r['ok']: row['via_family'] += 1; continue
            L = L or Lat(d, d, d, s); u = C.uncovered(L, Q)
            if u is not None and len(u) == 0: row['via_generic'] += 1
            else: row['unresolved'].append(list(Q))
    row['seconds'] = round(time.time() - t0, 1)
    return row


if __name__ == '__main__':
    dmin, dmax, out, sh, ns = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    done = {(json.loads(l)['d'], json.loads(l)['s']) for l in open(out)} if os.path.exists(out) else set()
    k = 0
    with open(out, 'a') as f:
        for d in range(dmin, dmax + 1):
            for s in range(1, d):
                if gcd(s, d) != 1 or inv(s, d) < s: continue
                k += 1
                if k % ns != sh or (d, s) in done: continue
                f.write(json.dumps(run(d, s)) + '\n'); f.flush()
