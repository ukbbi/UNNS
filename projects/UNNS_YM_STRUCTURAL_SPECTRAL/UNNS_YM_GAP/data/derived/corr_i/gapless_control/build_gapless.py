from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
M_MATCH = 0.3474
THETA = math.exp(M_MATCH) - 1.0

rows = [(t, 1.0/(1.0 + THETA*t)) for t in range(11)]

with (ROOT / "corr.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["t", "corr", "channel"])
    for t, c in rows:
        w.writerow([t, f"{c:.14g}", "gapless_exp_continuum_match"])

with (ROOT / "meff.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["t_mid_over_a", "aMeff", "channel", "construction"])
    for i in range(len(rows)-1):
        m = math.log(rows[i][1]/rows[i+1][1])
        w.writerow([f"{i+0.5:.1f}", f"{m:.14g}",
                    "gapless_exp_continuum_match",
                    "positive_gapless_exponential_spectral_density"])

print("Rebuilt gapless CORR-I control.")
