# YM1A Refinement Ladder — Frozen Specification v1.0

## Status

This file freezes the first actual UNNS object for the Yang–Mills project.

**Object:** `YM1A refinement ladder`  
**Source corpus:** Athenodorou–Teper 2020 (`AT20`)  
**Measured refinement levels:** 8  
**Coordinates per level:** 5

No adversarial gapless family is introduced in this step. This object is the
physical reference branch against which the gapless construction will later be
tested.

## 1. Object definition

For each lattice refinement level `β_i`, define the labeled spectral vector

\[
L_i =
(c_1,c_2,c_3,c_4,c_5)_i
\]

with every coordinate expressed in the dimensionless scale

\[
M/\sqrt{\sigma} = (aM)/(a\sqrt{\sigma}).
\]

The complete refinement object is

\[
\mathcal{L}_{YM1A} =
(L_1,L_2,\ldots,L_8),
\]

ordered by increasing `β` and therefore decreasing `a√σ`.

The continuum extrapolation supplied by the paper is stored separately as a
reference and is **not** treated as a ninth measured refinement level.

## 2. Frozen coordinate order

The coordinate identities are frozen before the adversarial branch is built.

| ID | Channel | State | Meaning |
|---|---|---:|---|
| c1 | A1++ | 0 | ground state; lattice representative of the 0++ mass-gap state |
| c2 | A1++ | 1 | first A1++ excitation |
| c3 | E++ | 0 | E++ ground state |
| c4 | T2++ | 0 | T2++ ground state |
| c5 | A1-+ | 0 | A1-+ ground state |

These are the **only five channel/state identities present at all eight AT20
refinement levels**, so their selection is coverage-driven rather than
outcome-driven.

The order is an identity order, not a per-level mass ranking. It must not be
re-sorted separately at each β because doing so would erase coordinate identity
under refinement.

## 3. Dedicated mass-gap trajectory

`ym1a_gap.csv` stores the Table 1 mass-gap trajectory independently of `c1`.

This is intentional. `c1` comes from the detailed spectrum tables (7–13),
whereas the dedicated trajectory comes from Table 1. They describe the same
physical state but provide an internal source-consistency check.

At β = 5.8941 the publication reports:

- Table 1: `aM = 0.7991(92)`
- spectrum table: `aM = 0.799(10)`

Both are preserved. The difference is 0.0001 and is not silently reconciled.

## 4. Why the canonical ladder uses M/sqrt(sigma)

The raw lattice mass `aM` decreases as the lattice spacing decreases. That by
itself is not physical gap closing.

The canonical refinement coordinates therefore divide by the simultaneously
measured `a√σ`, removing the explicit lattice scale and producing the
dimensionless quantity used by the source paper for continuum extrapolation.

Raw `aM` values remain available in `ym1a_long.csv`.

## 5. Uncertainties

`ratio_err_indep` is supplied as a **diagnostic only** using ordinary
independent-error propagation.

The mass and string-tension estimates arise from the same ensembles and may be
correlated. The extracted corpus does not provide the covariance needed for a
strict propagated uncertainty. Therefore `ratio_err_indep` must not be treated
as a covariance-aware source uncertainty.

The primary UNNS object is the sequence of point estimates plus preserved source
errors, with uncertainty robustness handled separately.

## 6. Files

- `ladders/ym1a_refinement.csv` — canonical 8×5 refinement object
- `ladders/ym1a_long.csv` — source-preserving long form with raw `aM`
- `ladders/ym1a_gap.csv` — dedicated 0++ mass-gap trajectory
- `ladders/ym1a_continuum.csv` — published continuum references
- `output/ym1a_build.json` — build and invariant checks
- `scripts/ym1a/build.py` — reproducible object construction
- `scripts/ym1a/verify.py` — structural verification
- `scripts/ym1a/RUN_BUILD.bat`
- `scripts/ym1a/RUN_VERIFY.bat`

## 7. Frozen interpretation boundary

This object does **not** establish vacuum non-crossability.

It establishes the physical refinement branch and its coordinate identity. The
next stage must construct a gapless adversarial family without changing this
coordinate selection or normalization merely to improve separation.
