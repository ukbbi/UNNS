# GEO-I v005 — Report: Uniform Geometric Laws and Essential Obstruction Dimension

Date of specification: 25 Oct 2026. v001–v004, SELECT-I/II, FIELD-I, the Foundations volumes and GitHub are untouched. Following the project owner's recommendation, **G5-C1 (uniform planar stabilization) and G5-C3 (span-two minimal obstruction) are the principal gates**; the symbolic `s = ±1` atlases are a parallel theorem track; no unrestricted four-dimensional atlas is required.

## Summary of outcomes
| Item | Outcome |
|---|---|
| G5-C1 (`U = conv(F)`, `Q ≥ (d,d)`, `Q ≠ (d,d)`) | **PROVED for all `d` when `s = ±1`** (layer/path cover; machine-checked on 8 229 boxes, `d ≤ 14`). Counterexample search for all other types: **none up to `d = 21`** (all 95 types `2 ≤ d ≤ 21`; 53 types / 53 535 new boxes in v005, 0 violations). General `(d,s)` **OPEN**. |
| G5-C2 (hollow box `Q = (d,d)`) | `β₁ = d` for `s = −1`, `= 2` for `s = +1`, `d ≥ 3`: **PROVED+CHECKED**. Other `s`: `β₁ = 2` **CHECKED** `d ≤ 21`; general **OPEN**. |
| G5-T3 / G5-T4 | Closed-form obstruction antichains for `s = −1` and `s = +1`: **PROVED+CHECKED** for all `d` (ingredients re-verified for every `d ≤ 40`). |
| G5-C3 (weak: some witness with `d_span ≤ 2`) | **FALSE.** Decisive counterexample: parity lattice in `Z⁴` at `(1,1,1,1)`; 14 certified lattice classes in total. |
| G5-C3′ (`d_span ≤ 3`) | **OPEN**, supported by 919 minimal boxes (census, `k = 3, 4`). |
| G5-C4 (irreducible ⇒ planar) | **FALSE** (irreducible witnesses of span 3 and 4). |
| support vs span | Independent: 4 coordinates with planar witness (`b = 24`), span 3 with support 4 (parity), span 3 with support 3 and a lifted 4th coordinate. |
| G5-T5 | **CHECKED** (mandatory families, bounded census); lifting lemma **PROVED**. |
| G5-T6 | **PROVED+CHECKED**: 80 independently verified witness certificates. |
| unrestricted `k = 4` atlas | **UNAVAILABLE** (bounded census of 455 + 221 non-direct classes shipped). |

Per the stopping rules, once the weak G5-C3 had a verified decisive counterexample it was no longer treated as viable; the corrected conjecture C3′ and the support/span structure were developed instead.

## Gates
| Gate | Requirement | Status |
|---|---|---|
| G1 | continuity with v004 definitions and results | **PASS** — v004 modules/tests reused unchanged (`test_geo3` 24, `test_geo4` 72); v004 certificates (d ≤ 13) extended to 21 |
| G2 | uniform planar stabilization result | **PASS** — proved for `s = ±1`, search to `d = 21`, no counterexample; general case honestly OPEN |
| G3 | hollow-box homology | **PASS** — proved `s = ±1`, checked other `s` |
| G4 | span/support classification and a G5-C3 result | **PASS** — C3 refuted with certificates; C3′ proposed; support/span table for all mandatory families |
| G5 | `s = ±1` atlas result | **PASS** — T3, T4 proved |
| G6 | independent verification | **PASS** — two routes for embeddedness (planar test vs templates vs LP audit) and for witnesses (cells vs templates); certificates re-checked by a standalone rational verifier. Limitation: the template route for 4 of the 14 refuting boxes did not finish within the time budget (**UNAVAILABLE**, not passed); these rest on cells route + exact LP audit |
| G7 | clean-unzip smoke and full runs, zero mandatory failures | see `output/reports/verify_full.json` (run recorded at release) |
| G8 | v001–v004 preserved | **PASS** — optional manifest checks of sibling releases, when present, are reported separately |

## Programme A — details (`STABILIZATION.md`)
The corrected v004 statement is proved for the two classes `s = ±1` by decomposing `conv(F)` into layers of constant `D = (j − s·i)/d`, bridging consecutive layers with a monotone lattice path of parallelogram cells whose generators are explicit Graver vectors (Lemma G), and handling single-point extreme layers by apex cells; the origin exclusion is absorbed by an explicit inequality (`d ≥ 2`). For general `s` the bridges have too short a range of offsets (shown explicitly for `(5,2),(7,3),(8,3)`), so a proof needs multi-layer cells governed by the continued fraction of `s/d`; the search finds no failure to `d = 21`.

## Programme B — details (`OBSTRUCTIONS.md`)
Weak G5-C3 fails already in the smallest genuinely four-dimensional example: the parity lattice at `(1,1,1,1)` has exactly three witnesses (pairs of equatorial squares of an octahedron meeting in a common diagonal), each with `d_span = 3`, `d_support = 4`, `d_intersection = 1`. Thirteen further classes behave alike or by lifting. Planar-witness failure is rare (14 of 455 classes with `k = 4`; 0 of 221 with `k = 3`), which motivates C3′.

## Programme C — details
T3: embedded ⇔ `Q1 + Q2 ≤ 2d`. T4: antichain `{(1,2d),(2,d+1),(d,d),(d+1,2),(2d,1)}`, `d ≥ 3`. The proofs use explicit parallelogram witnesses for non-embeddedness and the finitely many maximal boxes below the antichain for embeddedness; the data check them for every `d ≤ 40`.

## What this release does not claim
* No proof of G5-C1/C2 for `s ≠ ±1`; no unrestricted `k = 4` or `k ≥ 5` atlas; no proof of C3′.
* No priority claim (see `PRIOR_ART.md`); no intrinsic topology of UNNS structures; no physical interpretation.

## Reproduction
`python3 verify.py --smoke` (≈1.5 min), `python3 verify.py` (full), `experiments/*.py` as listed in `OBSTRUCTIONS.md` §8 and `STABILIZATION.md`.
