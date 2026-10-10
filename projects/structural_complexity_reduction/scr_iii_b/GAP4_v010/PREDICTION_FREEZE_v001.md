# SCR-III-GAP-4X4 — Prospective Prediction Freeze v001

**Record date:** 2026-10-10  
**Status:** `PREDICTION_FROZEN / REAL_4X4_NOT_EXECUTED / REAL_4X4_NOT_AUTHORIZED`  
**Scope:** New prediction only; prior SCR-III-B freezes and data unmodified.

## Exact prospective predictions

- Fixed physical model: frozen source-derived Dryad SPMMC v1.00 all-pair finite free-boundary Hamiltonian, same island geometry, source coupling sign, 2-in/2-out grammar, T_ref = 792 K; n = 40 and 16 constrained vertices.
- Let `delta4 = (E_nonG_min - E0)/(k_B * 792 K)`, where both minima refer to the **full** 40-spin Hamiltonian, and `E_nonG_min` minimizes over configurations violating the frozen grammar. The exact global ground energy must not be inferred from grammar-only states.
- **Prediction R2:** `delta4` lies in **[0.790439676056526, 1.0333534753990623]** (inclusive). This was set entirely from unblinded, frozen 1×1–3×3 evidence, not from any 4×4 real-energy result. Values outside the interval REJECT R2.
- **Separate prediction:** `delta4 < 1`. Equality or larger REJECTS that directional prediction. With an inclusive energy window W=1kBT and positive operational tau, exact preservation fails when W+tau >= delta4 kBT; record that distinction independently.
- Record degeneracy at first excluded energy descriptively only.

## Decision logic for incomplete certificates

Certified upper and lower intervals for E0 and E_nonG_min imply a rigorous range for delta4 (subject to correctly bounded floating-point error). If the *entire* certified interval lies inside R2, `GAP_CONSISTENT`; if entirely outside R2, `GAP_REJECTED`; otherwise `GAP_INCONCLUSIVE`. Directional `<1` prediction is adjudicated separately. A solver's numerical best values without matching rigorous lower bounds cannot establish these verdicts. Timeouts remain inconclusive, never silently adjusted.

## Execution boundary

Only solver development and small/public correctness tests are authorized by this package. **NO real 4×4 Hamiltonian instance may be generated or evaluated** until a separate explicit primary authorization. The v010 code is additive and must not replace v005–v009. Any real run must first pass an implementation check including the frozen source geometry, bit/orientation conventions, floating point certificate policy and exact small-size controls. All deviations require a dated additive amendment, never retroactive prediction edits.

## Independent limitations

The predicted R2 range is broad and crosses delta4=1; the two predictions can receive different verdicts. Source-derived Hamiltonian v005 was validated within SCR-III-B but is not itself the original Dryad binary. The minimal v010 solver is a candidate computation engine, not proof of feasible 40-spin certification.
