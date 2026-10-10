# SCR_III_T_DISCRIMINATION_PROTOCOL_v001 — Target-Blind Ensemble Discrimination Study

**Date:** 2026-10-10 · **Status:** FINAL FOR RATIFICATION (scientific choices fixed by Igor's decision record; items marked **[D]** are defaults I chose where that record is silent and need your confirmation before the freeze takes effect). **Nothing has been executed.** Supersedes `SCR_III_T_DISCRIMINATION_v001_DRAFT.md` (cd32764f…), which stays on disk unchanged.

## 0. Boundaries
- SCR-III-B results (G PASS, P FAIL, T NOT_TESTED, C NOT_ELIGIBLE) are unchanged and are not reopened by anything here.
- This study asks only whether the models make measurably different predictions. A pass does **not** establish physical transfer.
- No image value is used to choose models, observables, temperatures, thresholds or mappings. The Zenodo 50×50 archive is development data and may not serve as confirmatory T evidence.
- The study is independent of the 4×4 gap protocol; neither can rescue the other.

## 1. Models (registered)
| id | definition |
|---|---|
| M0 | Unrestricted Boltzmann ensemble on the frozen `physical_energy_v005` Hamiltonian, weights exp(−A(T)·E_norm/k_BT) over all 2^n states. |
| M1 | The same weights restricted to the frozen grammar set (2-in/2-out at every constrained vertex). |
| M2 | Uniform over the same grammar set. T-independent by construction. |
M1 and M2 give zero probability to any ice-rule violation. That deterministic prediction is reported in every table. It cannot establish T on its own.

## 2. Patches and sampling
Exact normalized weights are enumerated over 1×1 (n=4), 2×2 (n=12) and 3×3 (n=24; 2^24 states). **[D]** Patches are evaluated and gated separately, never pooled (pooling would mix different boundary fractions). The 1×1 patch has one constrained vertex and no nearest-neighbour pair, so it contributes only to the secondary observables. Patches larger than 3×3 are not required.

## 3. Temperature grid (registered)
300, 500, 600, 650, 700, 725, 750, 775, 790, 792, 810 K. Model temperature only; **no effective-temperature fitting** of any kind. Note: M2 does not depend on T, and above Tc = 820 K the model is not defined; 810 K is the highest grid point.

## 4. Observables
Vertex classes are read from the constrained (interior) vertices of the patch.
- **Primary:** nearest-neighbour vertex-type correlation C_NN = Σ_t [ P(type(v)=t, type(w)=t) − p_t² ], over nearest-neighbour pairs (v,w) of constrained vertices; p_t is the type marginal over constrained vertices of the same patch. Alphabet {T1,T2,T3,T4}.
- **Secondary (cannot rescue a primary failure):** vertex-type fractions p_t; violation density (share of constrained vertices that are T3 or T4).
- **Type mapping.** T3/T4 = vertices with |in−out| ≠ 0 (charge ±2 or ±4 in in-minus-out units); T1/T2 = 2-in/2-out vertices. **[D]** Candidate split by geometry: T1 = the two "in" arms adjacent (4 of the 6 configurations), T2 = the two "in" arms collinear (2 of 6), following the usual square-ice convention. This is **not yet checked against the source definition** (Menniti et al., Zenodo 15548088 uses T1–T4 labels, and its notebook further splits T2 into "perp" and "opp"). Before any prediction is computed, a one-page mapping record must cite the source definition. If the source differs, the mapping record controls and this section is amended and re-hashed first. The pilot image extraction may verify that the encoding 1…4 occurs; it may not be used to choose the mapping.

## 5. Standard errors
- Units of independence are **images**, never vertices. The 2,500 vertices of an image are not treated as independent.
- Planned data volume: 30 images per temperature/condition, a hypothetical measurement budget (the Zenodo archive is not claimed to hold 30 independent equilibrium samples).
- **[D]** Gating SE: a hypothetical image is modelled as one independent draw of the patch ensemble (B = 1 independent patch per image: the most conservative reading of within-image correlation). For each (patch, T, model) the estimator is simulated: 30 patch draws, C_NN computed on the pooled draws, R = 2000 replicates, from the registered stream seed. SE = standard deviation over replicates; model mean = mean over replicates (removes small-sample bias from the comparison).
- Sensitivity, never gating: SE_B = SE_1/√B for B = 16 and 256 (non-overlapping blocks of a 50×50 image), with the assumption of independence stated. A result that passes only under B > 1 is reported as PASS_ONLY_UNDER_OPTIMISTIC_CORRELATION, which is **not** a pass.

## 6. Separation criterion and gate
For a pair of models a, b at (patch, T): z = |mean_a − mean_b| / √(SE_a² + SE_b²) on the primary observable.
**Gate DISCRIMINATION_PASS** iff there is at least one registered (patch ∈ {2×2, 3×3}, T) with z(M1,M0) ≥ 3 **and** z(M1,M2) ≥ 3. Otherwise DISCRIMINATION_FAIL. Secondary observables cannot rescue a primary failure. k = 3 is a screening threshold across 22 cells, not a calibrated confirmatory significance test; no multiplicity correction is claimed. The report lists every cell's z, including failures.
Degenerate cases: a model with SE = 0 on a cell (all draws identical) is reported as such and z is set to "undefined, deterministic difference"; it counts toward the gate only if the means differ and the other model's SE is positive, and this is flagged explicitly.

## 7. Report contents
Full table of exact predictions (all models, patches, T, observables); simulated SE; the deterministic zero-violation prediction of M1/M2 next to M0's violation density; the B-sensitivity; the gate verdict. Statement that the exploratory excluded-mass table in the draft was post hoc and is not evidence.

## 8. Seeds
66 streams, one per (L ∈ {2,3}, T, model), in `scr_iii_b/heldout/SCR_III_SEED_REGISTRY_v001.csv` (master 20261010, labels `DISC_SIM_L{L}_T{T}_{M}`). Exact enumeration uses no randomness.

## 9. Image extraction pilot (separate, logged, non-confirmatory)
Authorized to be prepared and logged. Rules: record the time and hash of first inspection in `SCR_III_T_PILOT_LOG_v001.md`; work on a copy (original npz and sha 06b9d169… preserved); check only decoding, shapes, value alphabet and fraction of each value; the pilot output is not an input to any registered quantity here.

## 10. Verdict vocabulary
DISCRIMINATION_PASS, DISCRIMINATION_FAIL, PASS_ONLY_UNDER_OPTIMISTIC_CORRELATION. Nothing here supports a T verdict.
