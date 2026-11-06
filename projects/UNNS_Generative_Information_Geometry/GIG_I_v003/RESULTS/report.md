# GIG-I v003 — Higher-Dimensional Information and Arithmetic Boundary Rigidity in UNNS Generative Histories

Full run (Python 3.13, 2 CPUs, 3,937 s). Everything below is exact integer/Fraction arithmetic; entropies are the only floating-point quantities. Tags: [PROVED], [FINITE-EXACT], [BOUNDED-NEGATIVE], [CAND], [OPEN] (definitions in THEORY/DEFINITIONS.md; proofs in THEORY/PROOFS.md).

**Headline.** (i) Admissibility factors exactly over ordered blocks, and every permutohedral face has a closed-form arithmetic threshold. (ii) The two β₂ = 1 anchors carry the *same* combinatorial 2-cycle; it is a boundary exactly when a specific truncated octahedron becomes admissible, at thresholds 288·{2,3,5} (anchor A) and 432·{2,3,7} (anchor B). (iii) On every domain tested, the uncoloured swap graph determines the whole face poset, hence rank ∂₃ and all Betti numbers: GIG-Q3 has a negative answer on those domains (Discovery A, with a precisely located proof gap), and A₃ = 0 on the exhaustive domains. (iv) The targeted k = 7 probe produces the first β₃ ≠ 0 and β₂ ∈ {2, 3} regimes — outside the verified reconstruction range.

## 1. How does admissibility factor across arbitrary ordered blocks?
**Lemma F [PROVED].** w is admissible from m ⇔ m·R(I) ∈ ℤ for every prefix *set* I, i.e. D(I) | m; admissibility sees a word only through its prefix sets.
**T16 [PROVED].** For a face F = (B₁|…|B_r): V(F) ∩ A_C(m) = E₁ × … × E_r, where E_i is the set of orderings of B_i admissible from the *formal* entry state s_i = m·R(B₁∪…∪B_{i−1}), which does not depend on any ordering chosen in earlier blocks. A face is present iff every Boolean interval [B_<i, B_≤i] is feasible. No counterexample exists (the statement is an identity); verified on 6,999,300 face–source pairs (303 contents, k=6), 0 violations; Lemma F verified on all 720 arrangements × 303 contents, 0 violations.

## 2. Which 3D cells can the grammar realize?
P_k has three 3-face types: cube (2,2,2), hexagonal prism (3,2), truncated octahedron (4) (only blocks with Σ(|B|−1)=3). P_6 has **540** 3-faces: **90 cubes (8 vertices, 6 facets), 360 hexagonal prisms (12, 8), 90 truncated octahedra (24, 14)** — reproduced from the inherited construction (E9) *and* from the uncoloured graph of the full P_6 alone (E12). Counts for P_5: 20 prisms + 10 truncated octahedra; P_7: 2,520 / 5,040 / 840. Cubes meet A_C(m) in coordinate boxes (T16(b)); this is why no partial 3-cell other than a box can occur.

## 3. What determines each cell's activation threshold?
**T17 [PROVED].** K_F = lcm{ D(I) : I ∈ Pref(F) } and F ∈ X_C(m) ⇔ K_F | m, where Pref(F) = { B_<i ∪ U : ∅ ≠ U ⊆ B_i } (all prefix sets of vertices of F). Verified against the lcm of direct vertex thresholds on 1,418,949 face–content pairs, 0 violations. Complete threshold tables for all 540 3-faces: `results.json → E9.threshold_tables` (anchor A, anchor B, identity content (1..6)). E.g. identity content: truncated-octahedron thresholds range 4…720 (23 distinct values); anchor A: 15…1728; anchor B: 7…3024.
**T18 [PROVED].** m | m′ ⇒ X_C(m) ⊆ X_C(m′); F is born at the exponent vector b(F) = (v_q(K_F))_q, so the complexes form a multi-parameter filtration over ℕ^P with accounting law **Δβ_j = Δf_j − Δρ_j − Δρ_{j+1}** (checked on every one of the 240 covers of the two anchor contents, together with inclusion).

## 4. Which 3D boundaries are present in the two β₂ = 1 anchors?
| | Anchor A | Anchor B |
|---|---|---|
| content, source | (2,3,4,5,8,9), 288 | (2,3,6,7,8,9), 432 |
| arrangements | 372 | 276 |
| f₀…f₄ | 372, 832, 602, 147, 7 | 276, 604, 423, 97, 4 |
| rank ∂₁…∂₄ | 371, 461, 140, 7 | 275, 329, 93, 4 |
| 3-cells | 147 = 31 cubes + 109 hexagonal prisms + 7 truncated octahedra | 97 = 20 + 76 + 1 |
| β | (1,0,1,0,0,0) | (1,0,1,0,0,0) |
| ∂₂∂₃ = 0 etc. | 0 violations | 0 violations |

