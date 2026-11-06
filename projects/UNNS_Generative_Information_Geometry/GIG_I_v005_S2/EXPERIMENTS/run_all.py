import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s in ("E22_extract.py", "E23_families.py", "E24_atlas_coverage.py", "E25_refine.py", "E26_fresh_v2.py", "E27_assignment.py"):
    subprocess.check_call([sys.executable, os.path.join(here, s)] + (["300"] if s.startswith("E24") else []))
