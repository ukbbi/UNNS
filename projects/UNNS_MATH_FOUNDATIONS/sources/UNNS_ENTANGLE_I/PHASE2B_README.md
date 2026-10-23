# Phase 2B — Proto-Closure to Observable Measure

Incremental overlay for the *existing innermost* `UNNS_ENTANGLE_I/` directory. The archive contains no replacements for Phase 0, 1, or 2 original files. It adds source, tests, specification, source baseline lock and byte-identical frozen JSON copies. **Do not create a new project nested within the existing one.**

## Run without .bat (Windows Smart App Control compatible)

From the project root in Command Prompt:

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_proto_measure_2b_v001
```

The second command writes `output/XVI_PROTO_MEASURE_2B_v001.json`. It checks the frozen Phase 1/2 report hashes and, if present, their active `output/` counterparts. A mismatched baseline triggers an unsuccessful process exit. The substantive theorem remains OPEN/BLOCKED regardless of test pass status.

## What is demonstrated

A deterministic two-state symbolic generator has a nontrivial period-two orbit before numerical evaluation. Mapping the states to orthogonal unit vectors admits conserved orbit weights `||v||^q` for every positive q, so proto-closure does not imply additive refinement weights. `q=2` is singled out only if orthogonal additivity is added as an independent premise. This is a source-grounded *counterexample audit*, not a derivation of physical Born probabilities or canonical Operator XVI.

The document basis is *Mechanisms, Structural Closure, and Proto-Closure in the UNNS Substrate* (user-supplied PDF, especially Definitions 3–9 and Appendix A Definition 12). The PDF is not redistributed.
