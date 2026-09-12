# MC GRAMMAR v001 — FROZEN SPECIFICATION

## Status

**FROZEN BEFORE PROSPECTIVE CAMPAIGN**

This artifact completes the `freeze` box in the corrected research chain.

No prospective candidate/control data have been used to choose or alter this grammar.
C003 has not been loaded.

## Frozen temporal chart

The grammar is:

`D_2clk -> [ P_src ; J_frac | M_frac ]`

with a separate physical-evidence interface:

`+ C_coll`

This notation does not define a scalar score.

## 1. Domain `D_2clk`

A record is inside the chart only when all of the following are true:

- exactly two externally specified incommensurate source clocks are available;
- a genuine time-domain observable/state trajectory is available;
- the clock ratio comes from source metadata rather than fitting the response;
- no inverse-FFT or synthetic reconstruction is used as evidence.

### Frozen empirical ratio support

Version v001 is empirically qualified only on the golden-ratio branch.

A legitimate two-clock trajectory with another irrational ratio is therefore reported as:

`OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN`

not as a negative temporal verdict.

This supported ratio domain may not be broadened without a new grammar version.

## 2. `P_src` — source-torus anchor

Metric:

`JPR_parent_gain`

Frozen null:

`PHASE_LABEL_PERMUTE`

Frozen null qualification:

- deterministic stride to at most 5000 samples;
- no interpolation;
- 20000 JPR pairs;
- 99 surrogates;
- seed family fixed by `grammar_dev_v001.py`.

Frozen gate:

`p_upper <= 0.10`

If it fails:

`SOURCE_UNANCHORED`

No raw parent-magnitude threshold exists.

## 3. `J_frac` — joint-phase chart coordinate

Metric:

`JPR_cover_advantage = max(JPR(d=2,3,4)) - JPR(d=1)`

`J_frac` is mandatory output but **not a gate**.

No threshold may be inferred prospectively from its value.

## 4. `M_frac` — primary temporal decision coordinate

Metric:

`FC_frac_mixed_gain`

Depth selection remains descriptive:

`d* = argmax_d FC_frac_total_gain(d), d in {2,3,4}`

and `M_frac` is the mixed contribution at that selected d*.

Frozen raw gate:

`M_frac >= 0.12`

Frozen spectral-preserving null:

`FOURIER_PHASE`

with:

- deterministic stride to at most 5000 samples;
- no interpolation;
- 49 surrogates;
- identical v003/v002 basis and 5-fold contiguous CV;
- ridge alpha 1.0e-09.

Frozen null gate:

`p_upper <= 0.10`

## 5. Frozen stability clause

The raw `M_frac >= 0.12` gate must remain satisfied under **every** frozen transform:

- temporal-origin shift: 0.371 lower-clock cycles;
- clock exchange;
- coordinatewise affine state transform;
- x5 downsampling;
- first 0.75 of the trajectory;
- additive noise sigma = 0.02 * std;
- frozen robustness seed inherited from the versioned method.

If any transform falls below the raw M gate:

`MIXED_ORGANIZATION_UNSTABLE`

## 6. Frozen temporal-state precedence

The grammar returns the first applicable state in this order:

1. `OUTSIDE_CHART_DOMAIN`
2. `OUTSIDE_EMPIRICALLY_QUALIFIED_RATIO_DOMAIN`
3. `SOURCE_UNANCHORED`
4. `MIXED_ORGANIZATION_WEAK`
5. `MIXED_ORGANIZATION_SPECTRAL_NULL`
6. `MIXED_ORGANIZATION_UNSTABLE`
7. `TEMPORAL_CORE_SUPPORTED`

All failure flags are also retained in the machine output.

## 7. `C_coll` — physical extension

`C_coll` remains separate from the automated temporal verdict.

Allowed annotations:

- `COLLECTIVE_NOT_ASSESSED`
- `COLLECTIVE_EVIDENCE_UNAVAILABLE`
- `COLLECTIVE_EVIDENCE_AVAILABLE_FOR_DOMAIN_SPECIFIC_REVIEW`

No universal numeric collective gate is defined.

A prospective record may therefore be temporally supported while its broader physical
admissibility remains domain-specific.

## 8. Explicit exclusions

The following are frozen as **non-decision** quantities:

- vector-depth recurrence;
- raw frequency-lattice alignment;
- FC parent full R2;
- FC fractional total gain;
- any composite scalar;
- any hard J_frac threshold;
- fractional-depth agreement.

## 9. Firewall

From this freeze onward, none of the following may change within `MC_GRAMMAR_v001`:

- domain definition;
- supported ratio domain;
- representation;
- cover depths;
- CV rule;
- null models;
- surrogate counts;
- null gates;
- raw M gate;
- robustness transformations;
- state vocabulary;
- state precedence.

Any change requires a **new grammar version** and invalidates prospective status for data
already examined under v001.

C003 remains excluded until after the prospective analysis is locked and revealed.
