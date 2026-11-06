# GIG-I v002 — Arithmetic Realizability and Graph–Topology Separation in UNNS Generative Histories

Independent, versioned, standard-library-only research package (Python ≥ 3.10) built **on top of** the frozen `GIG_I_v001` (imported unchanged from the sibling folder; set `GIG_V001=<path>` if it lives elsewhere).

**Read first:** `RESULTS/report.md` (mathematics before procedure). Theory: `THEORY/`. Certificates: `CERTIFICATES/`.

## Run
```
python -m unittest discover -s TESTS -v          # v002 tests + the 28 v001 tests (run as a subprocess) + v001 hash check
cd EXPERIMENTS && python run_all.py --quick       # minutes: small bounds
cd EXPERIMENTS && python run_all.py               # full: k=6 with labels <=10 and <=12, k=5 <=16, k=4 <=40  (~25 min)
python EXPERIMENTS/make_manifest.py               # refresh MANIFEST.json
RUN_V002.bat test|quick|full                      # Windows
GIG_FROZEN_SRC=<...>/GEO_HD_1D_v004/src python -m unittest discover -s TESTS   # optional frozen cross-check
```

## Layout
`ENGINE/` — `cube_factor` (T11), `threshold_closure` (T12), `cycle_types` (E5), `realizability` (E6), `graph_iso` (exact isomorphism, uncoloured and coloured), `cell_signature` (T13 reconstruction, T15 graph-only recovery, systole), `certificates` (witness records + independent verifier).
`EXPERIMENTS/` — `E5_cycles`, `E6_realizability`, `E7_graph_iso`, `E8_cell_info`, `run_all`, `make_manifest`.
`RESULTS/` — `results.json`, `search_coverage.json`, `report.md`.  `CERTIFICATES/` — one JSON per certificate; `ENGINE/certificates.verify_certificate` re-checks any of them from contents + sources alone.

## Conventions
Distinct-label contents only (the inherited permutohedral cell rule). Every record states its source convention: *fixed source* `m` for a given content; `source_squarefree` marks complete-history sources. Exact integer arithmetic throughout; deterministic seed 20261105 for all sampling.
