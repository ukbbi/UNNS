import subprocess, sys, os
R = os.path.dirname(os.path.abspath(__file__))
for s in ("F10_features.py", "F11_minimal_signatures.py", "F12_nontriviality.py", "F13_distinct_masks.py", "F14_sharp_witness.py", "F15_witness_certificates.py", "F16_second_order_pool.py", "F17_witness_anatomy_and_naming.py", "F18_unresolved66_extended.py",
          "H20_heldout.py 6 2", "H20_heldout.py 7 2", "H21_evaluate.py", "H22_heldout_diagnostics.py", "G10_report.py", "make_manifest.py"):
    subprocess.check_call([sys.executable, os.path.join(R, "EXPERIMENTS", s.split()[0])] + s.split()[1:])
subprocess.check_call([sys.executable, os.path.join(R, "TESTS", "test_v003.py")])
