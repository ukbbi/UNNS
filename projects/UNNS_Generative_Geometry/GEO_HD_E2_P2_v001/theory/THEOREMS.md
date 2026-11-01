# E2-P2 — Results with proofs

Tags: **[P]** proved here · **[C]** exact finite computation (certificate id in `results/P2_CERTIFICATES.json`) · **[I]** inherited. Novelty status is stated per item (spec §12.10: elementary reformulations are not promoted).

## Lemma P2-L1 (region Graver = Graver ∩ box) [P] — elementary
For any lattice Λ ⊂ Z^k, G_q(Λ) = { g ∈ Gr(Λ) : |g_i| ≤ q_i }.
*Proof.* If h ⊏ g then |h_i| ≤ |g_i| ≤ q_i, so every conformal subvector of a vector of the box lies in the box; minimality in the box is therefore minimality in Λ. ∎

## Theorem P2-T1 (lattice-transport criterion) [P] — inherited algebra, implemented and certified
Let p₁..p_k be primes coprime to b, b′; m_i = ord_b(p_i). TFAE: (a) Λ_b ⊆ Λ_b′; (b) p_i mod b ↦ p_i mod b′ extends to a well-defined group homomorphism H_b → H_b′ (H_b = ⟨p_i mod b⟩); (c) every element of the finite generating set {m_i e_i} ∪ {α ∈ ∏[0,m_i) : χ_b(α)=1} lies in Λ_b′.
*Proof.* χ_b : Z^k → H_b is onto with kernel Λ_b; a homomorphism φ with φ∘χ_b = χ_b′ exists iff ker χ_b ⊆ ker χ_b′ (universal property), giving (a)⇔(b). For (c): m_i e_i ∈ Λ_b; any α ∈ Z^k is α = Σ t_i m_i e_i + r with r ∈ ∏[0,m_i), and α ∈ Λ_b ⇔ r ∈ Λ_b, so the displayed set generates Λ_b; Λ_b′ is a group. ∎
Consequences: **denominator divisibility is neither necessary nor sufficient.** b′ | b ⇒ Λ_b ⊆ Λ_b′ and b | b′ ⇒ Λ_b′ ⊆ Λ_b (trivial), but P2-A has 5 → 4 with Λ₅ ⊊ Λ₄ [C P03]; 121 of 275 ENLARGE corpus rows have b′ ∤ b [C CE5]. Implementation uses three agreeing procedures (kernel generators, homomorphism well-definedness, HNF basis) and an independent periodic-box brute force in the audit.

## Lemma P2-L2 (axis/order rule) [P] — elementary
Let n_i = ord_b′(p_i). If |g_i| ≥ n_i for some i and g ≠ ±n_i e_i, then g ∉ G_q(Λ′) (whether or not g ∈ Λ′).
*Proof.* h = sign(g_i) n_i e_i ∈ Λ′ is a nonzero conformal subvector of g with h ≠ g. ∎
An O(k) *necessary* condition for survival from the multiplicative orders alone. Empirical sharpness [C P18]: sound on all 596 corpus rows, exact on 432 of 582 planar rows; it is not sufficient in general (150 of 582 planar rows have survival failures the rule does not detect). In P2-A it is exact: all five non-surviving vectors are blocked.

## Theorem P2-T2 (generator survival without the target complex) [P] — elementary
Let g ∈ G_q(Λ). Then g ∈ G_q(Λ′) ⇔ g ∈ Λ′ and no vector of the sub-box ∏[0,|g_i|]·sign(g_i), other than 0 and g, lies in Λ′. This inspects ∏(|g_i|+1) − 2 vectors using χ_b′ only. *Proof:* definition of conformal minimality plus L1. ∎ (`graver_transport.survives`; verified against direct target Graver sets on every corpus row [C P16/P18].)

