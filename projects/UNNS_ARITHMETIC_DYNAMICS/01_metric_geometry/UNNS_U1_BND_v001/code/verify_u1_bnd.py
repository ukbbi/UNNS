#!/usr/bin/env python3
"""
UNNS-U1-BND v001 deterministic verifier.

Exact integer / rational / symbolic arithmetic only. Seeds fixed. No timestamps in
the report, so repeated runs give byte-identical output.

STATUS OF WHAT THIS PROVES. The symbolic certificates (V2) are exact computer-algebra
statements: they establish the polynomial identities behind the upper bound. The
remaining checks are finite computations that support, but do not replace, the proofs
in the manuscript. Nothing here is proof-assistant certification.

Usage:
    python3 verify_u1_bnd.py --out ../reports/u1_bnd_verification_report.json \
                             --csv ../data/successor_distance_table.csv \
                             [--table-max 13500] [--replay-max 400000]
"""
import argparse
import hashlib
import json
import platform
import sys
from collections import Counter

import sympy as sp

import u1_bnd_lib as L

SEED = 20261108


class Check:
    def __init__(self, cid, claim, kind, supports):
        self.d = dict(id=cid, claim=claim, kind=kind, supports=supports,
                      cases=0, failures=0, notes=[])

    def case(self, ok, note=None):
        self.d["cases"] += 1
        if not ok:
            self.d["failures"] += 1
            if len(self.d["notes"]) < 5:
                self.d["notes"].append(note or "failure")

    def done(self, **extra):
        self.d["passed"] = self.d["failures"] == 0 and self.d["cases"] > 0
        self.d.update(extra)
        return self.d


def v1_edge_test():
    c = Check("V1", "Closed-form edge test equals the definition {x,y} = {kN, k(N+1)^2}",
              "exhaustive over 1 <= x, y <= 200", "edge criterion lemma")
    for x in range(1, 201):
        for y in range(1, 201):
            c.case(L.is_edge(x, y) == L.is_edge_bruteforce(x, y), f"x={x} y={y}")
    return c.done()


def v2_symbolic():
    c = Check("V2", "Exact symbolic certificates: each identity maps n = Mt + r to n + 1; every label "
              "and every cofactor is an integral, positive polynomial value for all integers t >= t0",
              "computer algebra (sympy, exact rationals)", "upper bound (symbolic certificates, Appendix A)")
    table = []
    for ident in L.IDENTITIES:
        cert = L.certify(ident)
        c.case(cert["ok"], f"{cert['name']}: {cert['notes']}")
        table.append(dict(name=cert["name"], modulus=cert["M"], residue=cert["r"],
                          t_min=cert["t0"], length=cert["length"], certified=cert["ok"]))
    return c.done(result=table)


def v3_coverage():
    c = Check("V3", "Every residue class of n modulo 24 is assigned an identity of length <= 6, "
              "and n = 1, 3 have explicit paths of length <= 5",
              "exhaustive over residues 0..23 (representatives n = r + 24*j, j = 1..3)", "coverage lemma")
    lengths = {}
    for r in range(24):
        ls = set()
        for j in (1, 2, 3):
            n = r + 24 * j
            ident, _ = L.identity_for(n)
            ls.add(len(ident["steps"]))
            c.case(n % ident["M"] == ident["r"] % ident["M"] and n >= ident["M"] * ident["t0"] + ident["r"],
                   f"n={n} class {ident['name']}")
        lengths[r] = sorted(ls)
        c.case(len(ls) == 1 and max(ls) <= 6, f"r={r}")
    c.case(len(L.SPECIAL[1]) - 1 == 5 and len(L.SPECIAL[3]) - 1 == 2)
    return c.done(result=dict(length_by_residue_mod_24={str(k): v[0] for k, v in lengths.items()}))


def v4_replay(limit):
    c = Check("V4", "Plain-integer replay of the identities: every step is a legal forward/inverse "
              "transition (admissibility checked, and consecutive states are adjacent by the closed-form "
              "edge test), and the walk ends at n + 1",
              f"exhaustive over 1 <= n <= {limit}", "upper bound (integer replay)")
    per, mx = Counter(), 0
    for n in range(1, limit + 1):
        try:
            st = L.replay(n)
            ok = st[-1] == n + 1 and all(L.is_edge(st[i], st[i + 1]) for i in range(len(st) - 1))
        except Exception as e:           # noqa
            ok = False
        c.case(ok, f"n={n}")
        if ok:
            ident = L.identity_for(n)
            per[ident[0]["name"] if ident else "special"] += 1
            mx = max(mx, len(st) - 1)
    return c.done(result=dict(max_length=mx, count_by_class=dict(sorted(per.items()))))


def v5_connectivity(limit):
    c = Check("V5", "Background: the constructive connectivity proof (path 1 -> 2, multiplicative "
              "compatibility, odd primes via p ~ (p+1)^2 = 4q^2) yields a valid path from 1 to n",
              f"exhaustive over 1 <= n <= {limit}", "context only (connectivity)")
    from math import isqrt
    memo = {1: [1], 2: [1, 4, 18, 81, 8, 2]}
    sc = lambda p, k: [k * x for x in p]

    def path_from_1(n):
        if n in memo:
            return memo[n]
        for a in range(2, isqrt(n) + 1):
            if n % a == 0:
                b = n // a
                path = path_from_1(b) + sc(path_from_1(a), b)[1:]
                memo[n] = path
                return path
        q = (n + 1) // 2
        pq = path_from_1(q)
        path = [1, 4] + sc(pq, 4)[1:] + sc(pq, 4 * q)[1:] + [n]
        memo[n] = path
        return path

    for n in range(1, limit + 1):
        p = path_from_1(n)
        c.case(p[0] == 1 and p[-1] == n and all(L.is_edge(p[i], p[i + 1]) for i in range(len(p) - 1)),
               f"n={n}")
    return c.done()


