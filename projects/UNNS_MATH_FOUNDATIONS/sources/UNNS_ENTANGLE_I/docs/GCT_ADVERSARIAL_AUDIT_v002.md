# GCT v002 — Adversarial Audit and Frozen Stopping Rule

The goal is **not** to find favorable CHSH settings by sweeping model parameters. The settings are fixed before comparing models:

\[
a=0,\; a'=\pi/2,\; b=\pi/4,\; b'=-\pi/4.
\]

The alternative kernels were selected to test **uniqueness** rather than fit data. The smooth countermodel parameter K=6 is explicit and fixed. All are evaluated with the same joint event rules and no-signalling test.

## Expected outcomes

| Model | Target \(|S|\) | Why included |
|---|---:|---|
| Bell-local angular overlap | 2 | Common-source control satisfying factorization |
| Quarantined quantum singlet | \(2\sqrt2\) | Reference only, not generated from UNNS |
| Smooth saturated context kernel | ~3.9984 | Falsifies the claim that no-signalling/symmetry impose Tsirelson's bound |

## Pass/fail gates

- J0: Original v001 lock and negative verdict byte-for-byte preserved.
- J1: Representation theorem proved in documentation and checked numerically.
- J2: Recursive stationary law proved and checked under fixed refresh r=0.3.
- J3: Operational marginals equal 1/2 for all test contexts.
- J4: Local witness produces CHSH=2 at the frozen settings.
- J5: At least two additional distinct admissible kernels share the same conditions but yield different correlations.
- J6: Context dependence and failure of Bell-local factorization explicitly disclosed.
- J7: Independent UNNS selection of the correlation kernel **not established**.
- J8: Born-rule derivation **not established**.

## Falsification conclusion

If J0–J6 pass while J7–J8 remain open, the correct mathematical verdict is **underdetermination**. We must not relabel it as a positive derivation merely because one comparator reaches the quantum CHSH value.

## No automatic next phase

The stopping rule is applied. The next research action, if desired, is not another q-family, spectral, or projection experiment; it is to exhibit an independent, canonical UNNS axiom selecting the correlation kernel, or close the derivation claim as unsupported by current axioms.
