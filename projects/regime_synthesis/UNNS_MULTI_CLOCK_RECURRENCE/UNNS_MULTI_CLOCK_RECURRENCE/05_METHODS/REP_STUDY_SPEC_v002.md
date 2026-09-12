# MULTI-CLOCK CROSS-REPRESENTATION STUDY v002

## Status

**Development representation bake-off.**

This is not a chamber, not a classifier, and not a grammar freeze.

No threshold or verdict is defined.

C003 is not loaded.

## Research question

What structural quantity distinguishes organized multi-clock temporal order from
generic quasiperiodicity, integer-period recurrence, and breakdown without using
the expected response frequency as an input?

The study places four representations side by side.

## Core full-four-representation panel

Only records with legitimate externally specified two-clock coordinates enter the
full panel:

- Luo 2026: low / DTQC / high-decoupled entanglement trajectories, N=12 and N=32
- Zhu 2026: two experimental DTQC time-domain trajectories
- Malz–Smith 2021: twelve experimental three-component tomography trajectories,
  topological and trivial regimes

All presently available core records use the source-defined golden-ratio clock relation.

This is a limitation of the present corpus: invariance under *different irrational ratios*
cannot yet be tested empirically.

## Auxiliary controls

### Huang 2025

Limit-cycle, quasi-periodic and chaotic trajectories are retained as adjacent-domain
source-free controls.

Their canonical records do not contain an externally specified two-clock torus.
No second clock is inferred from their response.

### TIME-CRYSTAL-I integer controls

C001, C002, C002 control and the no-recompilation control are copied as small temporal
cross-chart controls.

They have no second external clock and therefore do not enter source-defined torus,
frequency-lattice or fractional-cover coordinates.

They are evaluated only by the source-free vector-depth representation.

C003 remains completely excluded.

# Representation 1 — Vector-depth recurrence family

This is the source-free representation.

For each state coordinate, compute the normalized autocorrelation magnitude R(q).
Average R(q) across coordinates.

Select the strongest recurrence lags without target-period input. For pairs q1,q2,
evaluate the four-node recurrence family

    {q1, q2, |q2-q1|, q1+q2}

using the geometric mean of R over those nodes.

Report:

- VD_best_single
- VD_best_pair
- VD_family_contrast = best pair score - median candidate pair score
- VD_q1, VD_q2, VD_pair_ratio

This representation can see ordinary integer recurrence and is deliberately allowed to
fail as a specific multi-clock discriminator.

# Representation 2 — Joint-phase-conditioned recurrence

This is the missing direct torus recurrence coordinate.

For source-cycle coordinate x and clock ratio r, define the d-cover phases

    phi1 = x/d mod 1
    phi2 = r*x/d mod 1

For non-local time pairs (i,j), calculate wrapped torus distance D_T and robustly scaled
state distance D_X.

Pairs are non-local only if both source clocks have advanced by at least one full cycle.

Define

    JPR(d) =
      1 - median[D_X | D_T in lowest 1%]
          / median[D_X]

and also the rank association between D_T and D_X.

This directly asks:

    Are similar physical states preferentially found near the same joint clock phase?

No response frequency is used.

The descriptive fractional-cover advantage is

    JPR_cover_adv =
       max_{d=2,3,4} JPR(d) - JPR(1).

Positive values mean a fractional torus cover organizes state recurrence better than
the integer parent torus.

# Representation 3 — Frequency lattice

Using the externally specified source ratio only, create low-order lattice families

    |m + n*r| / d

with |m|+|n| <= 3 and d=1..4.

Compute a coordinatewise-normalized Hann periodogram and report:

- median local spectral peak contrast at lattice nodes
- fraction of spectral power captured by node windows
- descriptive best depth
- best-fractional-minus-parent contrast

No spectral peak is used to infer the source clocks.

This representation is expected to reveal whether frequency-lattice alignment is too
generic across quasiperiodic systems.

# Representation 4 — Fractional-cover decomposition

This is the v003 architecture, generalized to vector states by equal-weight averaging
of coordinatewise cross-validated R2.

The integer parent basis is B_Z = B(d=1).

For d>=2 report:

    Delta_axis(d)
    Delta_mixed(d)
    Delta_frac(d)

where Delta_frac is the incremental cross-validated organization beyond the integer
parent lattice.

The descriptive fractional depth is the d>=2 with largest Delta_frac.

No classification threshold is introduced.

# Robustness and invariance

For the core records, the study checks:

- temporal-origin shift
- exchange of clock 1 and clock 2
- coordinatewise affine amplitude transformation
- x5 downsampling
- first 75% of the trajectory
- 2% RMS additive noise

Origin shift, clock exchange and affine amplitude transforms are invariance tests.
Downsampling, shortening and noise are robustness tests.

# Interpretation discipline

Numerical outputs are written and hashed before FINDINGS.md is generated.

Roles are used only for post-computation comparison.

No composite scalar is created.

No universal collective variable is fabricated. Luo's source-native entanglement level
is reported separately as physical context only.

# Firewall

- C003: excluded and unread.
- No response-derived source clock.
- No target subharmonic frequency injection.
- No synthetic second clock for Huang or integer DTC controls.
- No admission threshold.
- No verdict.
