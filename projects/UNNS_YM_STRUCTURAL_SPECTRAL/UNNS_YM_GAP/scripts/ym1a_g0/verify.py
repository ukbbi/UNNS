from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "nulls" / "ym1a_g0"

def rows(name):
    with (OUT/name).open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def main():
    offset = rows("g0_offset.csv")
    up = rows("g0_upctrl.csv")
    scale = rows("g0_scale.csv")
    gaponly = rows("g0_gaponly.csv")
    inv = rows("g0_invariants.csv")
    endpoint = rows("g0_endpoint.csv")

    checks = {
        "offset_88": len(offset)==88,
        "upctrl_88": len(up)==88,
        "scale_88": len(scale)==88,
        "gaponly_88": len(gaponly)==88,
        "eight_levels": sorted(set(int(r["level"]) for r in offset)) == list(range(1,9)),
        "k_0_to_10": sorted(set(int(r["k"]) for r in offset)) == list(range(11)),
        "positive_primary": min(float(r[c]) for r in offset for c in ["c1","c2","c3","c4","c5"]) > 0,
        "spacing_preserved_primary": max(float(r["max_pairwise_spacing_error"]) for r in inv if r["family"]=="offset") < 1e-9,
        "spacing_preserved_control": max(float(r["max_pairwise_spacing_error"]) for r in inv if r["family"]=="upctrl") < 1e-9,
        "ratio_preserved_scale": max(float(r["max_ratio_error_vs_source"]) for r in inv if r["family"]=="scale") < 1e-9,
        "formal_endpoints_present": len(endpoint) == 24,
    }
    out = {"checks": checks, "passed": all(checks.values())}
    print(json.dumps(out, indent=2))
    if not out["passed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
