from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

from chamber.runner import run_record
from adapters.validation_corpus import build_validation_corpus


EXPECTED = {
    "frey57_mbl_dtc": "INSUFFICIENT_DOMAIN_EVIDENCE",
    "mi20_mbl_dtc": "MANY_BODY_TIME_CRYSTAL_ADMISSIBLE",
    "mi20_prethermal": "TEMPORAL_RECURRENCE",
    "mi20_thermal": "NO_TEMPORAL_ORDER",
    "classical_exact_2T": "RIGID_RECURRENCE",
    "classical_logistic_2T": "TEMPORAL_RECURRENCE",
    "classical_logistic_4T": "TEMPORAL_RECURRENCE",
    "classical_damped_2T": "TEMPORAL_RECURRENCE",
    "classical_chaos": "NO_TEMPORAL_ORDER",
    "iid_random": "NO_TEMPORAL_ORDER",
}


def write_csv(path: Path, rows: list[dict]):
    fields = [
        "id", "label", "domain", "expected_physics_class",
        "verdict", "level", "temporal_status", "q0",
        "rigidity_status", "collective_status", "spectral_status",
        "validation_match",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def js_literal(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def main():
    ap = argparse.ArgumentParser(description="TIME-CRYSTAL-I v1.1.0 chamber validation corpus runner.")
    ap.add_argument("phys")
    ap.add_argument("closure")
    ap.add_argument("mi")
    ap.add_argument("ctrl")
    ap.add_argument("rigidity")
    ap.add_argument("collective")
    ap.add_argument("output", nargs="?", default="outputs")
    args = ap.parse_args()

    out = Path(args.output).resolve()
    out.mkdir(parents=True, exist_ok=True)

    corpus, dependencies = build_validation_corpus(
        args.phys, args.closure, args.mi, args.ctrl, args.rigidity, args.collective
    )

    results = [run_record(r) for r in corpus]
    table = []
    all_match = True
    for result in results:
        r = result["record"]
        s = r["sectors"]
        expected = EXPECTED[result["id"]]
        match = result["verdict"] == expected
        all_match &= match
        table.append({
            "id": result["id"],
            "label": result["label"],
            "domain": result["domain"],
            "expected_physics_class": r.get("expected_physics_class", ""),
            "verdict": result["verdict"],
            "level": result["level"],
            "temporal_status": s["temporal"]["status"],
            "q0": s["temporal"].get("q0"),
            "rigidity_status": s["rigidity"]["status"],
            "collective_status": s["collective"]["status"],
            "spectral_status": s["spectral"]["status"],
            "validation_match": match,
        })

    status = "PASS_INITIAL_VALIDATION_CORPUS" if all_match else "FAIL_INITIAL_VALIDATION_CORPUS"

    payload = {
        "chamber": {
            "name": "TIME-CRYSTAL-I",
            "version": "1.1.0",
            "status": status,
            "principle": (
                "Temporal recurrence is necessary but not sufficient. "
                "Quantum many-body time-crystal admissibility requires persistent "
                "temporal closure, recurrence rigidity, collective order, and "
                "many-body spectral/eigenstate breadth."
            ),
        },
        "dependencies": dependencies,
        "expected_verdicts": EXPECTED,
        "results": results,
    }

    (out / "validation_results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_csv(out / "validation_summary.csv", table)

    # Browser data layer. It is deliberately plain JS so the HTML works from file://
    root = Path(__file__).resolve().parent
    browser_payload = {
        "chamber": payload["chamber"],
        "dependencies": payload["dependencies"],
        "results": results,
    }
    (root / "CHAMBER_DATA.js").write_text(
        "window.TIME_CRYSTAL_I_DATA=" + js_literal(browser_payload) + ";\n",
        encoding="utf-8",
    )

    log = [
        f"STATUS: {status}",
        "CHAMBER: TIME-CRYSTAL-I v1.1.0",
        f"Frozen closure metric: {dependencies['frozen_closure_metric_sha256']}",
        "",
        "INITIAL VALIDATION CORPUS",
    ]
    for row in table:
        log.append(
            f"{row['id']}: {row['verdict']} "
            f"(expected={EXPECTED[row['id']]}, match={row['validation_match']})"
        )
    log += [
        "",
        "CORE CHAMBER PRINCIPLE",
        payload["chamber"]["principle"],
    ]
    (out / "RUN_LOG.txt").write_text("\n".join(log) + "\n", encoding="utf-8")

    print("\n".join(log))
    if not all_match:
        sys.exit(1)


if __name__ == "__main__":
    main()