**The cycle.** z has 96 faces (64 squares, 32 hexagons) on 130 arrangements, a cycle (∂₂z = 0). The cochain φ has **6** faces: the hexagons (2,4,5 | σ), σ a permutation of {0,1,3} (rank coordinates), φ(∂₃c) = 0 for all 147 (resp. 97) present 3-cells and φ(z) = 1, so [z] ≠ 0 (certificate files `CERTIFICATES/H2_anchor_{A,B}.json` list z, φ, every 3-cell with its facets and incidence with supp z). **The two anchors have identical z and φ in rank coordinates**; only the labels (hence thresholds) differ.
**Incidences.** z meets 77 of the 147 3-cells of A (each of its 96 faces lies in 1–3 present 3-cells: 43/49/4); in B it meets 65 of 97 (5 faces of z lie in no 3-cell, 46/42/3 in 1/2/3).
**Which 3-cells are absent.** Of the 540 3-faces of P_6, exactly **six** have φ(∂F) = 1: the truncated octahedra ({0,2,4,5}|1|3), ({0,2,4,5}|3|1), ({1,2,4,5}|0|3), ({1,2,4,5}|3|0), ({2,3,4,5}|0|1), ({2,3,4,5}|1|0), each extending the hexagon block {2,4,5} by one more label. None is present in either anchor complex.

## 5. Can new source-admissible cells eliminate nontrivial 2-cycles, and under what exact conditions?
**T21a [PROVED].** β₂ depends only on faces of dimension ≤ 3; a cover creating no 2- or 3-face leaves β₂ unchanged; a cover creating no 2-face can only lower β₂ (by Δρ₃).
**T21b (anchors).** The thresholds of the six obstructed truncated octahedra are K_F = 288·2, 288·3, 288·5 (A) and 432·2, 432·3, 432·7 (B). Hence
 • (A) if 288 | m and gcd(m/288, 30) = 1 then [z] ≠ 0 in H₂(X(m)) [PROVED via φ]; if 288·p | m for some p ∈ {2,3,5}, z = ∂c with an explicit verified 3-chain (34, 52, 126 faces for p = 2, 3, 5; every one of the 7 killing regimes verified) [FINITE-EXACT];
 • β₂ > 0 on exactly one regime of the content (the single regime 288, resp. 432) out of 55 (resp. 59) regimes; the predicate "A_C(m) equals the anchor set" ⇔ "288 | m ∧ gcd(m/288,30)=1" (resp. 432, 42) holds for all m ≤ 40,000 [FINITE-EXACT];
 • (B) the same with 432 and gcd(m/432, 42) = 1.
**Events (E11).** Anchor A: 55 regimes, 115 covers = 38 covers that change some Betti number (this includes β₀/β₁ changes), 76 cell-only covers with Δρ₃ ≠ 0 (new cells, no Betti change), 1 cell-only cover with Δρ₃ = 0. Anchor B: 59 regimes, 125 covers = 44 / 80 / 1. The H₂ class is *born* at covers 96→288 and 144→288 (A), 144→432 and 216→432 (B), and *killed* at 288→576, 864, 1440 (A) and 432→864, 1296, 3024 (B). Accounting identity and inclusion verified on every cover. Full tables: `CERTIFICATES/events_anchor_{A,B}.json`.
**General law (T21c) [OPEN]; hole-filler principle [CAND]:** in both anchors the class dies exactly when one of the six obstructed truncated octahedra becomes admissible. Whether this is the general mechanism is not shown — E14 finds further β₂ regimes (Q10, Q12).

## 6. Does the uncoloured graph determine third-boundary rank in any proved class?
**T19 [PROVED].** For realizable distinct-label complexes with isomorphic graphs (k ≤ 8): β₂(X) − β₂(Y) = ρ₃(Y) − ρ₃(X).
**T20 (graph → 3-cells).**
 • T20a [PROVED]: every face of dimension ≥ 3 of any X_A is a convex induced copy of its face graph in G_A.
 • T20b [PROVED, finite check inside the proof]: in the full P_k graph the convex induced copies of a face graph are exactly the faces, for all face types of dimension ≥ 3 with k ≤ 7 (22 type–k pairs) and the three 3-face types at k = 8 (at k=8 the type (3,2) has 32 induced copies through a root, 20 convex: the 12 extra are Petrie prisms, rejected by convexity). **Consequence: for every P_k-convex arrangement set (k ≤ 7), the graph determines the face poset, ρ₃ and all Betti numbers.**
 • T20c [FINITE-EXACT]: for every realizable set of the domains below the graph-derived face poset equals the true one in every dimension (vertex-set equality):
  k=4, L ≤ 40: 2,382 / 2,382 (exhaustive); k=5, L ≤ 16: 32,063 / 32,063 (exhaustive); k=6, L ≤ 10: **1,229 of 6,914** sets (seeded random sample, 25-minute budget; includes full P_6 — 720 vertices —, both anchors and the 1440-regime); k=7: 219 regimes with N ≤ 400 of the 20 extended anchor contents. **0 failures.** Boundary-squared violations: 0.
 • T20d [OPEN]: soundness for non-convex realizable sets in general (a subset convex in the sparser graph G_A need not be convex in P_k); precisely located in PROOFS.md.
 • Z1 negative control [FINITE-EXACT]: the non-arithmetic Petrie/braid pair has isomorphic graphs and identical graph-derived output; the reconstruction is wrong for the Petrie set (true f₂ = 0, β₁ = 1) — recognition requires the cube-product hypothesis.
