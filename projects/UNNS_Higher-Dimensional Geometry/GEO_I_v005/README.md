# GEO-I v005 — Uniform Geometric Laws and Essential Obstruction Dimension

Theorem-development release following GEO-I v004 (frozen, unchanged). Definitions are those of v004: relation lattice `Λ_b`, fibre `F_q`, Graver moves, parallelotope cells; `K_abs`, `U`, `K_emb` stay distinct.

**Headline results** (labels PROVED / PROVED+CHECKED / CHECKED / FALSE / OPEN / UNAVAILABLE / CORRECTED; details in `REPORT.md`):

* **G5-C1, uniform planar stabilization — PROVED for all d for the unit classes s = ±1** (explicit layer/path cover of `conv(F)` by cells; machine-checked box by box), **CHECKED** for every type `(d,s)` with `d ≤ 21` (0 violations), **OPEN** for general `(d,s)`.
* **G5-C2, hollow box** `Q=(d,d)`: `β₁ = d` for `s = −1`, `β₁ = 2` for `s = +1` (`d ≥ 3`) — PROVED; other `s` CHECKED `d ≤ 21`.
* **G5-T3, G5-T4** — the observed planar obstruction antichains for `s = −1` and `s = +1` are PROVED for all `d` (closed form).
* **G5-C3 (every minimal obstruction has a planar witness) is FALSE**: the 4D parity lattice at `(1,1,1,1)` and 13 further lattices have only witnesses of affine span 3. Corrected conjecture G5-C3′ (span ≤ 3) is OPEN. **G5-C4 (irreducible ⇒ planar) is FALSE.**
* **Support ≠ span**: obstructions that use four arithmetic coordinates while the intersecting cells span only a plane exist (`b=24`, residues `(5,7,13,23)`), and the converse also occurs. Lifting lemma proved.
* **G5-T6**: effective, independently re-verifiable witness certificates (rational interior-point equality); 80 shipped (48 refuting-box witnesses + 32 essential-family witnesses).
* Not achieved, reported as such: general-`s` proof of G5-C1/C2; unrestricted `k=4` atlas (UNAVAILABLE; a bounded, reproducible census of 676 non-direct classes is shipped).

## Run
Python 3.10+, `gmpy2`, `matplotlib` (figures only).

    python3 verify.py --smoke     # a few minutes
    python3 verify.py             # full
    python3 experiments/figures_v5.py

Windows: `RUN_SMOKE.bat`, `RUN_FULL.bat`. Exit code 0 only if every **core** check passes; core checks use only files inside this folder. Checks of sibling releases (`GEO_I_v001..v004` beside this folder) are *optional* and reported separately.

## Layout
* `REPORT.md` gates and findings · `MATHEMATICS.md` registry, recap of definitions and theorems · `STABILIZATION.md` Programme A · `OBSTRUCTIONS.md` Programmes B/C · `PRIOR_ART.md`.
* `theory/` — v004 modules plus `pure_lattice`, `planar_embed`, `uniform_coverage`, `hollow_box`, `symbolic_atlas`, `witness_dimension`, `certificates`.
* `experiments/` — v004 scripts plus `stabilization_search`, `layer_cover_check`, `hollow_homology`, `atlas_families`, `span_two_search`, `four_dimensional`, `irreducible_stats`, `make_certificates`, `figures_v5`.
* `output/data`, `output/certificates` exact data · `figures/` · `tests/` (`test_geo3`, `test_geo4`, `test_geo5`) · `MANIFEST.sha256`.

## Scope
v001–v004, SELECT-I/II, FIELD-I and the Foundations volumes are neither modified nor re-released. Results concern the parallelotope realization of v003; no intrinsic topology of UNNS structures and no physical interpretation is asserted.
