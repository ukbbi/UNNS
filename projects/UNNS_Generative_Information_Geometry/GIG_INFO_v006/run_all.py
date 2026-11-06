import subprocess, sys, os
R = os.path.dirname(os.path.abspath(__file__))
for s in ("D20_make_certificates.py", "C20_minimal_observation.py", "D21_minimal_observation_analysis.py", "G20_report.py", "make_manifest.py"):
    subprocess.check_call([sys.executable, os.path.join(R, "EXPERIMENTS", s)])
subprocess.check_call([sys.executable, os.path.join(R, "VERIFY", "standalone_verify.py")])
subprocess.check_call([sys.executable, os.path.join(R, "TESTS", "test_v006.py")])
