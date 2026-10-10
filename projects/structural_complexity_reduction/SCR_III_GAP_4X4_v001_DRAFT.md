# SCR_III_GAP_4X4_v001 — Exclusion-Gap Scaling Protocol (DRAFT, UNFROZEN)

**Date:** 2026-10-10 · **Status:** formalization from frozen 1×1–3×3 evidence only. **No 4×4 energy, ground state or gap has been computed or inspected.** Numbers marked ◇ need Igor's decision before anything is frozen. This protocol is independent of the T protocol; neither can rescue a failure of the other.

## 1. Question
Let δ_L = Δ_nonG(L) / (k_B·792 K), the energy of the lowest ice-rule-violating configuration above the global ground energy, in units of k_BT_ref. Does δ_4 stay in a range fixed in advance from δ_1, δ_2, δ_3? This tests whether the exclusion gap behaves like a local, size-insensitive scale. It does not test physical transfer.

## 2. Frozen evidence the prediction may use
| Patch | n spins | constrained vertices | Δ_nonG (A units) | δ_L | states at the gap |
|---|---|---|---|---|---|
| 1×1 | 4 | 1 | 0.009438264173023073 | 0.87141 | 8 |
| 2×2 | 12 | 4 | 0.010315265098625195 | 0.95238 | 16 |
| 3×3 | 24 | 9 | 0.010212546058288613 | 0.94290 | 16 |
(1×1 and 2×2 from `WINDOWS_v006.csv`; 3×3 from `PRIMARY_RESULT_v001.json`. Conversion: δ = Δ_A · A(792 K)/k_BT = Δ_A · 92.328.) 4×4 has n = 2L(L+1) = 40 and 16 constrained vertices.
The three values are 0.871, 0.952, 0.943: not monotone, spread 0.081. Three points support no scaling law, trend or error estimate.

## 3. Held fixed
Geometry rule, free boundary and island template of `physical_energy_v005`; Dryad dumbbell Hamiltonian and K from the frozen module; 2-in/2-out ice rule at constrained (interior) vertices; T_ref = 792 K, k_B exact; tau = 1e-9·Σ|K|; same bit/ID convention.

## 4. Prediction (two separate parts, both registered before any 4×4 energy operation)
**(i) Range prediction.** δ_4 ∈ I. Candidate rules for I ◇:
- **R1:** hull of observed values, [0.871, 0.952]. Tightest; a modest deviation fails it.
- **R2 (recommended for discussion):** hull widened on each side by the hull's width, [0.790, 1.033]. Chosen by a rule independent of any 4×4 information, but wide and straddling 1.
- **R3:** wider only if justified by a physical argument written down first.
Any I must be fixed with its rule stated, not tuned.
**(ii) Window consequence.** δ_4 < 1, i.e. grammar preservation at W = 1 k_BT would FAIL on 4×4 (W + tau ≥ Δ_nonG). Reported separately from (i): (i) can pass while (ii) fails or the reverse if I straddles 1.
Optional secondary item ◇: the number of states at the gap (8, 16, 16 so far, all multiples of 8) is reported descriptively, not as a verdict.

## 5. Computation and certification
- Needs the global ground energy E0 and the minimum energy over configurations violating the ice rule at ≥1 constrained vertex, both for n = 40 (2^40 ≈ 1.1e12 states, so exhaustive scan is not assumed).
- Method: exact branch-and-bound with certified lower bounds (from the v008/v009 B1 design) for E0 and for the violating-minimum, run per constrained vertex or with a violation flag. Certificates: lower bound = upper bound within tolerance tau, with witness states.
- Result classes: **CERTIFIED** (both E0 and Δ_nonG certified to tolerance); **BOUNDED** (interval for δ_4); **UNCERTIFIED**. If a BOUNDED interval straddles an edge of I or the value 1, that part is INCONCLUSIVE.
- Independent checks after certification: direct charge-position energies and geometric ice-rule membership of the witness states (as in `PRIMARY_AUDIT_v001.md`); a second solver implementation. The shared physical model remains a stated limitation.

## 6. Outcome-blind feasibility gate (before any real 4×4 energy operation)
- Build synthetic n = 40 instances: real incidence and real |K| magnitudes (geometry only), random signs, so no real energy or gap is revealed. Fingerprint-protect the real 4×4 instance in the guard list first.
- Measure B&B time and memory on n = 24, 28, 32, 36, 40 synthetic instances under 30 min per arm and 2 GiB. Gate: n = 40 certifies within budget on a pre-set fraction ◇ of synthetic instances. If not, the protocol is infeasible as specified and is reported as such, not weakened silently.
- Grammar-only quantities (4×4 survivor count, contraction) may be computed now: they use no energy.

## 7. Verdicts
- **GAP_CONSISTENT:** δ_4 certified inside I (and, separately, (ii) reported). Evidence is consistent with a stable gap scale; it is not a confirmation of a law.
- **GAP_REJECTED:** δ_4 certified outside I.
- **GAP_INCONCLUSIVE:** not certified, or the certified interval overlaps an edge.
Every deviation, solver failure and timeout is reported. The interval cannot be revised after any 4×4 energy operation. The grammar cannot be changed to recover excluded configurations.

## 8. Decisions needed from Igor ◇
1. Rule for I (R1, R2, R3).
2. Gate pass fraction for the feasibility check.
3. Whether to register the gap-level degeneracy as a descriptive item.
4. Whether the feasibility gate may begin before the T protocol is settled (they are independent).
