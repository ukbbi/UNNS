import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s in ("E41_J_map.py", "E42_facet_theorem.py", "E43_retraction.py", "E44_sandwich_and_second_lift.py"):
    subprocess.check_call([sys.executable, os.path.join(here, s)])
