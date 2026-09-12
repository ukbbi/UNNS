import pandas as pd
import numpy as np

df = pd.read_csv("unns_collision_trajectory.csv")

# Use raw signal
s = df["signal"]

# Normalize ONLY (keep structure!)
s_norm = (s - s.mean()) / s.std()

# Convert to structural ladder (CRITICAL STEP)
ladder = np.sort(s_norm.values)

# Output ONLY the ladder (no time index needed)
out = pd.DataFrame({"signal": ladder})

out.to_csv("collision_ladder_ranked.csv", index=False)

print("READY FOR STRUC_PERC (RANKED)")