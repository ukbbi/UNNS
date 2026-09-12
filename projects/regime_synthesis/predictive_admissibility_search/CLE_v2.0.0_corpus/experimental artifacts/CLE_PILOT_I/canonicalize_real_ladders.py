"""
canonicalize_real_ladders.py
────────────────────────────────────────────────────────────
MASTER REAL-DOMAIN CANONICALIZATION PIPELINE

Architecture
------------
CLE_PILOT_I/

    raw/
        helium/
        cosmology/
        neutrino/
        protein/

    canonical/
        helium/
        cosmology/
        neutrino/
        protein/

    adapters/
        helium_adapter.py
        cosmology_adapter.py
        neutrino_adapter.py
        protein_adapter.py

Meaning
-------
STRUC-PERC-I no longer analyzes arbitrary files.

It analyzes:

    canonicalized realizability trajectories.

This script orchestrates the full real-domain
canonicalization layer.

Responsibilities
----------------
1. Executes all domain adapters
2. Verifies canonical outputs
3. Builds corpus manifest
4. Produces unified canonical ladder corpus
5. Stabilizes downstream STRUC-PERC-I workflows

Outputs
-------
canonical/
    helium/
    cosmology/
    neutrino/
    protein/

    canonical_real_manifest.csv

Usage
-----
python canonicalize_real_ladders.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd


# ============================================================
# PATHS
# ============================================================

ROOT = Path(__file__).resolve().parent

ADAPTER_DIR = ROOT / "adapters"

CANONICAL_DIR = ROOT / "canonical"

MANIFEST_PATH = CANONICAL_DIR / "canonical_real_manifest.csv"


# ============================================================
# ADAPTER REGISTRY
# ============================================================

ADAPTERS = [
    {
        "domain": "helium",
        "script": ADAPTER_DIR / "helium_adapter.py",
        "output_dir": CANONICAL_DIR / "helium",
    },
    {
        "domain": "cosmology",
        "script": ADAPTER_DIR / "cosmology_adapter.py",
        "output_dir": CANONICAL_DIR / "cosmology",
    },
    {
        "domain": "neutrino",
        "script": ADAPTER_DIR / "neutrino_adapter.py",
        "output_dir": CANONICAL_DIR / "neutrino",
    },
    {
        "domain": "protein",
        "script": ADAPTER_DIR / "protein_adapter.py",
        "output_dir": CANONICAL_DIR / "protein",
    },
]


# ============================================================
# EXECUTION
# ============================================================

def run_adapter(entry: dict) -> bool:
    """
    Execute adapter script.
    """

    script = entry["script"]
    domain = entry["domain"]

    print("\n================================================")
    print(f"RUNNING ADAPTER: {domain}")
    print("================================================")

    if not script.exists():

        print(f"[FAIL] Missing adapter:")
        print(f"       {script}")

        return False

    try:

        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=False,
            check=True,
        )

        return result.returncode == 0

    except subprocess.CalledProcessError as e:

        print(f"[FAIL] Adapter crashed:")
        print(f"       {script.name}")

        return False


# ============================================================
# MANIFEST
# ============================================================

def build_manifest() -> pd.DataFrame:
    """
    Scan all canonical domains
    and construct unified corpus manifest.
    """

    rows = []

    for entry in ADAPTERS:

        domain = entry["domain"]
        out_dir = entry["output_dir"]

        if not out_dir.exists():

            print(f"[WARN] Missing canonical directory:")
            print(f"       {out_dir}")

            continue

        files = sorted(out_dir.glob("*_canonical.csv"))

        for path in files:

            try:

                df = pd.read_csv(path)

                rows.append({
                    "domain": domain,
                    "file": path.name,
                    "rows": len(df),
                    "columns": len(df.columns),
                    "path": str(path),
                })

            except Exception as e:

                print(f"[WARN] Failed manifest read:")
                print(f"       {path.name}")
                print(f"       {e}")

    manifest = pd.DataFrame(rows)

    return manifest


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print("================================================")
    print("REAL DOMAIN CANONICALIZATION")
    print("================================================")

    CANONICAL_DIR.mkdir(parents=True, exist_ok=True)

    adapter_success = 0
    adapter_failed = 0

    # --------------------------------------------------------
    # RUN ADAPTERS
    # --------------------------------------------------------

    for entry in ADAPTERS:

        ok = run_adapter(entry)

        if ok:
            adapter_success += 1
        else:
            adapter_failed += 1

    # --------------------------------------------------------
    # BUILD MANIFEST
    # --------------------------------------------------------

    print("\n================================================")
    print("BUILDING MANIFEST")
    print("================================================")

    manifest = build_manifest()

    manifest.to_csv(MANIFEST_PATH, index=False)

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    total_files = len(manifest)

    total_rows = 0

    if not manifest.empty:
        total_rows = manifest["rows"].sum()

    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    print("\n================================================")
    print("CANONICALIZATION COMPLETE")
    print("================================================")

    print(f"Adapters succeeded : {adapter_success}")
    print(f"Adapters failed    : {adapter_failed}")

    print(f"\nCanonical files    : {total_files}")
    print(f"Total ladder rows  : {total_rows}")

    print(f"\nManifest:")
    print(f"    {MANIFEST_PATH}")

    print("\nCanonical corpus:")
    print(f"    {CANONICAL_DIR}")

    print("================================================")


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()