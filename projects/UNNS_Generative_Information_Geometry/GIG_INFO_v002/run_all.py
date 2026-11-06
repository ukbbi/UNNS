import subprocess, sys, os
R = os.path.dirname(os.path.abspath(__file__))
for s in ("E10_census.py 2", "E11_equal_count_pairs.py", "E12_pair_certificates.py", "E13_report.py", "make_manifest.py"):
    subprocess.check_call([sys.executable] + [os.path.join(R, "EXPERIMENTS", s.split()[0])] + s.split()[1:])
subprocess.check_call([sys.executable, os.path.join(R, "TESTS", "test_v002.py")])
