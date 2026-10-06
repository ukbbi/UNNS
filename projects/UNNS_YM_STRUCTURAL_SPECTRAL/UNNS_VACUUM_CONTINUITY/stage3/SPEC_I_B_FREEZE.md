# SPEC_I_B_FREEZE.md

**Project:** `UNNS_VACUUM_CONTINUITY`  
**Stage:** 3 — Structural Continuity vs Spectral Discreteness  
**Branch:** SPEC-I/B — Independent Continuum Spectral Control  
**Status:** **FROZEN BEFORE BRIDGE-III VERDICT**  
**Date:** 2026-10-06

## Purpose

SPEC-I/B is the genuinely independent spectral control for Stage 3. It is independent of the Athenodorou–Teper SPEC-I/A calculation.

Frozen inputs carried forward, without retuning:

```text
Stage 2 interpretation:
STRUCTURAL-VACUUM-ACCESSIBILITY-SUPPORTED

SPEC-I/A:
SPECTRAL-SCALE-POSITIVE
```

SPEC-I/B may not modify either result and may not itself issue the Stage-3 coexistence verdict.

## Canonical source

Y. Chen et al., *Glueball Spectrum and Matrix Elements on Anisotropic Lattices*, Phys. Rev. D 73, 014516 (2006), arXiv:hep-lat/0510074.

Canonical local file:

```text
data/raw/chen06/chen06.pdf
```

Expected SHA-256:

```text
66973cf81063071cf5c58d93cff86d4778b7d8f11e83eb1f3b89a21be3047f22
```

## Theory / continuum status

The source is a pure SU(3) gauge-theory lattice calculation using anisotropic lattices and improved operators/actions. Five independent lattice spacings are used and the source reports continuum extrapolation of the glueball spectrum.

For the scalar `A1++` channel, the correlator construction explicitly subtracts the vacuum expectation value before extracting the nontrivial state.

## Frozen spectral coordinate

Primary state:

```text
J^PC = 0++
```

Native continuum coordinate:

```text
Delta_spec,B = r0 * M_0++
```

Final source value:

```text
r0 M_0++ = 4.16(11)(4)
```

Quoted uncertainties:

```text
first  = statistical uncertainty from continuum extrapolation = 0.11
second = 1% uncertainty from approximate anisotropy           = 0.04
```

The quoted `1710(50)(80) MeV` is retained only as provenance and is not the Stage-3 control coordinate.

## Frozen positivity rule

Use the conservative linear bound:

```text
L_B = 4.16 - 0.11 - 0.04
```

SPEC-I/B is `SPECTRAL-SCALE-POSITIVE` only if `L_B > 0`.

Quadrature combination is recorded for provenance only and cannot control the verdict.

## Source-supplied historical comparison

Table VIII also quotes the earlier Ref. [4] value:

```text
r0 M_0++ = 4.21(11)
```

This is a historical source check only and is not counted as another Stage-3 branch.

## Allowed statuses

```text
SPECTRAL-SCALE-POSITIVE
SPECTRAL-SCALE-INDETERMINATE
SOURCE-MISMATCH
EXTRACTION-INVALID
```

## Prohibited operations

Do not:

- convert SPEC-I/B into `M/sqrt(sigma)` merely to resemble SPEC-I/A;
- average SPEC-I/A and SPEC-I/B;
- use the GeV mass as the primary branch coordinate;
- change the scalar state after seeing the result;
- combine uncertainties in a way that strengthens the verdict;
- count the quoted Morningstar–Peardon value as another Stage-3 branch;
- modify Stage 2 or SPEC-I/A;
- issue BRIDGE-III from inside SPEC-I/B.

## Immediate executable action

Run:

```text
RUN_SPEC_I_B_EXTRACT.bat
```

Only after successful SPEC-I/B execution may BRIDGE-III be preregistered and evaluated.
