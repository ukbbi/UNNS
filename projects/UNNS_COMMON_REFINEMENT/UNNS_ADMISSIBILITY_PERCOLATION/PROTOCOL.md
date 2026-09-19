# PROTOCOL v0.2

## Status

**PREREGISTERED INPUTS FROZEN — CHAMBERS NOT YET RUN**

## 1. Objective

Test whether exact algebraic factor-traceability status has a reproducible
perturbative/percolative phenotype under two frozen UNNS structural chambers.

This is a comparative diagnostic experiment, not a proof experiment.

## 2. Ground truth

Each system is labeled before chamber analysis:

- `TRACEABLE`
- `NON_TRACEABLE`

Ground truth comes from the exact algebraic results of the parent
`UNNS_COMMON_REFINEMENT` project.

The chamber outputs cannot change those labels.

## 3. Frozen chambers

- STRUC-I v1.0.4
- STRUC-PERC-I v2.5.0

The chamber files in `chambers/` are immutable for experiment v0.1.

## 4. Preregistered corpus

The corpus contains 30 systems, six per class:

- `INT_FREE`
- `R1_FREE`
- `R1_FAIL`
- `AFF_FREE`
- `AFF_FAIL`

The exact system definitions and evidence are stored in:

`corpus/cases/`

The frozen index is:

`corpus/CORPUS_INDEX.csv`

The algebraic build audit is:

`corpus/CORPUS_AUDIT.json`

## 5. Primary ladder

The first experiment uses only the label-blind:

`SYSTEM_SPECTRUM`

defined in:

`adapters/ADAPTER_SPEC.md`

Each ladder contains the first 128 certified-complete scalar levels of the exact
monoid system.

This is a protocol refinement made **before any chamber run**.

The earlier idea of using route/refinement/failure-witness ladders is deferred to
a later secondary analysis because those encodings would place the exact witness
too close to the chamber input and could confound the primary phenotype question.

## 6. Chamber inputs

STRUC-I:

`inputs/struc_i/ALL_SYSTEM_SPECTRA.csv`

STRUC-PERC-I batch directory:

`inputs/struc_perc_i/`

## 7. Primary observables

STRUC-I:

- regime/state
- mean A_k
- min A_k
- mean rho
- max rho

STRUC-PERC-I:

- verdict tier
- giant ratio
- kappa_connect
- isolated fraction
- tail dominance

## 8. Primary comparisons

Report:

- TRACEABLE versus NON_TRACEABLE direction;
- within-class spread;
- cross-domain consistency;
- rank-one failure versus affine failure contrast;
- explicit failures of separation.

Do not report a single combined winner/score.

The 30 systems are a structural pilot corpus, not an iid population sample.

## 9. Falsification conditions

The structural-phenotype hypothesis is weakened if:

- profiles substantially overlap across exact labels;
- apparent separation is confined to one family;
- effect direction reverses across families;
- rank-one and affine failures do not show a coherent distinction;
- conclusions depend on changing the frozen adapter after results are seen.

A null result is valid.

## 10. Freeze sequence

Completed before chamber execution:

1. exact labels built and audited;
2. `CORPUS_INDEX.csv` frozen;
3. `ADAPTER_SPEC.md` frozen;
4. `SYSTEM_SPECTRUM` inputs built;
5. chamber hashes retained;
6. `FREEZE_RECORD.json` written and verified.

Next:

7. run STRUC-I;
8. retain raw STRUC-I outputs;
9. run STRUC-PERC-I batch;
10. retain raw STRUC-PERC-I outputs;
11. synthesize only after both raw result sets are fixed.
