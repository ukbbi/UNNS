#!/usr/bin/env python3

"""
construct_real_5d_vectors.py

========================================================
REAL DOMAIN 5D VECTOR CONSTRUCTION
========================================================

CORRECTED VERSION

Uses STRUC-PERC-I outputs directly:

    struc_perc_batch_results.csv

NOT raw ladders.

========================================================
"""

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(".")
CLE_ROOT = ROOT / "CLE_PILOT_I"
OUTPUT_FILE = ROOT / "real_STRUC_5D_vectors.csv"

REAL_DOMAINS = [
    "helium",
    "cosmology",
    "neutrino",
    "protein",
]

def load_struc_results(csv_path):
    try:
        return pd.read_csv(csv_path)
    except Exception as e:
        print(f"[FAILED] {csv_path.name}: {e}")
        return None

def as_float(value, default=0.0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default

def construct_vector(row):
    row = row.to_dict()

    kappa = as_float(row.get("kappa_connect", 0.0))
    giant = as_float(row.get("giantRatio", row.get("GR", 0.0)))
    isolated = as_float(row.get("isolatedFraction", 0.0))
    tail = as_float(row.get("tailDominance", 0.0))

    return {
        "P_depth": kappa,
        "sigma2_GR": giant,
        "frag_rate": isolated,
        "adm_persist": 1.0 - isolated,
        "aniso_persist": tail,
    }

print("=" * 60)
print("REAL DOMAIN 5D VECTOR CONSTRUCTION")
print("=" * 60)

rows = []
total_success = 0
total_failed = 0

for domain in REAL_DOMAINS:
    print()
    print(f"[DOMAIN] {domain}")

    domain_root = CLE_ROOT / "canonical" / domain

    if not domain_root.exists():
        print(f"  -> missing: {domain_root}")
        continue

    result_files = sorted(
        domain_root.rglob("struc_perc_batch_results*.csv")
    )

    if not result_files:
        print("  -> no STRUC-PERC-I outputs found")
        continue

    success = 0
    failed = 0

    for csv_path in result_files:
        print(f"  -> reading: {csv_path}")

        df = load_struc_results(csv_path)

        if df is None:
            failed += 1
            continue

        for _, row in df.iterrows():
            try:
                vec = construct_vector(row)

                rows.append({
                    "name": row.get("name", row.get("filename", "unknown")),
                    "class": domain,
                    "verdict": row.get("verdict", "unknown"),
                    **vec,
                    "kappa_connect": row.get("kappa_connect", 0.0),
                    "giantRatio": row.get("giantRatio", 0.0),
                    "isolatedFraction": row.get("isolatedFraction", 0.0),
                    "tailDominance": row.get("tailDominance", 0.0),
                    "n": row.get("n", 0),
                    "runStatus": row.get("runStatus", "unknown"),
                    "source_csv": str(csv_path),
                })

                success += 1

            except Exception as e:
                print(f"[FAILED ROW] {e}")
                failed += 1

    total_success += success
    total_failed += failed

    print(f"  -> success : {success}")
    print(f"  -> failed  : {failed}")

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_FILE, index=False)

print()
print("=" * 60)
print("DONE")
print("=" * 60)
print(f"Real vectors : {len(df)}")
print(f"Failed rows  : {total_failed}")
print(f"Saved        : {OUTPUT_FILE}")