# CONTEXT

Project: `UNNS_ADMISSIBILITY_PERCOLATION`

Former provisional name: `UNNS_TRACEABILITY_PHENOTYPE`

Parent corpus source: `UNNS_COMMON_REFINEMENT`

## Why the project was renamed

A closer audit of the chamber implementations makes the scientific division clear:

- STRUC-I measures perturbative **admissibility** of ordered ladders.
- STRUC-PERC-I measures **percolative connectivity** of the full pairwise gap-vulnerability graph.
- algebraic factor traceability / common refinement is an independent property of the source systems.

The earlier folder name made the algebraic label sound like the chamber target. It is not.

The rename occurred after the first STRUC-I run and before the STRUC-PERC-I run.

No frozen experimental input was changed.

## Current scientific question

How do perturbative admissibility and percolative connectivity relate on the same frozen ladder
corpus?

A secondary comparison asks whether independently known algebraic route-closure status correlates
with either chamber output.

## STRUC-I role

STRUC-I v1.0.4 evaluates:

```text
inv(P_epsilon ; L) <= nu(V_epsilon(L))
```

and estimates the admissibility rate `A_kappa`.

Its primary output is the admissibility regime/state taxonomy.

Its `rho` structural-pressure diagnostic is secondary.

## STRUC-PERC-I role

STRUC-PERC-I v2.5.0 constructs the full pairwise graph on gap values and follows component structure
over kappa.

Its primary output is one of:

```text
FULL_PERCOLATION
GIANT_COMPONENT_PERCOLATION
TAIL_FRAGMENTATION
HARD_FRAGMENTATION
```

The chamber treats `HARD_FRAGMENTATION` on original non-downsampled data as triggering the
established necessary-direction PRP theorem.

The sufficient direction from percolation to admissibility remains open.

## Current state

Status:

`STRUC-I COMPLETE — v2.5.0 RAW COMPLETE — v2.5.1 AUDIT/REPAIR READY`

The frozen 30-system corpus and 128-level `SYSTEM_SPECTRUM` inputs remain unchanged.

STRUC-I raw results, profiles and evidence are retained under:

`outputs/struc_i/`

The STRUC-I result is uniform at the core classification level:

```text
30 / 30:
Geometric Persistence / Stable Structure

mean_Ak = 1.0
min_Ak  = 1.0
```

Therefore all 30 frozen ladders are perturbatively admissible under STRUC-I.

This includes source systems with different algebraic route-closure status.

## Interpretation boundary

Do not describe STRUC-I as a traceability classifier.

Do not describe STRUC-PERC-I as a traceability classifier.

The algebraic labels remain useful as controlled metadata, but the principal branch now concerns
the relation:

```text
perturbative admissibility
        versus
percolative connectivity
```

## STRUC-PERC-I raw batch

The 30-file STRUC-PERC-I v2.5.0 batch has been completed and retained under:

`outputs/struc_perc_i/`

Raw verdicts:

```text
25 FULL_PERCOLATION
4 HARD_FRAGMENTATION
1 TAIL_FRAGMENTATION
```

These five non-full cases activated the predeclared audit condition because STRUC-I had found all
30 ladders fully admissible.

The deterministic audit in:

`outputs/records/CROSS_CHAMBER_AUDIT_001.md`

reproduces the batch and identifies two implementation-sensitive causes:

- premature adaptive-extension plateau stopping;
- near-zero IQR treated as a positive scale in `AFF04`.

## Next move

Pause final synthesis.

Create a separately versioned STRUC-PERC-I audit/repair instrument that fixes only the identified
scale/extension issues, then rerun the same frozen 30 inputs.

Do not rerun STRUC-I.

## Frozen-history rule

Do not rewrite:

- `PROTOCOL.md`
- `adapters/ADAPTER_SPEC.md`
- `outputs/records/FREEZE_RECORD.json`

merely to replace the former project name.

Those files are part of the preregistration trail.

The post-run interpretive correction is documented separately in:

`PROTOCOL_AMENDMENT_001.md`
`RENAME_RECORD.md`

## Audit/repair chamber

Created:

`chambers/STRUC-PERC-I_AUDIT_v2_5_1/struc_perc_i_audit_v2_5_1.html`

The parent v2.5.0 chamber and raw results remain frozen.

Next: run v2.5.1 on the same 30 files and return both versioned batch exports.


## Completed v2.5.1 audit

The browser run of STRUC-PERC-I Audit v2.5.1 is complete.

All 30 frozen ladders eventually reached `FULL_PERCOLATION` when the exact finite-graph connectivity
threshold was explicitly probed.

This closes the implementation audit but changes the interpretation: eventual full percolation is
not a useful binary discriminator when kappa is allowed to reach the exact connectivity threshold.

The retained informative variable is:

`kappa_connect_exact`

See:

`outputs/synthesis/ADMISSIBILITY_PERCOLATION_SYNTHESIS.md`
`outputs/records/FINAL_PILOT_RESULT.json`

## Current frontier

The first pilot is closed.

Any next study should be separately preregistered around bounded-scale percolation, exact threshold
geometry, or component-growth profiles.
