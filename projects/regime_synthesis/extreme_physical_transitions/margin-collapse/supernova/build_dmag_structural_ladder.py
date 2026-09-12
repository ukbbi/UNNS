import pandas as pd
import numpy as np

INPUT_FILE = "processed_lightcurve.csv"

df = pd.read_csv(INPUT_FILE)
df.columns = [c.strip().lower() for c in df.columns]

if "mjd" not in df.columns or "value" not in df.columns:
    raise ValueError(f"Expected columns mjd,value. Found: {df.columns}")

df = df.sort_values("mjd").reset_index(drop=True)

# Raw magnitude sequence
t = df["mjd"].to_numpy()
mag = df["value"].to_numpy()

# First structural observable: absolute step-to-step magnitude change
dmag = np.abs(np.diff(mag))
t_dmag = t[1:]

# Second structural observable: curvature / acceleration of lightcurve
curv = np.abs(np.diff(mag, n=2))
t_curv = t[2:]

# Save pure STRUC_PERC ladders
pd.Series(dmag).to_csv("ladder_dmag.txt", index=False, header=False)
pd.Series(curv).to_csv("ladder_curvature.txt", index=False, header=False)

# Save diagnostic table
diag_dmag = pd.DataFrame({
    "mjd": t_dmag,
    "dmag": dmag
})
diag_curv = pd.DataFrame({
    "mjd": t_curv,
    "curvature": curv
})

diag_dmag.to_csv("dmag_diagnostics.csv", index=False)
diag_curv.to_csv("curvature_diagnostics.csv", index=False)

print("[OK] Saved ladder_dmag.txt")
print("[OK] Saved ladder_curvature.txt")
print("[OK] Saved dmag_diagnostics.csv")
print("[OK] Saved curvature_diagnostics.csv")

print("[INFO] dmag points:", len(dmag))
print("[INFO] curvature points:", len(curv))
print("[INFO] dmag range:", float(np.min(dmag)), "→", float(np.max(dmag)))
print("[INFO] curvature range:", float(np.min(curv)), "→", float(np.max(curv)))