"""GEO-I v007 Programme C: certificate sweep  int T_i cap U = empty, boundary T_i subset U  (=> beta_1 >= 2) for all d in [DMIN,DMAX], all units s.
usage: hollow_attack.py DMIN DMAX OUT.json"""
import os, sys, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'theory'))
from math import gcd
import hollow_geometry as H
dmin, dmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
t0 = time.time(); n = 0; bad = []
for d in range(dmin, dmax + 1):
    for s in range(1, d):
        if gcd(s, d) != 1: continue
        n += 1
        if not H.check_hollow(d, s)['ok']: bad.append([d, s])
json.dump({'range': [dmin, dmax], 'pairs': n, 'failures': bad, 'seconds': round(time.time() - t0, 1)}, open(out, 'w'))
print(n, bad, round(time.time() - t0, 1))
