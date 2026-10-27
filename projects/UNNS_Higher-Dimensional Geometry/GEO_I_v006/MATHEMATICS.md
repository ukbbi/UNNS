# GEO-I v006 — Mathematical summary and theorem registry

Labels: **PROVED**, **PROVED+CHECKED**, **CHECKED**, **FALSE**, **OPEN**, **CORRECTED**, **UNAVAILABLE**. A failed proof is never recorded as a falsification, and a numerical pattern is never recorded as a theorem. Definitions of GEO-I v001–v005 are used unchanged.

## 1. Registry

| ID | Statement | Status | Where |
|---|---|---|---|
| G5-C1, s = ±1 | uniform stabilization | PROVED+CHECKED (v005, inherited) | regression suite |
| **G6-C1** | `U = conv(F)` for every unit `s` | CHECKED for all `(d,s)`, `2 ≤ d ≤ 30`; OPEN beyond; **no proof for all d** | STABILIZATION.md §0–§4, §6 |
| G6-C1 thick/thin | boxes with `max(Q) ≥ 2d` | explicit exact cover, CHECKED; covering lemma not proved for all parameters | STABILIZATION.md §2–§3 |
| Lemma S4 | window `[d,3d−1]²` decides all `Q` | PROVED (v004) | STABILIZATION.md §1 |
| H1 | `∂T₁, ∂T₂ ⊂ U` at `Q = (d,d)`, `s ≢ −1` | PROVED | STABILIZATION.md §5 |
| **G6-C2** | `β₁(U_(d,d)) = 2` for `s ≢ −1`, `d ≥ 3` | CHECKED (hole structure exact for `d ≤ 45`, Betti numbers `d ≤ 20`); OPEN in general | STABILIZATION.md §5 |
| B1, B2 | cells and centre criterion for 0/1 boxes of binary lattices | PROVED | OBSTRUCTION_RANK.md §1 |
| **G6-C3** | min witness span ≤ 3 for every minimal box | OPEN; no counterexample; CHECKED for binary 0/1 boxes (n ≤ 6 complete) | OBSTRUCTION_RANK.md |
| G6-C4 | arithmetic certificate avoiding full enumeration | partial: finite reduction (S4) + explicit covers + centre criterion; general criterion OPEN | CERTIFICATION.md |
| G5-C3 (span ≤ 2) | — | FALSE (v005; recomputed in the regression suite: parity 4) | — |
| G5-C4 | — | FALSE (v005; irreducible span 3 and 4) | — |

## 2. Notation reminders

*Binary lattices.* `Λ_M = {α ∈ Zⁿ : Mα ≡ 0 (mod 2)}` with `M ∈ F₂^{m×n}` with nonzero columns; they occur as relation lattices of residues of exponent 2 (parity lattice: `M = (1,…,1)`; mod 24: `(Z/24)^× ≅ F₂³`). Codewords = `ker M`; circuits = minimal supports. The 0/1 box `1ⁿ` has fibre = nonzero codewords.

*Witness.* `(A,B,δ)` up to translation and swap. A pair of cells can give the same witness as another pair (translation), so `# witnesses ≤ # cell pairs`; v005 counts witnesses, and v006 reports both (`n_witnesses`, `n_cell_pairs`) and uses witnesses for all comparisons with v005.

*Sufficient-family certificate.* If `𝓕` is a set of cells of `K_abs` with `∪𝓕 ⊇ conv(F)` then `U = conv(F)`. (`U ⊆ conv(F)` always.)

## 3. Corrections and notes on earlier releases

* **CORRECTED (documentation only; v005 archive untouched).** v005 `OBSTRUCTIONS.md` mentions 46 certificates; the certificate file contains **80** individual witnesses (48 in 14 counterexample cases + 32 in essential-family cases); 46 = 14 + 32 case groups. The regression suite (inherited verifier) counts the 80.
* The v005 full verifier validates the *shipped records* of the large surveys and recomputes selected items; it does not regenerate every search. The same holds for the v006 data files `general_s_d15_70.jsonl`, `general_s_d2_14.jsonl`, `window_full_*.jsonl`, `hollow_general_s.json`, `binrank_n*.json`: `verify.py` re-runs a subset and checks the rest for consistency.
* v006 does not modify any earlier artefact; modules inherited unchanged are listed with source hashes in `PROVENANCE.json`.

## 4. Independent validation paths used

| Claim | Path 1 | Path 2 |
|---|---|---|
| `U = conv(F)` on a box | explicit proof-cell/sufficient-family cover, exact rational clipping | v005 full cell enumeration + clipping (`coverage.uncovered`) — audits on random boxes (general run) and as fallback; v005 chain-complex homology |
| hollow box structure | exact uncovered pieces vs the two triangles (clipping) | `β₁` from the planar-arrangement chain complex |
| 0/1 binary witnesses | centre criterion (B2) on circuit cells | v005 cell/zonotope (T-REL) engine, mod-24 residues: 180 + 15 lattices, parity 4–6 |
| 80 witness certificates, parity benchmarks | v005 certificate checker | standalone rational checker (inherited) |
