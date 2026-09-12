# 04_CHAMBER_RUN_PLAN_TCV.md

## Decision

Yes, run the TCV CSVs in both chambers, but only after converting them into chamber-ready scalar ladders.

## Do not run directly

Avoid feeding these directly into either chamber:

```text
tcv_lh_events_canonical.csv
tcv_lh_events_raw_flat.csv
```

## Reason

The original CSV files are multivariate event tables. Both uploaded chambers operate on scalar ordered ladders. Therefore, a direct run would produce parser artifacts:

- STRUC-I would likely select one unintended numeric field.
- STRUC-PERC-I would flatten all numeric columns into one mixed-unit ladder.

## Correct inputs

Use the prepared files in this pack.

### STRUC-I v1.0.4

Run:

```text
chamber_inputs/STRUC_I_v1_0_4/tcv_lh_core_LH_only__struc_i_long.csv
```

Then run:

```text
chamber_inputs/STRUC_I_v1_0_4/tcv_lh_core_all_events__struc_i_long.csv
```

### STRUC-PERC-I v2.5.0

Use batch mode:

```text
chamber_inputs/STRUC_PERC_I_v2_5_0/lh_only/*.csv
```

Then:

```text
chamber_inputs/STRUC_PERC_I_v2_5_0/all_events/*.csv
```

## Output folder convention

Save chamber outputs into:

```text
outputs/chambers/STRUC_I_v1_0_4/
outputs/chambers/STRUC_PERC_I_v2_5_0/
```

Suggested exported filenames:

```text
tcv_lh_STRUC_I_LH_only_results.json
tcv_lh_STRUC_I_all_events_results.json
tcv_lh_STRUC_PERC_batch_LH_only_results.csv
tcv_lh_STRUC_PERC_batch_all_events_results.csv
```

## What to look for

Compare variables by:

- κ-connectivity
- fragmentation tier
- tail dominance
- admissibility profile
- gap vulnerability
- regime class

## UNNS meaning

The pilot question is:

> Do L-H threshold variables, edge-divertor indicators, stored-energy response, density, and geometry occupy different structural regimes?

If yes, the next step is to define `m_edge(t)` or an event-level `m_transition` using the variables that show stable and physically interpretable separation.
