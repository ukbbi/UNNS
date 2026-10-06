from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
M = 0.3474
P_VALUES = [0.5, 2.0, 4.0, 8.0]

for p in P_VALUES:
    theta = math.exp(M/p) - 1.0
    tag = "p05" if p == 0.5 else f"p{int(p)}"
    rows = [(t, (1.0 + theta*t)**(-p)) for t in range(11)]
    with (ROOT / f"{tag}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["t", "corr", "channel"])
        for t, c in rows:
            w.writerow([t, f"{c:.14g}", f"gapless_gamma_{tag}_match"])
print("Rebuilt gapless family controls.")
