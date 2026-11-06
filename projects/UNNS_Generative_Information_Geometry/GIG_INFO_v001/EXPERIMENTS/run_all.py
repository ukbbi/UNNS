import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s in ("E01_information_recovery.py", "E02_relabeling.py", "E03_report.py"):
    subprocess.check_call([sys.executable, os.path.join(here, s)])
