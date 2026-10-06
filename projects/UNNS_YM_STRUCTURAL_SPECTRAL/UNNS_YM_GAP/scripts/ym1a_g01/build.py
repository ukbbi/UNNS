from pathlib import Path
import csv, json, math, shutil

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "ladders" / "ym1a_refinement.csv"
OUT = ROOT / "nulls" / "ym1a_g01"
INPUTS = ROOT / "inputs" / "ym1a_g1"
RUN = ROOT / "output" / "ym1a_g01_build.json"

# Frozen dyadic 0+ approach.
K_GRID = list(range(0, 11))  # epsilon = 2^-k, k = 0..10
COORDS = ["c1", "c2", "c3", "c4", "c5"]

FAMILY_NOTES = {
    "offset": (
        "PRIMARY: vacuum fixed at 0; all positive spectral coordinates receive "
        "the same downward translation. Internal positive-spectrum pairwise "
        "spacings are preserved exactly while the vacuum gap tends to 0+."
    ),
    "upctrl": (
        "MATCHED MASSIVE CONTROL: vacuum fixed at 0; all positive coordinates "
        "receive the same upward translation of equal magnitude."
    ),
    "scale": (
        "NULL N1: vacuum fixed at 0; every positive coordinate is multiplied "
        "by epsilon. Spectral ratios are preserved while the whole spectrum "
        "collapses homogeneously toward the vacuum."
    ),
    "gaponly": (
        "NULL N2: vacuum fixed at 0; only c1 is multiplied by epsilon. "
        "The remaining positive coordinates are unchanged."
    ),
}

def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def source_vector(row):
    return [float(row[f"{c}_M_over_sqrt_sigma"]) for c in COORDS]

def transform(family, x, eps):
    x1 = x[0]
    shift = (1.0 - eps) * x1
    if family == "offset":
        return [v - shift for v in x]
    if family == "upctrl":
        return [v + shift for v in x]
    if family == "scale":
        return [eps * v for v in x]
    if family == "gaponly":
        return [eps * x1] + x[1:]
    raise ValueError(f"Unknown family {family}")

def positive_pairwise(v):
    return {(i, j): v[j] - v[i] for i in range(len(v)) for j in range(i + 1, len(v))}

def ratios_to_c1(v):
    return [z / v[0] for z in v]

def chamber_sorted(v):
    # Vacuum is explicit and fixed. Chambers sort scalar ladders internally;
    # we write already-sorted files for transparency.
    return sorted([0.0] + list(v))

def chamber_gaps(v):
    s = chamber_sorted(v)
    return [s[i+1] - s[i] for i in range(len(s)-1)]

def chamber_name(family, level, k):
    return f"{family}_L{level:02d}_K{k:02d}.csv"

def write_chamber_file(path, values):
    # One numeric column + header is accepted by STRUC-I v1.0.4 fallback
    # and STRUC-PERC-I v2.5.0 numeric CSV ingestion.
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("value\n")
        for z in chamber_sorted(values):
            f.write(f"{z:.12g}\n")

