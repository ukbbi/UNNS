# MC GRAMMAR DEVELOPMENT v001 — FINDINGS

## Stage completed

**Nulls + robustness + control discrimination.**

No threshold, verdict, compact grammar, or freeze has been introduced.

## 1. The qualification result narrows the roles of JPR and FC

The null engine does not support treating every surviving temporal coordinate as equally
decisive.

### Joint-phase-conditioned recurrence (JPR)

JPR continues to expose a real chart distinction between fractional joint-phase recurrence
and generic two-clock quasiperiodicity.

Against the phase-label reassignment null, median `JPR_cover_advantage` percentiles are:

- DTQC positive: 0.803
- Luo low breakdown: 0.990
- Luo high decoupled: 1.000
- Malz topological non-DTQC: 0.000
- Malz trivial non-DTQC: 0.045

The sign structure is important: Malz's strongly organized generic quasiperiodicity sits on
the integer parent torus and is strongly *below* the fractional-cover null expectation.

But JPR is **not a strong same-system DTQC discriminator**:

- DTQC vs Luo low AUC: 0.500
- DTQC vs Luo high AUC: 0.500

The hard Fourier-phase null also shows heterogeneous JPR strength across the positive records,
especially the Zhu traces.

**Qualification:** JPR should be carried forward as a chart/domain and recurrence-organization
coordinate, not promoted by itself to an admission coordinate.

## 2. Fractional mixed-clock gain is the strongest temporal discriminator found so far

For `FC_frac_mixed_gain`, descriptive DTQC-vs-control AUC is:

- versus Luo low breakdown: 1.000
- versus Luo high decoupled: 1.000
- versus Malz topological non-DTQC: 1.000
- versus Malz trivial non-DTQC: 1.000

All are maximal in the present development corpus.

The null test is also strong. Median DTQC observed percentile for FC mixed gain is:

- time permutation: 1.000
- block shuffle: 1.000
- Fourier-phase surrogate: 0.990

The Fourier-phase result matters because that null preserves spectral power. The observed
mixed gain therefore is not explained merely by having peaks at the relevant frequencies.

However, Luo low and high controls also show non-null positive mixed organization. Their
values are lower than the DTQC values, but they demonstrate that FC mixed gain is not by itself
a complete many-body admissibility condition.

**Qualification:** FC fractional mixed gain is the strongest candidate temporal decision
coordinate currently available, but it still requires physical-sector context.

## 3. Fractional total gain is not sufficient

`FC_frac_total_gain` separates DTQC from generic Malz quasiperiodicity, but it does not
separate DTQC from the high-frequency decoupled Luo regime:

- DTQC vs Luo high AUC: 0.500.

This confirms the earlier result: a large amount of fractional two-clock temporal structure
can survive after collective coupling has effectively weakened.

## 4. The collective sector remains necessary

The Luo controls provide the decisive lesson.

- low regime: high entanglement but weak fractional mixed organization;
- DTQC regime: finite/intermediate entanglement plus the strongest fractional mixed gain;
- high decoupled regime: low entanglement despite substantial fractional temporal structure.

No universal collective proxy is fabricated for Zhu or Malz-Smith.

The evidence therefore supports a genuinely layered object rather than a single scalar.

## 5. Robustness remains intact

The locked robustness suite from `MC_REP_STUDY_v002` is carried forward unchanged by hash:

- temporal-origin shift;
- clock exchange;
- affine state scaling;
- x5 downsampling;
- first 75 percent of trajectory;
- 2 percent RMS noise.

No robustness parameter was tuned after the null results.

## 6. Zhu's different irrational ratios do not solve the remaining ratio challenge

The archive contains the published non-golden ratios

- `f2/f1 = 1/sqrt(5)`;
- `f2/f1 = 3/(2 sqrt(5))`.

But the corresponding Fig.4 public files are Fourier spectra / spectral phase diagrams,
not genuine time-domain trajectories.

They are therefore unsuitable for JPR or FC time-domain qualification without synthetic
inverse reconstruction.

The different-irrational-ratio **time-domain** challenge remains unresolved.

## Qualification outcome

The evidence now supports carrying forward the following distinct sectors:

1. **parent/source organization** — chart context;
2. **JPR fractional-cover organization** — chart/domain recurrence structure;
3. **FC fractional mixed gain** — strongest temporal discrimination coordinate;
4. **collective/coupling evidence** — independent physical admissibility sector.

`FC_frac_total_gain` remains descriptive but is not sufficient.

Vector-depth and raw frequency-lattice alignment remain supporting charts.

This package completes the sixth box in the corrected research chain:

`nulls + robustness + control discrimination`

The next box is now legitimately:

**select compact grammar**

—not freeze, not prospective validation, and not C003.

C003 remains untouched.
