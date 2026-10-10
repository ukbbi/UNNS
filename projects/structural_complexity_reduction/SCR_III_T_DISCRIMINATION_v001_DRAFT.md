# SCR_III_T_DISCRIMINATION_v001 — Target-Blind Ensemble Discrimination Study (DRAFT, UNFROZEN)

**Date:** 2026-10-10 · **Status:** design only. No held-out or pilot image value has been used. Numbers in §2 are **exploratory and post hoc** (frozen 3×3 spectrum, already unblinded) and are design inputs, not evidence for any hypothesis. Items marked ◇ need Igor's decision.

## 1. Purpose
Before any transfer target is collected or opened, decide whether one exists on which a grammar-based prediction can be told apart from simple alternatives at realistic measurement precision. If none exists, the T question is untestable with the available data, and the study reports that.

## 2. What the frozen model already implies (exploratory, 3×3, exact over all 2^24 states)
Boltzmann weights exp(−A(T)ΔE/k_BT) on the frozen Hamiltonian, with A(T) from the v005 model. "Excluded mass" is the share of the thermal weight on configurations that break the ice rule at any interior vertex:

| T (K) | 300 | 400 | 500 | 600 | 700 | 750 | 792 | 810 |
|---|---|---|---|---|---|---|---|---|
| Excluded mass | 4e-16 | 6e-12 | 3e-7 | 5e-4 | 0.11 | 0.74 | 0.993 | 0.999 |
| Violated interior vertices / 9 | 7e-21 | 6e-13 | 4e-8 | 6e-5 | 0.014 | 0.15 | 0.44 | 0.56 |

Reading, with limits: (a) up to about 500 K the grammar-restricted and unrestricted ensembles of this model are indistinguishable at any practical precision; (b) between about 600 and 800 K the difference opens up fast, because the model's magnetisation (hence A) collapses toward Tc = 820 K; (c) at the primary reference temperature the grammar set holds under 1% of the thermal weight. This is one small free-boundary patch of one model. For larger patches the set-level mass falls like (1−p)^(vertices) for any per-vertex violation probability p>0, so set membership is a poor ensemble target at scale; per-vertex or local statistics are the natural unit. That last point is standard reasoning, to be tested, not shown here.

## 3. Models to compare ◇
- **M0:** unrestricted Boltzmann on the frozen Hamiltonian.
- **M1:** the same weights restricted to the grammar set (the sampler a grammar-based prediction would use).
- **M2:** uniform over the grammar set (pure ice rule, no energetics).
A grammar defines a set; M1 and M2 are two different ways to give it probabilities. Both must be declared before any data look. The comparison is meaningful only against M0 and M2, otherwise a match shows ordinary spin-ice physics.

## 4. Observables and discrimination criterion ◇
Per-vertex type frequencies; violation density (diagnostic only; M1 and M2 predict zero by construction); nearest-neighbour vertex-type correlations (principal). For each prospectively chosen T and observable: predicted difference between models divided by the standard error expected from the planned data volume (images, vertices per image, independent samples). Gate: proceed to a held-out protocol only if at least one registered observable/T pair separates M1 from both M0 and M2 by at least k standard errors ◇. If M1 predicts a zero where the data has nonzero values (for example any observed T3 population), the grammar-as-set prediction fails trivially and the study should say that instead of dressing it as discrimination.

## 5. Effective-temperature hazard
Real or kMC data live on a different energy scale and model. Mapping them to a model temperature adds a free parameter that can make any model fit. The mapping must be fixed from independent calibration before the data look (not from the observables under test), or the test is unfalsifiable and must be declared inconclusive.

## 6. Procedure
1. Freeze models, observables, T grid (chosen from the gap crossover and model validity T < Tc, not from data), data-volume assumptions and k.
2. Compute exact predictions on 1×1, 2×2, 3×3 patches for all models and observables; estimate sampling error by simulating the planned data volume from the models themselves.
3. Report the discrimination table and the gate result. No held-out or pilot image is opened in this study.
4. Pilot image use (extraction testing) is a separate, logged action.

## 7. Decisions needed ◇
Model set M0/M1/M2 and how M1 and M2 are sampled; k; T grid; planned data volume; whether patches larger than 3×3 are required (needs the n>32 solver work in the 4×4 feasibility protocol); calibration source for any effective temperature.
