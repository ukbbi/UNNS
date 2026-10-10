from __future__ import annotations
import json
from scr_iii.engine_common import safe_write_json, sha256_file
from scr_iii.engine_v002_common import output_root_v002


def main():
    out=output_root_v002()/"audit"; result=out/"AUDIT_RESULT_v002.json"; passed=out/"AUDIT_PASS_v002.json"
    if not result.exists() or not passed.exists():
        print("v002 audit freeze blocked: PASS audit files are absent."); return 2
    data=json.loads(result.read_text(encoding="utf-8"))
    if data.get("status")!="PASS":
        print("v002 audit freeze blocked: audit status is not PASS."); return 2
    freeze={
        "engine":"SCR_III_ENGINE_v002","status":"AUDIT_FROZEN","audit_result":"AUDIT_RESULT_v002.json",
        "audit_result_sha256":sha256_file(result),"audit_pass_sha256":sha256_file(passed),
        "rule":"No v002 audit/design value may change after this freeze. Primary verifies both hashes."
    }
    safe_write_json(out/"AUDIT_FREEZE_v002.json",freeze)
    print("SCR-III v002 audit frozen:",freeze["audit_result_sha256"]); return 0

if __name__=="__main__": raise SystemExit(main())
