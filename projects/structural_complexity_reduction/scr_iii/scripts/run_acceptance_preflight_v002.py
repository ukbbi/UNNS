from __future__ import annotations
import json, statistics

from scr_iii.engine_v002_common import output_root_v002, load_seeds_v002, Q_LEVELS_V002, SIGMA_LEVELS_V002, MAX_ATTEMPTS_V002
from scr_iii.generator.route_csp_c_v001 import generate_family
from scr_iii.engine_common import safe_write_json


def main():
    out = output_root_v002() / "preflight"
    gate = out / "ENGINE_PREFLIGHT_PASS_v002.json"
    if not gate.exists():
        print("Acceptance preflight blocked: run RUN_SCR_III_V002_VALIDATE.bat first.")
        return 2
    final = out / "ACCEPTANCE_PREFLIGHT_v002.json"
    if final.exists():
        print("Acceptance preflight already complete; rerun refused:", final)
        return 2
    seeds = load_seeds_v002()
    rows = []
    by_depth = {}
    for depth in (14, 16, 18):
        accepted_attempts = []
        drows = []
        for seed in seeds["acceptance_preflight"][f"depth_{depth}"]:
            fam = generate_family(seed, depth, Q_LEVELS_V002, SIGMA_LEVELS_V002, max_attempts=MAX_ATTEMPTS_V002)
            row = {
                "depth": depth,
                "seed": int(seed),
                "status": fam["status"],
                "accepted_attempt": fam.get("accepted_attempt"),
                "attempts_examined": len(fam["attempt_log"]),
            }
            # Permitted baseline-only acceptance diagnostics from the final attempted/accepted attempt.
            if fam["attempt_log"]:
                selected = fam["attempt_log"][int(fam["accepted_attempt"])] if fam["status"] == "ACCEPTED" else fam["attempt_log"][-1]
                row["acceptance_by_q"] = selected["by_q"]
            drows.append(row); rows.append(row)
            if fam["status"] == "ACCEPTED":
                accepted_attempts.append(int(fam["accepted_attempt"]))
            print(f"ACCEPTANCE d={depth} seed={seed}: {fam['status']} attempt={fam.get('accepted_attempt')}")
        nacc = sum(r["status"] == "ACCEPTED" for r in drows)
        rate = nacc / len(drows)
        by_depth[str(depth)] = {
            "families": len(drows),
            "accepted": nacc,
            "rate": rate,
            "median_accepted_attempt": statistics.median(accepted_attempts) if accepted_attempts else None,
            "LOW_COMMON_ATTEMPT_ACCEPTANCE": nacc < 15,
            "STRICT_VALIDITY_POWER_RISK": nacc < 21,
        }
    result = {
        "engine": "SCR_III_ENGINE_v002",
        "stage": "ACCEPTANCE_PREFLIGHT_V002",
        "status": "COMPLETE",
        "rule": "diagnostic only; no tuning authority; no SCR/filter survival outcome computed",
        "max_attempts": MAX_ATTEMPTS_V002,
        "by_depth": by_depth,
        "families": rows,
    }
    safe_write_json(final, result)
    safe_write_json(out / "ACCEPTANCE_PREFLIGHT_COMPLETE_v002.json", {"status": "COMPLETE", "result": final.name, "by_depth": by_depth})
    print("SCR-III v002 acceptance preflight COMPLETE")
    for d, x in by_depth.items():
        print(f"  d={d}: {x['accepted']}/{x['families']} accepted ({x['rate']:.3f}) median_attempt={x['median_accepted_attempt']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
