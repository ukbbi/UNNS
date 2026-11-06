# GIG-I v001 — Definitions

Status tags used throughout: **[EST]** established information theory / combinatorics; **[INH]** inherited frozen UNNS result; **[ELEM]** new elementary deduction, proved in `PROOFS.md`; **[FINITE-EXACT]** exact computation on stated finite data, no universal claim; **[CAND]** theorem candidate / conjecture; **[OPEN]**.

## 1. Generative arithmetic (frozen SELECT-II, reused unchanged)
* For a label `N ≥ 1` and a state `m` with `N | m`:  `T_N(m) = m (N+1)^2 / N`.  Multiplier `R(N) = (N+1)^2/N = N + 2 + 1/N`.
* A **history** is `h = (m0; N_1,…,N_ℓ)`: a source `m0` and an ordered label word, each label admissible at the state reached. `endpoint(h) = m0 ∏ R(N_i)`.
* **Content** `Q(h)` = the multiset `{N_i}`. **Threshold** `K(w) = ∏_p p^{max(0, max_j −Σ_{i≤j} Δ_p(N_i))}`, `Δ_p(N)=2v_p(N+1)−v_p(N)`; `w` is admissible from `m` iff `K(w) | m` [INH, GEO-HD-1D law D-T7]. The engine decides admissibility by **simulation**; the threshold law is used only as an independent check.
* A history is **complete** if its source is squarefree (equivalently: the source has no reverse edge, GIG-T1).
* A **legal adjacent swap** exchanges two adjacent *distinct* labels when the swapped word is still admissible from the same source.

## 2. Source conventions (every computation states one)
* **Complete-history fibre** `F_t` = all complete histories ending at `t` (sources vary over squarefree integers).
* **Fixed-source fibre** `F_t(m0)` = all histories from the given `m0` (any integer) ending at `t`.
* **Piece** `P(m0,Q)` = histories with source `m0` and content `Q`. A fibre is the disjoint union of its pieces.
* **Empty-fibre convention.** `A(t)` is *undefined* (reported as `None`), never `log 0`. By GIG-T1(e) the complete-history fibre `F_t` is nonempty for every `t ≥ 1`, so the convention is only needed for fixed-source fibres.

## 3. Information observables
* **Generative ambiguity** `A(t) = log2 |F_t|` (bits). Combinatorial (Hartley) quantity; no probability model.
* **Ensemble.** A probability distribution on the finite fibre. **Uniform** means the uniform distribution on the fibre. Every reported entropy names its model and working precision (`decimal`, 50 digits).
* Random variables on a history `W`: `T` endpoint, `M` source, `Q` content, `P=(M,Q)` piece, `C` swap class (connected component of the swap graph), `W` itself.
* **Hierarchy** L0 `T` ⊂ L1 `(M,Q)` ⊂ L2 `C` ⊂ L3 `W` (each level determines the previous one — GIG-T2).

## 4. Swap graph and accessibility
* `G_t`: vertices = histories of the fibre, edges = legal adjacent swaps (simple graph). Components = **recombination classes**.
* `B_r(w)` = histories at swap distance ≤ r from `w`. Eccentricity `ecc(w)`; **ρ(t)** = max over `w` of `ecc(w)` = largest component diameter.
* **Recombination information profile** (uniform model) `I_r(t) = (1/N) Σ_w log2 |B_r(w)| = log2(P_r)/N`, with the integer `P_r = ∏_w |B_r(w)|`.
* **Fine accessibility signature up to radius r** of a fibre/piece: (multiset of component sizes, multiset of per-vertex vectors `(|B_0|,…,|B_r|)`). **Scalar signature**: `(N, component sizes, P_0,…,P_r)`; equal scalar signatures ⇔ equal `(N, class sizes, I_0,…,I_r)`.
* Two pieces are **information-equivalent at radius r** if their fine signatures up to r coincide (hence also `A`, `H(C|T)`, `H(W|C,T)`, `I_0..I_r`).

## 5. The inherited history complex (distinct labels only)
For a content of `k` **distinct** labels, arrangements are permutations of the `k` labels. The **permutohedral complex** `K_A` of an admissible arrangement set `A` is the **full subcomplex of the permutohedron `P_k`**: faces of `P_k` are ordered set partitions `(B_1|…|B_j)` (vertices: arrangements listing `B_1` first, then `B_2`, …; dimension `k−j`); a face is kept iff **all** its vertices lie in `A` [INH, GEO-HD-1D v003]. Its 1-skeleton is the swap graph of the piece. Betti numbers are over GF(2).
* 2-faces are **squares** (two commuting adjacent swaps; blocks 2,2,1,…) or **hexagons** (a braid relation; one block of size 3).
* The **cubical complex** keeps only faces with all blocks of size ≤ 2 (reported for comparison with the inherited record).
* Contents with repeated labels are outside the inherited complex definition: their swap graphs are used, their Betti numbers are not claimed.
* **The swap graph and the history complex are different objects**; only the 1-skeleton coincides. Graph cycle rank is `β1(G) = E − N + β0`; `β1(K_A) ≤ β1(G)` because 2-cells only kill cycles.

## 6. Realizable sets (census)
For a content `C` of `k` distinct labels, `A_C(m) = {w : K(w) | m}`; it changes only when `m` crosses the lcm-closure of the thresholds. A set is **squarefree-realizable** if some squarefree source produces it (then it occurs in a complete-history fibre). The permutohedron graph automorphisms `S_k × Z_2` (relabel label ranks; reverse positions) act on arrangement sets and preserve all quantities above.
