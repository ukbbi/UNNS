# VREF-I/B Primary Report

**Source:** `CEA_2017_SU3`  
**Outcome:** **REFINEMENT-INDETERMINATE**

## Integrity

- deterministic extraction: VALID
- extracted CSV SHA-256: `a2a83c9a6d601b43ed6a51798192897b575fcf25b5b60f1ae5e015a3a2035d54`
- rows: 22
- common-grid points: 9
- common support: 0 to 0.761985714 fm
- primary tail cut: x >= 0.380 fm

## VREF path

- linear path: VACUUM-DIRECTED
- PCHIP path: VACUUM-DIRECTED
- interpolation-sensitive: false

## Refinement diagnostic

- tail common-grid points: 5
- chi2_ref / N_tail: 46.053751
- structured mismatch: true

## Floor-model comparison

| tail | family | Delta AICc = floor - zero | classification |
|---|---|---:|---|
| PRIMARY | exponential | 5.2380952 | UNDECIDED |
| PRIMARY | K0 | 5.2380952 | UNDECIDED |
| DROP-FIRST | exponential | 7.2 | ZERO |
| DROP-FIRST | K0 | 7.2 | ZERO |

Decisive threshold: `|Delta AICc| >= 6`.

Positive Delta AICc favors zero floor. Negative Delta AICc favors positive floor.

## Scope

This is a structural-vacuum-accessibility verdict in the frozen VREF representation. It is not a verdict that the physical Yang-Mills Hamiltonian mass gap vanishes or closes.
