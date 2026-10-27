"""G5-C1 for s = +-1: machine check of the layer construction (theory/uniform_coverage.py) on every box Q in [d, QMAX]^2, Q != (d,d).
usage: layer_cover_check.py DMAX OUT.jsonl [extra]   (extra = additional margin beyond 3d+2 for the box range)"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'theory'))
from uniform_coverage import verify_box

if __name__ == '__main__':
    dmax, out = int(sys.argv[1]), sys.argv[2]
    with open(out, 'w') as f:
        for s in (-1, 1):
            for d in range(2, dmax + 1):
                t = time.time(); n = bad = 0; hi = 3 * d + 2
                for q1 in range(d, hi + 1):
                    for q2 in range(d, hi + 1):
                        if (q1, q2) == (d, d): continue
                        if s == 1 and q2 < q1: continue                      # s = +1 is symmetric under the coordinate swap
                        n += 1; r = verify_box(d, s, (q1, q2)); bad += (not r['ok'])
                f.write(json.dumps({'s': s, 'd': d, 'boxes': n, 'failures': bad, 'qmax': hi, 'seconds': round(time.time() - t, 1)}) + '\n'); f.flush()
