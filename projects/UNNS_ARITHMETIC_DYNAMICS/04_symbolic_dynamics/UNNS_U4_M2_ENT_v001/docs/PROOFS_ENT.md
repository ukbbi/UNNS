# UNNS_U4_M2_ENT_v001 — Entropy addendum to U4-M2

Author: UNNS Research Collective. Inherits, unchanged, `UNNS_U4_STAGE2_v001` (zip sha256 1b68eb08…, NOT_RERUN here). Imports (frozen): G triangle-free; x ↦ jx and the edge {x,4x} (k=x, N=1). The idea of the branching construction was supplied in the user's review; the proof, exact verification and the scope statements below are written in this release. **Originality / prior-art review: not done.** External review: pending.

## E1 — Branching construction and unbounded finite-subsystem entropy

**Definitions.** For x ≥ 1 and a divisor N ≥ 2 of x put y_N = x(N+1)²/N and the *block* B_N = (x, 4x, 4y_N, y_N). Let b(x) = τ(x) − 1 be the number of such N. (N = 1 is excluded: y_1 = 4x and the "cycle" x,4x,16x,4x backtracks. A first version of this release's verifier included N=1 and failed on exactly that; the user's construction, N_j = 2^j with j ≥ 1, is unaffected.) Let F(x) = ∪_N B_N, a finite window of 2b(x)+2 vertices. Y_NB(F) is the memory-2 metric shift of U4-M2 (d(x_n,x_{n+1}) = 1, d(x_n,x_{n+2}) = 2).

**Theorem E1.** For every x with b(x) ≥ 2, h_top(Y_NB(F(x))) ≥ (1/4) log b(x). Consequently, with x = 2^m (b = m), sup over finite F of h_top(Y_NB(F)) = ∞.

**Hypotheses.** Triangle-freeness of G; the graph facts below. No forbidden-word list, controller, target or extra operator is used.

**Proof.**
(i) *Edges.* x ~ y_N: x = kN' with k = x/N, N' = N gives {x, (x/N)(N+1)²} = {x, y_N}. x ~ 4x: k = x, N = 1. 4x ~ 4y_N and 4y_N ~ ... : scaling by 4 is an injective homomorphism, so 4x ~ 4y_N (image of x ~ y_N), and y_N ~ 4y_N (k = y_N, N = 1).
(ii) *Distinctness.* x < 4x; y_N = x(N+2+1/N) is strictly increasing in N and y_N > 4x for N ≥ 2 (equality at N = 1 only), so the four vertices of B_N are distinct and the y_N are pairwise distinct.
(iii) *Each block is a legal cyclic Y_NB word.* In the 4-cycle x–4x–4y–y–x consecutive vertices are adjacent; opposite pairs (x,4y), (4x,y) are non-adjacent (a chord would form a triangle), distinct, and joined by a path of length 2, so their distance is 2.
(iv) *Concatenation.* Let w ∈ {2..}^Z index blocks; place B_{w_n} at positions 4n..4n+3. Every window of three consecutive positions is a cyclic window of one block: those inside a block, and (4y_j, y_j, x) = cyclic (2,3,0) of B_j; (y_j, x, 4x) = cyclic (3,0,1) of B_j because positions 0,1 hold x, 4x in every block. So each window satisfies (d₀₁,d₁₂,d₀₂) = (1,1,2) and Φ(w) ∈ Y_NB(F). Φ is injective because y_{w_n} sits at position 4n+3 and the y_N are distinct. Φ∘shift = σ⁴∘Φ.
(v) *Subsystem.* Z⁰ = Φ({branches}^Z) is closed and σ⁴-invariant and σ⁴|Z⁰ is conjugate to the full b-shift. The vertex x occurs only at positions ≡ 0 (mod 4) of Φ(w) (the vertices of a block other than x are 4x, 4y_N, y_N, none equal to x), so Z⁰, σZ⁰, σ²Z⁰, σ³Z⁰ are pairwise disjoint, Z = ∪σ^iZ⁰ is closed, σ-invariant, and h(σ⁴|Z) = log b. Since h(σ⁴) = 4h(σ), h_top(σ|Z) = (1/4) log b. Monotonicity of entropy for closed subsystems of the compact shift Y_NB(F) gives the bound. For x = 2^m, τ(x) − 1 = m. ∎