def v6_table(table_max, csv_path):
    c = Check("V6", "Exact successor distances d(n, n+1) (uncapped meet-in-the-middle search): all values "
              "lie in [2, 6] and do not exceed the length of the assigned identity",
              f"exhaustive over 1 <= n <= {table_max}", "upper bound consistency; exact distance table")
    rows, dist = [], Counter()
    for n in range(1, table_max + 1):
        d = L.distance(n, n + 1)
        ln = len(L.replay(n)) - 1
        c.case(d is not None and 2 <= d <= min(6, ln), f"n={n} d={d} len={ln}")
        rows.append((n, d))
        dist[d] += 1
    with open(csv_path, "w") as fh:
        fh.write("n,d_n_n_plus_1\n")
        for n, d in rows:
            fh.write(f"{n},{d}\n")
    six = [n for n, d in rows if d == 6]
    res = dict(range=[1, table_max],
               distribution={str(k): v for k, v in sorted(dist.items())},
               mean=str(sp.Rational(sum(d for _, d in rows), len(rows))),
               count_d6=len(six),
               d6_by_residue_mod_24={str(k): v for k, v in sorted(Counter(n % 24 for n in six).items())},
               first_d6=six[:12])
    return c.done(result=res), rows


def v7_independent(rows):
    c = Check("V7", "Independent engine (trial-division neighbours, no factoring library) reproduces the "
              "exact distances d(n, n+1)",
              "n = 1..60 and n in {163, 211}", "exact table, independent engine")
    tab = dict(rows)
    for n in list(range(1, 61)) + [163, 211]:
        c.case(L.distance(n, n + 1, nb=L.neighbours_simple) == tab[n], f"n={n}")
    return c.done()


def v8_lower_bound():
    c = Check("V8", "Lower-bound certificate for n = 163: no vertex lies within 3 of 163 and within 2 of 164, "
              "while the radius-(3,3) balls meet; both engines agree",
              "uncapped breadth-first balls, two engines", "sharpness at n = 163")
    out = {}
    for name, nb in (("fast", L.neighbours_fast), ("independent", L.neighbours_simple)):
        no = L.lower_bound_certificate(163, 164, 5, nb)       # radii (3, 2): d <= 5 impossible
        yes = L.lower_bound_certificate(163, 164, 6, nb)      # radii (3, 3): meets at total 6
        c.case(no["intersection"] == 0 and yes["intersection"] > 0, name)
        out[name] = dict(radii_3_2=no, radii_3_3=yes)
    c.case(out["fast"] == out["independent"], "engines disagree")
    return c.done(result=out)


def v9_trivial_lower():
    c = Check("V9", "d(n, n+1) >= 2 for every n, because (N+1)^2 / N >= 4 > (n+1)/n",
              "exhaustive over 1 <= n <= 5000, N <= 5000", "trivial lower bound lemma")
    from fractions import Fraction as F
    c.case(all(F((N + 1) ** 2, N) >= 4 for N in range(1, 5001)))
    c.case(all(F(n + 1, n) <= 2 for n in range(1, 5001)))
    return c.done()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="u1_bnd_verification_report.json")
    ap.add_argument("--csv", default="successor_distance_table.csv")
    ap.add_argument("--table-max", type=int, default=13500)
    ap.add_argument("--replay-max", type=int, default=400000)
    a = ap.parse_args()
    checks = [v1_edge_test(), v2_symbolic(), v3_coverage(), v4_replay(a.replay_max),
              v5_connectivity(1500)]
    c6, rows = v6_table(a.table_max, a.csv)
    checks += [c6, v7_independent(rows), v8_lower_bound(), v9_trivial_lower()]
    with open(__file__, "rb") as fh:
        sha = hashlib.sha256(fh.read()).hexdigest()
    with open(L.__file__, "rb") as fh:
        sha_lib = hashlib.sha256(fh.read()).hexdigest()
    rep = dict(
        package="UNNS_U1_BND_v001",
        status_note=("V2 is an exact computer-algebra verification; V1, V3-V9 are finite computations "
                     "supporting the manuscript's proofs. This is not proof-assistant certification."),
        arithmetic="exact integers, fractions and sympy rationals; no floating point",
        seed=SEED,
        verifier_sha256=sha, library_sha256=sha_lib,
        python=platform.python_version(), sympy=sp.__version__,
        checks=checks,
        total_cases=sum(c["cases"] for c in checks),
        total_failures=sum(c["failures"] for c in checks),
        all_passed=all(c["passed"] for c in checks),
    )
    with open(a.out, "w") as fh:
        json.dump(rep, fh, indent=2, sort_keys=True, default=str)
        fh.write("\n")
    for c in checks:
        print(f"{c['id']:3s} {'PASS' if c['passed'] else 'FAIL'}  cases={c['cases']:>9}  {c['supports']}")
    print("ALL PASSED" if rep["all_passed"] else "FAILURES PRESENT", "| total cases", rep["total_cases"])
    return 0 if rep["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
