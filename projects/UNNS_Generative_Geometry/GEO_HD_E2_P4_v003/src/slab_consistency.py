"""v002: slab sample search vs engine verdicts on all free-coordinate FIELD-I rows (a witness may exist only for NOT_CONTAINED rows)."""
import json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa: E402
sl = _boot.p4("slab_law")
F3 = json.load(open(os.path.join(ROOT, "results/P4_FIELDI3.json")))
tab = Counter(); bad = []
for r in F3["rows"]:
    if not any(p % r["b_next"] == 1 % r["b_next"] for p in r["primes"]):
        continue
    w = sl.slab_sample_witness(r["primes"], r["b"], r["b_next"], r["box"])
    tab[(r["verdict"], w is not None)] += 1
    if w is not None and r["verdict"] != "NOT_CONTAINED":
        bad.append({k: r[k] for k in ("primes", "b", "b_next", "box", "verdict")})
out = {"rows_free_coordinate": sum(tab.values()), "table": {"%s|slab_witness_found=%s" % k: v for k, v in sorted(tab.items())}, "contradictions": bad}
json.dump(out, open(os.path.join(ROOT, "results/P4_SLAB_CONSISTENCY.json"), "w"), indent=1)
print(out)
