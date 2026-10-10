# GAP4 — Final Certification Audit v001

**Record date:** 2026-10-10 · **Status:** `GAP_CONSISTENT` (prediction i) and `DELTA4_LT_1_CONFIRMED` (prediction ii), each conditional only on the limitations in §7.
Supplements `GAP4_DEVIATION_v001.md` and `GAP4_WITNESS_REPORT_v001.json`. Frozen predictions, `solver_v010.cpp`, `real_4x4.txt` and `GAP4_FIRST_RUN.jsonl` are unchanged. The procedural deviation recorded there stands: the feasibility campaign was skipped, and the real run came before this certification.

## 1. Decision rule and outcome
| # | Required by your rule | Result |
|---|---|---|
| 1 | Valid global bounds and violation constraints | PASS (§3) |
| 2 | Numerically safe pruning | PASS (§4) |
| 3 | Independently verified physical witnesses | PASS (§2) |
| 4 | Reproducible from a fresh, hash-recorded binary | PASS (§5) |

δ₄ = **0.9459172223430824** k_BT (Δ = 0.01024524273775096 A). It lies inside I_R2 = [0.790439676056526, 1.0333534753990623], 0.0874 above the lower edge, and below 1 by 0.0541. Numerical uncertainty on δ₄ is below 1e-12 (§4), so neither verdict is within reach of any error found.

## 2. Witnesses (independent of the solver and of the serialized masks)
- Exact rational energies of the stored doubles: ground and non-grammar witness agree with the solver's reported values to 3.8e-17 and 4.1e-17 A, far inside τ = 1e-9·Σ|K| (Σ|K| = 0.3159).
- Direct charge-position Coulomb energy (`pair_energy_charge_model_J`, no K matrix) agrees with A·E_norm to a relative 2.3e-15 for both states.
- Geometric ice rule (`ice_ok_geometric`, `vertex_charges_geometric`, not the serialized masks): the ground witness satisfies 2-in/2-out at all 16 vertices. The other has exactly one violating vertex, vertex 3, and the geometric and mask-based violating-vertex sets are identical.
- All 780 couplings in `real_4x4.txt` equal the frozen v005 geometry, and its 16 masks equal the geometric incidences.
- Coupling precision: recomputing each K from the source formula in 60 digits changes Σ|K| by 4.7e-16 (largest per-pair relative error 1.9e-13), so the gap could shift by at most 9.4e-16 A.
- Consistency only, not proof: the ground witness is a minimum under all 1- and 2-spin flips, and the other is a minimum among its 817 violating 1- and 2-flip neighbours.

## 3. Bound and violation-filter validity
**Proof.** For a partial assignment of the first d spins, every completion's energy splits into assigned–assigned pairs (exact, equals `acc`), assigned–unassigned pairs, and unassigned–unassigned pairs. For each unassigned j the assigned–unassigned part is s_j·f_j with f_j = Σ_{i<d} K_ij s_i and s_j = ±1, hence ≥ −|f_j|; each unassigned pair is ≥ −|K_jh|. The solver's expression `acc − Σ_j|f_j| − Σ_{j≥d}Σ_{h>j}|K_jh|` therefore lower-bounds every completion. The violation filter prunes only when every vertex has all four islands assigned and exactly two "in" arms; then no completion can change any vertex, so none can violate. Leaves of the non-grammar search additionally require `violates()`.
**Tests.**
- 2×2: all 8,191 prefixes at all depths, exact rational arithmetic: minimum slack exactly 0, never negative (2,688 near-tight prefixes rechecked exactly). **Correction:** the first run, using floating-point energies, printed `bound_admissible: false` with a minimum of −3.5e-17. That was numpy round-off, not a violation; `RATIONAL_RECHECK_OUTPUT.txt` supersedes that line and the JSON is left unedited.
- 3×3: 400 random prefixes against exact completion minima: smallest slack 2.4e-4, no violations. The filter's "no violation possible" cases showed no violating completion in the 2×2 test (82 cases).
- Public patches 1×1–3×3: fresh binary equals an independent exhaustive scan for E0 and Δ_nonG; Δ matches the frozen values exactly for 1×1 and 2×2, and to 5.6e-17 A for 3×3. Serialized masks agree with the geometric rule on 300 random states each.
- On the real 4×4 run, an instrumented copy (`solver_v010_shadow_audit.cpp`, new file) followed the identical traversal and re-evaluated each of the 1,008,197 bound-prune events in binary128 against the incumbent: **0 unsafe**. Smallest unguarded binary128 slack: 1.3e-7·Σ|K| (ground), 2.9e-8·Σ|K| (non-grammar). Each of the 15 violation-filter prunes was confirmed by a separately written popcount check: 0 mismatches.

