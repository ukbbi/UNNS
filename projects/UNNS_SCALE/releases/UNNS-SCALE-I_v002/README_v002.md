# UNNS-SCALE-I v002 — Boundary Arithmetic and Hierarchical Composition

Folder `UNNS-SCALE-I_v002` sits beside the frozen v001 chamber `UNNS-SCALE-I`; nothing in v001 or at the project root is modified.

```
UNNS-SCALE-I_v002/
  SPEC_v002.md
  THEORY/UNNS_SCALE_I_THEORY_v002.md     theorems A1-A4, B1-B2, C1-C3, W, with proofs and cross-checks
  code/  scale_lib.py (copy of v001), boundary_lib.py, sieve_lib.py,
         run_A_boundary.py, run_B_composition.py, run_C_information.py, run_W_window.py, verify_all_v002.py, RUN_VERIFY_v002.bat
  results/   A_boundary.json B_composition.json C_information.json W_window.json
  reports/   VERIFICATION_REPORT_v002.md
  SHA256SUMS_v002.txt
```

Run: `python code/verify_all_v002.py` (Python 3.9+, numpy; about 20 s). It writes only inside this folder and never writes bytecode.
