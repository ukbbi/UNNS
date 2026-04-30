import pandas as pd
import numpy as np
from pathlib import Path

# --- ROOT (script location, NOT working dir) ---
BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "cosmo_ladders"
OUTPUT_DIR = BASE_DIR / "generated_transition_data"
OUTPUT_DIR.mkdir(exist_ok=True)

# --- deformation axis ---
B_VALUES = np.linspace(0.0, 1.0, 100)


# =========================
# ROBUST LOADER (FIXED)
# =========================
def load_ladder(file_path):
    try:
        df = pd.read_csv(file_path)

        # Try every column → find numeric one
        for col in df.columns:
            values = pd.to_numeric(df[col], errors='coerce').dropna()

            if len(values) > 10:
                return np.sort(values.values)

        print(f"[ERROR] No usable numeric column in {file_path.name}")
        return None

    except Exception as e:
        print(f"[ERROR] Failed to read {file_path.name}: {e}")
        return None


# =========================
# STRUCTURE OPERATORS
# =========================
def apply_deformation(values, B):
    return values * (1 + B)


def compute_gaps(values):
    return np.diff(values)


def compute_margin(gaps):
    if len(gaps) < 3:
        return None

    med = np.median(gaps)
    mad = np.median(np.abs(gaps - med))

    if med + mad == 0:
        return None

    return med / (med + mad)


def compute_alpha(gaps):
    if len(gaps) < 5:
        return None

    x = np.arange(1, len(gaps) + 1)
    y = np.log(np.abs(gaps) + 1e-12)

    try:
        return np.polyfit(np.log(x), y, 1)[0]
    except:
        return None


def compute_dim(gaps):
    if len(gaps) < 3:
        return None

    var = np.var(gaps)

    if var < 1e-10:
        return 3
    elif var < 1e-5:
        return 2
    else:
        return 1


# =========================
# PROCESSING
# =========================
def process_file(file_path):
    values = load_ladder(file_path)

    if values is None:
        print(f"[SKIP] {file_path.name}")
        return

    rows = []

    for B in B_VALUES:
        deformed = apply_deformation(values, B)
        gaps = compute_gaps(deformed)

        rows.append({
            "file": file_path.name,
            "B": B,
            "alpha": compute_alpha(gaps),
            "m": compute_margin(gaps),
            "dim": compute_dim(gaps)
        })

    out_name = file_path.stem + "_transition.csv"
    out_path = OUTPUT_DIR / out_name

    pd.DataFrame(rows).to_csv(out_path, index=False)

    print(f"[OK] {file_path.name} → {out_name}")


# =========================
# MAIN
# =========================
def main():
    if not INPUT_DIR.exists():
        print(f"[FATAL] Missing folder: {INPUT_DIR}")
        return

    files = list(INPUT_DIR.glob("*.csv"))

    if not files:
        print("[FATAL] No CSV files found")
        return

    for f in files:
        process_file(f)


if __name__ == "__main__":
    main()