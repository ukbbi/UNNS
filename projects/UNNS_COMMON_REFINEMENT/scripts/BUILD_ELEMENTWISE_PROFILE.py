#!/usr/bin/env python3
"""Build the exact rank-one elementwise primal/route-closure profile.

Input:
  02_NONREF/output/rank1_generator_scan.csv

Outputs:
  04_PROOF_MAP/output/RANK1_ELEMENTWISE_SUMMARY.csv
  04_PROOF_MAP/output/RANK1_ELEMENTWISE_PROFILE.csv
  outputs/records/RANK1_ELEMENTWISE_RESULT.json

Mathematical basis
------------------
Let H=<g1,...,gk> be a nonzero finitely generated additive submonoid of N0.
Normalize by gamma=gcd(H): S=H/gamma.  If S=N0, every element is primal.
Otherwise S is a numerical monoid with conductor c.

Two lemmas make the classification finite and exact.

(1) Gap-localization lemma.
If x+t=y+z is a non-refinable equality with distinguished corner x, then
|x-y| and |x-z| are gaps of S.  Indeed, if (say) y>=x and y-x is in S,
then x=x+0 gives an immediate refinement; if x>=y and x-y is in S,
then x=y+(x-y) gives one.  The same holds for z.  Hence any obstruction
must occur with y and z within the finite gap window around x.

(2) Cofinal primal-tail theorem.
Every x in S with x>=4c is primal.  If a non-refinable equality existed,
the gap-localization lemma forces y,z to lie within c of x.  If either is
>=x, splitting x=(x-c)+c refines the equality.  Otherwise write
y=x-r, z=x-s with 0<r,s<c.  Then t=x-r-s>=2c, and
  x=(y-c)+(r+c)
refines because y-c, r+c, c, and t-c all lie in S.

Therefore all non-primal elements lie below 4c.  The script checks every
S-element x<4c, and for each x checks exactly the finite gap-localized set
of possible y,z.  This is an exact classification, not a bounded heuristic.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
INFILE = ROOT / "02_NONREF" / "output" / "rank1_generator_scan.csv"
OUT_SUMMARY = ROOT / "04_PROOF_MAP" / "output" / "RANK1_ELEMENTWISE_SUMMARY.csv"
OUT_PROFILE = ROOT / "04_PROOF_MAP" / "output" / "RANK1_ELEMENTWISE_PROFILE.csv"
OUT_RESULT = ROOT / "outputs" / "records" / "RANK1_ELEMENTWISE_RESULT.json"

SUMMARY_FIELDS = [
    "generators",
    "n_generators",
    "gcd_scale",
    "global_refinement",
    "normalized_conductor",
    "guaranteed_primal_tail_from_normalized",
    "guaranteed_primal_tail_from_original",
    "exact_tail_onset_normalized",
    "exact_tail_onset_original",
    "last_nonprimal_normalized",
    "last_nonprimal_original",
    "nonprimal_core_count",
    "early_primal_count",
    "first_nonzero_primal_normalized",
    "first_nonzero_primal_original",
    "tail_onset_over_conductor",
    "early_primal_examples_normalized",
]

PROFILE_FIELDS = [
    "generators",
    "gcd_scale",
    "normalized_conductor",
    "element_normalized",
    "element_original",
    "primal",
    "route_closed_at_corner",
    "counter_y_original",
    "counter_z_original",
    "counter_residual_t_original",
]


def gcd_list(xs: list[int]) -> int:
    g = 0
    for x in xs:
        g = math.gcd(g, x)
    return g


def semigroup_members(gens: list[int], bound: int) -> list[bool]:
    present = [False] * (bound + 1)
    present[0] = True
    for n in range(bound + 1):
        if present[n]:
            for g in gens:
                if n + g <= bound:
                    present[n + g] = True
    return present


def conductor_primitive(gens: list[int]) -> int:
    if 1 in gens:
        return 0
    multiplicity = min(gens)
    bound = max(100, max(gens) * max(gens) + max(gens) + 50)
    while True:
        present = semigroup_members(gens, bound)
        run = 0
        for n, ok in enumerate(present):
            run = run + 1 if ok else 0
            # A run of multiplicity consecutive members proves that every
            # subsequent integer belongs to the numerical monoid.
            if run >= multiplicity:
                return n - multiplicity + 1
        bound *= 2


def exact_failure_profile(gens_original: list[int]) -> tuple[int, int, list[dict[str, object]]]:
    gamma = gcd_list(gens_original)
    gens = sorted(set(g // gamma for g in gens_original))
    c = conductor_primitive(gens)
    if c == 0:
        return gamma, c, []

    # Enough room for all x<4c and all gap-localized comparison corners.
    bound = 6 * c + 20
    present = semigroup_members(gens, bound)

    # D[y] = additive divisors u of y in S: u in S and y-u in S.
    divisors: list[set[int]] = []
    for y in range(bound):
        divisors.append({u for u in range(y + 1) if present[u] and present[y - u]})

    gaps = [g for g in range(1, c) if not present[g]]
    rows: list[dict[str, object]] = []

    for x in range(1, 4 * c):
        if not present[x]:
            continue

        # By the gap-localization lemma these are the only possible y or z
        # values in a non-refinable equality containing x.
        neighbors = sorted(
            {
                x + sign * gap
                for gap in gaps
                for sign in (-1, 1)
                if 0 <= x + sign * gap < bound and present[x + sign * gap]
            }
        )

        primal = True
        witness: tuple[int, int, int] | None = None

        for y in neighbors:
            dy = divisors[y]
            for z in neighbors:
                t = y + z - x
                if t < 0 or t >= bound or not present[t]:
                    continue

                # A corner refinement exists exactly when x=u+v with
                # u dividing y and v dividing z in the additive monoid.
                refinable = False
                for u in dy:
                    if 0 <= u <= x and present[x - u] and (x - u) in divisors[z]:
                        refinable = True
                        break

                if not refinable:
                    primal = False
                    witness = (y, z, t)
                    break
            if not primal:
                break

        rows.append({
            "element_normalized": x,
            "element_original": x * gamma,
            "primal": primal,
            "witness": witness,
        })

    return gamma, c, rows


def main() -> None:
    with INFILE.open(newline="", encoding="utf-8-sig") as f:
        source_rows = list(csv.DictReader(f))

    summary_rows: list[dict[str, object]] = []
    profile_rows: list[dict[str, object]] = []

    for r in source_rows:
        gens = [int(x) for x in r["generators"].split(";")]
        predicts_global = r["theorem_predicts_refinement"] == "1"
        gamma = gcd_list(gens)
        normalized = sorted(set(g // gamma for g in gens))

        if predicts_global:
            # Established rank-one theorem: H=gamma*N0, so every element is primal.
            if 1 not in normalized:
                raise AssertionError(f"Expected normalized generator 1 for {r['generators']}")
            summary_rows.append({
                "generators": r["generators"],
                "n_generators": r["n_generators"],
                "gcd_scale": gamma,
                "global_refinement": "YES",
                "normalized_conductor": 0,
                "guaranteed_primal_tail_from_normalized": 0,
                "guaranteed_primal_tail_from_original": 0,
                "exact_tail_onset_normalized": 0,
                "exact_tail_onset_original": 0,
                "last_nonprimal_normalized": "",
                "last_nonprimal_original": "",
                "nonprimal_core_count": 0,
                "early_primal_count": 0,
                "first_nonzero_primal_normalized": 1,
                "first_nonzero_primal_original": gamma,
                "tail_onset_over_conductor": "",
                "early_primal_examples_normalized": "",
            })
            continue

        gamma2, c, prof = exact_failure_profile(gens)
        if gamma2 != gamma:
            raise AssertionError("gcd normalization mismatch")

        nonprimal = [int(p["element_normalized"]) for p in prof if not bool(p["primal"])]
        primal = [int(p["element_normalized"]) for p in prof if bool(p["primal"])]
        if not nonprimal:
            raise AssertionError(f"Failure system unexpectedly has no non-primal core: {r['generators']}")

        last_np = max(nonprimal)
        tail_onset = last_np + 1
        early_primal = [x for x in primal if x < tail_onset]
        first_primal = min(primal) if primal else 4 * c

        summary_rows.append({
            "generators": r["generators"],
            "n_generators": r["n_generators"],
            "gcd_scale": gamma,
            "global_refinement": "NO",
            "normalized_conductor": c,
            "guaranteed_primal_tail_from_normalized": 4 * c,
            "guaranteed_primal_tail_from_original": 4 * c * gamma,
            "exact_tail_onset_normalized": tail_onset,
            "exact_tail_onset_original": tail_onset * gamma,
            "last_nonprimal_normalized": last_np,
            "last_nonprimal_original": last_np * gamma,
            "nonprimal_core_count": len(nonprimal),
            "early_primal_count": len(early_primal),
            "first_nonzero_primal_normalized": first_primal,
            "first_nonzero_primal_original": first_primal * gamma,
            "tail_onset_over_conductor": tail_onset / c,
            "early_primal_examples_normalized": ";".join(str(x) for x in early_primal[:12]),
        })

        for p in prof:
            witness = p["witness"]
            profile_rows.append({
                "generators": r["generators"],
                "gcd_scale": gamma,
                "normalized_conductor": c,
                "element_normalized": p["element_normalized"],
                "element_original": p["element_original"],
                "primal": "YES" if p["primal"] else "NO",
                "route_closed_at_corner": "YES" if p["primal"] else "NO",
                "counter_y_original": "" if witness is None else witness[0] * gamma,
                "counter_z_original": "" if witness is None else witness[1] * gamma,
                "counter_residual_t_original": "" if witness is None else witness[2] * gamma,
            })

    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with OUT_SUMMARY.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=SUMMARY_FIELDS)
        w.writeheader()
        w.writerows(summary_rows)

    with OUT_PROFILE.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=PROFILE_FIELDS)
        w.writeheader()
        w.writerows(profile_rows)

    failures = [r for r in summary_rows if r["global_refinement"] == "NO"]
    refinable = [r for r in summary_rows if r["global_refinement"] == "YES"]
    ratios = [float(r["tail_onset_over_conductor"]) for r in failures]

    result = {
        "source_system_count": len(summary_rows),
        "globally_refinable_system_count": len(refinable),
        "globally_nonrefinable_system_count": len(failures),
        "failure_systems_with_early_primal_elements": sum(int(r["early_primal_count"]) > 0 for r in failures),
        "failure_systems_with_early_primal_fraction": sum(int(r["early_primal_count"]) > 0 for r in failures) / len(failures),
        "median_nonprimal_core_count": median(int(r["nonprimal_core_count"]) for r in failures),
        "max_nonprimal_core_count": max(int(r["nonprimal_core_count"]) for r in failures),
        "tail_onset_over_conductor_min": min(ratios),
        "tail_onset_over_conductor_median": median(ratios),
        "tail_onset_over_conductor_max": max(ratios),
        "universal_proved_tail_bound": "x >= 4*c in the normalized numerical monoid",
        "classification_status": "EXACT",
        "exactness_basis": [
            "gap-localization lemma exhausts possible failure corners for each x",
            "cofinal primal-tail theorem excludes all non-primal x >= 4c",
        ],
    }
    OUT_RESULT.parent.mkdir(parents=True, exist_ok=True)
    OUT_RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    assert len(summary_rows) == 793
    assert len(refinable) == 280
    assert len(failures) == 513
    assert all(int(r["exact_tail_onset_normalized"]) <= int(r["guaranteed_primal_tail_from_normalized"]) for r in failures)

    print(f"Wrote {OUT_SUMMARY.relative_to(ROOT)}: {len(summary_rows)} systems")
    print(f"Wrote {OUT_PROFILE.relative_to(ROOT)}: {len(profile_rows)} exact element rows")
    print(f"Wrote {OUT_RESULT.relative_to(ROOT)}")
    print(f"Non-refinement systems with early primal elements: {result['failure_systems_with_early_primal_elements']}/{len(failures)}")
    print(f"Exact tail-onset/conductor range: {min(ratios):.3f} .. {max(ratios):.3f}")


if __name__ == "__main__":
    main()
