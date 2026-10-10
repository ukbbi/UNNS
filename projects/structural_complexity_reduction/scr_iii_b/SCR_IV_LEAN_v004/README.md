# SCR_IV_LEAN_v004 — stages IV-1 to IV-4B

Lean 4 (core only) formalisation of the frozen SCR-III 4×4 instance. v004 adds IV-4B (frontier certificates for the ground and corrected non-grammar objectives, `Bat/`, `Fin_*.lean`, `SCR_IV_V4.lean`; read CERT_STATUS.md first: it records a correction of 928/2^70 to the frozen non-grammar value). v003 added the certificate design and checker (IV-4A) on top of v002 (IV-3) and the unchanged v001 sources (`SCR_IV_Spins/Data/Grammar/Hamiltonian/Witness/Check/Certificate.lean` are byte-identical to v001).
Status and limits: **CERT_STATUS.md**. Solver cross-reference: **SOLVER_CROSSREF.md**. Run: `bash RUN_TEST.sh` (add `FULL=1` to re-check all 1,148 batches, ~1.5 h on 2 cores, ≤3.3 GB per process) (needs `lean`/`lake` 4.34.1 via elan, and Python 3). `lean-toolchain` pins v4.34.1.

| File | Role |
|---|---|
| `SCR_IV_Spins/Data/Grammar/Hamiltonian/Witness.lean` | IV-1/IV-2 (unchanged from v001) |
| `SCR_IV_Sums.lean` | finite sums with structural recursion (split, swap, monotonicity) |
| `SCR_IV_Bound.lean` | IV-3 abstract theory: decomposition, lower bound, pruning with ties, spin-level partition |
| `SCR_IV_Bridge.lean` | `hScaled id = Hs 40 kAt (sigmaAt id)` for every id |
| `SCR_IV_Solver.lean` | loop-faithful transcription of `solver_v010.cpp::bound` and the path accumulator; equality with `Bnd` |
| `SCR_IV_Prune.lean` | id-level pruning/partition, C++ grammar filter and `violates()`, objectives kept distinct, discard theorems |
| `SCR_IV_Cert.lean` | IV-4A generic checker `chk`/`checkAll` + soundness |
| `SCR_IV_Part.lean` | IV-4A partitioned certificates: `stateAt`, `subOK`, `frontier_sound`, batch assembly |
| `SCR_IV_CertReal.lean` | IV-4A conditional global theorems on the frozen instance |
| `SCR_IV_Check4.lean` | IV-4A axiom audit |
| `IV4A_DESIGN.md` | format, invariant, estimates, IV-4B gates |
| `scripts/cert_tools.py` | untrusted certificate encoder + toy/calibration generators |
| `SCR_IV_Certificate.lean` | IV-4/IV-5: PENDING stub (unchanged) |
| `SCR_IV_Check.lean`, `SCR_IV_Check3.lean` | `#print axioms` audits (25 IV-1/IV-2 theorems; 44 IV-3 theorems) |
| `scripts/` | `gen_lean_data.py`, `diff_test.py` (v001, unchanged), `diff_test3.py` (IV-3), `scan_source.py` |
| `tests/` | `neg_*.lean` negative controls (must fail), `pos_controls.lean` (must compile) |
| `data/` | frozen instance copy (unmodified), provenance copies of `physical_energy_v005.py` and `solver_v010.cpp` |
| `output/` | logs of the recorded run |
| `MANIFEST_SCR_IV_v003.json` | hashes of every file, toolchain, upstream SCR-III hashes |
