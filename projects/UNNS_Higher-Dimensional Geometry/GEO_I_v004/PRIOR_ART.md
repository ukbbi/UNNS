# GEO-I v004 — Prior art and what is (not) claimed

Each reference is marked **verified** (the bibliographic record was retrieved and read *in this session*), **carried** (verified in an earlier GEO-I release or by the project owner's own review, not re-fetched here) or **unverified** (cited from general knowledge — check before relying on it). Nothing below is invented.

## Used (standard mathematics)

| Topic | Source | Status | Where used |
|---|---|---|---|
| Graver basis: conformally minimal elements of an integer lattice; finite | J. E. Graver, "On the foundations of linear and linear integer programming I," *Mathematical Programming* 9 (1975) 207–226 | **verified** (record retrieved via the Wikipedia article "Graver basis", which cites this paper; the paper itself was not opened) | move set; Lemma 0 |
| Nerve theorem for covers by closed convex sets, with a functorial and elementary proof | U. Bauer, M. Kerber, F. Roll, A. Rolle, "A unified view on the functorial nerve theorem and its variations," arXiv:2203.03571 (first submitted 7 Mar 2022; the arXiv page shows version 6 of 2 Jun 2025 and a journal DOI) | **verified** (arXiv abstract page read). Journal name, volume and pages **not verified** in this session | the independent nerve route over Q (convex cover ⇒ nerve ≃ union) |
| Variations of the nerve theorem for CW/open covers, multinerve | D. A. Ramras, "Variations on the Nerve Theorem," arXiv:2305.04794 (submitted 8 May 2023; no journal reference on the arXiv page) | **verified** (arXiv abstract page read). **Note:** the v004 specification suggested "Ramras 2026"; I found no 2026 item — the only Ramras nerve-theorem record found is the 2023 preprint above. It is background only: v004 uses only the closed-convex-cover nerve theorem | context |
| Survey of nerve theorems / topological Helly-type results (convex covers) | M. Tancer, arXiv:1102.0417 (2011), §5.1 | **carried** (verified in v003 and independently by the project owner's review) | nerve statement |
| Original nerve theorem | K. Borsuk, *Fund. Math.* 35 (1948) 217–234 | **unverified** (from memory) | historical |
| Alexander duality (β_1 of a compact planar polyhedron = number of bounded complementary components; β_2 = 0) | A. Hatcher, *Algebraic Topology* (2002), Ch. 3 | the book is standard; exact numbering **unverified** | planar topology, Programme A |
| Embedded polyhedral complex; faces of convex polytopes | G. M. Ziegler, *Lectures on Polytopes* (1995) | **unverified** (from memory) | definition of "embedded"; T-REL |

## Not found / not claimed

* **No priority claim.**  No source was found for (i) the scaling reduction of the planar modular-move complex to pure lattices `Γ_{d,s}`, (ii) the hollow-box counterexample and the corrected stabilization statement, (iii) the finite template criterion (T-REL/T-FIN) for embeddedness of the parallelotope complex of a Graver-move lattice, or (iv) the Klein-four classification and the O2 mechanism.  All are elementary and may exist in the literature on lattice-point enumeration, Markov-basis complexes, or lattice-polytope subdivisions in other language.  **The literature check is incomplete**; an equivalence-based priority review remains outstanding (as noted in the v003 assessment).
* The statements that the topology of `U_x` depends on the chosen parallelotope realization, and the absence of an intrinsic topology of UNNS occurrence structures, are limits of this work, not results.
* Nothing here concerns a physical interpretation of UNNS.

## Frozen sources
v001–v003 and the published Foundations materials are read, never modified.  `frozen/geo1lib.py` and `frozen/geo2lib.py` are byte-identical to the v002 release and their SHA-256 values are checked by `verify.py` (gate G7).
