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

    abs_path = os.path.normpath(abs_path)

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
    print("  python delta_ladder.py file.txt")
    sys.exit()

target = sys.argv[1]

# ============================================================
# FIND FILES
# ============================================================

files = []

if target == ".":

    files.extend(glob("*.csv"))
    files.extend(glob("*.txt"))

elif os.path.isdir(target):

    files.extend(glob(os.path.join(target, "*.csv")))
    files.extend(glob(os.path.join(target, "*.txt")))

elif os.path.isfile(target):

    files = [target]

else:

    print(f"[ERROR] Invalid path: {target}")
    sys.exit()

# REMOVE ALREADY GENERATED DELTAS

files = [

    f for f in files

    if not (
        f.endswith("_delta.txt")
        or "delta_outputs" in f
    )
]

if not files:

    print("[ERROR] No valid files found.")
    sys.exit()

print(f"\n[INFO] Found {len(files)} files\n")

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
# NORMALIZATION
# ============================================================

def normalize(x):

    x = np.asarray(x, dtype=float)

    x = x[np.isfinite(x)]

    if len(x) == 0:
        return x

    xmin = np.min(x)
    xmax = np.max(x)

    if xmax - xmin == 0:
        return x

    return (x - xmin) / (xmax - xmin)

# ============================================================
# TXT LOADER
# ============================================================

def load_txt_ladder(path):

    data = np.loadtxt(path)

    if data.ndim > 1:

        data = data.flatten()

    return data

# ============================================================
# CSV LOADER
# ============================================================

def load_csv_signal(path):

    df = pd.read_csv(path)

    if len(df.columns) < 2:
        raise Exception("CSV requires at least 2 columns")

    amp_col = df.columns[1]

    signal = pd.to_numeric(
        df[amp_col],
        errors="coerce"
    ).dropna().values

    return signal

# ============================================================
# PROCESS
# ============================================================

success = 0
failed = 0

for file in files:

    try:

        print(f"[PROCESSING] {file}")

        ext = os.path.splitext(file)[1].lower()

        # ====================================================
        # LOAD
        # ====================================================

        if ext == ".csv":

            signal = load_csv_signal(file)

        elif ext == ".txt":

            signal = load_txt_ladder(file)

        else:

            raise Exception("Unsupported file type")

        if len(signal) < 10:
            raise Exception("Signal too short")

        # ====================================================
        # CLEAN
        # ====================================================

        signal = np.asarray(signal, dtype=float)

        signal = signal[np.isfinite(signal)]

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
        # NORMALIZE
        # ====================================================

        delta = normalize(delta)

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