import pandas as pd

# === LOAD ===
df = pd.read_csv("detections.csv")

print("Columns:", df.columns)
print("Rows:", len(df))

# === AUTO-DETECT MAG COLUMN ===
possible_cols = ["mag", "magnitude", "diffmag", "psfMag", "magpsf"]

mag_col = None
for c in possible_cols:
    if c in df.columns:
        mag_col = c
        break

if mag_col is None:
    raise ValueError("No magnitude column found!")

print("Using column:", mag_col)

# === CLEAN ===
df = df[[mag_col]].copy()
df[mag_col] = pd.to_numeric(df[mag_col], errors="coerce")
df = df.dropna()

if len(df) < 5:
    raise ValueError("Too few valid data points!")

# === SORT (CRITICAL for ladders) ===
if "mjd" in df.columns:
    df = df.sort_values("mjd")

# === BUILD LADDERS ===
mass = df[mag_col]

energy = 10 ** (-0.4 * mass)

pt = energy.diff().fillna(0)

# === SAVE CLEAN LADDERS ===
mass.to_csv("ladder_mass.txt", index=False, header=False)
energy.to_csv("ladder_energy.txt", index=False, header=False)
pt.to_csv("ladder_pt.txt", index=False, header=False)

print("Saved:")
print(" - ladder_mass.txt")
print(" - ladder_energy.txt")
print(" - ladder_pt.txt")