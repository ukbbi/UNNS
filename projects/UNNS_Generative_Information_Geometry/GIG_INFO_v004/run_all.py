import subprocess, sys, os
R = os.path.dirname(os.path.abspath(__file__))
# registration of SYM-6 precedes C12 (THEORY/PREREGISTRATION.md)
for s in ("C10_symbolic_sweep.py", "C11_symbolic_information.py", "C12_sym6_digraphs.py", "C13_sym6_stress.py", "C15_prereg_evaluation.py", "B10_information_profiles.py", "B11_out_of_sample.py", "A10_alexander_duality.py", "A11_seven_hard_positives.py",
          "A12_scope_hierarchy.py", "A13_collision_concordance.py", "A15_stronger_signatures_PF.py", "A14_certified_counterexample.py", "A16_dead_subsets.py", "C14_beta1_transfer.py", "G10_report.py", "make_manifest.py"):
    subprocess.check_call([sys.executable, os.path.join(R, "EXPERIMENTS", s)])
subprocess.check_call([sys.executable, os.path.join(R, "TESTS", "test_v004.py")])
