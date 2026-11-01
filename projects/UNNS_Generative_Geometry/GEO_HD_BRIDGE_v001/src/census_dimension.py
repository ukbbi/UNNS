"""Resource-box census of route-complex features and their prime support.
usage: python census_dimension.py K LO HI TIME_LIMIT_S OUT.json [must_include_label]"""
import sys, json, time
from itertools import combinations
from collections import Counter
from dimension_tests import Content, kind


def run(k, lo, hi, T, must=None, cap=500):
    t0 = time.time(); hist = Counter(); ex = {}; n = 0; skipped = 0; last = None; complete = True
    pool = [x for x in range(lo, hi + 1) if x != must]
    for rest in combinations(pool, k - (1 if must else 0)):
        C = tuple(sorted(((must,) if must else ()) + rest))
        c = Content(C)
        if c.box_size() > cap: skipped += 1; continue
        n += 1
        for e, b, sup, ess, cut in c.features():
            key = (kind(b), len(sup), len(ess), cut)
            hist[key] += 1
            if key not in ex: ex[key] = {"content": list(C), "active": c.act, "source_valuations": dict(zip(c.act, e)), "betti": list(b), "support": sup, "essential": ess, "cut": cut}
        last = C
        if time.time() - t0 > T: complete = False; break
    return {"k": k, "label_range": [lo, hi], "must_include": must, "contents_run": n, "skipped_box_gt_cap": skipped, "box_cap": cap,
            "complete": complete, "last_content": list(last) if last else None, "seconds": round(time.time() - t0),
            "histogram": [{"kind": a, "support": b_, "essential": c_, "cut_order": d_, "count": v} for (a, b_, c_, d_), v in sorted(hist.items())],
            "examples": [{"key": list(k_), **v} for k_, v in sorted(ex.items())]}


if __name__ == "__main__":
    k, lo, hi, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]); out = sys.argv[5]
    must = int(sys.argv[6]) if len(sys.argv) > 6 else None
    r = run(k, lo, hi, T, must); json.dump(r, open(out, "w"), indent=1); print("done", r["contents_run"], r["complete"], r["seconds"])
