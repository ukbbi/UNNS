import pandas as pd
import numpy as np

# Load file
df = pd.read_csv("2e2mu_2012.csv")

# 🔹 Explicit energy columns (based on your file)
energy_cols = ["E1", "E2", "E3", "E4"]

# 🔹 Total energy per event
df["total_energy"] = df[energy_cols].sum(axis=1)

# 🔹 Use invariant mass (BEST signal)
if "M" in df.columns:
    df["signal"] = df["M"]
elif "mass" in df.columns:
    df["signal"] = df["mass"]
else:
    df["signal"] = df["total_energy"]

# 🔹 Build trajectory
df["t"] = np.arange(len(df))

# 🔹 Final dataset
unns = df[["t", "signal"]]

# Save
unns.to_csv("unns_collision_trajectory.csv", index=False)

print("✅ DONE")
print(unns.head())