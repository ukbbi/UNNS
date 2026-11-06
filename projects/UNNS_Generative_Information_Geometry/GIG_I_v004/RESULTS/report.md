# GIG-I v004 — Arithmetic Hole Survival

Baseline: v001–v003 frozen and imported read-only. All divisibility, rank and homology certificates use exact integer arithmetic. Tags: [PROVED], [FINITE-EXACT], [BOUNDED-NEGATIVE], [CAND], [OPEN].
Full run 974 s (E15 933 s, E16 41 s) + E17 1,069 s + E18 (Python 3.13). Records: `results.json`, `E17_H3-4.json`, `E18_other_patterns.json`, `CERTIFICATES/`.

## 1. Result: a general (sufficient) Arithmetic Hole-Survival Theorem — PS-1 [PROVED]
Let z be the 96-face 2-cycle of the v003 anchors and φ its 6-hexagon cochain (rank coordinates, content-independent). Put
P_z = the 43 rank sets that occur as prefix sets of faces of z, K_z(λ) = lcm_{I∈P_z} D(I), and three **gates** (rank sets):
 G₀ = {024}, G₁ = {15, 125}, G₃ = {3, 34, 35, 345}; gate G_a is *open at m* when every D(I), I ∈ G_a, divides m.
**For ANY six distinct positive integers λ and any m: if K_z(λ) | m and no gate is open at m, then [z] ≠ 0 in H₂(X_λ(m); F₂).**
Proof in three lines (PROOFS.md): z is present (Pref ⊆ P_z); φ∘∂₃ can be non-zero only on the six truncated octahedra ({a,2,4,5}|y|w), whose prefix sets beyond P_z are exactly the gate sets; if none is present, φ∘∂₃ = 0 while φ(z) = 1.
The anchors are the special cases: A has K_z = 288 and gate thresholds 576, 864, 1440 = 288·{2,3,5}; B has K_z = 432 and 864, 1296, 3024 = 432·{2,3,7}.
**Necessity.** Gate 0: [PROVED] — if K_z | m and D(024) | m then z = ∂c for an explicit 34-face chain valid for every content. Gates 1 and 3: a universal combinatorial filling does not exist (its faces need number-theoretic coincidences), so necessity there is a census statement [BOUNDED-NEGATIVE]: of 18,998 regimes (all 8,008 contents with labels ≤ 16, all 346,859 source regimes) in which z is present, 18 satisfy the hypotheses and all 18 have [z] ≠ 0; in the 18,980 others z bounds every time — no exception.
**Existence [PROVED criterion, census].** A hole regime exists for λ (under a role→rank bijection) iff all gates are closed at m = K_z. In labels ≤ 16 this holds for **46 of 8,008 contents** (list in `results.json`; e.g. (2,3,4,5,8,15) with K_z = 480, (2,3,8,9,10,11) with 720, (2,3,8,9,14,15) with five different K_z). The two anchors are therefore not isolated, but the mechanism is rare (0.6 % of contents).

## 2. Correction to the expectation "one mechanism"
The census of all 158 regimes with β₂ > 0 (β₂ = 3 once, content (2,3,8,9,14,15), source 1680) shows that **PS-1 explains 52 of them; 106 are not explained by it.** These carry other H₂ patterns: E18 certifies each (cycle + cochain, all verified) and finds 33 coarse signatures — the commonest (32 regimes, e.g. (1,2,3,8,9,14) at 252) has a 50-face cycle (20 hexagons, 30 squares) with 4 obstructed truncated octahedra; others have 6 obstructed truncated octahedra, or 2 hexagonal prisms + 3–4 truncated octahedra. The signatures are coarse (not canonical under S₆; cycle weights depend on the representative), so 33 is an upper bound on the number of distinct patterns. Labels 14 and 15 (= 2·7, 3·5) dominate these cases. **A uniform theorem covering all H₂ holes is therefore not yet available**; the structure "cycle + a few obstructed cells whose thresholds are the gates" is the same, which suggests a pattern atlas as the next step (Open problem P2).
Also: the "unlock factor" is not a universal law — K_T = K_z·c_a holds in only 44 of 972 (T, content) pairs tested; the exact statement is the gate form above.

## 3. Explicit certificates for the four H₃ regimes (k = 7)
| case | content | source | β | z₃ (faces) | φ₃ | killing sources (all verified fillings) |
|---|---|---|---|---|---|---|
| H3-1 | (2,3,4,5,8,9,14) | 4032 | (1,0,0,1,0,0,0) | 446 = 126 cubes + 270 prisms + 50 trunc. oct. (1006 arr.) | 6 faces | 2·, 3·, 5· multiples: 8064, 12096, 20160,… |
| H3-2 | (2,3,4,5,8,9,15) | 4320 | same | 438 (996 arr.) | 6 | 8640, 12960, 21600,… |
| H3-3 | (2,3,6,7,8,9,14) | 6048 | same | 446 | 6 | 12096, 18144, 42336,… |
| H3-4 | (2,3,6,7,8,9,15) | 6480 | same | 438 | 6 | 12960, 19440, 45360,… |
In every case: z₃ is a cycle, φ₃(z₃) = 1, φ₃∘∂₄ = 0 on all 4-faces of the complex, and exactly **six 4-faces of P₇ obstruct** — ({a,2,4,5,6}|y|w), a ∈ {0,1,3} — i.e. the H₂ obstruction with the new largest label (rank 6) added to the cap block; their thresholds are K_z₃·{2,3,5} (anchor A) / K_z₃·{2,3,7} (anchor B). φ₃ is identical in all four; z₃ has two classes (x = 14 pair, x = 15 pair). Observation (4 cases): K_z₃ = (anchor source)·x.
**Parametric H₃ statement (PS3, same proof):** [z₃] ≠ 0 whenever K_z₃ | m and no H₃-gate is open. Among **all 31,824 seven-contents with labels ≤ 18** (identity role map, two z₃ classes) the criterion predicts exactly these four hole regimes; exact homology confirms β₃ = 1 for all four. This is a census statement for the identity role map and these two z₃ classes — other z₃ patterns or role maps were not searched.
**Graph reconstruction (E17).** For H3-4 (2,160 arrangements) the face poset derived from the uncoloured graph equals the true poset in every dimension (f = 2160, 6000, 5980, 2521, 393, 12; ranks and Betti agree) [FINITE-EXACT, one regime; ~18 min]. This covers one of the four regimes that v003 left outside its verified range; the other three and the β₂ = 3 regime are not reconstructed.

## 4. What this changes
Arithmetic → face activation → boundary relations → topological survival is now a statement with named switches: a hole present at K_z dies at the first source that opens a gate, and the gate is a finite conjunction of divisibilities D(I) | m. The H₃ holes arise from the same switches one dimension up. What is *not* shown: necessity for gates 1, 3 beyond the census; a classification of the 106 other H₂ regimes; any statement for k ≥ 8; graph reconstruction beyond H3-4.

Reproduce: `RUN_V004.bat test | quick | full | graph H3-4`. Provenance: `MANIFEST.json`.
