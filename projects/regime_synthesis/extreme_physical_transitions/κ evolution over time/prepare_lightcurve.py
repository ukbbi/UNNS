import pandas as pd

# =========================
# LOAD
# =========================
det = pd.read_csv("detections.csv")
nondet = pd.read_csv("non_detections.csv")

print("[INFO] detections:", len(det))
print("[INFO] non-detections:", len(nondet))

print("[DEBUG] detection columns:", det.columns)

# =========================
# SELECT VALUE COLUMN (ROBUST)
# =========================
# Priority order for YOUR dataset
value_candidates = ["mag", "magcorr", "magap"]

value_col = None
for c in value_candidates:
    if c in det.columns:
        value_col = c
        break

if value_col is None:
    raise ValueError(f"No usable magnitude column found. Columns: {det.columns}")

print(f"[INFO] Using magnitude column: {value_col}")

# =========================
# DETECTIONS
# =========================
det = det[["mjd", value_col]].dropna()
det = det.rename(columns={value_col: "value"})

# =========================
# NON-DETECTIONS
# =========================
if "diffmaglim" not in nondet.columns:
    raise ValueError(f"diffmaglim not found. Columns: {nondet.columns}")

nondet = nondet[["mjd", "diffmaglim"]].dropna()
nondet = nondet.rename(columns={"diffmaglim": "value"})

# =========================
# MERGE
# =========================
df = pd.concat([det, nondet], ignore_index=True)
df = df.sort_values("mjd").reset_index(drop=True)

# =========================
# SAVE
# =========================
df.to_csv("processed_lightcurve.csv", index=False)

print("[OK] processed_lightcurve.csv created")
print(df.head())