from __future__ import annotations
import json
from scr_iii.engine_common import scr_iii_root, safe_write_json, sha256_file

def main():
    s3=scr_iii_root(); out=s3/'output'/'audit'; result=out/'AUDIT_RESULT_v001.json'; passed=out/'AUDIT_PASS_v001.json'
    if not result.exists() or not passed.exists():
        print('Audit freeze blocked: PASS audit files are absent.'); return 2
    data=json.loads(result.read_text())
    if data.get('status')!='PASS':
        print('Audit freeze blocked: audit status is not PASS.'); return 2
    freeze={
        'engine':'SCR_III_ENGINE_v001','status':'AUDIT_FROZEN','audit_result':'AUDIT_RESULT_v001.json',
        'audit_result_sha256':sha256_file(result),'audit_pass_sha256':sha256_file(passed),
        'rule':'No audit/design value may be changed after this freeze. Primary must verify these hashes.'
    }
    safe_write_json(out/'AUDIT_FREEZE_v001.json',freeze)
    print('SCR-III audit frozen:',freeze['audit_result_sha256']); return 0
if __name__=='__main__': raise SystemExit(main())
