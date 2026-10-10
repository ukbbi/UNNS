# DRAFT_AMENDMENTS_v009 (both drafts remain UNFROZEN; nothing is ratified)

Base: the v008 amendment drafts (themselves based on the user's revised SPEC/PREREG v001). These copies live inside the additive v009 package and do not overwrite or freeze the project-root originals.

## Added in v009

1. PREREG §12 and SPEC §9B record the closure proposals for E2, the common E0, the numerical policy, windows, nulls, ordering/Z₂, cost accounting, timing, axis criteria and blinding.
2. PREREG §9 checklist items are annotated with where each proposal stands; none is ticked because none is frozen.
3. Wording unchanged from v008: Δ_nonG, Generative Admissibility / Physical Sufficiency, H-C against optimised Gray-code B0 with B1 sensitivity, T = NOT_TESTED, low-energy-outcome blinding, separately implemented verifier, V4 post-hoc disclosure.

## Decisions recorded (all PROPOSED — AWAITING RATIFICATION)

| # | Decision | Proposed setting (PROPOSED — AWAITING RATIFICATION) | Required action |
|---|---|---|---|
| 1 | Primary patch | 3×3 free-boundary square ice (24 spins, 2^24 states) | Confirm |
| 2 | Primary window | W = k_B T_ref, T_ref = 792 K  (= 1.093474008e-20 J = 0.010831 in A units) | Ratify |
| 3 | Sensitivity windows | W = 0.5 k_B T_ref (5.46737e-21 J) and W = 2 k_B T_ref (2.18695e-20 J) | Ratify |
| 4 | Tolerance scale | τ = 1e-9 · Σ/K_ij/, membership E ≤ E0 + W + τ, PRESERVED ⇔ W + τ < Δ_nonG; UNRESOLVED_BOUNDARY (/d/ ≤ 2^-52 Q) is treated as target | Validate and ratify |
| 5 | Null seed | 20261010 (domain-separated '<seed>/<family>/<index>') | Ratify |
| 6 | Null sample size | 1,000 valid nulls per family (N1 degree-preserving, N2 free incidence), draw cap 5,000 per family | Validate and ratify |
| 7 | E2 retained interactions | strongest 25% of /K_ij/ (spec nominal; ties by pair index); v009 RECOMMENDS 75% on measured synthetic cost (exactness is independent of the fraction); certified remainder bound B_O | Validate and ratify |
| 8 | Z₂ symmetry | Disabled in the primary experiment; optional equal-opportunity sensitivity (--z2 for every solver) | Ratify |
| 9 | Primary B0 baseline | Optimised single-thread Gray-code exhaustive scan with periodic exact resynchronisation | Confirm |
| 10 | B1 | Exact branch-and-bound sensitivity comparator with the admissible bound LB = E_fixed − Σ/f_j/ − Σ/K_jk/ (decision form at the common threshold) | Confirm |
| 11 | H-G contraction | exact constructive = independent membership, and ≥ 99% contraction of the nominal space | Ratify |
| 12 | H-P preservation | FN = 0 at the prospectively declared window, exact verifier complete | Confirm |
| 13 | H-T | NOT_TESTED / PROTOCOL_UNFROZEN | Confirm |
| 14 | H-C performance | ≥ 1.20× charged median speedup against optimised B0; paired per-round ratios, 95% bootstrap lower bound ≥ 1.20; only if P passes and completeness is certified | Ratify |
| 15 | Timed repeats | 15 timed rounds after 3 warm-ups, deterministic balanced interleaving, single thread | Validate and ratify |
| 16 | Resource limits | 30 min per arm, 2 GiB resident memory | Validate and ratify |
| 17 | E0 | Frozen v007 physical anchor E0 = -0.091840413960727757 (A units) = -9.2719947518037269e-20 J, passed unchanged to every solver | Confirm |
| 18 | 3×3 W>0 unblinding | Forbidden until a separate freeze and authorisation | Confirm |

## Still OPEN

- OPEN: ratification (or replacement) of every entry above by the user.
- OPEN: null-separation success criterion and any numerical threshold for distinctive grammar versus nulls.
- OPEN: whether the 1.20× margin and the 99% contraction criterion should be changed given they are non-binding in light of disclosed results.
- OPEN: final tolerance constant, assembled final documents with SHA-256 manifest, dated freeze record and separate authorization.

This amendment does not freeze, ratify or authorize anything; the primary experiment remains NOT AUTHORIZED.
