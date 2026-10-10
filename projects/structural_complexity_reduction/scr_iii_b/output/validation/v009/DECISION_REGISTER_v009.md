# DECISION_REGISTER_v009 — proposed settings awaiting scientific ratification

**Nothing in this register is frozen.** Every entry is a recommendation with its evidence; a proposed value does not become frozen because v009 recommends it. Primary experiment: NOT AUTHORIZED. Date: 2026-10-10.

| # | Decision | Proposed setting | Required status | Supporting tests / sources |
|---|---|---|---|---|
| 1 | Primary patch | 3×3 free-boundary square ice (24 spins, 2^24 states) | Confirm | v007 EXACT3_VERIFIER_FEASIBLE; F1, E2, H1 |
| 2 | Primary window | W = k_B T_ref, T_ref = 792 K  (= 1.093474008e-20 J = 0.010831 in A units) | Ratify | R1 (units), T1/T3 (boundary policy), B1/B2 (blindness) |
| 3 | Sensitivity windows | W = 0.5 k_B T_ref (5.46737e-21 J) and W = 2 k_B T_ref (2.18695e-20 J) | Ratify | T1/T3, H1 |
| 4 | Tolerance scale | τ = 1e-9 · Σ/K_ij/, membership E ≤ E0 + W + τ, PRESERVED ⇔ W + τ < Δ_nonG; UNRESOLVED_BOUNDARY (/d/ ≤ 2^-52 Q) is treated as target | Validate and ratify | T1, T2, T3, E3, F1 (v007 V4 deviation preserved) |
| 5 | Null seed | 20261010 (domain-separated '<seed>/<family>/<index>') | Ratify | N1, N2 |
| 6 | Null sample size | 1,000 valid nulls per family (N1 degree-preserving, N2 free incidence), draw cap 5,000 per family | Validate and ratify | N2, N3 (NULL_FEASIBILITY_v009.json) |
| 7 | E2 retained interactions | strongest 25% of /K_ij/ (spec nominal; ties by pair index); v009 RECOMMENDS 75% on measured synthetic cost (exactness is independent of the fraction); certified remainder bound B_O | Validate and ratify | E1, E2, E3, E4; fraction sweep on synthetic n=24 (E2_VALIDATION_v009.json) |
| 8 | Z₂ symmetry | Disabled in the primary experiment; optional equal-opportunity sensitivity (--z2 for every solver) | Ratify | Z1 |
| 9 | Primary B0 baseline | Optimised single-thread Gray-code exhaustive scan with periodic exact resynchronisation | Confirm | E2, E4, C1, C2 |
| 10 | B1 | Exact branch-and-bound sensitivity comparator with the admissible bound LB = E_fixed − Σ/f_j/ − Σ/K_jk/ (decision form at the common threshold) | Confirm | R1, E3, T1, T3, v008 S3 (bound admissibility, frozen) |
| 11 | H-G contraction | exact constructive = independent membership, and ≥ 99% contraction of the nominal space | Ratify | H1, N2 |
| 12 | H-P preservation | FN = 0 at the prospectively declared window, exact verifier complete | Confirm | T1, T2, T3, H1 |
| 13 | H-T | NOT_TESTED / PROTOCOL_UNFROZEN | Confirm | H1; v008 amended drafts |
| 14 | H-C performance | ≥ 1.20× charged median speedup against optimised B0; paired per-round ratios, 95% bootstrap lower bound ≥ 1.20; only if P passes and completeness is certified | Ratify | C2 (uncertainty simulation), H1, E4 |
| 15 | Timed repeats | 15 timed rounds after 3 warm-ups, deterministic balanced interleaving, single thread | Validate and ratify | C2 |
| 16 | Resource limits | 30 min per arm, 2 GiB resident memory | Validate and ratify | C2, N3 |
| 17 | E0 | Frozen v007 physical anchor E0 = -0.091840413960727757 (A units) = -9.2719947518037269e-20 J, passed unchanged to every solver | Confirm | R1, R2 |
| 18 | 3×3 W>0 unblinding | Forbidden until a separate freeze and authorisation | Confirm | B1, B2 |

