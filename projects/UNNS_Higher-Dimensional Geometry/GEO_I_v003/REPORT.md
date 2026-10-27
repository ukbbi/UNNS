# GEO-I v003 — Abstract and Embedded Geometry

**Question.** v002 found nontrivial homology (β₁ saturation, β₂ growth) in the modular-move complex. Which of those features belong to the arithmetic, and which to the way cells were attached? v003 separates three objects: **K_abs** (v002's abstract complex), **U_x** (the union of its parallelotopes in exponent space), and **K_emb** (an exact, valid subdivision of U_x, built when k = 2; auxiliary vertices carry provenance and are never occurrences).

**Verification status.** `python verify.py` (full): **56 / 56 checks pass**, ≈ 4.5 min. Smoke mode passes as well. All geometric decisions are exact (integer / rational; exact-LP for cell intersections). The independent audit's witness 82944/5 is reproduced.

## 1. Main results

| # | Result | Status |
|---|---|---|
| R1 | **82944/5 confirmed non-embedded.** Edges (1,1)–(5,1) and (2,2)–(4,0) cross at (3,1) (t = λ = ½), which is not an occurrence and not even a point of Λ₅. Exact subdivision: 5 vertices (4 occurrences + 1 auxiliary), 8 edges, 4 triangles. Betti numbers: K_abs (1,2,0), K_emb (1,0,0), clique complex (1,0,0). | proved + exact (Fig. 1–2) |
| R2 | **Infinite family** x_t = 2^{10+2t}·3⁴/5: every member non-embedded (same crossing at (3,1)); β₂(K_abs) ≥ χ−1 → ∞ while β₂(U) = 0 (planar), so the abstract/geometric discrepancy is unbounded. | proved (Thm T4); exact data t ≤ 24 (Fig. 5) |
| R3 | **Arithmetic classification of crossings** (Thm T1): crossing ⇔ r−u ∈ Ω(g,h), |Ω| = ι−1, ι = \|det\|/\|H\| for k = 2. A predictor built only from (g,h,Ω) matches the exhaustive edge audit as a set of edge pairs on 2,849 k=2 and 1,485 k=3 fibres (0 mismatches). | proved + exact |
| R4 | **k = 2 is completely classified** (Thm T2b): crossing-free for every box ⇔ embedded for every box ⇔ \|⟨p₁,p₂⟩\| = ord(p₁)·ord(p₂) (direct product). Checked for all residue pairs, b ≤ 59; explicit crossing configuration for every non-direct pair, b ≤ 40. | proved + exact |
| R5 | **Direct-product fibres are embedded in every dimension** (Thm T2a), including every integer fibre (b = 1). The v002 3-cell (3600) and 4-cell (210⁴) are therefore genuinely valid, as is 44100 (no 4-cell). | proved |
| R6 | **k ≥ 3 is genuinely different.** (a) Edge-crossing freedom does **not** imply embedding: the Klein-four classes (b = 8, residues 3,5,7; b = 12, residues 5,7,11) have no crossing in any box, yet cells overlap improperly from box (3,3,2) (concrete x = 27348890625/8, K_abs (1,4,3,0), U (1,0,10)) via the Graver-diagonal obstruction (Prop. D). (b) Edge crossings occur in 3-D and 4-D in planes that are not coordinate planes (x = 5489031744/5: K_abs (1,12,6,0) vs U (1,0,0)); appending a unit axis (p ≡ 1 mod b) preserves every crossing (P5). | proved + exact (Fig. 3–4) |
| R7 | **Embedded ⇒ same homology** (Thm 1, standard): for every embedded fibre the abstract Betti numbers *are* the geometric ones. | standard; verified 3 ways |
| R8 | **Graph identity**: β₁(arrangement of the 1-skeleton) = β₁(abstract graph) + Σ_p (m_p − 1). Verified on 1,257 fibres. | proved + exact |

## 2. Data

### E7 — the rational corpus (8,203 fibres, same set as v002)
8,198 **embedded**; 5 non-embedded: 82944/5 (edge crossing); 6400/3, 12800/3, 63504/5, 112896/5 (cell-only: a Graver diagonal inside a 2-cell). No fibre was left unresolved.

### E8 — the 38 fibres with nonzero homology
**33 are valid embedded complexes**: their β₁ is a genuine topological feature of the realized set. **5 are non-embedded and all five change**:

| x | K_abs | geometric U |
|---|---|---|
| 6400/3 | (1,1,0) | (1,0,0) |
| 12800/3 | (1,1,0) | (1,0,0) |
| 63504/5 | (1,1,0) | (1) — U is a single convex cell |
| 82944/5 | (1,2,0) | (1,0,0) |
| 112896/5 | (1,4,0) | (1,3,0,0) |

So the v002 corpus β₁ findings are **mostly robust** (33 of 38), but the largest values come precisely from the fibres that are not embedded.

### E9 — collective C-orbits (7 orbits × 60 states = 420 states)
| orbit | embedded states | max β₁(K_abs) | β₁(U) at non-embedded states | U unavailable (budget) |
|---|---|---|---|---|
| 72 [C, G=1] | 60 / 60 | 0 | — | 0 |
| g=11 benchmark 67500²/11 | **0 / 60** | 8 | **0 at all 60** | 0 |
| g=11, L=2·3³·5⁴ | 1 / 60 | 3 | 0 at 58 | 0 |
| g=13 | 6 / 60 | 15 | 0–4 | 18 |
| g=17 | 2 / 60 | 16 | 0–3 | 21 |
| g=19 | 3 / 60 | 23 | 0–3 | 12 |
| g=23 | 3 / 60 | 25 | 0–13 | 0 |

Totals: 75 embedded, 334 non-embedded with an edge crossing, 11 cell-only. **The v002 “β₁ saturation at 8” for the g=11 benchmark is a property of the abstract complex**: the geometric image of every one of its 60 states has β₁ = 0 (and β₂ 0–7 from the 3-D cell overlaps). 51 states have no trusted β₁(U) within the LP budget; they are recorded as UNAVAILABLE and are not counted as results. The verifier recomputes a deterministic sample of 16 states against the cache (`--orbits-exhaustive` recomputes all; hours).

### k = 2 scan (b ≤ 11, boxes ≤ 6², 4,469 fibres)
680 fibres have an interior edge crossing — **in all 680 the Betti numbers of U differ from K_abs**. A further 206 fibres have no crossing but a diagonal inside a 2-cell and also differ. U never has β₂ > 0 (planar), while K_abs has β₂ > 0 in 368 fibres. β₁(K_abs) > 0 in 1,219 fibres but β₁(U) > 0 in only 357 (Fig. 7).

### E10 — three and four active axes
k = 3 (b ∈ {3,4,5,7}, 3 boxes, 240 fibres): 118 embedded, 70 with edge crossings, 52 cell-only; all 36 direct-product fibres embedded; 42 fibres have a crossing in a non-coordinate plane. k = 4 (84 fibres): 39 embedded, 20 edge-crossing, 25 cell-only; all 10 direct-product fibres embedded. A 4-D edge-crossing witness is in `output/certificates/e10_examples.json` (Fig. 4). The phenomenon is **not** a planar artifact.

## 3. Falsification table (H1–H4)

| | verdict | basis |
|---|---|---|
| H1 abstract ≈ embedded topology | **false** | R1, R2, 680/680 crossing fibres in the scan, E8 (5/5), g=11 orbit |
| H2 crossing controlled by modular arithmetic | **true; fully characterised for k = 2**; for k ≥ 3 crossings are governed by ι(g,h) but embedding also fails through cell-level obstructions invisible to edges | T1, T2 |
| H3 stable higher-dimensional patterns | **partly**: embedded fibres keep their homology under every realization; the β₁-saturation / β₂-growth patterns of K_abs vanish in U | T3, T4, E9 |
| H4 homology reflects arithmetic, not arbitrary attachment | **largely refuted for the v002 headline invariants**; caveat: U_x depends on the parallelotope-cell model (the clique complex of the same moves has other homology) | R2, E9 |

## 4. What is not established
* Eventual acyclicity of U for k = 2 once q_i > ord_i is **observed, not proved** (O1). One non-diagonal “edge through a 2-cell” mechanism (b = 5, residues (2,3), q = (4,4)) has no arithmetic criterion yet (O2). A classification of embedded fibres for k ≥ 3 beyond the direct-product and Klein-four families is open (O3). There is no explicit K_emb for k ≥ 3; U's homology there comes from the nerve (O4).
* Betti numbers in bulk scans use rank over GF(2⁶¹−1); 400 sampled cases are rechecked over ℚ. Corpus, benchmark and orbit values are over ℚ.
* The literature check is incomplete (see `PRIOR_ART.md`): no priority claim is made.
* The x_t Betti values β₂ = ⌊t/4⌋ are computed for t ≤ 24; the unbounded growth is proved independently of them.

## 5. Gates
| gate | status |
|---|---|
| G1 geometric correctness | met: all benchmark intersections exactly classified; subdivision certified (convexity, edge meeting, exact tiling, support equality); independent clipping cross-check on 1,500 random cell pairs |
| G2 topological correctness | met: ∂² = 0 and Euler–Poincaré on every complex computed; planar and nerve routes agree on 1,700 fibres |
| G3 higher-dimensional validity | met: 3600, 210⁴, 44100 preserved and certified; k = 3, 4 fibres investigated (E10) |
| G4 mathematical contribution | met with limits: infinite family proved; T1, T2, T4, Prop. D, P3, P5 proved; open problems stated |
| G5 reproducibility | met: smoke/full verifiers, manifest, data, figures; unavailable computations listed |
| G6 historical preservation | met: frozen libraries byte-identical to v002; v001/v002 manifests verified when the sibling folders are present |

## 6. Figures
`figures/` — Fig. 1 crossing witness · Fig. 2 abstract vs exact subdivision · Fig. 3 3-D obstructions · Fig. 4 4-D fibre (crossing plane + sections) · Fig. 5 the x_t family · Fig. 6 orbit β₁ · Fig. 7 k = 2 scan heat maps. Figures are regenerated from exact data by `figures/make_figures.py` (floats used only for drawing).

## 7. Files
`output/data/`: `corpus_audit.csv` (8,203 rows), `scan_k2.csv`, `e10_survey.csv`, `e9_orbits.json` + `e9_orbit_states.csv`. `output/certificates/`: `e1_witness.json`, `e10_examples.json`. `output/reports/verify_full.json` and `verify_smoke.json`.
