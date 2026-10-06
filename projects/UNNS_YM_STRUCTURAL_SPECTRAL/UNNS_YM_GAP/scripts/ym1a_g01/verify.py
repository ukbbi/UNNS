from pathlib import Path
import csv, json, sys, hashlib

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "nulls" / "ym1a_g01"
INPUTS = ROOT / "inputs" / "ym1a_g1"

def rows(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def numeric_file(path):
    with path.open("r", encoding="utf-8") as f:
        lines = [x.strip() for x in f if x.strip()]
    if lines[0].lower() != "value":
        return False
    vals = [float(x) for x in lines[1:]]
    return len(vals) == 6 and vals[0] == 0 and all(vals[i] <= vals[i+1] for i in range(5))

def main():
    allrows = rows(OUT / "g01_all.csv")
    inv = rows(OUT / "g01_invariants.csv")
    idx = rows(INPUTS / "index.csv")
    chamber_files = [ROOT / r["file"] for r in idx]

    checks = {
        "g01_rows_352": len(allrows) == 352,
        "families": sorted(set(r["family"] for r in allrows)) == ["gaponly","offset","scale","upctrl"],
        "levels_1_to_8": sorted(set(int(r["level"]) for r in allrows)) == list(range(1,9)),
        "k_0_to_10": sorted(set(int(r["k"]) for r in allrows)) == list(range(11)),
        "vacuum_fixed_zero": all(float(r["vacuum"]) == 0 for r in allrows),
        "vacuum_gap_positive": min(float(r["vacuum_gap"]) for r in allrows) > 0,
        "offset_spacing_exact": max(float(r["max_internal_spacing_error"]) for r in inv if r["family"]=="offset") < 1e-9,
        "upctrl_spacing_exact": max(float(r["max_internal_spacing_error"]) for r in inv if r["family"]=="upctrl") < 1e-9,
        "scale_ratio_exact": max(float(r["max_ratio_error_vs_source"]) for r in inv if r["family"]=="scale") < 1e-9,
        "input_index_328": len(idx) == 328,
        "all_index_files_exist": all(p.exists() for p in chamber_files),
        "all_inputs_six_node_sorted": all(numeric_file(p) for p in chamber_files),
        "no_endpoint_input": all(float(r["epsilon"]) > 0 for r in idx),
    }

    out = {"checks": checks, "passed": all(checks.values())}
    print(json.dumps(out, indent=2))
    if not out["passed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
