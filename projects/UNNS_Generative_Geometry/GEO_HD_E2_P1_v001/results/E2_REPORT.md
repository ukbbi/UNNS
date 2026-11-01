# GEO-HD-1B / E2-P1 — Geometric transport under a changing relation lattice

**Specimen.** x₀ = 110⁴/3 → x₁ = 2·110⁴/3 → x₂ = 110⁴ under the FIELD-I collective map C (L = 12100, G = 3, 3, 1).
Fibres 13 / 13 / 26 in the box [0,2]³; relation lattice: even-sum → even-sum → Z³.
Proofs: `theory/THEOREMS.md`. Data: `data/`, `results/E2_TRANSPORT.json`. Independent audit: `results/E2_CERTIFICATES.json` (29/29).

## Verdicts (kept separate)
| Gate | Verdict | Meaning |
|---|---|---|
| Exact computation | **EXACT_PASS** | 29/29 checks pass: builder output re-derived by an independent audit (brute-force D, inverse-free lattice test, brute-force Graver sets, exact-LP nerve, Betti over GF(2), GF(3), GF(2³¹−1)); tamper tests fail as they should. |
| Scientific | **COUNTEREXAMPLE** | Five plausible "persistence laws" L1–L5 are false, with exact witnesses (CE-1…CE-5). |
| Scientific | **THEOREM_PASS (scoped)** | E2-1 (orbit family, all k), E2-2…E2-6, E2-8 are proved for the stated scopes. These are elementary statements; no priority claim is made. |
| Scientific | **OPEN** | The general law for arbitrary orbits, boxes and k (see §4). |
| Scientific | **UNAVAILABLE** | Topology of the 4-D union; a 3-D embedded complex K_emb for the source; an interactive viewer (not justified: the static figures show everything claimed). |

EXACT_PASS does **not** upgrade to THEOREM_PASS: the finite computations support the theorems only within the stated scope.

## 1. What survives
* **Vertices: all 13.** Λ ⊆ Λ′ ⇒ F ⊆ F′ (E2-6.1). The occurrence indices are preserved exactly, as FIELD-I guarantees.
* **Graver edges: none, abstractly.** All 45 source edges change the coordinate sum by an even number; every target Graver edge (±eᵢ) changes it by 1. A cell survives iff all its generators lie in G ∩ G′, and here G ∩ G′ = ∅ (E2-6.2–3). Cells lost: 45 edges, 36 two-cells, 3 three-cells. Stage 0 → 1 is the identity.
* **Geometrically, almost everything survives.** All 45 edge segments lie inside the target union U(x₂) = {x ∈ [0,2]³ : max xᵢ ≥ 1} (E2-8, any k and box). 33 of 36 two-cells lie in it.

## 2. What changes
* **Cells disappearing / emerging (abstract):** edges 45 lost, 51 new; 2-cells 36 lost, 33 new; 3-cells 3 lost, 7 new; vertices 13 new (26 total).
* **Geometric unions:** the 6 cells whose corner set contains T = {(0,1,1),(1,0,1),(1,1,0)} (3 two-cells, 3 three-cells) leave U(x₂): e.g. P((0,0,2);(0,1,−1),(1,0,−1)) contains (⅔,⅔,⅔). Conversely U(x₂) ⊄ U(x₁): the new vertex (1,0,0) lies in no source cell. So the two unions are incomparable.
* **Topology (exact):**

| | source (stage 0 = 1) | target (stage 2) |
|---|---|---|
| f-vector of abstract complex | (13, 45, 36, 3) | (26, 51, 33, 7) |
| Betti of abstract complex | (1, 6, 6, 0) | (1, 0, 0, 0) |
| Betti of realized union | **(1, 0, 18, 0)** | (1, 0, 0, 0) |
| embedded? | no (a 2-cell contains the diagonal edge (0,1,1)–(2,1,1) as a non-face) | yes (7 unit cubes) |

The source's abstract and realized topologies disagree (b₁ = 6 vs 0; b₂ = 6 vs 18) because the complex is not embedded. The union has 18 two-dimensional voids that the abstract complex does not see; all disappear in the target.

## 3. Why (exact arithmetic)
1. D(x) = {d ≥ 2 : d² | numerator, d ≡ 1 mod b}. C(x) = x + L²/G, and 3 | d−1 for every d in D(x₀), so G = 3 and C(x₀) = 2·110⁴/3. The same D holds at x₁, hence the second step adds 110⁴/3 again and the denominator cancels: b = 3 → 1 (E2-1).
2. With b = 1 the congruence condition on d disappears, so the lattice jumps from the index-2 even-sum lattice to Z³ and the fibre doubles (13 → 26). Occurrence indices are monotone (Foundations F.T31), but Graver geometry depends on the **lattice**, not on the vertex set.
3. Graver sets of D₃ and Z³ are disjoint (E2-5): {±2eᵢ, ±eᵢ±eⱼ} vs {±eᵢ}. This is the whole cause of the abstract loss.
4. Geometric retention is a separate fact: Z³'s union is the "shell" Y = {max xᵢ ≥ 1}, so a convex piece survives iff it avoids the corner [0,1)³ (E2-7). Parity-lattice edges never enter that corner (E2-8); a few 2-/3-cells do.

## 4. The general law — what is established and what is not
**Established (proved):**
* *Lattice criterion.* Between consecutive states the lattice relation is decided by three group orders (E2-2); along any C-orbit it can only stay equal or enlarge when the fibre generates the lattice (E2-4; 405 sampled transitions: 276 EQUAL, 129 ENLARGE, 0 SHRINK).
* *Vertex law.* Vertices persist iff lattices are ordered (E2-6.1).
* *Abstract cell law.* A cell persists iff its generators are in G ∩ G′; for Λ′ = Zᵏ only the axes with pᵢ ≡ 1 (mod b) survive.
* *Geometric law (scoped).* For b′ = 1, a cell persists geometrically iff it misses [0,1)ᵏ; edges of the parity lattice always do (E2-8).
* **Therefore numerical persistence, occurrence persistence and geometric persistence obey different laws.** Occurrence persistence is monotone (set inclusion); abstract-cell persistence is a statement about Graver sets of two lattices; geometric persistence is a statement about a union and a fixed corner region. None implies another (CE-1…CE-4); a denominator change need not change anything (CE-5).

**Open:** whether "PARTIAL ⇔ corners ⊇ T" extends beyond k = 3 and box (2,2,2); a predictive geometric criterion for transitions that do not end at b = 1; topology of the 4-D union (a k = 4 abstract f-vector (40,262,549,350,15) → (80,212,210,92,15) with Betti (1,12,46,43,0) → (1,0,0,0,0) is recorded, abstract only).

## 5. What was learned about generative geometry
The generative step C adds **points** monotonically, but the geometry spanned by those points is determined by the lattice of relations, which can jump. A growing set of occurrences can therefore *destroy* every edge of its previous skeleton while keeping the space those edges occupied, and can fill voids (b₂: 18 → 0) as the lattice densifies. The right object to track along a FIELD-I orbit is the pair (fibre, lattice), not the fibre alone.

## 6. Limits
Builder and audit were written by the same author (the audit imports nothing from the builder, but this is not a third-party review). The union's Betti numbers use the nerve theorem on the 18 geometrically maximal cells (verified by two independent intersection methods). The inherited exhaustive GEO-I/Foundations suites were NOT_RERUN. Figures: `figures/fibre_transition.png`, `figures/geometry_comparison.png`, `figures/cell_survival.png`.
