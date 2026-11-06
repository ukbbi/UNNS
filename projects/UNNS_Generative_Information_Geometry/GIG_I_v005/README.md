# GIG_I_v005 (stage 1) — exact survival criterion for the common H₂ class; gates 1 and 3 are not necessary
Run: `python3 EXPERIMENTS/E19_bounding_lattice.py` (30 s), `E20_gate_counterexamples.py`, `python3 -m unittest discover -s TESTS` (7 tests).
`E21_construct_counterexamples.py [--write]` regenerates equivalent (not identical) counterexample certificates; the shipped certificates are the ones verified by E20.
Needs the frozen sibling folders GIG_I_v001..v004 (or env GIG_V001..GIG_V004). Results: RESULTS/report.md. Theory: THEORY/.