def main():
    src = sorted(read_csv(SRC), key=lambda r: int(r["level"]))
    OUT.mkdir(parents=True, exist_ok=True)
    INPUTS.mkdir(parents=True, exist_ok=True)

    # Clear generated family input folders on rebuild.
    for fam in ["baseline", "offset", "upctrl", "scale", "gaponly"]:
        d = INPUTS / fam
        if d.exists():
            for p in d.glob("*.csv"):
                p.unlink()
        d.mkdir(parents=True, exist_ok=True)

    wide_rows = []
    long_rows = []
    inv_rows = []
    endpoint_rows = []
    input_index = []

    for r in src:
        level = int(r["level"])
        x = source_vector(r)
        base_pw = positive_pairwise(x)
        base_rat = ratios_to_c1(x)

        # Common physical baseline: vacuum + measured five-coordinate spectrum.
        base_file = INPUTS / "baseline" / f"physical_L{level:02d}.csv"
        write_chamber_file(base_file, x)
        input_index.append({
            "family": "physical",
            "level": level,
            "k": 0,
            "epsilon": "1",
            "beta": r["beta"],
            "ensemble_id": r["ensemble_id"],
            "file": base_file.relative_to(ROOT).as_posix(),
            "primary_input": "true",
        })

        for k in K_GRID:
            eps = 2.0 ** (-k)
            lam = 1.0 - eps

            for fam in ["offset", "upctrl", "scale", "gaponly"]:
                y = transform(fam, x, eps)
                sorted_ladder = chamber_sorted(y)
                gaps = chamber_gaps(y)

                row = {
                    "family": fam,
                    "k": k,
                    "epsilon": f"{eps:.12g}",
                    "lambda": f"{lam:.12g}",
                    "level": level,
                    "ensemble_id": r["ensemble_id"],
                    "beta": r["beta"],
                    "a_sqrt_sigma": r["a_sqrt_sigma"],
                    "vacuum": "0",
                    "c1": f"{y[0]:.12g}",
                    "c2": f"{y[1]:.12g}",
                    "c3": f"{y[2]:.12g}",
                    "c4": f"{y[3]:.12g}",
                    "c5": f"{y[4]:.12g}",
                    "vacuum_gap": f"{sorted_ladder[1]:.12g}",
                    "sorted_gap_1": f"{gaps[0]:.12g}",
                    "sorted_gap_2": f"{gaps[1]:.12g}",
                    "sorted_gap_3": f"{gaps[2]:.12g}",
                    "sorted_gap_4": f"{gaps[3]:.12g}",
                    "sorted_gap_5": f"{gaps[4]:.12g}",
                }
                wide_rows.append(row)

                for cid, srcv, val in zip(COORDS, x, y):
                    long_rows.append({
                        "family": fam,
                        "k": k,
                        "epsilon": f"{eps:.12g}",
                        "level": level,
                        "ensemble_id": r["ensemble_id"],
                        "beta": r["beta"],
                        "coord_id": cid,
                        "source_value": f"{srcv:.12g}",
                        "value": f"{val:.12g}",
                    })

                pw = positive_pairwise(y)
                spacing_err = max(abs(pw[p] - base_pw[p]) for p in base_pw)
                ratio_err = 0.0
                if y[0] > 0:
                    yr = ratios_to_c1(y)
                    ratio_err = max(abs(yr[i] - base_rat[i]) for i in range(len(y)))

                inv_rows.append({
                    "family": fam,
                    "k": k,
                    "epsilon": f"{eps:.12g}",
                    "level": level,
                    "vacuum_gap": f"{sorted_ladder[1]:.12g}",
                    "min_positive": f"{min(y):.12g}",
                    "max_positive": f"{max(y):.12g}",
                    "max_internal_spacing_error": f"{spacing_err:.12g}",
                    "max_ratio_error_vs_source": f"{ratio_err:.12g}",
                    "all_positive": str(all(v > 0 for v in y)).lower(),
                    "six_node_ladder": str(len(sorted_ladder) == 6).lower(),
                    "five_gaps": str(len(gaps) == 5).lower(),
                })

                # Chamber inputs: common physical baseline is stored separately.
                # Family folders contain only actual deformations K01..K10.
                if k > 0:
                    fn = chamber_name(fam, level, k)
                    fpath = INPUTS / fam / fn
                    write_chamber_file(fpath, y)
                    input_index.append({
                        "family": fam,
                        "level": level,
                        "k": k,
                        "epsilon": f"{eps:.12g}",
                        "beta": r["beta"],
                        "ensemble_id": r["ensemble_id"],
                        "file": fpath.relative_to(ROOT).as_posix(),
                        "primary_input": "true" if fam == "offset" else "false",
                    })

        # Formal endpoint, never a primary chamber input.
        for fam in ["offset", "scale", "gaponly"]:
            y0 = transform(fam, x, 0.0)
            s0 = chamber_sorted(y0)
            endpoint_rows.append({
                "family": fam,
                "epsilon": "0",
                "level": level,
                "ensemble_id": r["ensemble_id"],
                "beta": r["beta"],
                "vacuum": "0",
                "c1": f"{y0[0]:.12g}",
                "c2": f"{y0[1]:.12g}",
                "c3": f"{y0[2]:.12g}",
                "c4": f"{y0[3]:.12g}",
                "c5": f"{y0[4]:.12g}",
                "has_vacuum_degeneracy": str(abs(s0[1]) < 1e-15).lower(),
            })

    wide_fields = [
        "family","k","epsilon","lambda","level","ensemble_id","beta","a_sqrt_sigma",
        "vacuum","c1","c2","c3","c4","c5","vacuum_gap",
        "sorted_gap_1","sorted_gap_2","sorted_gap_3","sorted_gap_4","sorted_gap_5"
    ]
    write_csv(OUT / "g01_all.csv", wide_rows, wide_fields)

    for fam in ["offset", "upctrl", "scale", "gaponly"]:
        write_csv(
            OUT / f"g01_{fam}.csv",
            [r for r in wide_rows if r["family"] == fam],
            wide_fields,
        )

    write_csv(
        OUT / "g01_long.csv",
        long_rows,
        ["family","k","epsilon","level","ensemble_id","beta","coord_id","source_value","value"],
    )
    write_csv(
        OUT / "g01_invariants.csv",
        inv_rows,
        ["family","k","epsilon","level","vacuum_gap","min_positive","max_positive",
         "max_internal_spacing_error","max_ratio_error_vs_source",
         "all_positive","six_node_ladder","five_gaps"],
    )
    write_csv(
        OUT / "g01_endpoint.csv",
        endpoint_rows,
        ["family","epsilon","level","ensemble_id","beta","vacuum","c1","c2","c3","c4","c5",
         "has_vacuum_degeneracy"],
    )
    write_csv(
        INPUTS / "index.csv",
        input_index,
        ["family","level","k","epsilon","beta","ensemble_id","file","primary_input"],
    )

    # Human-readable input guide.
    (INPUTS / "README.md").write_text(
        """# YM1A-G1 chamber-ready inputs

Every CSV contains exactly one header (`value`) and six ordered scalar values:

1. explicit vacuum node = 0
2. five positive YM1A spectral levels after the frozen G0.1 transformation

`baseline/` contains the eight physical measured ladders.
Each deformation family contains K01..K10 for all eight lattice levels.

The formal epsilon=0 endpoint is deliberately NOT included as a chamber input,
because it makes c1 degenerate with the vacuum. It remains recorded under
`nulls/ym1a_g01/g01_endpoint.csv`.

Use the canonical chamber defaults and do not modify the chamber HTML files.
""",
        encoding="utf-8"
    )

    # Frozen construction checks.
    off = [r for r in inv_rows if r["family"] == "offset"]
    up = [r for r in inv_rows if r["family"] == "upctrl"]
    sc = [r for r in inv_rows if r["family"] == "scale"]

    checks = {
        "source_levels_8": len(src) == 8,
        "dyadic_grid_11": len(K_GRID) == 11,
        "families_4": len(FAMILY_NOTES) == 4,
        "offset_rows_88": len([r for r in wide_rows if r["family"]=="offset"]) == 88,
        "strict_positive_0plus": all(r["all_positive"] == "true" for r in inv_rows),
        "six_nodes_everywhere": all(r["six_node_ladder"] == "true" for r in inv_rows),
        "five_gaps_everywhere": all(r["five_gaps"] == "true" for r in inv_rows),
        "offset_internal_spacings_preserved": max(float(r["max_internal_spacing_error"]) for r in off) < 1e-9,
        "upctrl_internal_spacings_preserved": max(float(r["max_internal_spacing_error"]) for r in up) < 1e-9,
        "scale_ratios_preserved": max(float(r["max_ratio_error_vs_source"]) for r in sc) < 1e-9,
        "baseline_files_8": len(list((INPUTS/"baseline").glob("*.csv"))) == 8,
        "deformation_input_files_320": sum(
            len(list((INPUTS/f).glob("*.csv")))
            for f in ["offset","upctrl","scale","gaponly"]
        ) == 320,
        "input_index_rows_328": len(input_index) == 328,
        "formal_endpoint_not_in_inputs": all(float(r["epsilon"]) > 0 for r in input_index),
    }

    summary = {
        "stage": "YM1A-G0.1",
        "version": "1.0",
        "vacuum_anchor": 0.0,
        "ladder_nodes": 6,
        "ladder_gaps": 5,
        "epsilon_grid": [2.0**(-k) for k in K_GRID],
        "formal_endpoint_epsilon": 0,
        "formal_endpoint_is_chamber_input": False,
        "families": FAMILY_NOTES,
        "g1_input_files": 328,
        "checks": checks,
        "passed": all(checks.values()),
    }
    RUN.parent.mkdir(parents=True, exist_ok=True)
    RUN.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
