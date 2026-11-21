# QTI-I baseline independent read-only audit — 21 November 2026

Source: user-supplied `QUANTUM_TELEPORTATION.zip`. No original source or archived result was modified.

## Scope

* `independent_audit.py` recomputes `R` and maximal square-divisor roots for all 18,647 included counter gaps using `sympy.factorint`, and checks against the source CSV and results.json. It also independently reconciles forward/backward history counts for every integer 1..3000.
* `block_permutation_audit.py` computes adjacent shared-square-divisor-root and adjacent nonempty-fibre counts after dividing each stream into non-overlapping 128-record local windows. Excluded records break adjacency. A seeded 1,400-replicate within-window permutation null preserves local marginal distributions, but not timing correlation or acquisition cycles. Results are exploratory; no multiple-testing correction or preregistered thresholds.
* Original QTI-I v001 archived results have **12 named verification groups** with `ok:true`, not 15 groups as stated in its NOTES.md. The original full slow verifier was attempted but not completed within the review execution budget; the two independent scripts above passed.
* The raw .pt files and independently calibrated clock/channel documentation are absent from the user-supplied archive; all audits start from supplied CSVs.

## Reproduce

From the audit folder, if your existing `QUANTUM_TELEPORTATION` directory is a sibling, run:

```bash
python3 independent_audit.py
python3 block_permutation_audit.py
```

Dependencies: Python, numpy, sympy. Alternatively append the path to your `QUANTUM_TELEPORTATION` directory as the first command-line argument. Results are written into the audit folder. The baseline is never overwritten.

## Interpretation

First-order integer gap nesting is mostly representation-driven; no quantum-teleportation-specific signal is established. One stream has a marginal within-block shared-root excess (empirical p ~ 0.046) while the other two do not. This exploratory comparison does not survive a three-stream multiplicity correction.
