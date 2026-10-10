from __future__ import annotations
import json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve()
SCRII = HERE.parents[1]
FINAL = SCRII / "output" / "v002_primary" / "PRIMARY_RESULT_v002.json"
REPORT = SCRII / "output" / "v002_primary" / "SUMMARY_v002.md"

def pct(x): return f"{100*x:.2f}%"

def main():
    if not FINAL.exists():
        print("No completed v002 primary result.")
        return 1
    data = json.loads(FINAL.read_text(encoding="utf-8"))
    rows = data["records"]
    agg = data["aggregate"]

    lines = [
        "# SCR-II v002 Primary Summary",
        "",
        f"**Status:** `{data['status']}`",
        f"**Verdict:** `{agg['primary_verdict']}`",
        "",
        f"- Preservation passes: **{agg['preservation_passes']}/30**",
        f"- Preservation failures: **{agg['preservation_failures']}/30**",
        f"- Median exact-solution recall: **{pct(agg['median_solution_recall'])}**",
        f"- Minimum exact-solution recall: **{pct(agg['minimum_solution_recall'])}**",
        f"- Maximum exact-solution recall: **{pct(agg['maximum_solution_recall'])}**",
        f"- Median node reduction: **{pct(agg['median_r_node'])}**",
        f"- Median time gain: **{agg['median_g_time']:.3f}×**",
        "",
        "## By depth",
        "",
        "| Depth | Preservation | Median baseline solutions | Median recall | Min recall | Median node reduction | Median time gain |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for d in ("14","16","18"):
        s=agg["by_depth"][d]
        lines.append(
            f"| {d} | {s['preservation_passes']}/{s['cells']} | "
            f"{s['median_solution_count_baseline']:.1f} | {pct(s['median_solution_recall'])} | "
            f"{pct(s['min_solution_recall'])} | {pct(s['median_r_node'])} | {s['median_g_time']:.3f}× |"
        )

    lines += [
        "",
        "## Interpretation boundary",
        "",
        "This benchmark tests whether a frozen structural grammar transfers to an independently generated arithmetic exact-solution set.",
        "A preservation failure is a valid non-transfer result for this benchmark and is not a failure of the SCR-I basin/class result.",
        "",
        "The v002 benchmark was frozen before any v002 primary seed was generated or solved.",
    ]

    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote", REPORT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
