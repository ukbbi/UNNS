from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
src = ROOT / "meff.csv"
dst = ROOT / "corr.csv"

rows = []
with src.open("r", encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f):
        rows.append((float(r["t_mid_over_a"]), float(r["aMeff"])))

rows.sort()
c = 1.0
out = [(0, c)]
for i, (_, m) in enumerate(rows, start=1):
    c *= math.exp(-m)
    out.append((i, c))

with dst.open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["t", "corr", "channel"])
    for t, value in out:
        w.writerow([t, f"{value:.14g}", "0pp_b650_fig7_proxy"])

print(f"Wrote {dst} with {len(out)} correlator points.")
