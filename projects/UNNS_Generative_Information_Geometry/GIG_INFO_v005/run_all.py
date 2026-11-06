import subprocess, sys, os
R = os.path.dirname(os.path.abspath(__file__))
for s in ("A20_nerve_model.py", "A21_motifs.py", "A22_pair_anatomy.py", "A23_cone_criterion.py", "A24_S2_vs_dead_sets.py", "A25_star_intersection_lemma.py", "A26_cocycle_certificates.py",
          "B20_adjacency_cover.py", "B21_locality_boundary.py", "B22_triple_counterexample.py", "B23_two_triple_mechanism.py", "B24_symbolic_theorem_check.py", "G10_report.py", "make_manifest.py"):
    subprocess.check_call([sys.executable, os.path.join(R, "EXPERIMENTS", s)])
subprocess.check_call([sys.executable, os.path.join(R, "TESTS", "test_v005.py")])
