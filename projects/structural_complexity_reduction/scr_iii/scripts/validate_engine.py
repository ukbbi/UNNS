from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path
from scr_iii.engine_common import scr_iii_root, safe_write_json
from scr_iii.source_lock import verify_source_lock, verify_design_freeze


def main():
    s3=scr_iii_root(); pr=s3/'SCR_III_PREREG_v001'; out=s3/'output'/'audit'; out.mkdir(parents=True,exist_ok=True)
    p=subprocess.run([sys.executable,str(pr/'scripts'/'validate_prereg.py')],cwd=str(pr),text=True,capture_output=True)
    print(p.stdout.strip())
    if p.returncode!=0:
        print(p.stderr); return 1
    design=verify_design_freeze()
    if not design['pass']:
        print('DESIGN FREEZE FAIL')
        for r in design.get('files',[]):
            if not r['match']: print(r)
        return 1
    lock=verify_source_lock()
    if not lock['pass']:
        print('SOURCE LOCK FAIL');
        for r in lock['files']:
            if not r['match']: print(r)
        return 1
    suite=unittest.defaultTestLoader.discover(str(s3/'tests'),pattern='test_*.py',top_level_dir=str(s3.parent))
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    passed=result.wasSuccessful()
    report={"engine":"SCR_III_ENGINE_v001","status":"PASS" if passed else "FAIL","prereg_validation":"PASS","design_freeze":design,"source_lock":lock,"tests_run":result.testsRun,"failures":len(result.failures),"errors":len(result.errors)}
    safe_write_json(out/'PREFLIGHT_v001.json',report)
    if passed: safe_write_json(out/'PREFLIGHT_PASS_v001.json',report)
    print('SCR_III_ENGINE_v001 preflight:',report['status'])
    return 0 if passed else 1
if __name__=='__main__': raise SystemExit(main())
