# MC GRAMMAR DEVELOPMENT v001

## Exact place in the research chain

This package implements only:

`nulls + robustness + control discrimination`

It does **not** perform:

- compact-grammar selection;
- grammar freeze;
- prospective validation;
- C003 analysis.

Those remain later stages.

## Input

The surviving candidate architecture comes from `MC_REP_STUDY_v002`:

1. integer/source parent organization;
2. joint-phase-conditioned recurrence (JPR);
3. fractional mixed-clock organization (FC);
4. independent collective/coupling evidence where source-native evidence exists.

Vector-depth and raw frequency-lattice coordinates remain descriptive charts and are not
promoted into the null qualification engine.

## Qualification grid

Long trajectories are deterministically strided to at most 5,000 samples for the surrogate
engine. There is no interpolation.

Observed coordinates and all surrogates are evaluated on the exact same qualification grid.

This grid is only for null qualification. The full-resolution coordinates from
`MC_REP_STUDY_v002` remain the canonical development observations.

## Null models

### TIME_PERMUTE

One random permutation is applied to time rows and shared across all state coordinates.

Preserves:
- state-value distribution;
- cross-coordinate state tuples.

Destroys:
- temporal ordering;
- state/source-phase relation;
- long-range recurrence.

### BLOCK_SHUFFLE

The trajectory is split into blocks approximately one lower-source-clock cycle long.
Blocks are randomly reordered; sample order inside a block is preserved.

Preserves:
- local dynamics;
- within-cycle smoothness;
- state-value distribution.

Destroys:
- long-range temporal organization;
- correct global source-phase sequencing.

### FOURIER_PHASE

Each Fourier frequency receives a random phase increment shared across all state coordinates.

Preserves:
- coordinate power spectra;
- cross-coordinate relative Fourier phases;
- sampling grid.

Destroys:
- original temporal phase realization;
- original alignment between physical state and source torus.

This is intentionally a hard spectral-preserving null.

### PHASE_LABEL_PERMUTE

JPR only.

The measured trajectory is left completely unchanged. The source-torus labels are randomly
reassigned among time samples.

Preserves:
- trajectory;
- state distances;
- empirical phase-label distribution.

Destroys specifically:
- the physical-state <-> source-torus correspondence.

This directly tests the conceptual heart of JPR.

## Statistics

For every record and null model, the package reports the observed value, null median,
5th/95th percentiles, upper- and lower-tail empirical Monte-Carlo probabilities, and the
observed percentile within the null distribution.

These probabilities are descriptive development statistics only.

No p-value threshold is converted into an admission rule.

## Candidate quantities

JPR:
- parent gain;
- fractional-cover advantage.

Fractional-cover representation:
- parent full R2;
- fractional mixed gain;
- fractional total gain.

The surrogate FC statistic repeats the same `d=2,3,4` descriptive depth selection for every
surrogate before reporting mixed/total gain. Therefore the null does not receive an easier
fixed depth than the observed record.

## Control discrimination

The study compares known DTQC-positive records with:

- Luo low-frequency breakdown;
- Luo high-frequency decoupled regime;
- Malz-Smith topological non-DTQC quasiperiodicity;
- Malz-Smith trivial non-DTQC quasiperiodicity.

Pairwise AUC/probability is reported for each surviving coordinate.

No classifier or combined score is fitted.

## Robustness

The locked robustness results from `MC_REP_STUDY_v002` are carried forward by hash and
evaluated alongside the null results. They are not recomputed or retuned here.

## Collective evidence

Luo source-native entanglement summaries are retained as physical context.

No universal collective proxy is invented for Zhu or Malz-Smith.

## Different irrational ratios

The unused Zhu Fig. 4 material is inventoried separately.

The incommensurate ratios

- `f2/f1 = 1/sqrt(5)`
- `f2/f1 = 3/(2 sqrt(5))`

are indeed represented in the public source package, but the supplied Fig. 4 records are
Fourier spectra / spectral phase diagrams, not genuine time-domain trajectories.

They therefore cannot be used for JPR or FC time-domain qualification without synthetic
inverse reconstruction, which remains prohibited.

## Firewall

- C003 is never loaded.
- No target response frequency is injected.
- No response-derived clock is used.
- No synthetic time series is promoted to evidence.
- No threshold.
- No verdict.
- No grammar selection.
- No grammar freeze.