## Theorem P2-T3 (abstract-cell transport) [P] — the general form of E2-P1 Addendum 002; corollaries elementary
For a source cell c with generators Gen(c) at its lex-minimal vertex: c ∈ K′ ⇔ V(c) ⊆ F′ ∧ Gen(c) ⊆ G_q(Λ′). Hence with S = G ∩ G′:
1. if Λ ⊆ Λ′: all 0-cells persist; a j-cell persists iff Gen(c) ⊆ S;
2. **no cell of dimension > rank ⟨S⟩ persists** (generators of a cell are independent); in particular S = ∅ ⇒ all positive-dimensional cells are lost (E2-P1), and rank S = 1 ⇒ all 2-cells are lost (P2-A);
3. G ⊆ G′ ⇒ K ⊆ K′.
Checked [C P18]: the prediction "vertices in F′ and generators surviving" equals the direct set intersection K ∩ K′ in every dimension on all 596 corpus rows; max surviving dimension ≤ rank S on all rows. *Novelty:* the criterion is the known grammar; the contribution is the effective computation of S by T2 and the rank bound.

## Theorem P2-TF1 (complete edge-survival classification of P2-F21) [P]+[C] — THEOREM_PASS (scoped); elementary
Let x_h = 21^{2h}/5, h ≥ 1.
(i) D(x_h) = {3^a 7^b : a ≡ b (4), 0 ≤ a,b ≤ h, (a,b)≠0}; L = 21^h, G = 20; C(x_h) = x_h′ = 21^{2h}/4; primes (3,7), box (h,h) unchanged.
(ii) Λ = {a ≡ b (4)} ⊊ Λ′ = {a ≡ b (2)}.
(iii) Gr(Λ) = ±{(1,1),(4,0),(0,4),(1,−3),(3,−1),(2,−2)}, Gr(Λ′) = ±{(1,1),(1,−1),(2,0),(0,2)}; region sets are their intersections with [−h,h]² (L1); G ∩ G′ = {±(1,1)} for every h ≥ 1.
(iv) All vertices persist; the persisting edges are exactly the (1,1)-edges {u, u+(1,1)}; **no 2-cell persists**; their number is
  E_kept(h) = Σ_{r=0}^{3} c_r(h)² − 1, c_r(h) = #{n ∈ [0,h−1] : n ≡ r (4)};
equivalently the quasi-polynomial (h = 4m + r): h²/4 − 1, (h²−1)/4, h²/4, (h²−1)/4 for r = 0,1,2,3 (r=1: (h²−1)/4 = h²/4 − 1/4).
(v) E_src(h) = (3/2)h² − (5/2)h + c_r (c = −3, −1, −2, −6 for r = 0..3), E_tgt(h) = 2h² + c′_r (c′ = −3, −4, −3, −4), V_src ≈ h²/4, V_tgt ≈ h²/2; so the fraction of source edges that survive tends to **1/6**. (Exact tables: `data/P2_F21.json`, verified for 4 ≤ h < 200 against the closed counting formula and by independent brute force for 4 ≤ h < 140 [C P12].)
*Proof.* (i) d | 21^h, d ≡ 1 mod 5. With 7 ≡ 3³ (mod 5) and ord₅(3)=4: 3^a 7^b ≡ 3^{a+3b}, ≡ 1 ⇔ a ≡ b (4). (h,h) ∈ D gives L = 21^h. Every such d has a + b even, and 3 ≡ 7 ≡ −1 (mod 4) gives d ≡ 1 (mod 4); with 5 | d−1: 20 | G. d = 21 ∈ D gives G | 20. Then C = 21^{2h}(1/5 + 1/20) = 21^{2h}/4 (numerator 3^{2h}7^{2h}: same primes and box). (ii) mod 4: 3^a 7^b ≡ (−1)^{a+b}. (iii) Λ: let v = (a,b) ≠ 0, a ≡ b (4). If a,b ≥ 1 then (1,1) ⊑ v; if b = 0 then 4 | a and (4,0) ⊑ v; likewise a = 0. If a > 0 > b write c = −b: a + c ≡ 0 (4); (4,0) ⊑ v when a ≥ 4 and (0,−4) ⊑ v when c ≥ 4, so minimal ones have a,c ≤ 3, a + c = 4: (1,−3),(2,−2),(3,−1), each minimal since all nonzero proper subvectors have a′+c′ ∈ {1,2,3}. Λ′: (a,b) with a+b even: a,b ≥ 1 ⇒ (1,1) ⊑; b = 0 ⇒ (2,0) ⊑; a>0>b ⇒ (1,−1) ⊑ ; the listed vectors are minimal. The common vectors are ±(1,1) only (the other source vectors are dominated in Λ′ by a vector of the target set: (4,0) ⊒ (2,0); (0,4) ⊒ (0,2); (1,−3),(3,−1),(2,−2) ⊒ (1,−1)). (iv) Vertices: F ⊆ F′ since Λ ⊆ Λ′. By T3, an edge persists iff its generator is in S = {±(1,1)}; a 2-cell needs two independent generators in S: impossible. The (1,1)-edges are {u,u+(1,1)} with u, u+(1,1) ∈ F: u = (a,b), a ≡ b (4), 0 ≤ a,b ≤ h−1, u ≠ 0; counting residue classes gives Σ c_r² − 1 (u = 0 excluded since 0 ∉ F). (v) lattice-point counts in rectangles by residue classes, edge by edge (`graver_transport.edge_count`); each is a quadratic in h on each residue class mod 4, hence fixed by three values and checked. ∎
*Prior art:* GEO-I's Graver/cell grammar and planar normalization are inherited; the explicit transport statement for this family was not found in the sources. *Novelty:* elementary within the model.

