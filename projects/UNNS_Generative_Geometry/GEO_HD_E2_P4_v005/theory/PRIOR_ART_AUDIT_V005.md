# Prior-art audit, v005 (LIMITED; this is NOT a novelty clearance)

Rule from the project: nothing may be called new before an audit; C3 is not assessed. This file records exactly what was searched, what was read, and what could not be read.

## Method and limits
* Tools: web search (7 queries, "standard" mode, snippets and result lists only), two page fetches, and a sparse read-only checkout of the public repository `ukbbi/unns` (commit `9a021346b2b3d964523440d2737b9d0c4ddbb3e5`, 2026-10-31).
* Not available here: MathSciNet, zbMATH, Google Scholar, full-text access to paywalled journals. One fetch (a ZIB preprint) returned an anti-bot page and was **not read**. Textbooks were not consulted.
* Consequently absence of a hit means only "not found by these queries".

## Ingredient-level sources (the standard tools used in the proofs)
| Ingredient | Where used | Source located | Read? |
|---|---|---|---|
| Graver basis / conformal order; every lattice vector is a conformal sum of Graver vectors | L1 | J. E. Graver, "On the foundations of linear and integer linear programming I", Math. Programming 9 (1975) -- listed in search results; attributions to Sturmfels (1996) and Onn (2010) taken from the Wikipedia article "Graver basis" | Wikipedia page read; the conformal-sum statement is NOT on that page and was proved directly (L1) |
| Fine zonotopal tilings; lifting construction; Bohne-Dress correspondence | T0 | J. Richter-Gebert, G. M. Ziegler, "Zonotopal tilings and the Bohne-Dress theorem" (ZIB SC 93-25, in search results); P. Huber, J. Rambau, F. Santos, "The Cayley Trick, lifting subdivisions and the Bohne-Dress theorem on zonotopal tilings" (J. Eur. Math. Soc., in search results) | titles/records only; texts NOT read |
| Lower facets of a lifted polytope give a regular subdivision of its shadow | SF in T0 | textbook fact (Ziegler, *Lectures on Polytopes*, chapter on polytopal subdivisions; section number not re-checked) | not re-read |

T0 is proved here in the explicit form needed (vertices are subset sums) from SF, so the proof does not rely on the unread Bohne-Dress texts, only on the textbook fact SF.

## Targeted searches for the project-specific statements
Queries combined "Graver", "zonotopal tiling", "lattice parallelotope cells", "sublattice", "monotone / containment of unions of cells under lattice enlargement", "deleted origin / nonzero corners". **No source was found** that states or refutes
(a) monotonicity of the union of Graver parallelotope cells with nonzero corners under lattice inclusion (P5-P1), (b) the three-dimensional failures (P5-C1..C3), or (c) the split-target slab law (P5-S4). The realized-union object is defined in the UNNS
GEO-I/E2 programme itself; its literature neighbours (Graver complexes, Graver fans, Lawrence liftings) are about different complexes. This is consistent with, but does not prove, that the statements are specific to this construction.

## Internal alignment (read-only GitHub)
`projects/UNNS_Higher-Dimensional Geometry/README.md` and `GEO_I_v012/GRAVER_STRIP.md` were read. Same objects: occurrence fibre F_x = (Lambda_b cap [0,q]) \ {0}, relation lattice Lambda_b, realized cell union U (the GEO-I statement G12-T8, U = conv F, is for the planar family Gamma_{d,s} with unit s and is a
*different* kind of statement from monotonicity under inclusion). The mechanism of G12-T2 ("if h were conformal to the step e, the points w+h and w2-h ... a Gamma-point sits strictly inside the edge") is of the same Graver-contradiction type as LG here; no overlap or conflict with P5 results was found. Nothing in the repository
(read portion only) states planar monotonicity or contradicts the 3D failures; the frozen GEO-I baseline is untouched.

## Status assigned
* P5-P1 (planar monotonicity): elementary consequence of standard tools; project-specific; novelty relative to the literature NOT_ASSESSED. A dedicated independent proof review and a fuller literature search (zbMATH/MathSciNet, Graver-basis and zonotopal-tiling experts) are still required before any priority statement.
* P5-C1..C3, P5-S4: specific to the construction; elementary; novelty NOT_ASSESSED.
* C3: not claimed.
