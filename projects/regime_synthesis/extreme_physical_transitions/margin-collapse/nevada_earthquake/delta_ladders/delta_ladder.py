import pandas as pd
import numpy as np
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python delta_ladder.py input.csv")
    exit()

file = sys.argv[1]

df = pd.read_csv(file)

# auto-detect columns
time_col = df.columns[0]
amp_col = df.columns[1]

t = df[time_col].values
a = df[amp_col].values

# ΔA construction
delta = np.abs(np.diff(a))

# remove noise floor (optional but recommended)
delta = delta[delta > np.percentile(delta, 5)]

# sort → ladder
ladder = np.sort(delta)

# build output filename
base = os.path.splitext(os.path.basename(file))[0]
out_name = f"{base}_delta.txt"

# save
np.savetxt(out_name, ladder)

print(f"[OK] Ladder saved: {out_name}")
print(f"[INFO] size: {len(ladder)}")
print(f"[INFO] range: {ladder.min()} → {ladder.max()}")