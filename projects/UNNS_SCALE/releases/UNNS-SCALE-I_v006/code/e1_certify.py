"""Merge E1 parts and re-certify every claimed lower bound d_A(n) >= d with the primality-audited complete-ball checker (audit_cert) + path edge check."""
import json, os, sys, time
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_cert import audit
from indep_check import check_path
res = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
E = {}
for f in ("E1_divisor_scales_part0.json", "E1_divisor_scales_part1.json", "E1_divisor_scales_part2.json"):
    E.update(json.load(open(os.path.join(res, f))))
tab = {}
for A in sorted(map(int, E)):
    e = E[str(A)]; row = {"A": A, "tested": e["tested"], "hist": e["hist"], "max_d_found": e["max_d"], "witness_n": e["witness_n"]}
    if e["max_d"] >= 5:
        p = e["witness_path"]; n = e["witness_n"]
        assert p[0] == A * n and p[-1] == A * (n + 1) and check_path(p) == e["max_d"]
        a = audit(A * n, A * (n + 1), e["max_d"]); row.update({"path": p, "audit": a, "certified": a["disjoint"] and a["factorisation_errors"] == 0 and a["primes_above_proof_bound"] == 0})
    tab[str(A)] = row; print(A, row["max_d_found"], row.get("certified"), flush=True)
json.dump({"scales": tab}, open(os.path.join(res, "E1_divisor_scales_certified.json"), "w"))
