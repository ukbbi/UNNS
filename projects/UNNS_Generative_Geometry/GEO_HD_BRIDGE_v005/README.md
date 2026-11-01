# GEO_HD_BRIDGE_v005 — Arithmetic Laws of Geometric Evolution

**Decisive target (as set by the author): A5-T3 and A5-T4** — can arithmetic predict creation/loss of realised moves, and can that be carried forward to predict homology changes — **supported by A5-T2** (exact first-event law); collective towers G=5, G=11 as the infinite-family testing ground.

## Headline results
* **Proved.** (i) Stage sieve `d∈D(Y_j/G) ⇔ Q(d)|Y_j`; the next occurrence event is the least solution of one linear congruence per candidate, always finite, |D_n|→∞ (A5-T2). (ii) `K_move(x)` is determined by `D(x)` alone via a divisor-interval edge rule; transition law: an old edge dies iff a new occurrence lies in its divisor interval; every new edge/cell contains a new vertex (A5-T3). (iii) Zig-zag identity for Δβ_i, necessary-cause theorem, exact rebuild-free predictor at graph level (A5-T4). (iv) Towers are induced-subcomplex filtrations (Dead=∅); Graver ℓ₁ ≤ φ(m); eventual quasi-polynomial Betti laws (qualitative) (A5-T5). (v) Proper-divisor obstruction for reachability (A5-T1).
* **Finite-exact.** 2,576 D-events (ℓ=5,7,11,13) satisfy every transition statement; Type census V 1,787 / II 603 / III 172 / IV 14; G=11 and G=5 towers to k≤140 (β₁=8, β₂=17, β₃(k+5)=β₃(k)+9; (1,6,5,0)); the 24 step-capped v004 cases = 22 BLOCKED + 2 REACHED; k=2 family scans: 1,131 (ℓ=3) + 1 (ℓ=5) reached members, q∈{2,5,11,17,19}.
* **Counterexamples.** v004 "reached ⇒ q∈{2,5}" is false; abstract dead-edge-with-β₁-increase exists; see `theory/COUNTEREXAMPLES.md`.
* **Open / not done.** Regularity threshold for the tower laws (so they are not proved for all k); rebuild-free Betti prediction in dim ≥2; arithmetic predicate for event Type; infinite reached family; dormant Graver relations; A5-T8, A5-T9 not attempted.

## Gates / caveats
C3 NOT claimed; novelty NOT assessed; all sources and this release share an author line (same author) — verification is reproducibility, not external review. Inherited verification NOT_RERUN (sha-256 integrity only, `results/PINS.json`). Only SELECT-II integer rule and the FIELD-I map are used.

## Layout
`theory/` (FIRST_EVENT, MOVE_TRANSITIONS, HOMOLOGY_UPDATES, TOWERS, REACHABILITY, THEOREMS, COUNTEREXAMPLES, OPEN_PROBLEMS, SOURCE_CROSSWALK) · `src/` (new: divisor_complex, stage_sieve, reachability, transition_calculus, tower_laws, scan_*, build_v005, verify_v005; frozen copies pinned) · `data/` · `results/` · `tests/test_v005.py`.

## Verify
`python RUN_VERIFY.py --fast` (default, minutes) · `--full` · `--shard Z6` · `--list` · `--write` (results/VERIFY_LAST.json). Shards Z0–Z9 use independent implementations (`src/verify_v005.py`).
