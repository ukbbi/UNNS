# Post-freeze numerical erratum — FIELD-I v012, T71 data sentence

**Registry record:** F.E71 (corrects the data clause of F.T71). **Status:** approved 23 October 2026 as a registry erratum.
**Frozen source (not overwritten):** `projects/UNNS_MATH_FOUNDATIONS/sources/FIELD-I/v012/THEOREMS.md`, line 56, in `ukbbi/UNNS` commit `bb8b12d753c600c597feb00df17fe139c7cc65fa`.
**What is affected:** one numerical example. T71's statement, hypotheses (g prime, or whenever T67 applies) and proof are unchanged.

## Original sentence (verbatim, line 56)

*Tests E3 (L1, L2, Φ-increase, monotone saturation, per-epoch size ≤ N_o+(N_o+1)(|Abs_{p*}|+1)) on 1 092 exact carry-level orbits (22 670 epochs); 0 violations. DATA E2: the largest observed entry index is 208 (g = 211), against H ≈ 10¹⁵ and K_poly ≈ 2·10⁸: the bounds are worst-case guarantees, not predictions.*

## Corrected reading

*Tests E3 (L1, L2, Φ-increase, monotone saturation, per-epoch size ≤ N_o+(N_o+1)(|Abs_{p*}|+1)) on 1 092 exact carry-level orbits (22 670 epochs); 0 violations. DATA E2: the largest observed entry index is 208 (g = 211), against H(211) ≈ 2.4·10¹³ and K_poly(211) ≈ 1.1·10⁸: the bounds are worst-case guarantees, not predictions.*

## Exactly what changed

`H ≈ 10¹⁵` → `H(211) ≈ 2.4·10¹³` and `K_poly ≈ 2·10⁸` → `K_poly(211) ≈ 1.1·10⁸`. Nothing else in the sentence is altered: the test list keeps `|Abs_{p*}|`, and the original digit grouping (`1 092`, `22 670`) is kept.

## Basis

- v012 `RESULTS.md`, line 37, already states: "H(211) ≈ 2.4·10¹³ and K_poly(211) ≈ 1.1·10⁸".
- Recomputed from the definitions (H(g) = ∏_{p²<g, p∤g}(2·ord_g(p) − 1), K_poly(g) = (Φ+1)(Σ+(Σ+1)(ω+1)+1)) with P_211 = {2, 3, 5, 7, 11, 13}: H(211) = 24 165 141 422 031, K_poly(211) = 113 903 360.
- The figures printed in the original sentence (≈ 10¹⁵, ≈ 2·10⁸) are those of g = 197: H(197) = 1 782 043 899 275 445, K_poly(197) = 229 237 866.

## Citation

Cite the original commit for v012, and this erratum for the corrected numerical reading. If a corrected source edition is later authorised, the original commit stays the historical reference.
