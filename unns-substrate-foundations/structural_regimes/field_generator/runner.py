import os
import json
import numpy as np
import csv

from config import *
from operators import apply_alpha, apply_mu
from engine_bridge import run_struc_perc
from analysis import compute_commutator


def save_csv(path, ladder):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "value"])
        for i, v in enumerate(ladder):
            writer.writerow([i, v])


def save_txt(path, ladder):
    with open(path, "w") as f:
        for i, v in enumerate(ladder):
            f.write(f"{i}\t{v}\n")


def normalize_ladder(ladder, target=2000):
    n = len(ladder)
    if n <= target:
        return ladder
    idx = np.linspace(0, n - 1, target).astype(int)
    return ladder[idx]


def load_ladder(path):
    values = []

    if path.endswith(".csv"):
        with open(path, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                for v in row:
                    v = v.strip()
                    if v == "" or v.lower() in ["step", "value"]:
                        continue
                    try:
                        values.append(float(v))
                    except:
                        pass
    else:
        with open(path) as f:
            content = f.read().replace(",", " ")
            for v in content.split():
                try:
                    values.append(float(v))
                except:
                    pass

    if len(values) == 0:
        raise ValueError(f"Empty or invalid ladder: {path}")

    values = sorted(set(values))
    return np.array(values)


# ==========================================
# 🔥 AUTO SPARSIFY (FIXED POSITION + WORKING)
# ==========================================
def auto_sparsify_to_kappa(base, config, target=1.0, tol=0.15, max_stride=50):

    best = base
    best_diff = float("inf")
    best_stride = 1
    best_kappa = None

    for stride in range(1, max_stride + 1):

        candidate = base[::stride]

        if len(candidate) < 8:
            break

        R = run_struc_perc(candidate, config)

        if isinstance(R, str):
            try:
                R = json.loads(R)
            except:
                continue

        if not isinstance(R, dict):
            continue

        kappa = R.get("kappa_connect")
        if kappa is None:
            continue

        diff = abs(kappa - target)

        if diff < best_diff:
            best = candidate
            best_diff = diff
            best_stride = stride
            best_kappa = kappa

        if diff < tol:
            break

    #print(f"🔥 auto-sparsify: stride={best_stride}, κ≈{best_kappa:.3f}")

    return best


def extract_metrics(name, alpha, mu, R):

    if not isinstance(R, dict):
        return {
            "ladder": name,
            "alpha": alpha,
            "mu": mu,
            "verdict": "INVALID",
            "kappa": None,
            "giant_ratio": None,
        }

    return {
        "ladder": name,
        "alpha": alpha,
        "mu": mu,
        "verdict": R.get("verdict"),
        "kappa": R.get("kappa_connect"),
        "giant_ratio": R.get("giantRatio"),
    }


def run_batch():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    config = {
        "k_points": K_POINTS,
        "k_min": K_MIN,
        "k_max": K_MAX,
    }

    for name, path in BASE_LADDERS.items():

        prev_verdict = None
        transition_found = False

        base = load_ladder(path)

        original_size = len(base)
        base = normalize_ladder(base)
        base = auto_sparsify_to_kappa(base, config)

        print(f"{name}: {original_size} → {len(base)} points")

        results = {}
        metrics_rows = []

        for alpha in ALPHA_GRID:
            for mu in MU_GRID:

                L1 = apply_mu(apply_alpha(base, alpha), mu)
                R1 = run_struc_perc(L1, config)

                if isinstance(R1, str):
                    try:
                        R1 = json.loads(R1)
                    except:
                        R1 = {}

                if not isinstance(R1, dict):
                    R1 = {}

                key = f"a={alpha:.5f}_m={mu:.5f}"

                results[key] = {
                    "forward": R1
                }

                # 🔥 AUTO-STOP TRANSITION
                current_verdict = R1.get("verdict")

                if prev_verdict is None:
                    prev_verdict = current_verdict

                elif current_verdict != prev_verdict:
                    print("\n=== 🚨 TRANSITION DETECTED ===")
                    print(f"{name}: α={alpha:.3f}, μ={mu:.3f}")
                    print(f"{prev_verdict} → {current_verdict}\n")

                    results["TRANSITION"] = {
                        "alpha": alpha,
                        "mu": mu,
                        "from": prev_verdict,
                        "to": current_verdict
                    }

                    transition_found = True
                    break

                prev_verdict = current_verdict

                metrics_rows.append(extract_metrics(name, alpha, mu, R1))

                print(f"{name} α={alpha:.3f} μ={mu:.3f} done")

            if transition_found:
                break

        out_path = os.path.join(OUTPUT_DIR, f"{name}_results.json")

        with open(out_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"Saved {name}")

        if metrics_rows:
            metrics_path = os.path.join(OUTPUT_DIR, f"{name}_metrics.csv")

            with open(metrics_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=metrics_rows[0].keys())
                writer.writeheader()
                writer.writerows(metrics_rows)

            print(f"Saved metrics {name}")


if __name__ == "__main__":
    run_batch()