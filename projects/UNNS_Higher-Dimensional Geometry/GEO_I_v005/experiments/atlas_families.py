"""G5-T3 / G5-T4: re-derive the proof ingredients for s = -1 and s = +1 (theory/symbolic_atlas.py) for d up to DMAX, plus the brute-force Obs for small d.
usage: atlas_families.py DMAX BRUTE_MAX OUT.json"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'theory'))
from symbolic_atlas import check_T3, check_T4

if __name__ == '__main__':
    dmax, bmax, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; rows = []
    for d in range(2, dmax + 1):
        t = time.time(); r3 = check_T3(d, brute=d <= bmax); r3.pop('witnesses'); rows.append({'theorem': 'G5-T3', **r3, 'seconds': round(time.time() - t, 1)})
    for d in range(3, dmax + 1):
        t = time.time(); r4 = check_T4(d, brute=d <= bmax); r4.pop('witnesses'); rows.append({'theorem': 'G5-T4', **r4, 'seconds': round(time.time() - t, 1)})
    json.dump(rows, open(out, 'w'), indent=1); print(sum(r['ok'] for r in rows), '/', len(rows))
