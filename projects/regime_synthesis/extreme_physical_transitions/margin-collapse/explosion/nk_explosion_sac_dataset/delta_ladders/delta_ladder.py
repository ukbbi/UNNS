import pandas as pd
import numpy as np
import os
import sys
import re
from glob import glob

# ============================================================
# WINDOWS LONG PATH FIX
# ============================================================

def win_safe(path):
    """
    Convert to Windows long-path-safe absolute path.
    """

    abs_path = os.path.abspath(path)

    # normalize slashes
    abs_path = os.path.normpath(abs_path)

    # add long path prefix only on Windows
    if os.name == "nt":

        if not abs_path.startswith("\\\\?\\"):

            abs_path = "\\\\?\\" + abs_path

    return abs_path


# ============================================================
# INPUT
# ============================================================

if len(sys.argv) < 2:

    print("\nUsage:")
    print("  python delta_ladder.py .")
    print("  python delta_ladder.py folder")
    print("  python delta_ladder.py file.csv")
    sys.exit()

target = sys.argv[1]

# ============================================================
# FIND CSV FILES
# ============================================================

if target == ".":

    csv_files = glob("*.csv")

elif os.path.isdir(target):

    csv_files = glob(os.path.join(target, "*.csv"))

elif os.path.isfile(target):

    csv_files = [target]

else:

    print(f"[ERROR] Invalid path: {target}")
    sys.exit()

if not csv_files:

    print("[ERROR] No CSV files found.")
    sys.exit()

print(f"\n[INFO] Found {len(csv_files)} CSV files\n")

# ============================================================
# OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR = "delta_outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

safe_output_dir = win_safe(OUTPUT_DIR)

print("[INFO] Output directory:")
print(safe_output_dir)
print()

# ============================================================
# PROCESS
# ============================================================

success = 0
failed = 0

for file in csv_files:

    try:

        print(f"[PROCESSING] {file}")

        # ====================================================
        # LOAD CSV
        # ====================================================

        df = pd.read_csv(file)

        if len(df.columns) < 2:
            raise Exception("CSV requires at least 2 columns")

        amp_col = df.columns[1]

        signal = pd.to_numeric(
            df[amp_col],
            errors="coerce"
        ).dropna().values

        if len(signal) < 10:
            raise Exception("Signal too short")

        # ====================================================
        # DELTA
        # ====================================================

        delta = np.abs(np.diff(signal))

        if len(delta) == 0:
            raise Exception("Empty delta")

        # ====================================================
        # FILTER
        # ====================================================

        threshold = np.percentile(delta, 5)

        delta = delta[delta > threshold]

        if len(delta) == 0:
            raise Exception("All values filtered")

        # ====================================================
        # SORT
        # ====================================================

        ladder = np.sort(delta)

        # ====================================================
        # SAFE NAME
        # ====================================================

        base = os.path.basename(file)

        base = os.path.splitext(base)[0]

        safe = re.sub(r'[^A-Za-z0-9]+', '_', base)

        safe = re.sub(r'_+', '_', safe)

        safe = safe.strip("_")

        # SHORTEN INSANELY LONG FILENAMES
        if len(safe) > 80:
            safe = safe[:80]

        output_name = safe + "_delta.txt"

        output_path = os.path.join(
            safe_output_dir,
            output_name
        )

        output_path = win_safe(output_path)

        # ====================================================
        # SAVE
        # ====================================================

        np.savetxt(output_path, ladder)

        print(f"[OK] {output_name}")
        print(f"[SIZE] {len(ladder)}\n")

        success += 1

    except Exception as e:

        print(f"[FAILED] {file}")
        print(f"Reason: {e}\n")

        failed += 1

# ============================================================
# SUMMARY
# ============================================================

print("===================================")
print("[DONE]")
print(f"[SUCCESS] {success}")
print(f"[FAILED ] {failed}")
print("===================================")