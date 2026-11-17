# Provenance — UNNS-SCALE

## Read-only reference
- Repository: https://github.com/ukbbi/UNNS
- Pinned commit: `cc77e91af530b881b161bf3ff86a2fe0f9819c19`, directory `projects/`
- Access: shallow read-only fetch of that single commit into a scratch directory outside this project; no push credentials were attached; no repository modification occurred.
- The web page view of the tree is not machine-readable through the available fetch tool (robots restriction), so the read-only git fetch was used instead.

## Definitions rebuilt locally (not imported)
- SELECT-II transition `T_N(x) = x(N+1)^2/N, N | x`; arithmetic graph with edges `{kN, k(N+1)^2}`.
  Source: `projects/UNNS_ARITHMETIC_DYNAMICS/README.md` (overview) and `.../02_routes_selectors/UNNS_U2_SQ_v001/manuscript/UNNS_U2_SQ_v001.tex`, Preliminaries.
- Scaling Lemma (edge `{x,y}` ⇒ edge `{mx,my}`; `d(ma,mb) ≤ d(a,b)`): same manuscript, Lemma "Scaling".
- Degree formula `deg(x) = τ(x) + #{q≥2: q²|x}`: stated in `UNNS_U2_TI_DYN_v001` (README of the collection); re-derived here (Lemma 0) and re-checked (G2e).
- `d(163,164) = 6` (frozen U1-BND certificate): used only as a sanity value for the local BFS.

## Material consulted but not used mathematically
`structural_complexity_reduction/README.md` (spin-ice result 2,604 / 16,777,216, 10 of 26 targets), `UNNS_Generative_Information_Geometry/GIG_INFO_v004/README.md`, `UNNS_COMMON_REFINEMENT/README.md`, directory listings of `UNNS_Generative_Geometry`, `UNNS_MATH_FOUNDATIONS`.
Not read in depth (listed for later chambers): GEO-HD bridge releases, GEO-I, FIELD-I, Math Foundations volumes, SCR-II code.

## What this project adds
Statements in `UNNS-SCALE-I/THEORY/` that are not claimed in the frozen sources as far as the consulted files show: Theorem 2 (induced-subgraph isomorphism with label preservation, proof via `B | k`), Theorem 3 (boundary law, exit degree), Theorem 4 (no floor-projection quotient), the edge-count formula, the certified shortcut witnesses. Originality against the wider literature has not been reviewed.
