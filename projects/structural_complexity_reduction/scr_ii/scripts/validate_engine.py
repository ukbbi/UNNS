from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path

HERE = Path(__file__).resolve()
SCRII = HERE.parents[1]
PROJECT = SCRII.parent
sys.path.insert(0, str(SCRII))

from engine_common import ENGINE_VERSION

def main():
    prereg = SCRII / "SCR_II_PREREG_v001"
    if not prereg.is_dir():
        print("FAIL missing SCR_II_PREREG_v001"); return 1

    p = subprocess.run([sys.executable, str(prereg/"scripts"/"validate_prereg.py")],
                       cwd=prereg, text=True, capture_output=True)
    print(p.stdout.strip())
    if p.returncode != 0:
        print(p.stderr); return 1

    suite = unittest.defaultTestLoader.discover(str(SCRII/"tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        return 1

    print(f"{ENGINE_VERSION} validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
