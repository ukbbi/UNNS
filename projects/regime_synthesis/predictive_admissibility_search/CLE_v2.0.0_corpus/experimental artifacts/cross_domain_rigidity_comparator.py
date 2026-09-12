# cross_domain_rigidity_comparator.py

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, pstdev


OUT_DIR = Path("CLE_OUTPUT/cross_domain")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "helium": [
        Path("CLE_OUTPUT/helium_refined/helium_refined_metrics.json"),
    ],
    "neutrino": [
        Path("CLE_OUTPUT/neutrino/neutrino_rigidity_metrics.json"),
    ],
    "cosmology": [
        Path("CLE_PILOT_I/cosmology/comparison/cosmology_family_summary.json"),
    ],
}

COMMON_KEYS = [
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


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_cosmology_row(row):
    adm = float(row.get("admissibility_fraction", 0.0))
    gr_max = float(row.get("gr_max", 1.0))
    gr_min = float(row.get("gr_min", 0.0))
    gr_std = float(row.get("gr_std", 0.0))

    return {
        "source_file": row.get("family", "cosmology"),
        "family": row.get("family", "cosmology"),
        "mean_gr": float(row.get("gr_mean", 0.0)),
        "gr_variance": gr_std,
        "full_region_volume": adm,
        "collapse_onset_radius": 1.0 if adm >= 0.95 else adm,
        "fragmentation_rate": 1.0 - adm,
        "admissibility_persistence": adm,
        "bifurcation_sharpness": gr_std,
        "recovery_elasticity": (gr_max - gr_min) / max(gr_max, 1e-9),
        "anisotropic_persistence": math.exp(-gr_std),
    }


def normalize_generic_row(row, domain):
    return {
        "source_file": row.get("source_file", row.get("encoding_id", domain)),
        "family": row.get("family", row.get("encoding_id", domain)),
        "mean_gr": float(row.get("mean_gr", row.get("GR", 0.0))),
        "gr_variance": float(row.get("gr_variance", row.get("gr_std", 0.0))),
        "full_region_volume": float(row.get("full_region_volume", 0.0)),
        "collapse_onset_radius": float(row.get("collapse_onset_radius", 0.0)),
        "fragmentation_rate": float(row.get("fragmentation_rate", 0.0)),
        "admissibility_persistence": float(row.get("admissibility_persistence", 0.0)),
        "bifurcation_sharpness": float(row.get("bifurcation_sharpness", 0.0)),
        "recovery_elasticity": float(row.get("recovery_elasticity", 0.0)),
        "anisotropic_persistence": float(row.get("anisotropic_persistence", 0.0)),
    }


def load_domain_rows(domain):
    rows = []

    for path in SOURCES[domain]:
        if not path.exists():
            print(f"[missing] {path}")
            continue

        data = load_json(path)

        if domain == "cosmology":
            if isinstance(data, dict) and "families" in data:
                data = data["families"]
            if isinstance(data, dict):
                data = [data]
            for row in data:
                rows.append(normalize_cosmology_row(row))
            continue

        if isinstance(data, dict) and "families" in data:
            data = data["families"]

        if isinstance(data, dict) and "mapped_entries" in data:
            data = data["mapped_entries"]

        if isinstance(data, dict):
            data = [data]

        for row in data:
            if isinstance(row, dict):
                rows.append(normalize_generic_row(row, domain))

    return rows


def classify_domain_signature(summary):
    gr = summary["mean_gr"]
    frag = summary["fragmentation_rate"]
    persist = summary["admissibility_persistence"]

    if gr >= 0.85 and frag <= 0.05 and persist >= 0.90:
        return "DEEP_PERSISTENCE_MANIFOLD"

    if gr >= 0.70 and frag <= 0.20:
        return "COHERENT_RIGID_MANIFOLD"

    if 0.45 <= gr < 0.70:
        return "PLASTIC_TRANSITION_MANIFOLD"

    if frag >= 0.80:
        return "COLLAPSE_DOMINATED_MANIFOLD"

    return "MIXED_RIGIDITY_MANIFOLD"


def summarize_domain(domain, rows):
    summary = {"domain": domain, "n": len(rows)}

    for key in COMMON_KEYS:
        values = [float(r.get(key, 0.0)) for r in rows]
        summary[key] = safe_mean(values)
        summary[key + "_std"] = safe_std(values)
        summary[key + "_min"] = min(values) if values else 0.0
        summary[key + "_max"] = max(values) if values else 0.0

    summary["rigidity_signature"] = classify_domain_signature(summary)
    return summary


def vector(summary):
    return [summary[k] for k in COMMON_KEYS]


def cosine_similarity(a, b):
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(y * y for y in b))
    return 0.0 if da == 0 or db == 0 else num / (da * db)


def build_similarity_matrix(summaries):
    matrix = {}

    for a in summaries:
        matrix[a["domain"]] = {}
        for b in summaries:
            matrix[a["domain"]][b["domain"]] = cosine_similarity(
                vector(a),
                vector(b),
            )

    return matrix


def export_json(payload):
    path = OUT_DIR / "cross_domain_rigidity_summary.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return path


def export_csv(rows):
    path = OUT_DIR / "cross_domain_rigidity_summary.csv"

    if rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    return path


def export_report(summaries, matrix):
    path = OUT_DIR / "cross_domain_rigidity_report.txt"

    lines = [
        "=" * 72,
        "CLE v2 CROSS-DOMAIN RIGIDITY COMPARISON",
        "=" * 72,
        "",
    ]

    for s in summaries:
        lines += [
            f"[{s['domain']}]",
            f"  n                         : {s['n']}",
            f"  mean GR                   : {s['mean_gr']:.6f}",
            f"  fragmentation             : {s['fragmentation_rate']:.6f}",
            f"  admissibility persistence : {s['admissibility_persistence']:.6f}",
            f"  recovery elasticity       : {s['recovery_elasticity']:.6f}",
            f"  anisotropic persistence   : {s['anisotropic_persistence']:.6f}",
            f"  signature                 : {s['rigidity_signature']}",
            "",
        ]

    lines += [
        "=" * 72,
        "DOMAIN SIMILARITY MATRIX",
        "=" * 72,
        "",
    ]

    for a, row in matrix.items():
        lines.append(a)
        for b, value in row.items():
            lines.append(f"    {b:<16} {value:.6f}")
        lines.append("")

    lines += [
        "=" * 72,
        "INTERPRETATION",
        "=" * 72,
        "",
        "This report uses refined helium metrics only.",
        "Old coarse helium pathology outputs are excluded.",
        "Similarity indicates shared rigidity geometry, not shared source physics.",
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path


def main():
    print()
    print("=" * 72)
    print("CLE v2 CROSS-DOMAIN RIGIDITY COMPARATOR")
    print("=" * 72)
    print()

    domain_rows = {}
    summaries = []

    for domain in SOURCES:
        rows = load_domain_rows(domain)
        domain_rows[domain] = rows

        print(f"{domain}: loaded {len(rows)} rows")

        if rows:
            summaries.append(summarize_domain(domain, rows))

    matrix = build_similarity_matrix(summaries)

    payload = {
        "domains": summaries,
        "similarity_matrix": matrix,
        "domain_rows": domain_rows,
    }

    print()
    print("Exports written:")
    print(export_json(payload))
    print(export_csv(summaries))
    print(export_report(summaries, matrix))
    print()
    print("Done.")


if __name__ == "__main__":
    main()