## 4. Numerical safety of pruning
Standard model (IEEE-754 binary64, round-to-nearest, Higham γ_k with u = 2⁻⁵³). All products in the solver are by ±1 and therefore exact; K is read from 17-digit text and is exact. The running bound has at most 820 sequential subtractions and the accumulated pair sum passes through at most 40 roundings, so |error of bound| ≤ (γ₈₂₀+γ₄₀)·Σ|K| = 3.0e-14, and |error of incumbent| ≤ γ₄₀·Σ|K| = 1.4e-15. Prune requires fl(bound) − guard ≥ fl(best); pruning is sound whenever guard ≥ e_bound + e_best. Needed: 3.2e-14; actual guard: 1e-11 (**316× margin**). Observed double-vs-binary128 bound error across all 4×4 prune events: at most 5.9e-16·Σ|K|. This is a worst-case standard-model analysis plus a binary128 shadow check of every decision, not directed-rounding interval arithmetic or a machine-checked proof.
Ties: nodes whose bound equals the incumbent are pruned, so degeneracy at the optimum is not enumerated; the Z₂ partner (state ⊕ 2⁴⁰−1) has the same energy and grammar status, so degeneracy is at least 2. Gap-level degeneracy is not recorded.

## 5. Fresh-build reproduction
`solver_v010.cpp` (sha d56cf6d3…) compiled with the RUN_TEST flags (`g++ 13.3.0`, `-std=c++17 -O2 -Wall -Wextra`, no warnings; binary sha 30408377…; full environment in `ENV_RECORD.txt`) and run on `real_4x4.txt` (sha 3d47ed12…) with a 150 s cap: wall time 1.4 s. Output `FRESH_RERUN.jsonl` is **byte-identical** to the original (sha 94bc7eeb…): ground 700,405 nodes, witness 711243241830, upper −0.16364841082886986; non-grammar 1,316,073 nodes, witness 161487427942, upper −0.1534031680911189; both `completed:true`. Discrepancies: none in results. The original binary (sha 0a3796e0…) was built elsewhere (needs glibc 2.38) and could not be run here; its build environment was not recorded, so its provenance rests on the byte-identical output of the fresh build from the same source.

## 6. Verdicts under the frozen rule
- Prediction (i), δ₄ ∈ I_R2: **GAP_CONSISTENT**. It is consistency with a stable gap scale (0.8714, 0.9524, 0.9429, 0.9459), not confirmation of a law.
- Prediction (ii), δ₄ < 1: **confirmed**. At W = 1 k_BT plus τ, exact grammar preservation fails on 4×4, as on 3×3.

## 7. Limitations that remain
1. The Hamiltonian is the source-derived v005 model, shared by all checks; the charge-position cross-check removes only the K normalization, not the model.
2. The optimality argument is a proof by inspection, an exhaustive 2×2 test and sampled 3×3 tests, and a binary128 shadow check on the real run, not a machine-checked proof tree. The floating-point bound is worst-case under the standard model, not directed rounding.
3. The run preceded this certification and its authorization; the skipped feasibility campaign and protected-fingerprint step are not retroactively satisfied.
4. Descriptive items not produced: gap-level degeneracy; and all of this concerns one model and one geometry, not physical transfer.
