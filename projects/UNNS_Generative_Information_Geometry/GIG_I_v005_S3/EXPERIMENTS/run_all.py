import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s, a in (("E28_h3_certificates.py", []), ("E29_lift_pairs.py", []), ("E30_arithmetic_census.py", ["30"]), ("E31_verify_regimes.py", ["30"]), ("E32_lift_all_classes.py", [])):
    subprocess.check_call([sys.executable, os.path.join(here, s)] + a)
