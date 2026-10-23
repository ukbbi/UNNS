# UNNS Entanglement I — Phase 3: Structural Measure Representation

Incremental overlay for the existing innermost `UNNS_ENTANGLE_I` directory. Merge folders. Nothing in Phase 0, 1, 2, 2B or 2C is replaced. A byte-identical Phase 2C outcome is placed in `output/frozen/` and checksum-locked.

Run from the project root using Python 3.12+ and standard library only:

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.measure_rep_phase3_v001
```

Report: `output/MEASURE_REP_PHASE3_v001.json`. Windows Smart App Control may block downloaded BAT scripts; direct Python commands above are preferred.

## New theorem target

Replace the earlier *derive q=2 from structural recurrence* target with a **conditional representation problem**: identify a rigorous bridge from generative event equivalence and exclusive alternatives to a normalized, measurement-noncontextual probability assignment over projection lattices. Study whether standard representation hypotheses can be obtained from independent UNNS operations, instead of declaring that they follow from proto-closure.

The model provides a context-label counterexample, a dimension-two obstruction to automatic use of Gleason's theorem, and finite dimension-three frame tests. None derives the Born rule; standard quantum density-matrix probabilities are a labelled reference, not substrate output.

Read `docs/PHASE3_SPEC.md` and `docs/PHASE3_THEOREM_AUDIT.md` before interpreting the JSON verdict.
