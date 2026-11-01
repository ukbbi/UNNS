# E2-P4 v002 report -- P4-C1 correction, P4-E3 residual planar, P4-E4 coupled spatial obstruction

Governing question: does nonrectangular geometric transport admit a genuinely predictive arithmetic obstruction law?
Short answer: **an obstruction exists and is explained, but it is an inherited planar-gap mechanism, not a new three-dimensional law; a scoped predictor works, a general law is not proved; CP3-A stays open; C3 is not claimed.**

## 1. P4-C1 correction (done)
The equality clause was false.  2Z^3 < E_3 at n = 4 has all ten hull vertices in F but omits (1,1,1) (witness (4/7,4/7,10/7)).  Inclusion kept, equality withdrawn (ERRATA addendum; RUN_VERIFY S8, independent cells).
P4-T2 (all-m containment for P4-F110) is unaffected.

## 2. New tools (all elementary, proved)
* **P4-Z1 zero-vertex screen.**  A source cell is contained in the target union if no choice of target-lattice vectors s_i conformally below its generators makes base + sum s_i = 0.  Reads only (u,g_i) and a membership oracle.  One-sided.  Edges never obstruct (Z1.a).
* **P4-S1 slab lemma.**  For a target with a free coordinate (e_i in the lattice; FIELD-I: p_i = 1 mod b'), the thin slab 0 < c < 1 of the target union is exactly U(planar target) x (0,1).

## 3. P4-E3 -- residual planar CP3-A (finite-exact; general statement OPEN)
| Scope | Result |
|---|---|
| E2-P3 open-class corpus, 846 rows (includes the 62 E2-P2 cases: 14 hollow-box, 48 sub-threshold) | 564 hull-covered, 282 hollow -- **all 282 zero-vertex free, hence contained by P4-Z1**; 0 failures |
| New window: 13 primes <= 41, boxes [1,7]^2, b up to 4000 (E2-P3 stopped at q <= 6, b <= 400) | 1,443 residual rows, 0 zero-vertex flagged, 0 failures |
| Pure lattice scan: all 1,938 pairs Lambda < Lambda' of Z^2, [Z^2:Lambda] <= 24, boxes [1,6]^2 | 42,287 exact runs, 0 failures; 51 flagged runs all CONTAINED |
No counterexample to CP3-A and no proof.  P4-Z1 gives a verifiable arithmetic sufficient condition and shows every residual row in scope is covered by hull coverage or by it.  The 51 flagged-but-contained planar runs show the screen is not necessary, so it is not a criterion.

## 4. P4-E4 -- coupled spatial obstruction (obstruction FOUND, mechanism explained)
* FIELD-I search (6 primes, q <= 3, b <= 100, odd exponents): 191,376 states -> **3,845 rows with nonrectangular target**.
* **21 exact failures** (U not contained in U'), all with a free target coordinate, target index 2, source index 6 or 12, essential 3D (full support, all coordinate-face restrictions contained).  Smallest: x = 2^5 5^4 7^6 / 9 -> 2^4 5^4 7^6 / 3, box (2,2,3), witness (16/9, 10/9, 2/3).
  This **falsifies P4-F1** (strict enlargement between nonrectangular lattices does not in general preserve realized geometry).
* **36 more lattice-level failures** (lattice-only candidates, 153 nonrectangular targets, 2,608 pairs, 23,302 box runs) -- never reported as FIELD-I results.
* Mechanism (P4-S1.a): every one of the 57 failures has witness coordinate in (0,1) along the free coordinate and planar part inside the planar target gap (E2 at box (2,2) in 51 cases).  Verified by independent code (S9, S10).
* Predictor: on the 1,418 free-coordinate rows a slab witness exists **exactly** for the 21 failures (0 contradictions); the 21 UNAVAILABLE_COST rows (box (3,3,3)) show none.  On the 2,427 rows with no free coordinate: **0 failures** (2,374 proved by P4-Z1, 53 exact).
* Why P4-F110 is safe: its target E_3 is hull-covered from n = 4 (no planar gap to exploit).

## 5. What is proved / finite-exact / open
**Proved (elementary):** P4-A, P4-L, P4-T1, P4-T2 (v001, unchanged); P4-C1 inclusion; P4-Z1; P4-Z1.a; P4-S1; P4-S1.a.
**Finite-exact:** the 57 noncontainment witnesses; the planar and spatial scans within recorded limits; slab-vs-engine agreement on 1,418 rows; independent re-screens (S12-S14).
**Open:** CP3-A in general; converse of S1.a beyond scope; 21 UNAVAILABLE_COST rows; preservation theorem for targets without a free coordinate; prior-art audit; P4-T3, P4-T4.
**Withdrawn:** P4-C1 equality clause.  **Falsified:** P4-F1 in general.

## 6. Honest limits
Search scopes are small and recorded in `data/SEARCH_LIMITS_V002.json`.  The lattice-level exact engine ran on every zero-vertex-flagged run and on a validation sample (every 6th ZV-free run, box sum <= 5); ZV-free runs outside the sample are proved by P4-Z1, not re-run.
No prior-art search was done; nothing is called a discovery.  Builder and verifier share an author (independence caveat).  Project STATUS/CHANGELOG/MANIFEST are untouched; v001 is preserved.
