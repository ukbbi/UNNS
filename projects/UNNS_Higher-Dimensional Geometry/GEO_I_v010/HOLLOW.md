# GEO-I v010 — Programme A: the exact hollow-box complement (G10-T1, G10-T1H)

* **G10-T1 (= G9-C1), PROVED+CHECKED.** For `d ≥ 5` and units `2 ≤ s ≤ d−2` (and the separate small cases `d = 3, 4`, where all units are `≡ ±1`): `H0 ∖ U0 = int T1 ⊔ int T2`. Two bounded complement components, each of area `d/2`.
* **G10-T1H (= G9-T1H), PROVED+CHECKED.** `β1(U0) = 2`, `β2 = 0`: Alexander duality on the bounded components (`MATHEMATICS.md` §2.5).
* **G10-R1, PROVED+CHECKED.** Together with the v008 theorem G8-R1: `H0 ⊆ U_Q` for every `Q ≥ (d,d)`, `Q ≠ (d,d)`, `d ≥ 5`, `s ≢ ±1`.
* `s ≡ −1` is separate (fan graph, `β1 = d`, v005); `s ≡ 1` and `d ≤ 4` are the earlier trivial cases.

**Proof route.** G7-T3 (v007, proved) gives `H0 ∖ U0 ⊇ int T1 ⊔ int T2`. G10-Z gives `H0 ⊆ Z ∪ T1 ∪ T2 ∪ K` with `Z`, `K` unions of cells, hence `H0 ∖ U0 ⊆ int T1 ∪ int T2`.

**Gap criterion** (kept from v009): a counterexample would be a point of `H0` outside `U0 ∪ T1° ∪ T2°`, certified by a GAP certificate. The BOUNDARY certificate kind (v010) certifies the positive statement (cells cover) and recomputes `U0` from scratch for `d ≤ 48`.

**Evidence summary.** All 6560 unit pairs `d ≤ 150` pass the exact cover check; 262 pairs (`d ≤ 32`) also agree with the frozen cell engine; 453 certificates are accepted by the standalone `checker10.py`.