## Detail per decision

### 1. Primary patch

- **Proposed:** 3×3 free-boundary square ice (24 spins, 2^24 states)
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** Smallest patch at which exact exhaustive verification is non-trivial yet feasible on one thread (v007); 4×4 exact verification is not shown to be feasible.
- **Supporting test / source:** v007 EXACT3_VERIFIER_FEASIBLE; F1, E2, H1
- **Unresolved limitations:** Single geometry; no claim about larger patches.
- **Informed by previously disclosed physical results:** Yes: the 2,604/2^24 count and the exact-verification feasibility were disclosed (v007).

### 2. Primary window

- **Proposed:** W = k_B T_ref, T_ref = 792 K  (= 1.093474008e-20 J = 0.010831 in A units)
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** Physically interpretable thermal scale fixed from T_ref and k_B alone; no 3×3 excited-state information was used.
- **Supporting test / source:** R1 (units), T1/T3 (boundary policy), B1/B2 (blindness)
- **Unresolved limitations:** Exceeds the known exclusion gaps of both public patches (1×1: Δ=0.871 k_BT, ρ_G≈1.15; 2×2: Δ=0.952 k_BT, ρ_G≈1.05), so a P FAIL at 3×3 is a genuine possibility. The window must not be changed after unblinding.
- **Informed by previously disclosed physical results:** Partly: the public small-patch gaps were known when the window was proposed (disclosed); the 3×3 gap was not.

### 3. Sensitivity windows

- **Proposed:** W = 0.5 k_B T_ref (5.46737e-21 J) and W = 2 k_B T_ref (2.18695e-20 J)
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** Bracket the primary window by a factor of two on a logarithmic scale; reported separately, never to rescue a failed primary.
- **Supporting test / source:** T1/T3, H1
- **Unresolved limitations:** 0.5 k_BT lies below both public gaps (would pass on 1×1/2×2), 2 k_BT lies above them; neither is independent of the primary window.
- **Informed by previously disclosed physical results:** Partly (same as primary window).

### 4. Tolerance scale

- **Proposed:** τ = 1e-9 · Σ|K_ij|, membership E ≤ E0 + W + τ, PRESERVED ⇔ W + τ < Δ_nonG; UNRESOLVED_BOUNDARY (|d| ≤ 2^-52 Q) is treated as target
- **Required status:** Validate and ratify — *AWAITING RATIFICATION*
- **Rationale:** Scale known before any scan; only enlarges the target, so it can never turn an excluded target into a preserved one; separated from evaluation error (eps_direct, eps_gray) and from level grouping.
- **Supporting test / source:** T1, T2, T3, E3, F1 (v007 V4 deviation preserved)
- **Unresolved limitations:** τ is a convention, not derived from physics; ≈1e-9 relative matches the v006/v007 grouping tolerance only in magnitude (different normalisation); v007's drift threshold was revised post hoc and must not be cited as prospective.
- **Informed by previously disclosed physical results:** Partly: v007 V4 drift measurements (disclosed) motivated eps_gray; the final hierarchy was tested on synthetic and public data only.

### 5. Null seed

- **Proposed:** 20261010 (domain-separated '<seed>|<family>|<index>')
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** Same master seed and derivation as the frozen v006 nulls, which makes the registry reproducible and auditable.
- **Supporting test / source:** N1, N2
- **Unresolved limitations:** An arbitrary constant; no sensitivity analysis over seeds.
- **Informed by previously disclosed physical results:** No.

### 6. Null sample size

- **Proposed:** 1,000 valid nulls per family (N1 degree-preserving, N2 free incidence), draw cap 5,000 per family
- **Required status:** Validate and ratify — *AWAITING RATIFICATION*
- **Rationale:** Large enough for a stable null distribution of Δ_null and survivor counts; the primary evaluation needs one Gray-code scan per null.
- **Supporting test / source:** N2, N3 (NULL_FEASIBILITY_v009.json)
- **Unresolved limitations:** No power analysis for any null-separation threshold was performed (that threshold remains OPEN); timing is from a synthetic 24-spin instance.
- **Informed by previously disclosed physical results:** No.

