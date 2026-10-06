# SPEC_I_A_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 3 — Structural Continuity vs Spectral Discreteness  
**Branch:** SPEC-I/A — Primary Continuum Spectral Anchor  
**Status:** **FROZEN BEFORE STAGE-3 COEXISTENCE VERDICT**  
**Date:** 2026-10-05

## 1. Purpose

SPEC-I/A supplies the independent spectral side of Stage 3. It does not recompute or modify Stage 2.

Frozen structural input carried forward only as status:

```text
STAGE2 = NO-UNIVERSAL-STRUCTURAL-EXCLUSION-DETECTED
INTERPRETATION = STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED
```

No structural datum enters the spectral extraction. No spectral datum may rewrite Stage 2.

## 2. Canonical source

Primary source:

```text
Athenodorou & Teper
The glueball spectrum of SU(3) gauge theory in 3+1 dimensions
JHEP 11 (2020) 172
```

Canonical local file:

```text
data/raw/at20/Athenodorou-Teper2020_Article_TheGlueballSpectrumOfSU3GaugeT.pdf
SHA-256: af40f084cf4f4624224af726d0bb4822e449b161b03ce38972077023cbd0ca7c
```

Same-calculation source-version cross-check:

```text
data/raw/at20/2007.06422v2.pdf
SHA-256: f0eb6406bf49a00d376c0be25917173426c826050046a1bf0f32987895de23d0
```

These two PDFs are **not independent spectral confirmations**.

## 3. Frozen theory match

```text
pure SU(3) gauge theory
3+1 dimensions
continuum extrapolation
standard plaquette action
string tension sqrt(sigma) used as continuum energy scale
```

## 4. Frozen spectral observable

Primary state:

\[
J^{PC}=0^{++}
\]

Primary coordinate:

\[
oxed{\Delta_{m spec}=M_{0^{++}}/\sqrt{\sigma}}
\]

Source-adopted continuum value:

\[
oxed{3.405\pm0.021}
\]

Source-supplied alternate continuum extrapolation:

\[
oxed{3.391\pm0.023}
\]

The source explicitly adopts the first value. The second is retained as the preregistered source sensitivity.

## 5. Vacuum reference

The source's spectral construction measures energies relative to the vacuum and sets the vacuum energy to zero once the temporal extent is large enough. For vacuum quantum numbers, the nontrivial state of interest is the first excited state above the vacuum.

The source explicitly identifies the lightest `0++` glueball as the theory's mass gap.

Operationally:

\[
E_0=0,\qquad E_1=M_{0^{++}},\qquad \Delta E=E_1-E_0.
\]

## 6. Positivity and robustness rules

Primary positivity:

```text
3.405 - 0.021 > 0
```

Source-sensitivity robustness:

```text
3.391 - 0.023 > 0
```

Both must hold. No GeV conversion is used for the primary Stage-3 spectral anchor.

Allowed SPEC-I/A statuses:

```text
SPECTRAL-SCALE-POSITIVE
SPECTRAL-SCALE-INDETERMINATE
SOURCE-MISMATCH
EXTRACTION-INVALID
```

## 7. No-retuning rule

After this freeze do not:

- replace `M_0++/sqrt(sigma)` with another scale;
- change the primary state;
- average the two continuum extrapolations;
- count JHEP and arXiv versions as independent confirmation;
- convert to GeV for the primary verdict;
- let spectral data modify Stage 2;
- issue the Stage-3 coexistence verdict before SPEC-I/B is independently acquired and frozen.

## 8. Next executable action

Run:

```text
RUN_SPEC_I_A_EXTRACT.bat
```

It verifies both PDFs, extracts the frozen source statements, and writes the SPEC-I/A spectral result only.