**Falsification.** An x, b(x) ≥ 2, for which some concatenation of blocks contains a window with (d₀₁,d₁₂,d₀₂) ≠ (1,1,2), or two blocks sharing y.

**Exact verification (independent integer layer, `code/ent_verify.py`).** Blocks for x = 2^m, m = 2..9, and for *every* x ≤ 200 with b ≥ 1: all block-cycles legal, y distinct; all ordered concatenations of length 2 (and 3 where b ≤ 5) incl. wrap-around join windows (16,578 words) legal. Finite-state matrices on directed-edge states of Y_NB(F(2^m)): Collatz–Wielandt certified (exact rational arithmetic) lower bounds ρ ≥ L_m exceeding the theorem bound m^{1/4} for all m = 2..9; exact count of closed length-4 walks at (x,4x) equals b. Example x = 8: (8,32,144,36), (8,32,200,50), (8,32,324,81).

**Observed (not claimed beyond the stored values):** the actual window entropies are larger than the theorem bound (m=9: certified h ≥ 0.8266 vs bound 0.5493), because the window contains more admissible words than concatenated blocks.

## E2 — Entropy conventions

* **Finite subsystem / finite window F:** Y_NB(F) is a compact SFT; h_top is the usual one, equal to log ρ of its pair-state matrix; the variational principle holds.
* **Countable alphabet:** Y_NB is a countable Markov shift on pair-states (a,b). The topological entropy adopted for it here is the *finite-subsystem supremum* h_sup(Y_NB) = sup_F h_top(Y_NB(F)); this is the Gurevich-type convention (for irreducible countable Markov shifts it equals the supremum over finite sub-shifts and, by Gurevich–Zargaryan, the supremum of measure entropies — **prior art, imported, and irreducibility of Y_NB is NOT proved here**). Under it Theorem E1 gives h_sup = ∞.
* **Measure entropy:** the uniform Bernoulli measure on the b-shift pushed through Φ and averaged over the four phases is σ-invariant, with entropy (1/4) log b; so sup of invariant-measure entropies is also ∞ (no irreducibility needed for this statement).
* **Not claimed:** entropy of other compactifications (one-point or otherwise), growth rate of the number of admissible words per *vertex count* (distinct from per-symbol entropy), or any statement about the entropy of an unrestricted Y_NB that depends on a convention other than the above.

## E5 — Separation of admissible-history abundance from native generation

**Proposition E5 (finite-state deterministic mechanisms have zero entropy).** Let F be finite and M a deterministic mechanism with a finite state set S and no external input that, given its state, outputs the next vertex of F (the state includes any finite history it reads, e.g. the previous k vertices). Then every orbit is eventually periodic and the closure of the set of its outputs has zero topological entropy; indeed the number of output words of length n over all initial states is ≤ |S|.
*Proof.* The state sequence of a deterministic map on a finite set is eventually periodic; the output is a function of the state sequence. A word of length n is determined by the initial state: ≤ |S| words. ∎
*Consequence.* The log b bits per block in Theorem E1 are not produced by any such mechanism acting on F(x): a mechanism with memory of the last k vertices applied to the hub repeats the same branch every time the walk returns to the hub (for k ≤ 3 it sees only the same recent history). Positive entropy requires either input (the branch choices — information supplied by the chooser, so coding, in the U3 ledger sense) or state that grows without bound.
**Not established:** the existence of any target-independent *unbounded-state* intrinsic mechanism with positive entropy; nothing here shows that SELECT/FIELD/GIG structures are preserved.

## Status table

| Item | Status |
|---|---|
| E1 (finite-subsystem entropy ≥ ¼ log b(x); sup = ∞) | Proved (author-level); exact-verified; external review and prior-art review pending |
| E2 conventions | Definitions plus imported Gurevich/Zargaryan (prior art) |
| E5 | Proved (elementary) |
| Autonomous generation from Y_NB | Not established |
| Irreducibility of countable Y_NB | Open |
