import pandas as pd
import numpy as np

# Load your collision data
df = pd.read_csv("unns_collision_trajectory.csv")

s = df["signal"]

# Normalize (keep this)
s_norm = (s - s.mean()) / s.std()

# -----------------------------
# 1. TRAJECTORY LADDER (RAW)
# -----------------------------
traj = pd.DataFrame({
    "signal": s_norm.values
})
traj.to_csv("ladder_trajectory.csv", index=False)

# -----------------------------
# 2. GAP LADDER (IMPORTANT)
# -----------------------------
gaps = np.abs(np.diff(s_norm.values))

gap_df = pd.DataFrame({
    "signal": gaps
})
gap_df.to_csv("ladder_gaps.csv", index=False)

# -----------------------------
# 3. PEAK LADDER
# -----------------------------
threshold = np.percentile(s_norm, 90)
peaks = s_norm[s_norm > threshold]

peak_df = pd.DataFrame({
    "signal": peaks.values
})
peak_df.to_csv("ladder_peaks.csv", index=False)

print("ALL 3 LADDERS GENERATED")