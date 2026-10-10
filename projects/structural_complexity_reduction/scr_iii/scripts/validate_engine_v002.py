from __future__ import annotations
import json, sys, unittest
from pathlib import Path

from scr_iii.engine_common import scr_iii_root, safe_write_json
from scr_iii.engine_v002_common import output_root_v002, load_seeds_v002
from scr_iii.source_lock_v002 import verify_source_lock_v002, verify_design_freeze_v002


def _flatten_seed_values(seeds):
    vals = []
    for section in ("acceptance_preflight", "audit", "primary"):
        for v in seeds.get(section, {}).values():
            if isinstance(v, list):
                vals.extend(int(x) for x in v)
    for v in seeds.get("analysis_rng", {}).values():
        vals.append(int(v))
    return vals


def _seed_checks(seeds):
    vals = _flatten_seed_values(seeds)
    unique = len(vals) == len(set(vals))
    burned = set(range(9100000, 9100030))
    burned.update(range(9212000, 9212040)); burned.update(range(9214000, 9214040)); burned.update(range(9216000, 9216040)); burned.update(range(9218000, 9218040))
    burned.update(range(2026111101, 2026111113)); burned.update(range(2026111201, 2026111213))
    burned.update(range(2026112101, 2026112121)); burned.update(range(2026112201, 2026112221)); burned.update(range(2026112301, 2026112321))
    for prefix, count in [
        (2026101100,8),(2026101200,8),(2026101300,8),(2026101400,6),
        (2026102100,10),(2026102200,10),(2026102300,10),
        (2026106100,8),(2026106200,8),(2026106300,8),(2026106400,6),
        (2026107100,10),(2026107200,10),(2026107300,10),
    ]:
        burned.update(prefix+i for i in range(1, count+1))
    burned.update(range(2026100701,2026100706)); burned.update(range(2026101001,2026101006))
    burned.update([2026103001,2026104001,2026105001,2026108101,2026108201,2026108301])
    overlap = sorted(set(vals) & burned)
    expected_counts = {
        "pre14": len(seeds["acceptance_preflight"]["depth_14"]),
        "pre16": len(seeds["acceptance_preflight"]["depth_16"]),
        "pre18": len(seeds["acceptance_preflight"]["depth_18"]),
        "audit14": len(seeds["audit"]["depth_14"]),
        "pri14": len(seeds["primary"]["depth_14"]),
        "pri16": len(seeds["primary"]["depth_16"]),
        "pri18": len(seeds["primary"]["depth_18"]),
    }
    counts_pass = all(v == 30 for v in expected_counts.values())
    return {"pass": unique and not overlap and counts_pass, "unique": unique, "overlap": overlap, "counts": expected_counts, "counts_pass": counts_pass}


def main():
    out = output_root_v002() / "preflight"
    out.mkdir(parents=True, exist_ok=True)
    design = verify_design_freeze_v002()
    source = verify_source_lock_v002()
    seeds = load_seeds_v002()
    seedcheck = _seed_checks(seeds)

    # v002-specific unit tests only. v001 tests remain independently reproducible.
    s3 = scr_iii_root()
    suite = unittest.defaultTestLoader.discover(str(s3 / "tests_v002"), pattern="test_*.py", top_level_dir=str(s3.parent))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    passed = design.get("pass") and source.get("pass") and seedcheck.get("pass") and result.wasSuccessful()
    report = {
        "engine": "SCR_III_ENGINE_v002",
        "stage": "VALIDATE_V002",
        "status": "PASS" if passed else "FAIL",
        "design_freeze": design,
        "source_lock": source,
        "seed_check": seedcheck,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
    }
    safe_write_json(out / "ENGINE_PREFLIGHT_v002.json", report)
    if passed:
        safe_write_json(out / "ENGINE_PREFLIGHT_PASS_v002.json", report)
    print("SCR_III_ENGINE_v002 validation:", report["status"])
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