### 7. E2 retained interactions

- **Proposed:** strongest 25% of |K_ij| (spec nominal; ties by pair index); v009 RECOMMENDS 75% on measured synthetic cost (exactness is independent of the fraction); certified remainder bound B_O
- **Required status:** Validate and ratify — *AWAITING RATIFICATION*
- **Rationale:** Fixed before any 3×3 target was examined; exactness does not depend on the fraction, only cost does. The recommended fraction minimises worst-case pair operations over two synthetic 24-spin instances (Gaussian and sign-randomised real magnitudes) at 1 and 2 k_BT.
- **Supporting test / source:** E1, E2, E3, E4; fraction sweep on synthetic n=24 (E2_VALIDATION_v009.json)
- **Unresolved limitations:** Sweep on synthetic couplings only; on flat-coupling instances 25% degenerates towards a full fallback scan and is slower than B0; cost on the real geometry may differ; E2 may be slower than B0 by design. Recommended fraction 75% is not frozen.
- **Informed by previously disclosed physical results:** No (geometry-only retained-weight fraction is a property of the frozen couplings).

### 8. Z₂ symmetry

- **Proposed:** Disabled in the primary experiment; optional equal-opportunity sensitivity (--z2 for every solver)
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** Keeps comparability with the frozen v005–v008 counts and avoids one-sided symmetrisation.
- **Supporting test / source:** Z1
- **Unresolved limitations:** Halving of every search is forgone in the primary comparison.
- **Informed by previously disclosed physical results:** No.

### 9. Primary B0 baseline

- **Proposed:** Optimised single-thread Gray-code exhaustive scan with periodic exact resynchronisation
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** Competitive exact baseline for the complete-target task, not a slow direct evaluator.
- **Supporting test / source:** E2, E4, C1, C2
- **Unresolved limitations:** A hand-optimised or vectorised B0 could be faster; only single-thread scalar code was built.
- **Informed by previously disclosed physical results:** Yes (v007/v008 timings of the Gray-code scan were disclosed).

### 10. B1

- **Proposed:** Exact branch-and-bound sensitivity comparator with the admissible bound LB = E_fixed − Σ|f_j| − Σ|K_jk| (decision form at the common threshold)
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** Strong Hamiltonian-aware conventional comparator; reported honestly even if it beats G2.
- **Supporting test / source:** R1, E3, T1, T3, v008 S3 (bound admissibility, frozen)
- **Unresolved limitations:** At the W=0 anchor B1 is faster than G2 (v008); its advantage at W>0 is unknown.
- **Informed by previously disclosed physical results:** Yes (v008 W=0 timings).

### 11. H-G contraction

- **Proposed:** exact constructive = independent membership, and ≥ 99% contraction of the nominal space
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** Separates structural contraction from computational work (nodes and work are reported separately).
- **Supporting test / source:** H1, N2
- **Unresolved limitations:** Non-discriminating: the 3×3 count 2,604/2^24 (99.985%) is already known, so the contraction condition cannot fail unless membership disagrees; the substantive test is exact membership and absence of target leakage.
- **Informed by previously disclosed physical results:** Yes: explicitly (v007 count).

### 12. H-P preservation

- **Proposed:** FN = 0 at the prospectively declared window, exact verifier complete
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** Direct restatement of S_T(W) ⊆ S_G, equivalent to W + τ < Δ_nonG.
- **Supporting test / source:** T1, T2, T3, H1
- **Unresolved limitations:** Logically equivalent to a statement about the gap: a pass is not independent evidence of transfer.
- **Informed by previously disclosed physical results:** No.

### 13. H-T

- **Proposed:** NOT_TESTED / PROTOCOL_UNFROZEN
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** The beyond-gap criterion is logically unsatisfiable for inclusive energy windows; a future target family needs its own protocol.
- **Supporting test / source:** H1; v008 amended drafts
- **Unresolved limitations:** No transfer claim is possible from this study.
- **Informed by previously disclosed physical results:** No.

### 14. H-C performance