## Finding P2-D (lattice classes occurring under FIELD-I) [C]
Corpus: 596 admissible non-EQUAL transitions (582 with k=2, 14 with k=3), classes ENLARGE 275, SHRINK 262, INCOMPARABLE 59; in every one F ⊆ F′. **No SHRINK or INCOMPARABLE row has a source fibre spanning its lattice** (321/321), which agrees with E2-P1 Lemma E2-4 (spanning ⇒ EQUAL/ENLARGE); the spanning hypothesis is sufficient, not necessary (40 ENLARGE rows are non-spanning). If b | b′ the class is SHRINK in all 199 such rows (Λ_b′ ⊆ Λ_b is trivial); b′ | b ⇒ ENLARGE in all 154 rows. Consequence: the E2-P1 observation "never SHRINK" (405 transitions of one family) does **not** generalize (CE-P2-L6).

## Conjecture CP2 (planar containment) — OPEN
k = 2, Λ ⊊ Λ′ (same primes and box) ⇒ U(x) ⊆ U(C(x)). Supported: P2-A, P2-B, P2-F21 for h ≤ 8, and all 266 planar ENLARGE rows (0 PARTIAL cells) [C P13, P19, P20]; not proved. It is **false** in k = 3 (CE-P2-F5: E2-P1's 13 → 26 transition; explicit witness certified independently in check CE8). Whether the planar pattern is an instance of GEO-I v012 planar coverage is NOT established here (the v012 text is not part of this package; its hypotheses were not matched).

## Proposition P2-G (specimen geometry) [C]
P2-A: all 8 lost edges and the lost 2-cell remain inside U′ (U ⊊ U′, witness (0,2)); realized Betti (1,2,0) → (1,0,0) while the abstract complexes have Betti (1,5,0) → (1,2,6); neither complex is embedded. P2-B: all 5 edges kept, U embedded with Betti (1,0,0), but U′ is non-embedded with realized Betti (1,2,0) (abstract (1,8,0)): **enlargement can create holes** (b₁ 0 → 2) as P2-A's destroys them (b₁ 2 → 0).

## Theorem E2-P2-V (verdicts on the preregistered propositions) [C]/[P]
P2-F1 FALSE (P2-B; 57 corpus rows). P2-F2 FALSE (321 FIELD-I rows; also 484/3 vs 484/7). P2-F3 FALSE (P2-A; 121 rows). P2-F4 FALSE (P2-A; 199 rows with abstract edge loss and full geometric containment). P2-F5 FALSE (k=3 witness, CE-P2-F5; the planar pattern does not extend). P2-F6 FALSE (same primes, box, class and indices 16 → 8, different survival). See `results/P2_COUNTEREXAMPLES.json`.
