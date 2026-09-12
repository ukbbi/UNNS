from obspy import read
import pandas as pd
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python sac_to_csv.py <file.sac>")
    sys.exit(1)

file = sys.argv[1]

if not os.path.exists(file):
    print("File not found:", file)
    sys.exit(1)

st = read(file)
tr = st[0]

time = tr.times()
amp = tr.data.astype(float)

df = pd.DataFrame({
    "time": time,
    "amplitude": amp
})

out = os.path.splitext(file)[0] + ".csv"
df.to_csv(out, index=False)

print("Saved:", out)