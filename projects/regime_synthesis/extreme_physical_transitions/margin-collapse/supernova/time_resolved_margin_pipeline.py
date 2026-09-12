import pandas as pd

df = pd.read_csv("processed_lightcurve.csv")

# sort by time
df = df.sort_values("mjd")

# raw observable (no smoothing!)
L = df["value"].values

pd.Series(L).to_csv("ladder_raw.txt", index=False, header=False)

print("READY: ladder_raw.txt")