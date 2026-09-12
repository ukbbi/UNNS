# rigidity_phase_mapper.py
#
# CLE v2 — Rigidity Phase Mapper
#
# Purpose:
#   Map internal geometry of rigidity classes from metric outputs.
#
# Main use case:
#   Neutrino showed all families classified as RIGID_PLASTIC,
#   but with very different internal structure.
#
# This script extracts sub-phases:
#
#   - stable islands
#   - collapse basins
#   - bifurcation corridors
#   - recovery channels
#   - near-critical plastic zones
#
# Input:
#   CLE_OUTPUT/neutrino/neutrino_rigidity_metrics.json
#
# Output:
#   CLE_OUTPUT/neutrino/rigidity_phase_map.json
#   CLE_OUTPUT/neutrino/rigidity_phase_map.csv
#
# Usage:
#   python rigidity_phase_mapper.py

from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev


INPUT_PATH = Path("CLE_OUTPUT/neutrino/neutrino_rigidity_metrics.json")

OUT_DIR = Path("CLE_OUTPUT/neutrino")
OUT_DIR.mkdir(parents=True, exist_ok=True)

JSON_OUT = OUT_DIR / "rigidity_phase_map.json"
CSV_OUT = OUT_DIR / "rigidity_phase_map.csv"


def safe_mean(values):
    return mean(values) if values else 0.0


def safe_std(values):
    return pstdev(values) if len(values) > 1 else 0.0


def classify_phase(row):
    gr = float(row.get("mean_gr", 0.0))
    frag = float(row.get("fragmentation_rate", 1.0))
    persist = float(row.get("admissibility_persistence", 0.0))
    recover = float(row.get("recovery_elasticity", 1.0))
    bif = float(row.get("bifurcation_sharpness", 0.0))
    aniso = float(row.get("anisotropic_persistence", 0.0))
    full_vol = float(row.get("full_region_volume", 0.0))

    if frag == 0.0 and persist >= 0.75 and gr >= 0.75:
        return "STABLE_ISLAND"

    if frag >= 0.90 and full_vol == 0.0:
        return "COLLAPSE_BASIN"

    if 0.15 <= frag <= 0.85 and 0.40 <= gr <= 0.65:
        return "PLASTIC_CORRIDOR"

    if bif >= 0.006 and recover >= 0.22:
        return "BIFURCATION_RIDGE"

    if aniso >= 0.98 and recover <= 0.10:
        return "RECOVERY_CHANNEL"

    if frag > 0.0 and gr >= 0.50:
        return "MARGINAL_PERSISTENCE_ZONE"

    return "NEAR_CRITICAL_BACKGROUND"


def phase_score(row):
    gr = float(row.get("mean_gr", 0.0))
    frag = float(row.get("fragmentation_rate", 1.0))
    persist = float(row.get("admissibility_persistence", 0.0))
    recover = float(row.get("recovery_elasticity", 1.0))
    aniso = float(row.get("anisotropic_persistence", 0.0))

    return (
        0.35 * gr
        + 0.25 * persist
        + 0.20 * aniso
        + 0.10 * (1.0 - frag)
        + 0.10 * (1.0 - recover)
    )


def load_rows():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def map_rows(rows):
    mapped = []

    for row in rows:
        item = dict(row)

        phase = classify_phase(row)
        score = phase_score(row)

        item["rigidity_phase"] = phase
        item["phase_score"] = score

        mapped.append(item)

    return mapped


def summarize_by_phase(rows):
    grouped = {}

    for row in rows:
        phase = row["rigidity_phase"]
        grouped.setdefault(phase, []).append(row)

    summaries = []

    for phase, phase_rows in grouped.items():
        grs = [float(r.get("mean_gr", 0.0)) for r in phase_rows]
        frags = [float(r.get("fragmentation_rate", 1.0)) for r in phase_rows]
        persists = [float(r.get("admissibility_persistence", 0.0)) for r in phase_rows]
        recoveries = [float(r.get("recovery_elasticity", 1.0)) for r in phase_rows]
        anisos = [float(r.get("anisotropic_persistence", 0.0)) for r in phase_rows]

        summaries.append({
            "phase": phase,
            "n": len(phase_rows),
            "mean_gr": safe_mean(grs),
            "std_gr": safe_std(grs),
            "mean_fragmentation": safe_mean(frags),
            "mean_persistence": safe_mean(persists),
            "mean_recovery_elasticity": safe_mean(recoveries),
            "mean_anisotropic_persistence": safe_mean(anisos),
            "members": [
                r.get("source_file", "")
                for r in phase_rows
            ],
        })

    summaries.sort(
        key=lambda x: x["mean_gr"],
        reverse=True,
    )

    return summaries


def summarize_by_family(rows):
    grouped = {}

    for row in rows:
        fam = row.get("family", "misc")
        grouped.setdefault(fam, []).append(row)

    summaries = []

    for family, family_rows in grouped.items():
        phase_counts = {}

        for r in family_rows:
            p = r["rigidity_phase"]
            phase_counts[p] = phase_counts.get(p, 0) + 1

        summaries.append({
            "family": family,
            "n": len(family_rows),
            "phase_counts": phase_counts,
            "dominant_phase": max(
                phase_counts,
                key=phase_counts.get,
            ),
            "mean_phase_score": safe_mean([
                float(r["phase_score"])
                for r in family_rows
            ]),
        })

    summaries.sort(
        key=lambda x: x["mean_phase_score"],
        reverse=True,
    )

    return summaries


def export_json(mapped, phase_summary, family_summary):
    payload = {
        "source": str(INPUT_PATH),
        "mapped_entries": mapped,
        "phase_summary": phase_summary,
        "family_summary": family_summary,
    }

    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def export_csv(mapped):
    if not mapped:
        return

    keys = list(mapped[0].keys())

    with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=keys,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in mapped:
            writer.writerow(row)


def main():
    print()
    print("========================================")
    print("RIGIDITY PHASE MAPPER")
    print("========================================")
    print()

    rows = load_rows()
    mapped = map_rows(rows)

    phase_summary = summarize_by_phase(mapped)
    family_summary = summarize_by_family(mapped)

    print("Phase summary:")
    print()

    for phase in phase_summary:
        print(
            f"{phase['phase']:<30} | "
            f"n={phase['n']:<3} | "
            f"GR={phase['mean_gr']:.5f} | "
            f"frag={phase['mean_fragmentation']:.5f} | "
            f"persist={phase['mean_persistence']:.5f}"
        )

    print()
    print("Family summary:")
    print()

    for fam in family_summary:
        print(
            f"{fam['family']:<10} | "
            f"n={fam['n']:<3} | "
            f"dominant={fam['dominant_phase']:<28} | "
            f"score={fam['mean_phase_score']:.5f}"
        )

    export_json(mapped, phase_summary, family_summary)
    export_csv(mapped)

    print()
    print("Exports written:")
    print(JSON_OUT)
    print(CSV_OUT)
    print()
    print("Done.")
    print()


if __name__ == "__main__":
    main()