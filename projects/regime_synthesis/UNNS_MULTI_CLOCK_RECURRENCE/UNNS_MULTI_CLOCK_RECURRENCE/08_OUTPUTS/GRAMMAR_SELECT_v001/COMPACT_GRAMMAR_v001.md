# COMPACT MULTI-CLOCK GRAMMAR SELECTION v001

## Status

**SELECTED, NOT FROZEN.**

This is the seventh box in the corrected research chain:

`select compact grammar`

It does not perform the next box, `freeze`.

C003 is not loaded.

## Selected compact architecture

The development evidence does not support a one-number DTQC score.

The selected candidate grammar is:

`D_2clk -> [ P_src ; J_frac | M_frac ]`

with a separate physical extension:

`+ C_coll`

where:

- `D_2clk` is the explicit source-defined two-clock chart domain;
- `P_src` is a source-torus anchoring clause;
- `J_frac` is a reported fractional joint-phase chart coordinate;
- `M_frac` is the primary temporal decision coordinate;
- `C_coll` is independent source-native collective/coupling evidence.

### P_src — source anchor

Metric:

`JPR_parent_gain`

Selected candidate null clause:

`p_upper(PHASE_LABEL_PERMUTE) <= 0.10`

No raw P magnitude threshold is selected.

Reason: parent magnitude is high in generic Malz-Smith quasiperiodicity, so it is useful for
anchoring the trajectory to the source torus but not for DTQC discrimination.

### J_frac — chart coordinate, not a hard gate

Metric:

`JPR_cover_advantage`

J_frac is retained because it implements the original conceptual question directly:
does a fractional joint-phase cover organize state recurrence better than the integer parent
torus?

It separates DTQC from generic two-clock quasiperiodicity, but:

- DTQC vs Luo LOW AUC = 0.50;
- DTQC vs Luo HIGH AUC = 0.50;
- Zhu J_frac can change sign after x5 downsampling.

Therefore no J_frac admission threshold is selected.

This is an important selection decision: JPR survives as a **chart coordinate**, not as the
primary temporal gate.

### M_frac — primary temporal decision coordinate

Metric:

`FC_frac_mixed_gain`

Current development values:

- minimum DTQC-positive M_frac = 0.138611;
- maximum control M_frac = 0.100526.

The midpoint is:

`0.119568`

The selected compact candidate gate is therefore:

`M_frac >= 0.12`

This value has not yet been frozen.

The hard spectral-preserving null clause is:

`FOURIER_PHASE p_upper <= 0.10`

The raw M gate must also remain satisfied under the already-frozen robustness transformations:

- origin shift;
- clock exchange;
- affine state transformation;
- x5 downsampling;
- first 75% trajectory;
- 2% RMS noise.

All four current DTQC-positive records retain M_frac >= 0.12 under every perturbation.

### Why FC total gain is removed from the decision grammar

`FC_frac_total_gain` has Spearman correlation approximately
`0.949`
with M_frac and fails to distinguish DTQC from the high-frequency decoupled Luo control.

It remains descriptive only.

### Why FC parent R2 is removed

`FC_parent_full_r2` has Spearman correlation approximately
`0.887`
with JPR parent anchoring.

The compact grammar keeps the geometrically direct JPR parent/null clause and removes the
redundant FC parent gate.

## Physical extension C_coll

The temporal grammar and physical admissibility are deliberately not collapsed.

Luo provides source-native entanglement evidence:

- LOW: high coupling/entanglement with weak M_frac;
- DTQC: finite/intermediate coupling with strongest M_frac;
- HIGH: weak coupling despite substantial fractional temporal organization.

But Zhu and Malz-Smith do not supply a portable equivalent scalar.

Therefore C_coll is selected as a **required physical evidence interface**, not as a fabricated
universal numerical coordinate.

The frozen temporal grammar may later return temporal structural visibility even when a
universal physical-admissibility verdict is unavailable.

## Current empirical chart domain

All fully qualified source-defined time-domain records currently use the golden-ratio clock
relation.

Accordingly, v001 selection does **not** claim ratio-general validity.

The unused Zhu non-golden-ratio records are frequency-domain only and cannot repair this
without synthetic reconstruction.

## Development replay

Applying the selected candidate clauses back to the known development corpus is an audit,
not validation and not a verdict.

The result is stored in `DEVELOPMENT_REPLAY.csv`.

No prospective data have been used.

## Next stage

The next stage is now exactly:

`freeze`

The freeze must make immutable:

- the domain contract;
- P_src null model and p gate;
- M_frac raw magnitude gate;
- M_frac Fourier-phase null gate;
- robustness suite;
- supported ratio domain;
- output state vocabulary;
- hashes.

Only after freeze may the prospective unseen candidate/control campaign begin.
