# REPORT_v005 — Physical Energy and Hamiltonian Convention Lock

**Verdict:** `PHYSICAL_HAMILTONIAN_LOCK_PASS`

This verdict concerns the selected finite-patch SPMMC v1.00 all-pair model with template parameters. It is **not** a transfer result and does not generalise to artificial square spin ice in general or to the published 24×24 arrays.

## Headline

- 1×1 (4 spins): 16 configs, 6 2-in/2-out, ground energy -9.528652e-21 J at 792 K (A(T)=1.009577e-18 J), degeneracy 2, all ground states ice-rule=True, min ice -9.528652e-21 J, min non-ice 0.000000e+00 J, non-ice-minus-ice gap 9.529e-21 J; ground vertices all Type 1 = True
- 2×2 (12 spins): 4096 configs, 82 2-in/2-out, ground energy -4.089422e-20 J at 792 K (A(T)=1.009577e-18 J), degeneracy 2, all ground states ice-rule=True, min ice -4.089422e-20 J, min non-ice -3.048016e-20 J, non-ice-minus-ice gap 1.041e-20 J; ground vertices all Type 1 = True
- v001–v004 non-ice ground states reproduced ONLY with the legacy sign E=−ΣKss (regression, exact negative of the verified energy). The source's own flip update gives ΔE=−2A s h, i.e. E=+ΣKss; under it the 1×1 and 2×2 ground states are ice-rule (Type 1) states. Cause: energy sign convention, not geometry, units, boundary or temperature.

## Test summary

| ID | Test | Evidence level | Status | Mandatory |
|---|---|---|---|---|
| P1 | Original-source files present; SHA-256 equals the v004 provenance record | STATIC_SOURCE_TEXT_ANALYSIS | **PASS** | yes |
| P2 | Every VERBATIM block in the probe is byte-identical to the original line range | STATIC_SOURCE_TEXT_ANALYSIS | **PASS** | yes |
| E1 | Geometry (coordinates, unit vectors, free-boundary vertex incidence): python vs verbatim initialize_dipole_system/initialize_vertex_system | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E2 | Pair coupling K_ij and all-pair web (no cutoff, no self-term): python vs verbatim; symmetry for identical islands | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E3 | Physical Coulomb dumbbell energy (explicit charges, SI) equals A(T)*K_ij (fixes 3/16 normalisation, q=(pi/4)Mwh, moment=MV) | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** | yes |
| E4 | Local interaction field h_i = sum_j K_ij s_j: python vs verbatim initialize_dipole_athermal_interaction_fields | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E5 | Single-spin-flip dE = -2 A s_i h_i: verbatim update_reference_dipole_reversal_time vs python direct subtraction (normalised and joules) | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E6 | Incremental field / reversal-time updates (verbatim update_interaction_fields) agree with fresh recomputation (identical islands) | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E7 | Ice-rule classification (2-in/2-out at every vertex): independent geometric rule vs verbatim compute_vertex_statistics (all 16 and 4096 states) | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E10 | Exact 1x1 and 2x2 enumeration under the verified model: ground states, ice verdict, gaps, degeneracy | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** | yes |
| E8 | Source-derived energy landscape from verbatim flip energies is a single-valued potential equal to python H up to the known constant ratio | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E9 | Temperature-dependent magnetization: E(s,T)=A(T)E_ref(s) with A>0, B=0; ordering, ground set, degeneracy, flip-ΔE scaling at 5 temperatures | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| E9b | Verbatim reduced-temperature factor: f(T)*T ∝ (1-T/Tc)^(2 beta) (beta=0.5) exactly | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| A1 | Reverse every spin: H(-s)=H(s); verbatim h(-s)=-h(s); flip exponent unchanged | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| A2 | Flip one selected spin: direct subtraction equals -2 s_k h_k | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** | yes |
| A3a | Physically equivalent convention: y-mirror of the whole patch (positions and unit vectors) | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** | yes |
| A3b | Equivalent gauge: flip vertical unit vectors AND relabel vertical states | SOURCE_DERIVED_INDEPENDENT_PYTHON | **PASS** | yes |
| A3c | Convention-mismatch detector: flip vertical unit vectors WITHOUT relabelling states (a modelling error, not a symmetry) | SOURCE_DERIVED_INDEPENDENT_PYTHON | **INFO** | no |
| A4 | Change normalisation (python K scale 3.7; verbatim interaction_adjustment_ratio 0.5) without moving coordinates: ordering invariant, flip exponent scales linearly | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| A5 | Double-counting detector: counting every ordered pair doubles ΔE relative to the source; single-counted H matches the source | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| A6 | ΔE sign detector against verbatim source: verified H agrees, legacy v001-v004 sign (E=-sum K s s) contradicts the source | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| F1 | FINDING: v001-v004 energy sign was inverted relative to the original source; the non-ice minima are its consequence (see E10) | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **FINDING** | no |
| A7 | Omitted long-range interactions (verbatim web builder with cutoff 200/270/400 nm vs all-pair): sensitivity of ground states | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **INFO** | no |
| A8 | Unit consistency: uniform length scaling leaves K invariant and scales source f and python A(T) by scale^3 (volume) | VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE | **PASS** | yes |
| A9 | Free boundary: source offers no alternative (periodic branch empty in v1.00); embedded-vertex check of the 2x2 ground states | STATIC_SOURCE_TEXT_ANALYSIS | **INFO** | no |
| A10 | MMC vs SPMMC kept distinct: shared pair functions identical; defaults and interaction sets differ; MMC acceptance uses the same sign | STATIC_SOURCE_TEXT_ANALYSIS | **PASS** | yes |
| A11 | Regression: previously transcribed v002-v004 pair formula (models/physical_energy.py, y-up geometry) pair-coupling multiset equals v005 K at h=15 nm (index/orientation-independent) | PREVIOUSLY_TRANSCRIBED_V002_V004_FORMULAS | **PASS** | no |

## Unresolved items

- v1.01 production island width/height per geometry folder (data archives not acquired).
- Unmodified simulator execution not performed (GSL not required by the probe; the simulator exposes no total energy).
- Paper/supplement not in package; README used for Eq. 3.
- Boundary alternatives cannot be compared: periodic branch is empty in v1.00.
- Gaussian size disorder (stdev>0) untested; probe stand-in supports stdev=0.

## Evidence levels

- UNMODIFIED_SIMULATOR_EXECUTION
- VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE
- SOURCE_DERIVED_INDEPENDENT_PYTHON
- PREVIOUSLY_TRANSCRIBED_V002_V004_FORMULAS
- STATIC_SOURCE_TEXT_ANALYSIS

## Scope

Selected model: SPMMC-SSI-Unix-v1.00 all-pair dumbbell interaction, free-boundary finite patches 1×1 (4 spins) and 2×2 (12 spins), template parameters a=260, l=160, w=60, h=15 nm, M0=7.9e5 A/m, β=0.5, Tc=820 K, κ=1, supported domain 0<T<Tc (tested 760–815 K). 3×3 (24 spins, 16,777,216 configurations) used for targeted field/energy/flip tests only (48 random configurations); no exhaustive run.
