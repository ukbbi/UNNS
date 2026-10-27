# GEO-I v005 — Mathematics: registry and recap

Full proofs of the v004 results (T-REL, T-FIN, S1, S4 and the Klein-four analysis) are in the frozen v004 release and are **not repeated or modified**; they are recalled here only as far as v005 uses them. New proofs are in `STABILIZATION.md` (Programme A) and `OBSTRUCTIONS.md` (Programmes B/C).

## 1. Definitions (unchanged from v004)
* `Λ_b = ker(Z^k → (Z/b)^×, α ↦ ∏ r_i^{α_i})`, box `q ∈ N^k`, fibre `F_q = (Λ ∩ [0,q]) ∖ {0}`.
* Moves: Graver (conformally minimal) vectors of `Λ` inside the box. Cell `P(u; g_1..g_m)`: independent Graver generators, all `2^m` corners in `F_q`.
* `K_abs` = face-closed family of these cells; `U` = their union (point set); `K_emb` = exact subdivision. `K_abs`, `U`, `K_emb` are distinct objects; `U` carries the topology.
* Planar pure types: `Γ_(d,s) = {(i,j) ∈ Z² : j ≡ s·i (mod d)}`, `gcd(s,d)=1`; fibre of `Q`.

## 2. Tools used from v004
* **T-REL.** A face-closed polyhedral family is embedded iff the relative interiors of distinct cells are disjoint.
* **T-FIN.** With a template `(A,B,δ)`, `δ` in the open zonotope of `A ∪ B`: `K_abs` is non-embedded iff some template is realized in the box; hence embeddedness is a down-set in `q`, characterized by a finite antichain `Obs` of minimal obstruction boxes.
* **S1 / S4.** Scaling reduction of the planar case to `(d,s,Q)`; translation lemma: coverage in the base window `[d,3d−1]² ∖ {(d,d)}` implies coverage for all `Q ≥ (d,d)`, `Q ≠ (d,d)`.

## 3. v005 registry

| ID | Statement | Label | Where |
|---|---|---|---|
| G5-C1 | `U = conv(F)` for `d ≥ 2`, `Q1,Q2 ≥ d`, `Q ≠ (d,d)` | `s = ±1`: **PROVED+CHECKED**; general: **CHECKED** `d ≤ D*`, **OPEN** | STABILIZATION §3–5 |
| G5-C2 | `β₁(U) =` `d` (`s=−1`), `2` (`s=+1`, `d≥3`) at `Q=(d,d)` | `s = ±1`: **PROVED+CHECKED**; other `s`: **CHECKED** `d ≤ D*`, **OPEN** | STABILIZATION §4 |
| G5-T3 | `Obs(Γ_(d,−1)) = {Q1+Q2 = 2d+1}` | **PROVED+CHECKED** `d ≥ 2` | OBSTRUCTIONS §2 |
| G5-T4 | `Obs(Γ_(d,1)) = {(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}`, `d ≥ 3` | **PROVED+CHECKED** | OBSTRUCTIONS §2 |
| G5-C3 | every minimal obstruction box has a witness with `d_span ≤ 2` | **FALSE** (14 certified lattice classes) | OBSTRUCTIONS §3 |
| G5-C3′ | … with `d_span ≤ 3` | **OPEN** (CHECKED on a bounded census) | OBSTRUCTIONS §3 |
| G5-C4 | irreducible witnesses are planar | **FALSE** | OBSTRUCTIONS §4 |
| G5-T5 | classification of essential higher-coordinate obstructions | **CHECKED** (mandatory families, bounded census); lifting lemma **PROVED** | OBSTRUCTIONS §4–5 |
| G5-T6 | effective witness / rank certificates | **PROVED+CHECKED** | OBSTRUCTIONS §6 |
| unrestricted `k=4` atlas | — | **UNAVAILABLE** | OBSTRUCTIONS §5 |

## 4. Definitions added in v005
* **Witness** of non-embeddedness: two distinct cells with intersecting relative interiors (equivalently a realized forbidden template).
* **`d_span`** = `rank_Q[A,B,δ]`; **`d_support`** = number of coordinates touched by generators or `δ`; **`d_intersection`** = `|A|+|B|−d_span`.
* **Essential coordinate obstruction**: non-embedded box all of whose coordinate restrictions `q_i := 0` are embedded.
* **Irreducible witness**: no other pair of faces of its two cells is a witness.
* **Layers** of a planar type: level sets of `D = (j − s i)/d`; **hollow box**: `Q = (d,d)`.

## 5. Computational conventions
Exact arithmetic only (Python integers, `gmpy2.mpq`); no floating-point certificate. Every embeddedness decision is made by at least two independent routes (planar test vs template route vs polyhedral audit; cells route vs template route for witnesses). Resource exhaustion yields `UNAVAILABLE`, never a pass. Searches write resumable JSONL checkpoints.
