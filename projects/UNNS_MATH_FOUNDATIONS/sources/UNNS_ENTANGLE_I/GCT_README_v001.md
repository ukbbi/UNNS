# GCT v001 — UNNS Entanglement Generative Correlation Theorem

This is an **incremental overlay** for the existing `UNNS_ENTANGLE_I` project.
It does not replace any previous phase.

## Purpose
Return the project to the central question:

> Can a UNNS-style generative substrate produce Bell-violating entanglement correlations without importing quantum probabilities by hand?

## Contents
- `config/GCT_LOCK_v001.json`
- `docs/GCT_AXIOMS_v001.md`
- `docs/GCT_THEOREM_v001.md`
- `docs/GCT_BELL_AUDIT_v001.md`
- `docs/GCT_VERDICT_v001.md`
- `src/gct_generator_v001.py`
- `src/gct_verify_v001.py`
- `tests/test_gct_v001.py`
- `output/GCT_RESULTS_v001.json`

## Current status
The v001 lock preserves Bell-local factorization and measurement independence. Under those assumptions, Bell violation is not derivable.

Current verdict:
`NO_GO_WITH_LOCAL_FACTORIZATION`

## Run locally
```cmd
python -m unittest tests.test_gct_v001 -v
python -m src.gct_verify_v001
```
