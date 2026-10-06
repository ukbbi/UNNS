# YM1A-G1 — Dual-Chamber Run Protocol

## Canonical instruments

- `chambers/struc_i_v104.html` — PRIMARY admissibility chamber.
- `chambers/struc_perc_i_v250.html` — SECONDARY connectivity/percolation diagnostic.

The chamber files are preserved byte-for-byte from the supplied canonical
versions. Do not edit them for YM1A.

## Inputs

All ready-made inputs are under:

`inputs/ym1a_g1/`

The index file `inputs/ym1a_g1/index.csv` records family, lattice level, k,
epsilon, beta, ensemble, and filename.

There are:

- 8 physical baseline files;
- 80 primary offset files;
- 80 upward-control files;
- 80 scale-null files;
- 80 gap-only files.

Total: 328 chamber-ready CSV files.

Each file contains the explicit vacuum `0` plus five positive spectral levels.

## STRUC-I v1.0.4 settings

Use the chamber's canonical defaults:

- MAX LADDER SIZE = 2000
- MC RUNS = 2000
- kappa steps = 40
- kappa min = 0.01
- kappa max = 1.0

Do not fit chamber settings to the YM result.

Because STRUC-I v1.0.4 uses unseeded browser randomness, any candidate
classification transition should later be repeated for stability. Do not modify
the chamber merely to insert a seed.

## STRUC-PERC-I v2.5.0 settings

Use:

- kappa grid points = 17
- kappa min = 0.01
- kappa max = 1.0
- domain adapter = Generic

Its result is a connectivity/percolation diagnostic, not a replacement for
STRUC-I admissibility.

## Primary sweep order

For each lattice level L01..L08:

1. Run `baseline/physical_Lxx.csv`.
2. Run `offset_Lxx_K01.csv` through `offset_Lxx_K10.csv`.
3. Record the first deformation whose STRUC-I regime/state differs from that
   level's physical baseline.
4. Repeat the matched `upctrl` sequence.
5. Run the `scale` and `gaponly` nulls.
6. Run the corresponding STRUC-PERC-I diagnostic sequence.

Do not insert new epsilon values until the preregistered coarse grid has been
fully recorded.

## G0.1 boundary criterion

Retain the already frozen cross-refinement rule:

1. primary-family boundary event at at least 6 of 8 refinement levels;
2. event present at all four finest levels;
3. qualifying first-boundary k values span no more than two dyadic steps;
4. upward massive control does not show the same event at equal or smaller
   deformation depth in at least 6 of 8 levels.

Null behavior is reported separately and used to determine specificity.

## Short-ladder limitation

Each vacuum-anchored YM1A ladder has 6 nodes / 5 gaps. This is sufficient for
the chamber input contract, but it is a short structural ladder. G1 is therefore
the first controlled probe, not the final Yang–Mills evidence layer.
