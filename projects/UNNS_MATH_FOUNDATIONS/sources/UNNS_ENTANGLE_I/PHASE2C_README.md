# Phase 2C — Proto-Closure to Observable Projection

Incremental overlay for the existing **innermost** `UNNS_ENTANGLE_I` directory. Merge `config/`, `docs/`, `src/`, `tests/`, `output/` without deleting or overwriting existing Phase 0/1/2/2B files. New files have unique `2C` names.

## Run in Windows Command Prompt (Python 3.12+)

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_proto_projection_2c_v001
```

Expected new report: `output\XVI_PROTO_PROJECTION_2C_v001.json`.

## Frozen Phase 2B
`output/frozen/XVI_PROTO_MEASURE_2B_v001.json` is a byte-identical copy of the user-supplied Phase 2B output, hash locked in `config/PHASE2C_LOCK.json`. The runner also checks `output/XVI_PROTO_MEASURE_2B_v001.json`, if present, and refuses to report integrity PASS when changed. It does not regenerate earlier reports.

## Research interpretation
The demonstration is a source-grounded *negative control*, not the construction of a physical measurement rule. A two-state proto-closed orbit admits different observation projections and radial powers, so recurrence by itself does not yield orthogonal additivity or the Born rule. C3/C4 remain open. This package does not claim to implement canonical Operator XVI.

Specification: `docs/PHASE2C_SPEC.md`.
