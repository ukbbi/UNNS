#!/usr/bin/env python3
"""Build exact non-primality certificates from project D_R=1 equalities.

Mathematical basis (commutative cancellative monoid): if an endpoint equality
has no 2x2 refinement, then every one of its four corner positions is non-primal.
Conversely, a non-primality witness x | yz gives a non-refinable equality xd=yz.

This script does not infer primality numerically.  It records the exact logical
certificate carried by already-established no-refinement rows.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RANK1 = ROOT / "02_NONREF" / "output" / "canonical_counterexamples.csv"
AFFINE = ROOT / "02_NONREF" / "output" / "affine_examples.csv"
OUT = ROOT / "04_PROOF_MAP" / "output" / "FAILURE_CERTIFICATES.csv"

FIELDS = [
    "certificate_id",
    "domain",
    "system",
    "endpoint_equality",
    "corner_a",
    "corner_b",
    "corner_c",
    "corner_d",
    "distinct_corner_elements",
    "all_four_positions_nonprimal",
    "no_refinement",
    "certificate_rule",
    "source_file",
]

RULE = (
    "In a commutative cancellative monoid, if any corner of a+b=c+d were primal, "
    "its primal split across the opposite two corners plus cancellation would build "
    "a 2x2 refinement; therefore a no-refinement equality certifies every corner position non-primal."
)


def distinct_join(items: list[str]) -> str:
    seen: list[str] = []
    for x in items:
        if x not in seen:
            seen.append(x)
    return ";".join(seen)


def parse_affine_corners(eq: str) -> list[str]:
    # Project equalities use tuple coordinates, e.g.
    # (2,0)+(0,2)=(1,1)+(1,1) or the analogous 3D form.
    return re.findall(r"\([^()]+\)", eq)


def build() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    cid = 1

    with RANK1.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["valid_witness_count"] != "0":
                continue
            corners = [r["a"], r["b"], r["c"], r["d"]]
            eq = f"{r['a']}+{r['b']}={r['c']}+{r['d']}"
            rows.append({
                "certificate_id": f"R1_{cid:04d}",
                "domain": "rank_one_additive",
                "system": f"H=<{r['generators']}>",
                "endpoint_equality": eq,
                "corner_a": corners[0],
                "corner_b": corners[1],
                "corner_c": corners[2],
                "corner_d": corners[3],
                "distinct_corner_elements": distinct_join(corners),
                "all_four_positions_nonprimal": "YES",
                "no_refinement": "YES",
                "certificate_rule": RULE,
                "source_file": "02_NONREF/output/canonical_counterexamples.csv",
            })
            cid += 1

    aid = 1
    with AFFINE.open(newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["global_refinement"] != "NO":
                continue
            eq = r["explicit_D_R_1_equality"].strip()
            if not eq:
                raise ValueError(f"Affine failure {r['system']} has no explicit D_R=1 equality")
            corners = parse_affine_corners(eq)
            if len(corners) != 4:
                raise ValueError(f"Could not parse four corners from {r['system']}: {eq}")
            rows.append({
                "certificate_id": f"AF_{aid:03d}",
                "domain": "positive_affine_additive",
                "system": r["system"],
                "endpoint_equality": eq,
                "corner_a": corners[0],
                "corner_b": corners[1],
                "corner_c": corners[2],
                "corner_d": corners[3],
                "distinct_corner_elements": distinct_join(corners),
                "all_four_positions_nonprimal": "YES",
                "no_refinement": "YES",
                "certificate_rule": RULE,
                "source_file": "02_NONREF/output/affine_examples.csv",
            })
            aid += 1

    return rows


def main() -> None:
    rows = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    rank1_n = sum(r["domain"] == "rank_one_additive" for r in rows)
    affine_n = sum(r["domain"] == "positive_affine_additive" for r in rows)
    assert rank1_n == 513, rank1_n
    assert affine_n == 4, affine_n
    assert all(r["all_four_positions_nonprimal"] == "YES" for r in rows)
    assert all(r["no_refinement"] == "YES" for r in rows)
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} certificates ({rank1_n} rank-one, {affine_n} affine).")


if __name__ == "__main__":
    main()
