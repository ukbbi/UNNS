# GCT v002 — Joint Origin of Quantum Correlations

**Incremental ZIP overlay** for the existing innermost `UNNS_ENTANGLE_I` project. Adds files, does not overwrite previous GCT or Chamber XVI results.

## Execute on Windows

From the existing project directory:

```cmd
python -m unittest discover -s tests -p "test_gct_joint_origin_v002.py" -v
python -m src.gct_joint_origin_v002
```

New output: `output/GCT_JOINT_ORIGIN_v002.json`.

## Scientific result

The joint-correlation representation and recursive stationary law are proved, but a countermodel family establishes that the listed symmetries and operational no-signalling do not uniquely determine quantum correlations.

**Verdict: `UNDERDETERMINED_NONLOCAL_GENERATIVE_RULE`**.

`src/gct_joint_core_v002.py` is an independent generic generator and does not import quantum probabilities; `src/gct_quantum_comparator_v002.py` explicitly contains the singlet reference for comparison only.

## Files

- `config/GCT_LOCK_v002.json` — frozen assumptions, thresholds, baseline hashes
- `docs/frozen/` — byte-identical v001 lock and result snapshot, not active replacements
- `docs/GCT_JOINT_THEOREM_v002.md` — four formal results and proofs
- `docs/GCT_GENERATIVE_CONSTRUCTION_v002.md` — route grammar and locality audit
- `docs/GCT_ADVERSARIAL_AUDIT_v002.md` — preregistered countermodel audit
- `docs/GCT_VERDICT_v002.md` — unambiguous scientific verdict
- `src/gct_joint_core_v002.py` — generic recursion and joint probabilities
- `src/gct_countermodels_v002.py` — local and superquantum controls
- `src/gct_quantum_comparator_v002.py` — quarantined quantum target
- `src/gct_joint_origin_v002.py` — deterministic research runner
- `tests/test_gct_joint_origin_v002.py` — formal/numerical regression tests
- `output/GCT_JOINT_ORIGIN_v002.json` — resulting report

No additional pip packages are needed.
