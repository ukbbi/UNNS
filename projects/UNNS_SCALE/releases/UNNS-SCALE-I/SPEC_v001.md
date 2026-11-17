# UNNS-SCALE-I — Specification v001

**Question.** Which parts of the SELECT-II arithmetic graph on `[1, B·M]` are exactly recovered by the scale copy on `[1, M]`, which parts cross scales, and what survives projection to the outer coordinate?

## Gates
| Gate | Content | Status |
|---|---|---|
| 1 Representation | `n = Bq + r`, mixed radix, boundary and range accounting | PASS (`code/run_gate1.py`) |
| 2 Scale embedding | induced-subgraph isomorphism (Thm 2), boundary law (Thm 3), floor-projection obstruction (Thm 4), exact edge counts | PASS (`code/run_gate2.py`) |
| 3 Structural invariance | distances (first slice done), degrees (Thm 3); next: history counts, reachability, admissibility, geometric invariants across `B = 10, 10², 10³, 10⁶` | PARTIAL (`code/run_gate3.py`, `run_witness.py`) |
| 4 Complexity | direct vs nested cost with SCR-style baselines and nulls | NOT STARTED (by decision: only after Gates 1–3 laws are settled) |

## Acceptance rules
- Proofs are stated with their domain; every proved statement has an independent computational cross-check where finite checking is meaningful.
- Truncated distances are upper bounds; strictness claims need exact (untruncated) lower-bound certificates (done for two witnesses).
- No claim about a grammar other than SELECT-II without a separate check of scale compatibility.
- Trillion-scale statements come from exact arithmetic or proved laws, not enumeration.

## Next mathematical steps (proposed, in order)
1. Closed form / generating function for the exit count `ε_B(x)`; its mean over `x ≤ X`.
2. Exact value of `sup_n d(Bn, B(n+1))` for small `B` (path identities in the style of U1-BND), to compare with 6.
3. Multiplicativity of the boundary law across nested levels `B₁B₂`.
4. Decide whether a *reduced* outer dynamics exists on the pair `(q, J)` where `J` is a finite summary of `r` (the information left in `r` that Theorem 4 shows is needed).
