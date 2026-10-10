from pathlib import Path
import json, subprocess, sys, unittest

HERE=Path(__file__).resolve()
SCRII=HERE.parents[1]

def main():
    prereg=SCRII/"SCR_II_PREREG_v002"
    p=subprocess.run([sys.executable,str(prereg/"scripts"/"validate_prereg.py")],
                     cwd=prereg,capture_output=True,text=True)
    print(p.stdout.strip())
    if p.returncode!=0:
        print(p.stderr); return 1
    suite=unittest.defaultTestLoader.discover(str(SCRII/"tests"),pattern="test_v002_*.py")
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful(): return 1
    print("SCR-II v002 prep validation: PASS")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
