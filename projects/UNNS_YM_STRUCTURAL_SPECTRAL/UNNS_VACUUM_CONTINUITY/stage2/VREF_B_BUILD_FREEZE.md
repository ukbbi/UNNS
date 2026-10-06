# VREF_B_BUILD_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 2  
**Branch:** VREF-I/B — Structural Vacuum Accessibility  
**Status:** **FROZEN — IMPLEMENTATION ADDENDUM BEFORE PRIMARY FIT**  
**Date:** 2026-10-05

## 1. Extraction gate

The local deterministic extraction completed with:

```text
EXTRACTION-VALID
rows = 22
R1 points = 11
R2 points = 11
```

The primary chamber accepts only the exact extracted CSV with SHA-256:

```text
a2a83c9a6d601b43ed6a51798192897b575fcf25b5b60f1ae5e015a3a2035d54
```

The extraction JSON must independently report `EXTRACTION-VALID`, the expected source/EPS hashes, and the same CSV hash.

## 2. Natural-units clarification

`PREREG_VREF_B.md` writes the dimensionless VREF coordinate schematically as

\[
z=d^2E_l.
\]

The executable implementation freezes the dimensionally explicit form

\[
\boxed{
z=
\left(
\frac{d_{\rm fm}}{\hbar c}
\right)^2E_l
}
\]

with

\[
d_{\rm fm}=0.76\ {\rm fm},
\qquad
\hbar c=0.1973269804\ {\rm GeV\,fm}.
\]

This is a unit clarification only. It does not alter the ordering, monotonicity, interpolation comparison, or asymptotic floor models.

## 3. Common-grid path audit

The common grid remains the R1 native grid truncated to two-resolution common support.

All available five-point fixed-width windows are audited. This prevents selection of a favorable subset after seeing the result.

For each window the exact pointwise-box RMS envelope is computed. A reversal is **material** only when

\[
D_{\rm next}^{\min}>D_{\rm previous}^{\max}.
\]

Central-value increases whose uncertainty envelopes overlap are not classified as material reversals.

The path verdict is `VACUUM-DIRECTED` when no material reversal occurs.

Linear and PCHIP mappings must give the same path verdict. Otherwise the final result is:

```text
INTERPOLATION-SENSITIVE
```

## 4. Refinement-indeterminacy rule

For every common-grid tail point \(x\ge0.38\) fm,

\[
Q_j=
\frac{E_1-E_2}
{\sqrt{\sigma_1^2+\sigma_2^2+\sigma_{\rm EPS}^2}}.
\]

A **structured refinement mismatch** is frozen as:

> at least two consecutive tail common-grid points with the same sign of \(Q\) and \(|Q|\ge3\).

A single isolated \(3\sigma\) point does not trigger the rule.

If the rule is triggered, the primary verdict is:

```text
REFINEMENT-INDETERMINATE
```

rather than continuity or isolation.

The chamber also reports \(\chi^2_{\rm ref}/N_{\rm tail}\) descriptively, but no second threshold is introduced.

## 5. Nonlinear-fit algorithm

The four preregistered models are fitted by deterministic weighted nonlinear least squares.

Constraints:

\[
A_1>0,\quad A_2>0,\quad \lambda>0,\quad \delta\ge0.
\]

The optimization uses deterministic multistart seeds:

\[
\lambda/d\in
\left\{
\frac1{16},
\frac18,
\frac14,
\frac12,
1,
2
\right\}.
\]

For positive-floor models, the \(\delta\) starts are:

```text
0
0.25 * min(tail E)
0.50 * min(tail E)
1.00 * min(tail E)
```

The minimum-\(\chi^2\) converged solution is retained.

No fit parameter is initialized or bounded using the desired scientific conclusion.

## 6. Tail-cut sensitivity

The preregistered sensitivity analysis drops exactly the first eligible native tail point from each refinement and changes nothing else.

For each family, the floor classification must agree between:

```text
PRIMARY_TAIL
DROP_FIRST_TAIL_POINT
```

A classification change is treated as instability and contributes to:

```text
UNCERTAINTY-LIMITED
```

unless the two model families themselves give opposite decisive conclusions, in which case `MODEL-SPLIT` has priority.

## 7. Outcome priority

The chamber applies the following deterministic priority:

1. source/extraction failure -> `EXTRACTION-INVALID`
2. linear/PCHIP path disagreement -> `INTERPOLATION-SENSITIVE`
3. structured refinement mismatch -> `REFINEMENT-INDETERMINATE`
4. opposite decisive floor conclusions from exponential and K0 families -> `MODEL-SPLIT`
5. both families decisively favor a stable positive floor on both tail cuts -> `ISOLATION-SUPPORTED`
6. both families decisively favor zero floor on both tail cuts **and** the VREF path is vacuum-directed -> `CONTINUITY-SUPPORTED`
7. otherwise -> `UNCERTAINTY-LIMITED`

No additional outcome class may be invented after the run.

## 8. Scientific scope

A possible `CONTINUITY-SUPPORTED` result means only:

> within the frozen CEA_2017 VREF representation, the measured refinement-stable tail supports asymptotic approach to the zero-vacuum structural locus rather than a detected positive structural floor.

It does not imply:

\[
\Delta_{\rm YM}=0.
\]

A possible `ISOLATION-SUPPORTED` result likewise concerns this structural representation and is not by itself a proof of a positive Yang–Mills Hamiltonian mass gap.