Domain-relative ambiguity: **A₃ = 0 for every graph class** of k=4 (76 classes) and k=5 (3,956 classes); no class has two J₃, f₃ or Betti vectors.

## 7. What information is needed beyond graph connectivity and accessibility?
Measured as conditional entropies over the sets of each domain (uniform measure, domain-relative):
| domain | sets | H(J₃) | H(J₃ ∣ T15 data) | classes with several J₃ in a T15-data class |
|---|---|---|---|---|
| k=4, L≤40 | 2,382 | 0.005 | 0 | 0 |
| k=5, L≤16 | 32,063 | 2.84 | **0.0006** | **1** |
| k=6, L≤10 (sample) | 1,263 | 7.13 | 0 | 0 |
So the 2-skeleton data of v002 (f₀,f₁,f₂,ρ₁,ρ₂) almost, but not entirely, determine J₃ — one exhaustive-domain class contains two third-boundary ranks — yet the *full uncoloured graph* does (A₃ = 0). The extra information is not new data; it is the 3-dimensional convex structure already inside the graph. The defect D₃ = f₃ − J₃ is nonzero for 743/1,263 sampled k=6 sets (up to 49) and for 1 set at k=5, 0 at k=4. β₂ > 0 occurs for 5 of 32,063 sets at k=5 (all with Betti (1,0,1,0,0), 96 arrangements) and for none of the 1,263 sampled k=6 sets (the anchors have β₂ = 1 but were not in that random sample). For non-cube-product sets, generator colours (v002 T13) are sufficient and the graph alone fails (Z1).

## 8. Implications for GIG-Q3 and the separating-radius conjectures
**Q3.** Narrowed, not closed. By T19 a counterexample must differ in ρ₃; by T20 it cannot exist among P_k-convex sets (k ≤ 7) or in any domain above; it would have to be a non-convex cube-product set with an unverified convex-in-G_A spurious face copy (T20d), or lie outside the tested range (k=6 beyond the sample, k ≥ 8, or the large k=7 regimes). Within the verified domains the answer is negative: the graph determines the Betti vector (Discovery A, domain-scoped). Discoveries B and C are *not* claimed: no higher-dimensional information loss was found; the arithmetic H₂-transition law is established only for the two anchors (T21b), not in general.
**Separating radius.** 3-faces have graph diameter ≤ 6, and convexity of a set of diameter ≤ 6 can be tested inside the radius-6 ball of any of its vertices; so, if T20d holds, the radius-6 rooted ball determines the cells through a vertex [CAND]. v002's radius-2 (k=6) and radius-3 (k=5) fine-profile results are not changed; the global rank ρ₃ still needs the whole graph.
**Unexpected, outside the verified range.** E14 (20 contents = anchor ∪ {x}, x ≤ 16, **all 1,672 regimes enumerated and Betti-computed, no unresolved branch**): 56 regimes with β₂ or β₃ ≠ 0, including β₂ = 2 and 3 and four regimes with Betti (1,0,0,1,0,0,0) — the first β₃ ≠ 0 in the programme. These have N ≥ 2,160 and were not graph-reconstructed; they are the natural next targets (Q10, Q12).

## Search coverage and limits
Contents for T16/T17: 303 (300 seeded-random k=6 contents with labels ≤ 14, plus both anchors and the identity content); k=4 L ≤ 40, k=5 L ≤ 16 exhaustive; k=6 L ≤ 10 sampled (1,229–1,263 of 6,914 sets; seed 20260611); k=7: anchors ∪ {x}, x ≤ 16 only, no symmetry reduction used (`search_coverage.json`). Nothing here is a statement for k ≥ 8 beyond T19/T20b as marked. The frozen GEO-HD-1D v004 cross-check requires `GIG_FROZEN_SRC` and is executed on the user's machine (see `crosscheck_frozen_v003.json` if present).
Reproduce: `RUN_V003.bat test|quick|full`. Provenance: MANIFEST.json (SHA-256 of every file and of the v001/v002 manifests).
