from __future__ import annotations
import argparse, json, hashlib, sys
from pathlib import Path

from external.analyzer import analyze_bundle
from chamber.runner import run_record

def sha_text(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()

def audit_markdown(candidate_id,audit,result):
    lines=[f"# TIME-CRYSTAL-I Evidence Audit — {candidate_id}","",
           f"**Verdict:** `{result['verdict']}`","",
           "## Sector audit",""]
    for sector,info in audit.items():
        lines += [f"### {sector.capitalize()}",f"Status: **{info.get('status','—')}**",""]
        files=info.get("files")
        if isinstance(files,dict):
            for f,p in files.items():
                lines.append(f"- {'FOUND' if p else 'MISSING'}: `{f}`")
        elif info.get("file"):
            lines.append(f"- {'FOUND' if info.get('present') else 'MISSING'}: `{info['file']}`")
        if info.get("metrics"):
            lines += ["","Metrics:","```json",json.dumps(info["metrics"],indent=2),"```"]
        lines.append("")
    if result.get("missing"):
        lines += ["## Evidence required for a higher verdict",""]
        for x in result["missing"]:
            lines.append(f"- {x}")
    return "\n".join(lines)+"\n"

def main():
    ap=argparse.ArgumentParser(description="TIME-CRYSTAL-I v1.1.0 External Analysis Mode")
    ap.add_argument("candidate",help="candidate bundle folder or ZIP")
    ap.add_argument("output",nargs="?",default="external_output")
    ap.add_argument("--blind",action="store_true",help="suppress manifest label/class during analysis")
    args=ap.parse_args()

    root=Path(__file__).resolve().parent
    out=Path(args.output).resolve()
    out.mkdir(parents=True,exist_ok=True)

    analysis=analyze_bundle(args.candidate,root,blind=args.blind)
    result=run_record(analysis["record"])

    lock_payload={
        "chamber":"TIME-CRYSTAL-I",
        "version":"1.1.0",
        "mode":"BLIND" if args.blind else "OPEN",
        "candidate_id":analysis["manifest"]["candidate_id"],
        "candidate_evidence_sha256":analysis["evidence_sha256"],
        "frozen_metric_sha256":analysis["metric_sha256"],
        "protocol_sha256":sha_text(analysis["protocol"]),
        "verdict":result["verdict"],
        "level":result["level"],
    }
    lock_payload["analysis_lock_sha256"]=sha_text(lock_payload)

    external={
        "export_type":"TIME-CRYSTAL-I external analysis",
        "chamber":{"name":"TIME-CRYSTAL-I","version":"1.1.0"},
        "blind_mode":bool(args.blind),
        "analysis_lock":lock_payload,
        "result":result,
        "audit":analysis["audit"],
    }

    (out/"external_result.json").write_text(json.dumps(external,indent=2),encoding="utf-8")
    if args.blind:
        (out/"blind_verdict.json").write_text(json.dumps(external,indent=2),encoding="utf-8")
    (out/"evidence_audit.json").write_text(json.dumps(analysis["audit"],indent=2),encoding="utf-8")
    (out/"EVIDENCE_AUDIT.md").write_text(
        audit_markdown(analysis["manifest"]["candidate_id"],analysis["audit"],result),encoding="utf-8")
    (out/"analysis_lock.json").write_text(json.dumps(lock_payload,indent=2),encoding="utf-8")

    log=[
        "STATUS: EXTERNAL_ANALYSIS_COMPLETE",
        f"MODE: {'BLIND' if args.blind else 'OPEN'}",
        f"CANDIDATE: {analysis['manifest']['candidate_id']}",
        f"VERDICT: {result['verdict']}",
        f"LEVEL: {result['level']}",
        f"EVIDENCE SHA256: {analysis['evidence_sha256']}",
        f"ANALYSIS LOCK SHA256: {lock_payload['analysis_lock_sha256']}",
    ]
    (out/"RUN_LOG.txt").write_text("\n".join(log)+"\n",encoding="utf-8")
    print("\n".join(log))

if __name__=="__main__":
    main()
