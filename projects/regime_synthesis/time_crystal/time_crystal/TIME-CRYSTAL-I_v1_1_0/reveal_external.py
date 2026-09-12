from __future__ import annotations
import argparse,json,hashlib
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description="Reveal ground truth only after a blind TIME-CRYSTAL-I verdict is locked.")
    ap.add_argument("blind_output",help="folder containing blind_verdict.json and analysis_lock.json")
    ap.add_argument("ground_truth",help="separate ground_truth.json")
    args=ap.parse_args()

    out=Path(args.blind_output).resolve()
    blind=json.loads((out/"blind_verdict.json").read_text(encoding="utf-8"))
    lock=json.loads((out/"analysis_lock.json").read_text(encoding="utf-8"))
    truth=json.loads(Path(args.ground_truth).read_text(encoding="utf-8"))

    cid=blind["result"]["id"]
    if str(truth["candidate_id"])!=str(cid):
        raise RuntimeError("ground-truth candidate_id does not match locked blind candidate")

    expected=truth.get("expected_verdict")
    observed=blind["result"]["verdict"]
    comp={
        "status":"POSTHOC_REVEAL_COMPLETE",
        "candidate_id":cid,
        "locked_analysis_sha256":lock["analysis_lock_sha256"],
        "physical_class":truth.get("physical_class"),
        "expected_verdict":expected,
        "observed_blind_verdict":observed,
        "verdict_match":None if expected is None else bool(expected==observed),
        "ground_truth_sha256":hashlib.sha256(Path(args.ground_truth).read_bytes()).hexdigest()
    }
    (out/"posthoc_comparison.json").write_text(json.dumps(comp,indent=2),encoding="utf-8")
    print("STATUS: POSTHOC_REVEAL_COMPLETE")
    print("PHYSICAL CLASS:",comp["physical_class"])
    print("LOCKED BLIND VERDICT:",observed)
    print("EXPECTED VERDICT:",expected)
    print("MATCH:",comp["verdict_match"])

if __name__=="__main__":
    main()
