from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[2]
LAD = ROOT / "ladders"

def rows(name):
    with (LAD / name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def main():
    ref = rows("ym1a_refinement.csv")
    long = rows("ym1a_long.csv")
    gap = rows("ym1a_gap.csv")
    cont = rows("ym1a_continuum.csv")

    checks = {
        "refinement_rows_8": len(ref) == 8,
        "long_rows_40": len(long) == 40,
        "gap_rows_8": len(gap) == 8,
        "continuum_rows_5": len(cont) == 5,
        "levels_1_to_8": [int(r["level"]) for r in ref] == list(range(1, 9)),
        "a_decreases": all(float(ref[i]["a_sqrt_sigma"]) > float(ref[i+1]["a_sqrt_sigma"]) for i in range(7)),
        "all_positive": all(float(r["M_over_sqrt_sigma"]) > 0 for r in long),
        "fixed_coordinate_set": sorted(set(r["coord_id"] for r in long)) == ["c1","c2","c3","c4","c5"],
        "gap_source_match": max(abs(float(r["table1_minus_spectrum_aM"])) for r in gap) <= 0.0001000001,
    }
    out = {"checks": checks, "passed": all(checks.values())}
    print(json.dumps(out, indent=2))
    if not out["passed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