- **Proposed:** ≥ 1.20× charged median speedup against optimised B0; paired per-round ratios, 95% bootstrap lower bound ≥ 1.20; only if P passes and completeness is certified
- **Required status:** Ratify — *AWAITING RATIFICATION*
- **Rationale:** A modest margin above timing noise; conditional on a certified complete output.
- **Supporting test / source:** C2 (uncertainty simulation), H1, E4
- **Unresolved limitations:** The disclosed W=0 timings (B0 ≈ 0.33 s, G2 ≈ 0.3 ms) suggest the margin will not bind against B0; B1 and E2 are sensitivity arms and may beat G2; W>0 costs are unknown.
- **Informed by previously disclosed physical results:** Yes (v008 W=0 timings).

### 15. Timed repeats

- **Proposed:** 15 timed rounds after 3 warm-ups, deterministic balanced interleaving, single thread
- **Required status:** Validate and ratify — *AWAITING RATIFICATION*
- **Rationale:** Enough rounds for a paired median with a stable block bootstrap on this machine class; position-balanced across solvers.
- **Supporting test / source:** C2
- **Unresolved limitations:** Simulated coverage of the nominal 95% interval is only about 0.78-0.87 with 15 rounds (more rounds or a wider margin would be needed for true 95%); load on the user's machine may differ.
- **Informed by previously disclosed physical results:** No.

### 16. Resource limits

- **Proposed:** 30 min per arm, 2 GiB resident memory
- **Required status:** Validate and ratify — *AWAITING RATIFICATION*
- **Rationale:** Worst-case synthetic 24-spin windows and the null scans fit with large margin.
- **Supporting test / source:** C2, N3
- **Unresolved limitations:** Based on this container's CPU; a slower machine scales times proportionally.
- **Informed by previously disclosed physical results:** No.

### 17. E0

- **Proposed:** Frozen v007 physical anchor E0 = -0.091840413960727757 (A units) = -9.2719947518037269e-20 J, passed unchanged to every solver
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** A single certified global minimum prevents a grammar-restricted estimate from silently shifting the target.
- **Supporting test / source:** R1, R2
- **Unresolved limitations:** G1/G2/E2 cannot self-certify E0; certification is external and hash-checked.
- **Informed by previously disclosed physical results:** Yes (disclosed anchor).

### 18. 3×3 W>0 unblinding

- **Proposed:** Forbidden until a separate freeze and authorisation
- **Required status:** Confirm — *AWAITING RATIFICATION*
- **Rationale:** Protects the primary outcome from adaptive decisions.
- **Supporting test / source:** B1, B2
- **Unresolved limitations:** Procedural guard, not cryptographic.
- **Informed by previously disclosed physical results:** No.

## Axis decision table (implemented and tested as code, test H1)

| Axis | PASS | FAIL | Other |
|---|---|---|---|
| G | exact constructive = independent membership, no target leakage, contraction ≥ 99% | any mismatch / leakage / contraction below threshold | INCONCLUSIVE if unverifiable |
| P | FN = 0 with complete exact verifier at the prospective window | FN ≥ 1 | INCONCLUSIVE if verifier incomplete or window not prospective |
| T | — | — | NOT_TESTED / PROTOCOL_UNFROZEN |
| C | P passed, output completeness certified, paired lower 95% bound of the B0/G2 median ratio ≥ 1.20 | upper bound < 1.20 | INCONCLUSIVE if the interval straddles; NOT_ELIGIBLE if P/completeness not established |

## Not decided by v009 (remain OPEN for the user)

- Whether to keep W = k_B T_ref as the single primary window or declare a different rule (the register only recommends).
- The null-separation success criterion and any numerical threshold for 'distinctive grammar' versus nulls (no power analysis was done).
- Whether a margin above 1.20× is more appropriate given the disclosed W=0 timings, and whether B1 or E2 results should carry any pre-declared interpretation.
- The final tolerance constant and whether UNRESOLVED_BOUNDARY should be reported as its own outcome class in addition to FAIL.
- The dated freeze record, SHA-256 manifest of the final documents, and the separate authorisation to lift the W>0 guard.

