from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCKED = ROOT / "locked_runs"
OUT = ROOT / "TC_P01_DATA.js"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": str(exc)}


def role_for(candidate_id: str, folder_name: str) -> str:
    s = f"{candidate_id} {folder_name}".upper()
    return "CONTROL" if ("CTRL" in s or "NRCTRL" in s) else "CANDIDATE"


def campaign_order(item):
    cid = item.get("id", "")
    folder = item.get("folder", "")
    # Candidates before their controls; stable lexical ordering.
    role_rank = 1 if item.get("role") == "CONTROL" else 0
    return (cid.replace("_CTRL", ""), role_rank, folder)


def main():
    records = []

    if LOCKED.exists():
        for folder in sorted(p for p in LOCKED.iterdir() if p.is_dir()):
            blind_path = folder / "blind_verdict.json"
            if not blind_path.exists():
                continue

            blind = load_json(blind_path) or {}
            lock = load_json(folder / "analysis_lock.json") or {}
            audit = load_json(folder / "evidence_audit.json") or {}
            posthoc = load_json(folder / "posthoc_comparison.json")

            result = blind.get("result", {})
            record = result.get("record", {})
            sectors = record.get("sectors", {})
            cid = result.get("id") or lock.get("candidate_id") or folder.name
            label = result.get("label") or cid
            role = role_for(cid, folder.name)

            if posthoc and not posthoc.get("_read_error"):
                reveal_status = posthoc.get("status", "REVEALED")
                stage = "CLOSED"
            elif lock.get("analysis_lock_sha256"):
                reveal_status = "NOT_REVEALED"
                stage = "BLIND_LOCKED"
            else:
                reveal_status = "NOT_REVEALED"
                stage = "PARTIAL"

            temporal = sectors.get("temporal", {})
            rigidity = sectors.get("rigidity", {})
            collective = sectors.get("collective", {})
            spectral = sectors.get("spectral", {})

            item = {
                "id": cid,
                "folder": folder.name,
                "label": label,
                "role": role,
                "domain": result.get("domain") or record.get("domain", "unknown"),
                "stage": stage,
                "reveal_status": reveal_status,
                "verdict": result.get("verdict", "UNKNOWN"),
                "level": result.get("level"),
                "path": result.get("path", []),
                "missing": result.get("missing", []),
                "sectors": {
                    "temporal": temporal,
                    "rigidity": rigidity,
                    "collective": collective,
                    "spectral": spectral,
                },
                "lock": {
                    "mode": lock.get("mode"),
                    "candidate_evidence_sha256": lock.get("candidate_evidence_sha256"),
                    "frozen_metric_sha256": lock.get("frozen_metric_sha256"),
                    "protocol_sha256": lock.get("protocol_sha256"),
                    "analysis_lock_sha256": lock.get("analysis_lock_sha256"),
                },
                "posthoc": posthoc if posthoc and not posthoc.get("_read_error") else None,
                "links": {
                    "blind_verdict": f"locked_runs/{folder.name}/blind_verdict.json",
                    "analysis_lock": f"locked_runs/{folder.name}/analysis_lock.json",
                    "evidence_audit_json": f"locked_runs/{folder.name}/evidence_audit.json",
                    "evidence_audit_md": f"locked_runs/{folder.name}/EVIDENCE_AUDIT.md",
                    "external_result": f"locked_runs/{folder.name}/external_result.json",
                    "run_log": f"locked_runs/{folder.name}/RUN_LOG.txt",
                    "posthoc": (
                        f"locked_runs/{folder.name}/posthoc_comparison.json"
                        if (folder / "posthoc_comparison.json").exists() else None
                    ),
                },
            }
            records.append(item)

    records.sort(key=campaign_order)

    candidates = [r for r in records if r["role"] == "CANDIDATE"]
    controls = [r for r in records if r["role"] == "CONTROL"]
    closed = [r for r in candidates if r["stage"] == "CLOSED"]
    blind_locked = [r for r in candidates if r["stage"] == "BLIND_LOCKED"]

    payload = {
        "campaign": {
            "id": "TC_PROSPECTIVE_01",
            "chamber": "TIME-CRYSTAL-I v1.1.0",
            "principle": "Analyze first, lock second, reveal third, interpret fourth.",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "candidate_count": len(candidates),
            "control_count": len(controls),
            "closed_count": len(closed),
            "blind_locked_count": len(blind_locked),
            "record_count": len(records),
        },
        "records": records,
        "documents": [
            {"label": "Campaign Manual", "href": "TC_P01_MANUAL.md"},
            {"label": "C001 Results Summary", "href": "C001_RESULTS_SUMMARY.md"},
            {"label": "C001 README", "href": "README_C001.md"},
            {"label": "C002 README", "href": "README_C002.md"},
        ],
    }

    OUT.write_text(
        "window.TC_P01_DATA=" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )

    print("TC_P01 DATA BUILD: COMPLETE")
    print("Records:", len(records))
    print("Candidates:", len(candidates))
    print("Controls:", len(controls))
    print("Closed candidates:", len(closed))
    print("Blind-locked candidates:", len(blind_locked))
    print("Output:", OUT)


if __name__ == "__main__":
    main()
