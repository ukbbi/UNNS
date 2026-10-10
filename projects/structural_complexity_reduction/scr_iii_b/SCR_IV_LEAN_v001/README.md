# SCR_IV_LEAN_v001 — stages IV-1 and IV-2

Lean 4 (core only) formalisation of the frozen SCR-III 4×4 instance: 40 spins, 16 ice-rule vertices, exact rational Hamiltonian, and the two frozen witnesses.
Status and limits: **CERT_STATUS.md**. Run: `bash RUN_TEST.sh` (needs `lean`/`lake` 4.34.1 via elan, and Python 3). `lean-toolchain` pins v4.34.1.

| File | Role |
|---|---|
| `SCR_IV_Spins.lean` | spin decoding, ID validity, injectivity |
| `SCR_IV_Data.lean` | GENERATED: 780 exact coefficients (`kRows`/`kShift`), 16 vertices, reported doubles, claimed constants |
| `SCR_IV_Grammar.lean` | 2-in/2-out predicate, violation counts, vertex-table checks |
| `SCR_IV_Hamiltonian.lean` | exact Hamiltonian (two implementations) |
| `SCR_IV_Witness.lean` | IV-2 theorems for the two witnesses |
| `SCR_IV_Bound.lean`, `SCR_IV_Certificate.lean` | IV-3 … IV-5: PENDING stubs |
| `SCR_IV_Check.lean` | `#print axioms` audit |
| `scripts/gen_lean_data.py` | frozen instance → Lean data, `data/coeff_bits.csv`, `data/instance_manifest.json` |
| `scripts/diff_test.py`, `scripts/scan_source.py` | differential test; forbidden-token scan |
| `tests/neg_*.lean` | negative controls (must fail) |
| `data/` | frozen instance copy (unmodified), provenance copy of `physical_energy_v005.py`, manifests |
| `output/` | logs of the run recorded in CERT_STATUS.md |
| `MANIFEST_SCR_IV_v001.json` | hashes of every file, toolchain, upstream SCR-III hashes |

To regenerate the data after changing the instance: `python3 scripts/gen_lean_data.py .` (the test compares against the committed files).
