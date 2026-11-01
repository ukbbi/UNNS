# E2-P1 — Proof obligations, dependencies and what is NOT established

## 1. Inherited statements used (not re-proved here; sources are the pinned GEO-I / Foundations records)
| id | statement | source |
|---|---|---|
| I1 | Rational-Fibre Theorem: occurrences ↔ D(x) | Vol. I Thm 1.2 (F.T1) |
| I2 | D(x) ⊆ D(C(x)); G(C(x)) divides G(x); reduced denominator of C(x) divides G(x) | Vol. II Thm 1.3 (F.T31) and ch. 1 |
| I3 | b=1: K_axis is contractible, U = {max x_i ≥ 1}; d_cell formula | GEO-I v002 Prop 1, Prop 2 |
| I4 | Prop D (diagonal obstruction) ⇒ non-embedded | GEO-I v004 §6 |
| I5 | Nerve theorem for finite closed convex covers | Borsuk 1948; used in GEO-I v003 Cor. 1 |
| I6 | Graver bases / conformal decomposition | Graver 1975 (classical) |

## 2. Obligations discharged here
| claim | kind | discharge |
|---|---|---|
| E2-1 orbit family | hand proof | explicit; C01, C22, C23 check 46 members (k = 2,3,4) |
| E2-2 lattice order | hand proof | CRT + index formula; C24 (405 transitions) |
| E2-3 denominator floor | hand proof from I2 | C25 |
| E2-4 no shrinking | hand proof from I2 | C25 |
| E2-5 Graver sets | hand proof | brute force C03/C05 |
| E2-6 abstract transport | hand proof | C05, C09 |
| E2-8 edges stay in U | hand proof | exact LP C16 (all 45) |
| E2-9 partial cells | one cell by hand; classification by exact computation | C16–C18 (LP) |
| E2-10 Betti numbers | finite exact computation | builder (Q) vs audit (GF(2), GF(3), GF(2^31−1), exact LP nerve): C06–C15 |
| embedded-pair criterion | proof sketch: faces are closed under intersection | pairwise test between face-maximal cells suffices (if two maximal cells meet in a common face F then any faces a ⊆ P, b ⊆ Q meet in a face of both) |

## 3. How independence was obtained
`src/geometry_audit.py` imports nothing from `fibre_transport.py` / `cell_transport.py`. Different methods: trial division vs factorisation; brute-force minimality vs the same definition coded separately; subset search for cells vs generator choice; exact two-phase simplex vs candidate vertices; GF(p) ranks vs exact Q. Builder and auditor were written by the same author (same session): the audit is an independent *code path*, not an independent *reviewer*. `tests/test_e2_p1.py` mutates stored data and requires the audit to fail.

## 4. NOT established (OPEN) or NOT run
* A general (any k, any box) criterion for which cells leave `U(x')` (E2-9 is verified for k=3 box (2,2,2) only).
* Betti numbers of `U` for k = 4 (no 4-D geometry code); only the abstract K_abs and the target `f`-vector are computed (UNAVAILABLE for U).
* `K_emb` in dimension 3 (v003 open problem O4): not constructed.
* Behaviour when coordinates/box change along an orbit (COORDINATES_CHANGE): out of scope.
* Closed forms for the Betti numbers of `K_abs`/`U` of the parity lattice as functions of k.
* Literature audit of Graver bases of D_k beyond the classical facts cited.
* Interactive 3-D viewer: not built (static PNG only).

## 5. Reading guide for the scientific gate
`EXACT_PASS` says the computations are right. `COUNTEREXAMPLE` is established by E2-11. `THEOREM_PASS` is claimed only for the scoped, elementary statements E2-1…E2-6 and E2-8, each proved above; none is deep, and no priority is claimed. The question "is there a law predicting the full geometry of a C-orbit step?" remains OPEN.
