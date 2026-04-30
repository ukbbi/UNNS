#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd


# ----------------------------
# Helpers
# ----------------------------

def safe_read_csv(path):
    for enc in ["utf-8", "utf-8-sig", "latin1"]:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            pass
    return None


def normalize(df):
    df = df.copy()
    df.columns = [str(c).lower().strip() for c in df.columns]
    return df


def find_column(columns, keywords):
    for c in columns:
        for k in keywords:
            if k in c:
                return c
    return None


def select_energy_column(cols):
    """
    For Zeeman datasets, prefer the field-perturbed column (LevelB_cm1)
    over the zero-field column (Level0_cm1) so that each B group yields
    a distinct, physically meaningful ladder.
    Priority: levelb_cm1 > energy_cm-1 > generic energy/level fallback.
    """
    if "levelb_cm1" in cols:
        return "levelb_cm1"
    if "energy_cm-1" in cols:
        return "energy_cm-1"
    return find_column(cols, ["energy", "level"])


def power_law(values):
    if len(values) < 3:
        return None

    idx = np.arange(1, len(values) + 1)
    mask = (values > 0) & np.isfinite(values)

    if mask.sum() < 3:
        return None

    x = np.log(idx[mask])
    y = np.log(values[mask])

    slope, _ = np.polyfit(x, y, 1)
    return float(slope)


def compute_gaps(arr):
    arr = np.sort(arr)
    g = np.diff(arr)
    return g[(g > 0) & np.isfinite(g)]


def margin_proxy(gaps):
    if len(gaps) < 3:
        return None
    med = np.median(gaps)
    mad = np.median(np.abs(gaps - med))
    return med / (med + mad) if med > 0 else None


def dim_eff(gaps):
    if len(gaps) < 6:
        return 1

    X = np.array([[gaps[i], gaps[i+1], gaps[i+2]] for i in range(len(gaps) - 2)])
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-9)

    cov = np.cov(X, rowvar=False)
    eig = np.linalg.eigvalsh(cov)
    eig = np.sort(eig)[::-1]

    return int(np.sum(eig / eig.sum() > 0.1))


# ----------------------------
# Core
# ----------------------------

def analyze_file(path):
    df = safe_read_csv(path)
    if df is None:
        print(f"[WARN] Cannot read {path.name}")
        return []

    df = normalize(df)
    cols = df.columns

    # Zeeman
    if "b_t" in cols:
        energy_col = select_energy_column(cols)
        if energy_col is None:
            print(f"[WARN] No usable energy column in {path.name}")
            return []

        print(f"[INFO] Zeeman mode — using energy column: '{energy_col}'")

        results = []

        for val, grp in df.groupby("b_t"):
            e = pd.to_numeric(grp[energy_col], errors="coerce").dropna().values
            if len(e) < 3:
                continue

            g = compute_gaps(e)

            results.append({
                "file": path.name,
                "type": "zeeman",
                "B": val,
                "gamma": power_law(e),
                "alpha": power_law(g),
                "m": margin_proxy(g),
                "dim": dim_eff(g)
            })

        return results

    # Gap
    if any("gap" in c for c in cols):
        gap_col = find_column(cols, ["gap"])
        g = pd.to_numeric(df[gap_col], errors="coerce").dropna().values

        return [{
            "file": path.name,
            "type": "gap",
            "gamma": None,
            "alpha": power_law(g),
            "m": margin_proxy(g),
            "dim": dim_eff(g)
        }]

    # Spectrum
    energy_col = select_energy_column(cols)
    if energy_col:
        e = pd.to_numeric(df[energy_col], errors="coerce").dropna().values
        g = compute_gaps(e)

        return [{
            "file": path.name,
            "type": "spectrum",
            "gamma": power_law(e),
            "alpha": power_law(g),
            "m": margin_proxy(g),
            "dim": dim_eff(g)
        }]

    return []


# ----------------------------
# Main
# ----------------------------

def main():
    folder = Path(__file__).resolve().parent
    print(f"[INFO] Running in: {folder}")

    files = list(folder.glob("*.csv"))

    if not files:
        print("[ERROR] No CSV files found")
        return

    results = []

    for f in files:
        print(f"[INFO] Processing: {f.name}")
        results.extend(analyze_file(f))

    if not results:
        print("[ERROR] No usable data")
        return

    df = pd.DataFrame(results)

    output_dir = folder / "output"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = output_dir / f"results_{timestamp}.csv"

    df.to_csv(out_file, index=False)
    df.to_csv(output_dir / "latest.csv", index=False)

    print(f"[OK] Saved to: {out_file}")


if __name__ == "__main__":
    main()