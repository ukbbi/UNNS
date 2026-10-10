# SCR_III_GAP_4X4_PROTOCOL_v001 — Exclusion-Gap Prediction and Outcome-Blind Feasibility

**Date:** 2026-10-10 · **Status:** FINAL FOR RATIFICATION. Choices fixed by Igor's decision record; items marked **[D]** are defaults I chose where that record is silent. **Nothing has been executed.** Supersedes `SCR_III_GAP_4X4_v001_DRAFT.md` (4d36da0c…) and `SCR_III_GAP_4X4_FEASIBILITY_v001_DRAFT.md` (4d8ca733…), both left unchanged on disk.

## 0. Boundaries
SCR-III-B results are unchanged. The grammar is not modified to recover excluded configurations. **No real 4×4 energy, ground state or gap may be computed** until a separate authorization. Grammar-only 4×4 quantities (survivor count, contraction) use no energy and are allowed. This protocol is independent of the T protocol.

## 1. Question
δ_L = Δ_nonG(L)/(k_B·792 K). Does δ_4 stay in a range fixed in advance from δ_1…δ_3, and does the first non-grammar excitation fall below the frozen 1 k_BT window? This tests a local, size-insensitive gap scale, not physical transfer.

## 2. Frozen evidence and exact interval (rule R2)
Inputs: Δ_nonG(1×1) = 0.009438264173023073 A, Δ_nonG(2×2) = 0.010315265098625195 A (`WINDOWS_v006.csv`); Δ_nonG(3×3) = 1.0310349155819018e-20 J (`PRIMARY_RESULT_v001.json`); A(792 K) = 1.0095767595046513e-18 J; k_B = 1.380649e-23 J/K exact; k_BT_ref = 1.0934740080000001e-20 J.
Computed from these, not from rounded entries (reproduced twice, A-unit and J routes agree for 3×3):
- δ_1 = 0.871410942504038, δ_2 = 0.9523822089515501, δ_3 = 0.9428984210312401
- δ_min = δ_1, δ_max = δ_2, width w = 0.08097126644751207
- **I_R2 = [δ_min − w, δ_max + w] = [0.790439676056526, 1.0333534753990623]**; the rule, not these digits, is the registration: if floating-point reproduction differs, the rule on the exact inputs controls (comparison tolerance 1e-12).

## 3. Predictions (two separate decisions)
- **(i) Range.** δ_4 ∈ I_R2.
- **(ii) Window.** δ_4 < 1, equivalently W + tau ≥ Δ_nonG at W = 1 k_BT (grammar preservation would FAIL on 4×4), tau = 1e-9·Σ|K|.
(i) and (ii) are reported independently. Because I_R2 straddles 1, (i) can pass while (ii) is either way. Gap-level degeneracy is recorded descriptively only (observed 8, 16, 16).

## 4. Verdicts (after authorization of the real computation)
GAP_CONSISTENT (δ_4 certified inside I_R2), GAP_REJECTED (certified outside), GAP_INCONCLUSIVE (not certified, or the certified interval overlaps an edge of I_R2). Part (ii) is likewise CONFIRMED / REFUTED / INCONCLUSIVE with respect to 1. Three points support no scaling law; consistency is not confirmation of a law. The interval cannot be revised after any real 4×4 energy operation.

## 5. Solver v010 (additive; v009 frozen binaries are never used for n > 32)
- New files only; v009 is read-only. Spin masks and state IDs are explicit `uint64_t`; every shift is guarded (`n ≤ 40` supported, `1ULL << k` only with k < 64 asserted).
- Unsupported n (n < 1 or n > 40) returns an explicit error and no result. A test must show bits 32…39 are preserved (masks, grammar check, state IDs) and that a deliberately 33+-spin input is not truncated.
- Carries over the v009 guard design: protected-fingerprint list (FNV-1a of the instance-file bytes), refusal of energy/E0/gap requests on protected instances without the unblind flag, append-only invocation audit.
- **First action before any synthetic run:** build the real 4×4 instance file (geometry and K only, no energy), compute its fingerprint, add it to the protected list, and record it in the manifest. Computing K is geometry; no energy is evaluated.

## 6. Synthetic feasibility study
**Instances.** Geometry only: for each n ∈ {24, 28, 32, 36, 40}, **[D]** the sub-instance of the 4×4 geometry induced by islands 0…n−1 in `source_geometry(4)` order; pair set = all pairs among them; constrained vertices = those whose four incident islands all lie in the prefix (6, 7, 9, 12, 16 vertices for the five sizes; the n=40 instance is the full 4×4 incidence). Magnitudes |K_ij| from the frozen geometry; **signs never taken from the real Hamiltonian.**
- Family S (random signs): for pairs in lexicographic (i<j) order, sign = +1 if `random.Random(label).random() < 0.5` else −1.
- Family P (planted): s*_i drawn the same way from the label stream (one draw per island); K_ij = −|K_ij|·s*_i·s*_j, so the ground energy is exactly −Σ|K| and E0 is known.
- 20 instances per (family, n): 5 sizes × 2 families × 20 = **200**. Seeds: `scr_iii_b/heldout/SCR_III_SEED_REGISTRY_v001.csv` (master 20261010, labels `FEAS_{S|P}_n{n}|{idx}`; registry digest 54983330…d681). Instances are generated from these labels only; none is selected, reordered or replaced after observing results. Failures are kept and counted.

**Certification.** An *arm* is one certificate for one instance: (a) E0, (b) Δ_nonG (minimum energy over configurations violating the ice rule at ≥1 constrained vertex). Certified = lower bound equals upper bound within tau = 1e-9·Σ|K| with a witness state. Each arm is limited to **30 minutes wall time and 2 GiB peak RSS**, one thread; hardware recorded. Record wall time, nodes, bound evaluations, RSS, failures.

**Gates.**
1. *Implementation:* v010 reproduces frozen v009 results exactly at n ≤ 24 on the public/permitted cases (1×1, 2×2, 3×3 at W=0 only, and synthetic instances including Δ_nonG); rejects unsupported n; passes the 64-bit safety tests of §5.
2. *Correctness:* at n = 28, certified E0 and Δ_nonG equal an **exhaustive** independent Gray-code scan on all 40 synthetic instances. At n = 32, exhaustive scan is attempted within the same limits; an instance for which it cannot complete is labelled `NOT_EXHAUSTIVE` and checked only against independently certified bounds, and the report states how many were exhaustive. A partial n = 32 check is never called exhaustive. Planted instances reproduce E0 = −Σ|K| exactly at every n.
3. *Feasibility:* at n = 40, **at least 18/20 instances certified in each family separately** (both arms within limits). Family P cannot compensate for failures in family S, or the reverse.

**Outcomes.** FEASIBLE (all gates pass); PARTIAL (correct but over budget somewhere; report scaling and what would be needed); INFEASIBLE_AS_SPECIFIED. The certification requirement is not loosened silently; a bounds-only variant, if needed, must be specified before any real computation. Feasibility results inform solver design only, never I_R2.

## 7. Execution note
Each arm may run up to 30 minutes and the full study has up to 80 n=40 arms, so execution needs a host that can keep long jobs running; the current cloud sandbox cannot (calls are capped and background jobs die). Where it runs is a decision for you before execution.

## 8. Not authorized
Real 4×4 E0, ground state or gap; use of external data as confirmatory T evidence; any change to frozen SCR-III-B results.
