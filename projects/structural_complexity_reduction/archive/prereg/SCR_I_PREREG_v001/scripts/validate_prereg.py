from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "config" / "scr_i_prereg_v001.json"

REQUIRED_DOCS = [
    "README.md", "PREREG.md", "BENCH_A.md", "GATES.md", "METRICS.md",
    "NULLS.md", "DECISION_RULES.md", "UPI_BLIND.md", "SOURCE_LOCK.md", "RUN_PLAN.md"
]


def main() -> int:
    errors: list[str] = []
    for name in REQUIRED_DOCS:
        p = ROOT / name
        if not p.exists() or p.stat().st_size < 200:
            errors.append(f"missing/too-small required document: {name}")

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    if cfg["preregistration"] != "SCR_I_PREREG_v001":
        errors.append("wrong preregistration id")
    if cfg["benchmark"] != "SCR-I-A":
        errors.append("wrong benchmark id")
    if cfg["gate_order"] != ["G1", "G2", "G3", "G4"]:
        errors.append("gate order changed")
    if cfg["primary_requirements"]["target_recall"] != 1.0:
        errors.append("target recall requirement must be exactly 1.0")
    if cfg["upi"]["prunes"] is not False:
        errors.append("UPI must remain non-pruning")
    if cfg["candidate_pool"]["sizes"] != [2500, 10000, 40000]:
        errors.append("pool sizes changed")
    if len(cfg["candidate_pool"]["primary_seeds"]) != 5:
        errors.append("expected five frozen primary seeds")
    mix = cfg["candidate_pool"]["generator_mix"]
    if abs(sum(mix.values()) - 1.0) > 1e-12:
        errors.append("generator mix does not sum to 1")
    g = cfg["gates"]
    if g["G2"]["delta_kappa_gt"] != 0.05:
        errors.append("G2 threshold changed")
    if (g["G3"]["s_lo"], g["G3"]["s_hi"], g["G3"]["temporal_quality_min"]) != (0.08, 0.10, 0.70):
        errors.append("G3 baseline parameters changed")
    if g["G4"]["locality_score_lt"] != 0.10:
        errors.append("G4 threshold changed")

    if errors:
        print("SCR-I preregistration validation: FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print("SCR-I preregistration validation: PASS")
    print("ID: SCR_I_PREREG_v001")
    print("Benchmark: SCR-I-A")
    print("Gate order: G1 -> G2 -> G3 -> G4")
    print("UPI: blinded secondary / non-pruning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
