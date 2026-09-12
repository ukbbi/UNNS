"""
canonicalize_adversarial_ladders.py

FULLY PATCHED VERSION
FINAL STABLE VERSION
"""

from pathlib import Path
import hashlib
import numpy as np
import pandas as pd

# ============================================================
# CONFIG
# ============================================================

ROOT = Path("CLE_PILOT_I")

RAW_ROOT = ROOT / "adversarial" / "raw"

CANONICAL_ROOT = RAW_ROOT / "canonical"

CLASSES = [
    "uniform",
    "pareto",
    "randomwalk",
    "shuffle",
]

# ============================================================
# UTILITIES
# ============================================================

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)


def canonicalize(values):

    values = np.array(values, dtype=float)

    values = np.sort(values)

    values = np.unique(values)

    if len(values) < 2:
        return np.array([])

    gaps = np.diff(values)

    return gaps


def build_output_name(class_name, stem):

    digest = hashlib.md5(
        stem.encode("utf-8")
    ).hexdigest()[:12]

    return f"{class_name}_{digest}_canonical.csv"


# ============================================================
# FILE PROCESSOR
# ============================================================

def process_file(class_name, csv_path, out_dir):

    try:

        df = pd.read_csv(csv_path)

        if "value" in df.columns:
            values = df["value"].values
        else:
            values = df.iloc[:, 0].values

        gaps = canonicalize(values)

        out_name = build_output_name(
            class_name,
            csv_path.stem
        )

        out_path = out_dir / out_name

        out_df = pd.DataFrame({
            "gap": gaps
        })

        out_df.to_csv(
            out_path,
            index=False
        )

        return {
            "source": str(csv_path),
            "canonical": str(out_path),
            "count": len(gaps),
            "status": "success"
        }

    except Exception as e:

        print(f"[FAILED] {csv_path.name}: {e}")

        return {
            "source": str(csv_path),
            "canonical": "",
            "count": 0,
            "status": f"failed: {e}"
        }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("======================================")
    print("ADVERSARIAL CANONICALIZATION")
    print("======================================")
    print()

    ensure_dir(CANONICAL_ROOT)

    manifest_rows = []

    total_success = 0
    total_failed = 0

    for class_name in CLASSES:

        in_dir = RAW_ROOT / class_name

        out_dir = CANONICAL_ROOT / class_name

        ensure_dir(out_dir)

        # ====================================================
        # IGNORE MANIFEST FILES
        # ====================================================

        files = [
            f for f in sorted(in_dir.glob("*.csv"))
            if "manifest" not in f.name.lower()
        ]

        print(f"[CLASS] {class_name} ({len(files)} files)")

        success = 0
        failed = 0

        for csv_path in files:

            result = process_file(
                class_name,
                csv_path,
                out_dir
            )

            manifest_rows.append(result)

            if result["status"] == "success":
                success += 1
            else:
                failed += 1

        total_success += success
        total_failed += failed

        print(f"  -> success : {success}")
        print(f"  -> failed  : {failed}")
        print()

    manifest_df = pd.DataFrame(manifest_rows)

    manifest_path = (
        CANONICAL_ROOT /
        "canonical_manifest.csv"
    )

    manifest_df.to_csv(
        manifest_path,
        index=False
    )

    print("======================================")
    print("DONE")
    print("======================================")
    print()

    print(f"Canonical files: {total_success}")
    print(f"Failed files   : {total_failed}")
    print(f"Output         : {CANONICAL_ROOT}")
    print(f"Manifest       : {manifest_path}")
    print()


if __name__ == "__main__":
    main()