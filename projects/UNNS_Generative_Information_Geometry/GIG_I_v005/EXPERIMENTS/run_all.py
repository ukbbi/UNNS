import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s in ("E19_bounding_lattice.py", "E20_gate_counterexamples.py"):
    subprocess.check_call([sys.executable, os.path.join(here, s)])
