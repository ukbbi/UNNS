from pathlib import Path
import csv, math

ROOT = Path(__file__).resolve().parent
M = 0.3474
DM = 0.0022
T = list(range(0, 11))

with (ROOT / "corr.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["t", "corr", "channel"])
    for t in T:
        w.writerow([t, f"{math.exp(-M*t):.14g}", "0pp_b650_plateau_control"])

with (ROOT / "meff.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["t_mid_over_a", "aMeff", "channel", "beta", "lattice", "construction"])
    for t in range(10):
        w.writerow([f"{t+0.5:.1f}", f"{M:.4f}", "0pp_ground", "6.50", "38^4",
                    "published_mass_plateau_control"])

with (ROOT / "mass_band.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["t", "corr_Mminus1sigma", "corr_central", "corr_Mplus1sigma"])
    for t in T:
        w.writerow([t, f"{math.exp(-(M-DM)*t):.14g}",
                    f"{math.exp(-M*t):.14g}", f"{math.exp(-(M+DM)*t):.14g}"])

print("Rebuilt CORR-I plateau control.")
