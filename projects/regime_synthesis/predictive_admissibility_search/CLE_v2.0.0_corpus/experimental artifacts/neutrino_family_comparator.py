# neutrino_family_comparator.py
#
# CLE v2 — Neutrino Family Comparator
#
# Purpose:
#   Aggregate neutrino rigidity metrics by detected family and compare
#   second-order rigidity behavior across:
#
#       tmva
#       deepl
#       raw_sig
#       raw_bkg
#       fib
#       misc
#
# Input:
#   CLE_OUTPUT/neutrino/neutrino_rigidity_metrics.json
#
# Output:
#   CLE_OUTPUT/neutrino/neutrino_family_comparison.json
#   CLE_OUTPUT/neutrino/neutrino_family_comparison.csv
#
# Usage:
#   python neutrino_family_comparator.py

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev


INPUT_PATH = Path("CLE_OUTPUT/neutrino/neutrino_rigidity_metrics.json")

OUT_DIR = Path("CLE_OUTPUT/neutrino")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "neutrino_family_comparison.json"
CSV_OUT = OUT_DIR / "neutrino_family_comparison.csv"


METRIC_KEYS = [
    "mean_gr",
    "gr_variance",
    "full_region_volume",
    "collapse_onset_radius",
    "fragmentation_rate",
    "admissibility_persistence",
    "bifurcation_sharpness",
    "recovery_elasticity",
    "anisotropic_persistence",
]


def safe_mean(values):
    return mean(values) if values else 0.0


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def rigidity_class(avg_gr, frag, persistence):
    if avg_gr >= 0.80 and frag == 0 and persistence >= 0.75:
        return "RIGID_STABLE"
    if avg_gr >= 0.60 and frag <= 0.25:
        return "RIGID_ELASTIC"
    if avg_gr >= 0.45 and frag < 1.0:
        return "RIGID_PLASTIC"
    if frag >= 0.90:
        return "RIGID_BRITTLE"
    return "INDETERMINATE"


def load_metrics():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def group_by_family(rows):
    grouped = {}

    for row in rows:
        family = row.get("family", "misc")
        grouped.setdefault(family, []).append(row)

    return grouped


def summarize_family(family, rows):
    summary = {
        "family": family,
        "n": len(rows),
    }

    for key in METRIC_KEYS:
        vals = [
            float(r.get(key, 0.0))
            for r in rows
            if r.get(key) is not None
        ]

        summary[f"{key}_mean"] = safe_mean(vals)
        summary[f"{key}_std"] = safe_std(vals)
        summary[f"{key}_min"] = min(vals) if vals else 0.0
        summary[f"{key}_max"] = max(vals) if vals else 0.0

    summary["rigidity_class"] = rigidity_class(
        summary["mean_gr_mean"],
        summary["fragmentation_rate_mean"],
        summary["admissibility_persistence_mean"],
    )

    summary["stable_fraction"] = sum(
        1 for r in rows
        if float(r.get("fragmentation_rate", 1.0)) == 0.0
        and float(r.get("admissibility_persistence", 0.0)) >= 0.75
    ) / len(rows)

    summary["collapse_fraction"] = sum(
        1 for r in rows
        if float(r.get("fragmentation_rate", 0.0)) >= 0.90
    ) / len(rows)

    summary["transitional_fraction"] = sum(
        1 for r in rows
        if 0.0 < float(r.get("fragmentation_rate", 0.0)) < 0.90
    ) / len(rows)

    return summary


def rank_families(summaries):
    return sorted(
        summaries,
        key=lambda s: (
            s["mean_gr_mean"],
            -s["fragmentation_rate_mean"],
            s["admissibility_persistence_mean"],
            s["anisotropic_persistence_mean"],
        ),
        reverse=True,
    )


def export_json(payload):
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def export_csv(rows):
    if not rows:
        return

    fieldnames = list(rows[0].keys())

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def main():
    print()
    print("========================================")
    print("NEUTRINO FAMILY COMPARATOR")
    print("========================================")
    print()

    rows = load_metrics()
    grouped = group_by_family(rows)

    summaries = []

    for family, family_rows in grouped.items():
        summary = summarize_family(family, family_rows)
        summaries.append(summary)

    ranked = rank_families(summaries)

    print("Family rigidity ranking:")
    print()

    for i, item in enumerate(ranked, start=1):
        print(
            f"{i:02d} | "
            f"{item['family']:<10} | "
            f"class={item['rigidity_class']:<16} | "
            f"n={item['n']:<3} | "
            f"GR={item['mean_gr_mean']:.5f} | "
            f"frag={item['fragmentation_rate_mean']:.5f} | "
            f"stable={item['stable_fraction']:.5f} | "
            f"collapse={item['collapse_fraction']:.5f}"
        )

    payload = {
        "source": str(INPUT_PATH),
        "families": ranked,
    }

    export_json(payload)
    export_csv(ranked)

    print()
    print("Exports written:")
    print(JSON_OUT)
    print(CSV_OUT)
    print()
    print("Done.")
    print()


if __name__ == "__main__":
    main()