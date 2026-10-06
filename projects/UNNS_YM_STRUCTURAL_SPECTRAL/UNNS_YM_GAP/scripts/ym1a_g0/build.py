from pathlib import Path
import csv, json, math

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "ladders" / "ym1a_refinement.csv"
OUT = ROOT / "nulls" / "ym1a_g0"
RUN = ROOT / "output" / "ym1a_g0_build.json"

# Frozen dyadic approach to 0+: epsilon = 2^-k.
K_GRID = list(range(0, 11))  # epsilon from 1 down to 1/1024
COORDS = ["c1", "c2", "c3", "c4", "c5"]

FAMILIES = {
    "offset": "Primary adversary: common downward translation; preserves every pairwise spectral spacing exactly.",
    "upctrl": "Matched massive control: equal-magnitude common upward translation; preserves every pairwise spacing.",
    "scale": "Null: uniform multiplicative collapse; preserves spectral ratios while all coordinates approach zero.",
    "gaponly": "Mechanism null: only c1 approaches zero; excited coordinates remain fixed.",
}

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def xvec(row):
    return [float(row[f"{c}_M_over_sqrt_sigma"]) for c in COORDS]

def transform(family, x, eps):
    gap = x[0]
    if family == "offset":
        # Drives the vacuum separation to zero while preserving all pairwise spacings.
        shift = (1.0 - eps) * gap
        return [v - shift for v in x]
    if family == "upctrl":
        # Same deformation magnitude, opposite direction; remains massive.
        shift = (1.0 - eps) * gap
        return [v + shift for v in x]
    if family == "scale":
        # Pure scale collapse: all ratios remain fixed.
        return [eps * v for v in x]
    if family == "gaponly":
        # Isolate the first coordinate: only the mass-gap coordinate is changed.
        return [eps * gap] + x[1:]
    raise ValueError(family)

def pairwise(v):
    return {(i,j): v[j]-v[i] for i in range(len(v)) for j in range(i+1, len(v))}

def main():
    src = read_csv(SRC)
    OUT.mkdir(parents=True, exist_ok=True)

    long_rows = []
    wide_by_family = {fam: [] for fam in FAMILIES}
    invariant_rows = []
    endpoint_rows = []

    for r in src:
        level = int(r["level"])
        x = xvec(r)
        base_pw = pairwise(x)
        base_rat = [v/x[0] for v in x]

        for k in K_GRID:
            eps = 2.0 ** (-k)
            lam = 1.0 - eps
            for fam in FAMILIES:
                y = transform(fam, x, eps)
                wide = {
                    "family": fam,
                    "k": k,
                    "epsilon": f"{eps:.12g}",
                    "lambda": f"{lam:.12g}",
                    "level": level,
                    "ensemble_id": r["ensemble_id"],
                    "beta": r["beta"],
                    "a_sqrt_sigma": r["a_sqrt_sigma"],
                }
                for c, val in zip(COORDS, y):
                    wide[c] = f"{val:.12g}"
                wide_by_family[fam].append(wide)

                for c, src_val, val in zip(COORDS, x, y):
                    long_rows.append({
                        "family": fam,
                        "k": k,
                        "epsilon": f"{eps:.12g}",
                        "lambda": f"{lam:.12g}",
                        "level": level,
                        "ensemble_id": r["ensemble_id"],
                        "beta": r["beta"],
                        "coord_id": c,
                        "source_value": f"{src_val:.12g}",
                        "value": f"{val:.12g}",
                    })

                pw = pairwise(y)
                spacing_err = max(abs(pw[p]-base_pw[p]) for p in base_pw)
                ratio_err = max(abs((y[i]/y[0] if y[0] != 0 else float("inf")) - base_rat[i])
                                for i in range(len(y))) if y[0] != 0 else float("inf")
                invariant_rows.append({
                    "family": fam,
                    "k": k,
                    "epsilon": f"{eps:.12g}",
                    "level": level,
                    "min_value": f"{min(y):.12g}",
                    "gap_value": f"{y[0]:.12g}",
                    "max_pairwise_spacing_error": f"{spacing_err:.12g}",
                    "max_ratio_error_vs_source": "" if math.isinf(ratio_err) else f"{ratio_err:.12g}",
                    "ordered_non_decreasing": str(all(y[i] <= y[i+1] for i in range(len(y)-1))).lower(),
                })

        # Formal epsilon=0 endpoints are stored separately and are not primary chamber inputs.
        for fam in ["offset", "scale", "gaponly"]:
            y0 = transform(fam, x, 0.0)
            er = {
                "family": fam,
                "epsilon": "0",
                "level": level,
                "ensemble_id": r["ensemble_id"],
                "beta": r["beta"],
            }
            for c, val in zip(COORDS, y0):
                er[c] = f"{val:.12g}"
            endpoint_rows.append(er)

    long_fields = [
        "family","k","epsilon","lambda","level","ensemble_id","beta",
        "coord_id","source_value","value"
    ]
    write_csv(OUT / "g0_long.csv", long_rows, long_fields)

    wide_fields = [
        "family","k","epsilon","lambda","level","ensemble_id","beta","a_sqrt_sigma",
        "c1","c2","c3","c4","c5"
    ]
    for fam, rows in wide_by_family.items():
        write_csv(OUT / f"g0_{fam}.csv", rows, wide_fields)

    inv_fields = [
        "family","k","epsilon","level","min_value","gap_value",
        "max_pairwise_spacing_error","max_ratio_error_vs_source","ordered_non_decreasing"
    ]
    write_csv(OUT / "g0_invariants.csv", invariant_rows, inv_fields)

    endpoint_fields = ["family","epsilon","level","ensemble_id","beta","c1","c2","c3","c4","c5"]
    write_csv(OUT / "g0_endpoint.csv", endpoint_rows, endpoint_fields)

    checks = {
        "levels_8": len(src) == 8,
        "grid_points_11": len(K_GRID) == 11,
        "primary_rows_88": len(wide_by_family["offset"]) == 88,
        "all_positive_primary_0plus": all(float(r["min_value"]) > 0 for r in invariant_rows if r["family"]=="offset"),
        "offset_preserves_spacings": max(float(r["max_pairwise_spacing_error"]) for r in invariant_rows if r["family"]=="offset") < 1e-9,
        "upctrl_preserves_spacings": max(float(r["max_pairwise_spacing_error"]) for r in invariant_rows if r["family"]=="upctrl") < 1e-9,
        "scale_preserves_ratios": max(float(r["max_ratio_error_vs_source"]) for r in invariant_rows if r["family"]=="scale") < 1e-9,
        "formal_offset_endpoint_gap_zero": all(abs(float(r["c1"])) < 1e-12 for r in endpoint_rows if r["family"]=="offset"),
        "formal_gaponly_endpoint_gap_zero": all(abs(float(r["c1"])) < 1e-12 for r in endpoint_rows if r["family"]=="gaponly"),
    }

    summary = {
        "stage": "YM1A-G0",
        "version": "1.0",
        "primary_family": "offset",
        "epsilon_grid": [2.0**(-k) for k in K_GRID],
        "formal_endpoint_epsilon": 0,
        "formal_endpoint_used_as_primary_chamber_input": False,
        "families": FAMILIES,
        "checks": checks,
        "passed": all(checks.values()),
    }
    RUN.parent.mkdir(parents=True, exist_ok=True)
    RUN.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
