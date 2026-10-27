"""E3 validation: finite-template prediction vs. exhaustive v003 polyhedral audit (independent code paths).
usage: validate_templates.py K BMAX BOXMAX OUT [shard nshard]"""
import os, sys, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from obstruction_atlas import validate, residue_classes
from obstruction_templates import Lattice


def main(k, bmax, boxmax, out, sh=0, ns=1):
    n = 0
    with open(out, 'w') as f:
        for b, res in residue_classes(k, range(2, bmax + 1)):
            n += 1
            if n % ns != sh: continue
            lat = Lattice(res, b); o = lat.o
            rng = [range(1, min(2 * oi + 2, boxmax) + 1) for oi in o]
            boxes = list(itertools.product(*rng))
            t = time.time()
            nb, bad, nn, (ts, anti), mm = validate(res, b, boxes)
            f.write(json.dumps({'k': k, 'b': b, 'res': list(res), 'boxes': nb, 'mismatches': bad, 'non_embedded': nn,
                                'minimal_obstruction_boxes': [list(a) for a in anti], 'mismatch_boxes': [list(m) for m in mm[:5]],
                                't': round(time.time() - t, 1)}) + '\n'); f.flush()


if __name__ == '__main__':
    a = sys.argv
    main(int(a[1]), int(a[2]), int(a[3]), a[4], *(map(int, a[5:7]) if len(a) > 6 else (0, 1)))
