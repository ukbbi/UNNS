# MULTI-CLOCK CROSS-REPRESENTATION STUDY v002 — FINDINGS

## Status

**Development representation bake-off complete.**

No threshold, verdict, or grammar freeze is introduced.

C003 was not loaded.

## Core result

The four representations do **not** collapse to one universal coordinate.

Instead they separate into two useful and two weak/generic families.

### 1. Vector-depth recurrence remains non-specific

The source-free vector-depth family can show strong recurrence in integer DTCs and in
smooth/ordered non-DTQC trajectories, but it does not uniquely identify multi-clock order.

This is confirmed by the auxiliary cross-chart panel:

- C001 integer DTC has a strong vector-depth recurrence-family contrast;
- C002 also has organized recurrence;
- Huang limit-cycle, quasi-periodic and chaotic traces all retain very high raw lag coherence.

Therefore vector-depth recurrence is useful as a recurrence chart but not as a sufficient
multi-clock grammar.

### 2. Frequency-lattice alignment is too permissive

Low-order source-lattice spectral peaks occur not only in DTQC trajectories but also in the
independent Malz–Smith quasiperiodic non-DTQC system.

Median best spectral lattice peak contrast:

- DTQC positive: 2.895603
- Malz topological non-DTQC: 1.310326
- Malz trivial non-DTQC: 0.662010

Thus frequency-lattice organization is real but too generic to serve alone as the desired
multi-clock discriminator.

### 3. Joint-phase-conditioned recurrence exposes a genuine chart distinction

The new coordinate asks directly whether state similarity improves near the same joint source
phase, and whether a fractional cover organizes those returns better than the integer parent torus.

Median JPR fractional-cover advantage:

- DTQC positive: 0.361625
- Luo low breakdown: 0.398091
- Luo high decoupled: 0.602543
- Malz topological non-DTQC: -0.255187
- Malz trivial non-DTQC: -0.077095

The crucial observation is cross-domain:

- Luo and Zhu DTQC trajectories prefer a fractional joint-phase cover;
- the strongly organized Malz–Smith topological quasiperiodic trajectories prefer the
  **integer parent torus**, yielding negative fractional-cover advantage over most of that regime.

This is the first direct evidence in the project that

    state similarity conditioned on joint phase

contains information not reducible to generic two-clock quasiperiodicity.

However, the Luo low and high controls can also prefer d=2. Therefore JPR is not sufficient
by itself to identify the ordered many-body DTQC regime.

### 4. Fractional-cover decomposition contributes a complementary distinction

Median fractional mixed gain:

- DTQC positive: 0.224364
- Luo low breakdown: 0.052765
- Luo high decoupled: 0.100526
- Malz topological non-DTQC: -0.009239
- Malz trivial non-DTQC: -0.054902

The Malz–Smith non-DTQC system has strong integer-parent organization but generally negative
incremental fractional organization. This independently supports the parent-vs-cover split.

Within Luo, however, the high-frequency decoupled control still has substantial positive
fractional structure. Therefore temporal fractional structure remains insufficient without
the independent collective/coupling sector.

## Convergence of representations

The study does **not** support a single scalar multi-clock score.

It supports a layered structural picture:

    integer/source recurrence
        ->
    fractional joint-phase recurrence
        ->
    fractional mixed clock organization
        ->
    independent collective/coupling evidence

The most promising genuinely new coordinate is the joint-phase-conditioned recurrence
advantage, because it directly implements the original research question without injecting
an expected response frequency.

The fractional-cover mixed gain is complementary rather than redundant.

Vector-depth and frequency-lattice coordinates remain valuable descriptive charts but are
too non-specific to define admissibility alone.

## Cross-chart controls

The Phase-I integer DTC controls are not forced through the source-defined multi-clock charts.

This is deliberate: the new chart requires two externally specified clocks. Introducing a
synthetic second clock would manufacture evidence.

Their source-free vector-depth results show that ordinary integer recurrence remains visible
to a recurrence representation while being outside the domain of the source-defined multi-clock
torus. This is exactly the chart-domain distinction the structural-atlas hypothesis requires.

## Robustness

The study tests:

- temporal-origin shift;
- exchange of clock 1 and clock 2;
- coordinatewise affine amplitude changes;
- x5 downsampling;
- first 75% of each trajectory;
- 2% RMS noise.

See ROBUSTNESS_SUMMARY.csv.

Origin shift, clock exchange and affine transformation behave as invariance checks rather than
new tuning operations.

The major qualitative separation—Malz parent-torus organization versus DTQC fractional-cover
organization—survives the robustness suite.

### Invariance checkpoint

With the corrected identical pair budget for nominal invariance transforms, median absolute
JPR-cover-advantage changes are:

- temporal-origin shift: 0.001629
- clock exchange: 0.002242
- affine state transformation: 0.000000

The other representations are invariant to numerical precision under these transforms.
JPR depth retention is recorded explicitly in ROBUSTNESS_SUMMARY.csv.

## Current limitation

Every fully eligible explicit two-clock record presently available in the corpus uses the
golden-ratio relation. Therefore robustness to **different irrational clock ratios** remains
unresolved and is recorded as such, not simulated away.

## Research consequence

We should not freeze a grammar yet.

The study has narrowed the candidate architecture substantially:

1. keep joint-phase-conditioned recurrence as a primary temporal coordinate;
2. keep fractional mixed organization as an independent temporal coordinate;
3. retain source/parent organization explicitly rather than subtracting it away conceptually;
4. keep collective/coupling evidence separate;
5. demote raw vector-depth and frequency-lattice alignment from candidate decision coordinates
   to supporting descriptive charts.

The next development step is therefore not another broad representation search. It is to
formalize and stress-test the **joint-phase recurrence + fractional mixed + collective**
architecture, including null models and the missing different-irrational-ratio challenge,
before any grammar freeze.

C003 remains untouched.
