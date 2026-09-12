# Workflow

## Phase 0 — structure
Status: COMPLETE in v0.1

Repository architecture, data lineage, research questions and separation rules
are defined before acquisition.

## Phase 1 — source lock

Collect only source documentation and metadata first:

- official JHTDB forced-isotropic dataset description;
- README/provenance document;
- field definitions;
- coordinate and time conventions;
- acquisition method and authentication requirements;
- published energy spectrum and global time-history reference files.

Store these under `data/source/`.

No analysis is performed here.

## Phase 2 — acquisition pilot

Create a small, explicitly specified corpus of JHTDB cutouts.

Raw cutouts:
`data/raw/jhtdb/isotropic1024coarse/cutouts/`

Acquisition/provenance records:
`data/raw/jhtdb/isotropic1024coarse/meta/`

Each raw item must be traceable to:
dataset, time, index/coordinate bounds, stride/filter settings, requested fields,
retrieval method, retrieval timestamp and checksum.

## Phase 3 — validation

Tools under `tools/validate/` verify:

- shapes and component ordering;
- periodic-coordinate interpretation;
- time/index metadata;
- finite values;
- checksums;
- field units/conventions;
- basic statistical sanity;
- reproducibility of the raw-to-derived transformation.

Validation logs go to `outputs/logs/`.

## Phase 4 — physical derivation

Derived fields go under:

- `data/derived/fields/`   — vorticity, strain, enstrophy, helicity, etc.
- `data/derived/scales/`   — filtered/coarse-grained representations
- `data/derived/objects/`  — connected/coherent structural objects

Source cutouts are never overwritten.

## Phase 5 — controls

Matched controls are generated only from validated source/derived data.

Initial control families:

- `data/controls/phase_rand/`
  phase-randomized / spectrum-preserving controls where technically valid;

- `data/controls/amp_shuffle/`
  amplitude/spatial-shuffle controls used only when the intended invariant is
  explicitly stated.

Every control must document what was preserved and what was destroyed.

## Phase 6 — native turbulence ladders

Build scale-ordered UNNS turbulence ladders under:

`ladders/native/`

This representation is the scientific object of the project and must remain
independent of any one chamber input grammar.

## Phase 7 — chamber adapters

Transform native ladders into chamber-specific inputs:

- `ladders/struc_i/`
- `ladders/struc_perc_i/`

Adapter code lives under `tools/ladders/`.

Canonical STRUC-I and STRUC-PERC-I are not edited.

## Phase 8 — chamber runs

Chamber outputs are stored only as direct exports:

- `outputs/exports/struc_i/`
- `outputs/exports/struc_perc_i/`

These are outputs, never raw data.

## Phase 9 — structural analysis

Four parallel analysis tracks:

- `analysis/families/`       recurring admissibility/structural families
- `analysis/routes/`         parent->daughter and temporal route statistics
- `analysis/intermittency/`  relation to bursts / anomalous organization
- `analysis/controls/`       matched real-vs-control tests

## Phase 10 — synthesis

Human-readable products:

- reports: `outputs/reports/`
- figures: `outputs/figures/`
- tables: `outputs/tables/`
- machine-readable result records: `outputs/records/`

A result record must state the exact data corpus, transform versions, control
construction, chamber version, parameters and statistical comparison.
