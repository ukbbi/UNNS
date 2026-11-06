import subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__))
for s in ("E33_filling_independence.py", "E34_filling_dependence.py", "E35_verify_dependence.py", "E36_role_map_correction.py", "E37_h3_to_h4.py", "E38_h4_arithmetic.py", "E39_reduction_check.py", "E40_h4_certificates.py"):
    subprocess.check_call([sys.executable, os.path.join(here, s)] + (["36"] if s.startswith("E38") else []))
